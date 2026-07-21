#!/usr/bin/env python3
"""Harmonize scientists-photos to one standard: 296x352 transparent-cutout PNGs.

Target spec (approved):
  * 296x352 px (2x the 148x176 display frame) -> retina-crisp, uniform.
  * Background removed on every photo -> clean transparent cutout.
  * Subject reframed to the 37:44 avatar-frame ratio with breathing room, so the
    person fills the frame without cropping (matches the CSS object-fit:contain).
  * Saved as PNG. Any photo currently referenced as .jpg becomes .png (the caller
    updates the profile JSON + deletes the stale .jpg).

Scope: only the photos actually used by i18n/scientists-profiles.json. Files in
the folder that no profile references are listed but left untouched.

    python helpers/_harmonize_scientist_photos.py            # process all used photos
    python helpers/_harmonize_scientist_photos.py NAME ...   # only these stems/files
    python helpers/_harmonize_scientist_photos.py --list     # just report scope, no edits
"""
from __future__ import annotations

import json
import sys

import cv2
import numpy as np
from PIL import Image, ImageOps
from rembg import remove, new_session

from _paths import ROOT

PHOTOS = ROOT / "images" / "scientists-photos"
PROFILES_JSON = ROOT / "i18n" / "scientists-profiles.json"
EXTS = {".jpg", ".jpeg", ".png", ".webp"}

# Frame geometry
FRAME_W, FRAME_H = 296, 352            # 2x the 148x176 display frame
TARGET_R = FRAME_W / FRAME_H           # 37:44 = 0.8409
SIDE_MARGIN = 0.06                     # breathing room left/right of the subject
TOP_MARGIN = 0.07                      # headroom above the subject
WORK_MIN_H = 900                       # upscale small sources to this height before matting

session = new_session("u2net")

# When True, always run background removal even if the source already has some
# transparency. Needed for photos that carry transparent padding *around* a real
# photographic background (green/blue/red), which the auto heuristic would wrongly
# treat as "already cut" and skip.
FORCE_CUT = False


def used_photos() -> list[str]:
    data = json.loads(PROFILES_JSON.read_text(encoding="utf-8"))
    seen, out = set(), []
    for card in data.get("profiles", []):
        name = str(card.get("photo", "")).strip()
        if name and name not in seen:
            seen.add(name)
            out.append(name)
    return out


def keep_largest_region(img: Image.Image) -> Image.Image:
    """Drop stray specks: keep only the largest opaque connected component."""
    alpha = np.array(img.getchannel("A"))
    mask = (alpha > 30).astype(np.uint8)
    n, labels, stats, _ = cv2.connectedComponentsWithStats(mask, connectivity=8)
    if n <= 2:
        return img
    largest = 1 + int(np.argmax(stats[1:, cv2.CC_STAT_AREA]))
    new_alpha = np.where(labels == largest, alpha, 0).astype(np.uint8)
    out = img.copy()
    out.putalpha(Image.fromarray(new_alpha))
    return out


def already_cut(img: Image.Image) -> bool:
    """True if the image already has a real transparent background."""
    if img.mode != "RGBA":
        return False
    alpha = np.array(img.getchannel("A"))
    transparent = float((alpha < 16).mean())
    return transparent > 0.05


def cutout(img: Image.Image) -> Image.Image:
    """Return a transparent-background RGBA cutout of the subject."""
    if already_cut(img) and not FORCE_CUT:
        return keep_largest_region(img)
    if FORCE_CUT and img.mode == "RGBA":
        # flatten any transparent padding onto white so rembg sees a clean RGB
        # frame and only the true photographic background is what it removes.
        flat = Image.new("RGBA", img.size, (255, 255, 255, 255))
        flat.alpha_composite(img)
        img = flat
    cut = remove(
        img,
        session=session,
        alpha_matting=True,
        alpha_matting_foreground_threshold=240,
        alpha_matting_background_threshold=15,
        alpha_matting_erode_size=8,
    )
    return keep_largest_region(cut)


def reframe(cut: Image.Image) -> Image.Image:
    """Crop to subject, pad to 37:44 with breathing room, resize to 296x352."""
    bbox = cut.getchannel("A").getbbox()
    subj = cut.crop(bbox)
    w, h = subj.size

    side = round(w * SIDE_MARGIN)
    top = round(h * TOP_MARGIN)
    w2, h2 = w + 2 * side, h + top
    if w2 / h2 > TARGET_R:
        new_w, new_h = w2, round(w2 / TARGET_R)
    else:
        new_w, new_h = round(h2 * TARGET_R), h2

    canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    canvas.alpha_composite(subj, ((new_w - w) // 2, top))
    return canvas.resize((FRAME_W, FRAME_H), Image.Resampling.LANCZOS)


def process(src) -> None:
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGBA")
    if im.height < WORK_MIN_H:
        factor = max(1, round(WORK_MIN_H / im.height))
        im = im.resize((im.width * factor, im.height * factor), Image.Resampling.LANCZOS)
    out = reframe(cutout(im))
    dest = src.with_suffix(".png")
    out.save(dest, "PNG", optimize=True)
    if dest != src:
        src.unlink()  # standardizing to PNG; drop the stale .jpg
    print(f"  {src.name:<32} -> {dest.name}  {out.size[0]}x{out.size[1]}")


def main() -> int:
    global FORCE_CUT
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    FORCE_CUT = "--force-cut" in flags

    used = used_photos()
    used_stems = {name.rsplit(".", 1)[0] for name in used}

    on_disk = {p.name for p in PHOTOS.iterdir() if p.is_file() and p.suffix.lower() in EXTS}
    extras = sorted(
        n for n in on_disk if n.rsplit(".", 1)[0] not in used_stems
    )

    print(f"Used by profiles: {len(used)} photos")
    print(f"Unused extras in folder (left untouched): {len(extras)}")
    for n in extras:
        print(f"    - {n}")
    print()

    if "--list" in flags:
        return 0

    if "--extras" in flags:
        # every non-profile photo in the folder (caller is responsible for skips)
        targets = extras
    elif args:
        # explicit files: process exactly what's named, whether or not a profile
        # references them (lets us harmonize the non-profile "extras" too).
        targets = args
    else:
        targets = used

    print(f"Processing {len(targets)} photo(s)...")
    missing = []
    for name in targets:
        src = PHOTOS / name
        if not src.is_file():
            stem = name.rsplit(".", 1)[0]
            alts = [PHOTOS / f"{stem}{e}" for e in (".png", ".jpg", ".jpeg", ".webp")]
            src = next((p for p in alts if p.is_file()), None)
            if src is None:
                missing.append(name)
                continue
        process(src)

    if missing:
        print("\nMISSING source files:")
        for m in missing:
            print(f"    - {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

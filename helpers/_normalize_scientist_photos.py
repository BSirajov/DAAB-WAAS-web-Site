#!/usr/bin/env python3
"""Face-normalize scientist portraits so every card looks framed identically.

Problem: the earlier harmonize pass normalized the whole *silhouette*, so a
broad-shouldered photo got bottom-padded (tiny face) while a narrow one filled
the frame (big face). This pass instead detects the face and scales/positions
every portrait to a CONSISTENT face size and eye-line, on a 296x352 transparent
cutout — the true "looks-uniform" fix.

Pipeline per photo:
  1. Load the highest-res source available (pristine backup > current file).
  2. Upscale small sources for crisp output + reliable detection.
  3. Remove background (rembg u2net + alpha matting), keep largest region.
  4. Detect the face (OpenCV Haar, frontal + alt fallback).
  5. Scale so the face width == FACE_W_FRAC of the frame; place the face centre
     at (horizontal centre, FACE_CY_FRAC from top).
  6. Composite onto 296x352 and save PNG.
  Photos where no face is found fall back to the silhouette reframe (unchanged
  behaviour) and are reported so they can be checked by hand.

Usage (from repo root):
  python helpers/_normalize_scientist_photos.py            # all portraits
  python helpers/_normalize_scientist_photos.py NAME ...   # only these stems
  python helpers/_normalize_scientist_photos.py --dry      # report only, no writes
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

import cv2
import numpy as np
from PIL import Image, ImageOps
from rembg import new_session, remove

from _paths import ROOT

PHOTOS = ROOT / "images" / "scientists-photos"
BACKUP = Path(os.path.expandvars(r"%TEMP%")) / "daab-photos-backup"

FRAME_W, FRAME_H = 296, 352
WORK_MIN_H = 900

# Framing targets (fractions of the final frame).
FACE_W_FRAC = 0.46     # face box width relative to frame width
FACE_CY_FRAC = 0.42    # vertical position of the face centre (eye-line-ish)

# "fill" mode: scale the subject silhouette to occupy the whole frame height
# (head near the top, shoulders spanning the width) instead of leaving margins.
# Cutouts still show the card background in the corners beside the head/shoulders.
FILL_TOP_FRAC = 0.02       # headroom above the top of the head
FILL_HEIGHT_FRAC = 0.98    # subject height as a fraction of the frame height
FILL_MODE = False

session = new_session("u2net")
_CASCADES = [
    cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml"),
    cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_alt2.xml"),
]


def keep_largest_region(img: Image.Image) -> Image.Image:
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


def detect_face(rgb: np.ndarray):
    """Return (x, y, w, h) of the best face, or None."""
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    h = gray.shape[0]
    cands = []
    for cc in _CASCADES:
        if cc.empty():
            continue
        found = cc.detectMultiScale(
            gray, scaleFactor=1.08, minNeighbors=6,
            minSize=(int(h * 0.12), int(h * 0.12)),
        )
        cands.extend(list(found))
    if not cands:
        return None
    # Prefer the largest face in the upper 70% of the image (avoid stray matches).
    def score(f):
        x, y, w, hh = f
        cy = (y + hh / 2) / gray.shape[0]
        penalty = max(0.0, cy - 0.70) * 4.0
        return w * hh * (1.0 - penalty)
    return max(cands, key=score)


def cutout(img: Image.Image) -> Image.Image:
    # alpha_matting is off for speed; at the 148x176 display size the edge
    # difference is imperceptible and this is ~20x faster over 100+ photos.
    cut = remove(img, session=session)
    return keep_largest_region(cut)


def silhouette_reframe(cut: Image.Image) -> Image.Image:
    """Fallback: pad the subject silhouette to 37:44 and resize (old behaviour)."""
    bbox = cut.getchannel("A").getbbox()
    subj = cut.crop(bbox)
    w, h = subj.size
    side, top = round(w * 0.06), round(h * 0.07)
    w2, h2 = w + 2 * side, h + top
    r = FRAME_W / FRAME_H
    if w2 / h2 > r:
        new_w, new_h = w2, round(w2 / r)
    else:
        new_w, new_h = round(h2 * r), h2
    canvas = Image.new("RGBA", (new_w, new_h), (0, 0, 0, 0))
    canvas.alpha_composite(subj, ((new_w - w) // 2, top))
    return canvas.resize((FRAME_W, FRAME_H), Image.Resampling.LANCZOS)


def fill_frame(cut: Image.Image) -> Image.Image:
    """Scale the subject to fill the frame top-to-bottom, head anchored at top.

    Scales by height so the silhouette spans (almost) the full frame height; the
    subject is centred horizontally. Broad shoulders that exceed the frame width
    are clipped at the edges (natural portrait crop); narrow subjects keep small
    transparent side margins that blend with the card background.
    """
    bbox = cut.getchannel("A").getbbox()
    subj = cut.crop(bbox)
    scale = (FILL_HEIGHT_FRAC * FRAME_H) / subj.height
    new_size = (max(1, round(subj.width * scale)), max(1, round(subj.height * scale)))
    scaled = subj.resize(new_size, Image.Resampling.LANCZOS)
    off_x = round((FRAME_W - scaled.width) / 2.0)
    off_y = round(FILL_TOP_FRAC * FRAME_H)
    canvas = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))
    canvas.alpha_composite(scaled, (off_x, off_y))
    return canvas


def face_frame(cut: Image.Image, face) -> Image.Image:
    x, y, w, h = [float(v) for v in face]
    fcx, fcy = x + w / 2.0, y + h / 2.0
    scale = (FACE_W_FRAC * FRAME_W) / w
    new_size = (max(1, round(cut.width * scale)), max(1, round(cut.height * scale)))
    scaled = cut.resize(new_size, Image.Resampling.LANCZOS)
    off_x = round(FRAME_W / 2.0 - fcx * scale)
    off_y = round(FACE_CY_FRAC * FRAME_H - fcy * scale)
    canvas = Image.new("RGBA", (FRAME_W, FRAME_H), (0, 0, 0, 0))
    canvas.alpha_composite(scaled, (off_x, off_y))
    return canvas


def source_for(stem: str) -> Path | None:
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = BACKUP / f"{stem}{ext}"
        if p.is_file():
            return p
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        p = PHOTOS / f"{stem}{ext}"
        if p.is_file():
            return p
    return None


def process(stem: str) -> str:
    src = source_for(stem)
    if src is None:
        return "MISSING"
    im = ImageOps.exif_transpose(Image.open(src)).convert("RGBA")
    if im.height < WORK_MIN_H:
        factor = max(1, round(WORK_MIN_H / im.height))
        im = im.resize((im.width * factor, im.height * factor), Image.Resampling.LANCZOS)
    cut = cutout(im)
    if FILL_MODE:
        out = fill_frame(cut)
        tag = "fill"
    else:
        face = detect_face(np.array(cut.convert("RGB")))
        if face is None:
            out = silhouette_reframe(cut)
            tag = "no-face(fallback)"
        else:
            out = face_frame(cut, face)
            tag = "face"
    dest = PHOTOS / f"{stem}.png"
    out.save(dest, "PNG", optimize=True)
    return tag


def portrait_stems() -> list[str]:
    stems: set[str] = set()
    for ext in ("*.jpg", "*.jpeg", "*.png"):
        stems.update(p.stem for p in PHOTOS.glob(ext))
    return sorted(stems)


def main() -> int:
    global FILL_MODE
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    FILL_MODE = "--fill" in flags
    targets = args or portrait_stems()
    mode = "fill" if FILL_MODE else f"face_w={FACE_W_FRAC}, face_cy={FACE_CY_FRAC}"
    print(f"Normalizing {len(targets)} portrait(s)  ({mode})")
    if "--dry" in flags:
        for s in targets:
            print("   ", s, "<-", source_for(s))
        return 0
    fallbacks = []
    for i, stem in enumerate(targets, 1):
        tag = process(stem)
        if tag != "face":
            fallbacks.append((stem, tag))
        print(f"  [{i:>3}/{len(targets)}] {stem:<30} {tag}")
    print(f"\nDone. face-aligned: {len(targets) - len(fallbacks)}, fallback/other: {len(fallbacks)}")
    for s, t in fallbacks:
        print("   ", s, t)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

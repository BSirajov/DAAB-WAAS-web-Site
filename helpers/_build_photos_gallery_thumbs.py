#!/usr/bin/env python3
"""Generate optimized JPEG thumbnails for photos-gallery grid display."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from _paths import ROOT

try:
    from PIL import Image, ImageOps
except ImportError:
    raise SystemExit("Install: pip install Pillow")

GALLERY_ROOT = ROOT / "images" / "photos-gallery"
THUMB_ROOT = GALLERY_ROOT / "_thumbs"
THUMB_INDEX = ROOT / "js" / "photos-gallery-thumbs.json"

# ~2.5× largest grid cell (168px desktop) for crisp retina; keeps files small vs originals
MAX_EDGE = 420
JPEG_QUALITY = 85
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def make_thumb(src: Path, dest: Path) -> tuple[int, int]:
    """Resize preserving aspect ratio; return (width, height) of output."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    with ImageOps.exif_transpose(Image.open(src)) as im:
        im = im.convert("RGB")
        im.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        w, h = im.size
        im.save(
            dest,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
            subsampling=0,
        )
    return w, h


def prune_orphan_thumbs() -> int:
    """Remove thumbnails whose original was deleted (stale grid images)."""
    removed = 0
    if not THUMB_ROOT.is_dir():
        return removed
    for thumb_dir in THUMB_ROOT.iterdir():
        if not thumb_dir.is_dir():
            continue
        src_dir = GALLERY_ROOT / thumb_dir.name
        if not src_dir.is_dir():
            continue
        stems = {
            f.stem.lower()
            for f in src_dir.iterdir()
            if f.is_file() and f.suffix.lower() in EXTS and not f.name.startswith("_")
        }
        for thumb in thumb_dir.glob("*.jpg"):
            if thumb.stem.lower() not in stems:
                thumb.unlink(missing_ok=True)
                removed += 1
    return removed


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Regenerate all thumbnails even when up to date",
    )
    args = parser.parse_args()

    if not GALLERY_ROOT.is_dir():
        raise SystemExit(f"Missing: {GALLERY_ROOT}")

    pruned = prune_orphan_thumbs()
    written = skipped = errors = 0
    orig_bytes = thumb_bytes = 0
    index: dict[str, dict[str, dict]] = {}

    for folder in sorted(p for p in GALLERY_ROOT.iterdir() if p.is_dir() and p.name != "_thumbs"):
        folder_key = folder.name
        index[folder_key] = {}
        for src in sorted(folder.iterdir()):
            if src.suffix.lower() not in EXTS or not src.is_file():
                continue
            if src.name.startswith("_"):
                continue

            dest = THUMB_ROOT / folder_key / (src.stem + ".jpg")
            up_to_date = (
                dest.is_file()
                and dest.stat().st_mtime >= src.stat().st_mtime
                and dest.stat().st_size > 0
            )
            if up_to_date and not args.force:
                skipped += 1
                try:
                    with Image.open(dest) as thumb_im:
                        w, h = thumb_im.size
                except Exception:
                    w, h = 0, 0
            else:
                try:
                    w, h = make_thumb(src, dest)
                    written += 1
                except Exception as exc:
                    print("skip", src, exc)
                    errors += 1
                    continue

            orig_bytes += src.stat().st_size
            if dest.is_file():
                thumb_bytes += dest.stat().st_size
                index[folder_key][src.name] = {
                    "thumb": f"_thumbs/{folder_key}/{src.stem}.jpg",
                    "w": w,
                    "h": h,
                }

    meta = {
        "version": 1,
        "maxEdge": MAX_EDGE,
        "quality": JPEG_QUALITY,
        "format": "jpeg",
        "folders": index,
    }
    THUMB_INDEX.write_text(
        json.dumps(meta, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    ratio = (1 - thumb_bytes / orig_bytes) * 100 if orig_bytes else 0
    print(
        f"Thumbs: {written} written, {skipped} up-to-date, {pruned} orphan(s) removed, "
        f"{errors} error(s)"
    )
    print(
        f"Size: originals {orig_bytes / 1_048_576:.1f} MB -> thumbs {thumb_bytes / 1_048_576:.1f} MB "
        f"({ratio:.0f}% smaller)"
    )
    print(f"Index -> {THUMB_INDEX}")


if __name__ == "__main__":
    main()

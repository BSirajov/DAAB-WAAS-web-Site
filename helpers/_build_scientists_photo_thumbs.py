#!/usr/bin/env python3
"""Generate small JPEG thumbnails for scientists-photos (forum tables, TOC avatars)."""
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageOps

from _paths import ROOT

PHOTOS_DIR = ROOT / "images" / "scientists-photos"
THUMB_DIR = PHOTOS_DIR / "_thumbs"

# 2× largest forum avatar (72px card photo) for retina; keeps files tiny vs full portraits
MAX_EDGE = 104
JPEG_QUALITY = 82
EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def scientist_thumb_src(filename: str, asset_prefix: str = "") -> str:
    """Public URL path for a scientist avatar thumb (always .jpg)."""
    stem = Path(filename).stem
    return f"{asset_prefix}images/scientists-photos/_thumbs/{stem}.jpg"


def make_thumb(src: Path, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with ImageOps.exif_transpose(Image.open(src)) as im:
        if im.mode in ("RGBA", "LA", "P"):
            bg = Image.new("RGB", im.size, (255, 255, 255))
            if im.mode == "P":
                im = im.convert("RGBA")
            if im.mode in ("RGBA", "LA"):
                bg.paste(im, mask=im.split()[-1])
            else:
                bg.paste(im)
            im = bg
        else:
            im = im.convert("RGB")
        im.thumbnail((MAX_EDGE, MAX_EDGE), Image.Resampling.LANCZOS)
        im.save(
            dest,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
            subsampling="4:2:0",
        )


def prune_orphan_thumbs() -> int:
    removed = 0
    if not THUMB_DIR.is_dir():
        return removed
    stems = {
        f.stem.lower()
        for f in PHOTOS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in EXTS
    }
    for thumb in THUMB_DIR.glob("*.jpg"):
        if thumb.stem.lower() not in stems:
            thumb.unlink(missing_ok=True)
            removed += 1
    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Regenerate all thumbnails even when up to date",
    )
    args = parser.parse_args()

    if not PHOTOS_DIR.is_dir():
        raise SystemExit(f"Missing: {PHOTOS_DIR}")

    pruned = prune_orphan_thumbs()
    written = skipped = errors = 0
    orig_bytes = thumb_bytes = 0

    for src in sorted(PHOTOS_DIR.iterdir()):
        if not src.is_file() or src.suffix.lower() not in EXTS:
            continue
        dest = THUMB_DIR / f"{src.stem}.jpg"
        up_to_date = (
            dest.is_file()
            and dest.stat().st_mtime >= src.stat().st_mtime
            and dest.stat().st_size > 0
        )
        if up_to_date and not args.force:
            skipped += 1
        else:
            try:
                make_thumb(src, dest)
                written += 1
            except OSError as exc:
                print(f"skip {src.name}: {exc}")
                errors += 1
                continue
        orig_bytes += src.stat().st_size
        if dest.is_file():
            thumb_bytes += dest.stat().st_size

    ratio = (1 - thumb_bytes / orig_bytes) * 100 if orig_bytes else 0
    print(
        f"Scientist thumbs: {written} written, {skipped} up-to-date, "
        f"{pruned} orphan(s) removed, {errors} error(s)"
    )
    print(
        f"Size: originals {orig_bytes / 1_048_576:.1f} MB -> "
        f"thumbs {thumb_bytes / 1_048_576:.1f} MB ({ratio:.0f}% smaller)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

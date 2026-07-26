#!/usr/bin/env python3
"""Convert images/scientists-photos/*.{png,jpeg,webp} → .jpg and delete originals."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageOps

from _paths import ROOT

PHOTOS = ROOT / "images" / "scientists-photos"
JPEG_QUALITY = 88
SOURCE_EXTS = {".png", ".jpeg", ".webp"}


def to_jpg(src: Path) -> Path:
    dest = src.with_suffix(".jpg")
    with ImageOps.exif_transpose(Image.open(src)) as im:
        if im.mode in ("RGBA", "LA", "P"):
            if im.mode == "P":
                im = im.convert("RGBA")
            bg = Image.new("RGB", im.size, (255, 255, 255))
            if im.mode in ("RGBA", "LA"):
                bg.paste(im, mask=im.split()[-1])
            else:
                bg.paste(im)
            im = bg
        else:
            im = im.convert("RGB")
        im.save(
            dest,
            "JPEG",
            quality=JPEG_QUALITY,
            optimize=True,
            progressive=True,
            subsampling=0,
        )
    return dest


def main() -> int:
    if not PHOTOS.is_dir():
        raise SystemExit(f"Missing {PHOTOS}")

    sources = sorted(
        p
        for p in PHOTOS.iterdir()
        if p.is_file() and p.suffix.lower() in SOURCE_EXTS
    )
    # Also convert uppercase .JPG leftovers that aren't .jpg
    sources += sorted(
        p
        for p in PHOTOS.iterdir()
        if p.is_file() and p.suffix.lower() == ".jpeg"
    )
    # de-dupe
    seen: set[Path] = set()
    unique: list[Path] = []
    for p in sources:
        if p not in seen:
            seen.add(p)
            unique.append(p)

    written = 0
    for src in unique:
        dest = to_jpg(src)
        written += 1
        if dest.resolve() != src.resolve():
            src.unlink(missing_ok=True)
        print(f"  {src.name} -> {dest.name}")

    remaining_png = list(PHOTOS.glob("*.png")) + list(PHOTOS.glob("*.PNG"))
    print(f"Done. Converted {written}. Remaining PNG: {len(remaining_png)}")
    print(f"JPG count: {len(list(PHOTOS.glob('*.jpg')))}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

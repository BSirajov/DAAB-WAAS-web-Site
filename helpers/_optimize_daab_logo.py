#!/usr/bin/env python3
"""Optimize images/daab-logo.png — replace embedded raster with a small PNG favicon/nav asset."""
from __future__ import annotations

import base64
import re
import struct
import zlib
from io import BytesIO
from pathlib import Path

from PIL import Image

from _paths import ROOT

SVG = ROOT / "images" / "daab-logo.png"
SVG_BACKUP = ROOT / "images" / "daab-logo.source.svg"
PNG = ROOT / "images" / "daab-logo.png"
WEBP = ROOT / "images" / "daab-logo.webp"


def extract_embedded_png(svg_text: str) -> Image.Image | None:
    m = re.search(r"data:image/png;base64,([A-Za-z0-9+/=]+)", svg_text)
    if not m:
        return None
    raw = base64.b64decode(m.group(1))
    return Image.open(BytesIO(raw))


def write_optimized_png(im: Image.Image, dest: Path, size: int = 128) -> None:
    im = im.convert("RGBA")
    im.thumbnail((size, size), Image.Resampling.LANCZOS)
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    rgb = bg.convert("RGB")
    rgb.save(dest, "PNG", optimize=True, compress_level=9)


def write_webp(im: Image.Image, dest: Path, size: int = 128, quality: int = 82) -> None:
    im = im.convert("RGBA")
    im.thumbnail((size, size), Image.Resampling.LANCZOS)
    im.save(dest, "WEBP", quality=quality, method=6)


def write_minimal_svg(png_name: str = "daab-logo.png", size: int = 256) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'width="{size}" height="{size}" viewBox="0 0 {size} {size}" role="img" aria-hidden="true">\n'
        f'  <image href="{png_name}" width="{size}" height="{size}"/>\n'
        f"</svg>\n"
    )


def main() -> int:
    if SVG_BACKUP.is_file() and SVG_BACKUP.stat().st_size > 10_000:
        source = SVG_BACKUP
    elif SVG.is_file() and SVG.stat().st_size > 10_000:
        source = SVG
    else:
        raise SystemExit(f"Missing logo source ({SVG_BACKUP} or large {SVG})")
    before = source.stat().st_size
    text = source.read_text(encoding="utf-8", errors="replace")
    im = extract_embedded_png(text)
    if im is None:
        raise SystemExit("Could not find embedded PNG in logo source")

    write_optimized_png(im, PNG, size=128)
    write_webp(im, WEBP, size=128, quality=82)
    SVG.write_text(write_minimal_svg(png_name="daab-logo.png", size=128), encoding="utf-8", newline="\n")
    print(f"logo source: {before // 1024} KB")
    print(f"daab-logo.png: {PNG.stat().st_size / 1024:.1f} KB")
    print(f"daab-logo.webp: {WEBP.stat().st_size / 1024:.1f} KB")
    print(f"daab-logo.png: {SVG.stat().st_size} bytes (wrapper)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

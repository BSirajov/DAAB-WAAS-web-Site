#!/usr/bin/env python3
"""Create SVG logo files (external PNG reference + normalized PNG)."""
from __future__ import annotations

import sys
from io import BytesIO
from pathlib import Path

from PIL import Image

from _paths import ROOT

IMAGES = ROOT / "images"

JOBS = [
    (IMAGES / "DİDK Loqo.jpg", "didk-emblem", "State Committee on Diaspora Affairs (DİDK)"),
    (IMAGES / "ETN.png", "etn-logo", "Ministry of Science and Education (ETN)"),
]


def write_logo(src: Path, name: str, label: str) -> None:
    img = Image.open(src).convert("RGBA")
    w, h = img.size
    png_path = IMAGES / f"{name}.png"
    img.save(png_path, "PNG")

    svg = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" '
        f'aria-label="{label}">\n'
        f"<title>{label}</title>\n"
        f'<image href="{name}.png" width="{w}" height="{h}" '
        f'preserveAspectRatio="xMidYMid meet"/>\n'
        "</svg>\n"
    )
    svg_path = IMAGES / f"{name}.svg"
    svg_path.write_text(svg, encoding="utf-8")
    print(
        f"Wrote {svg_path.relative_to(ROOT)} + {png_path.name} "
        f"({w}×{h}, svg {svg_path.stat().st_size} B)"
    )


def main() -> None:
    for src, name, label in JOBS:
        if not src.is_file():
            print(f"Missing: {src}", file=sys.stderr)
            sys.exit(1)
        write_logo(src, name, label)


if __name__ == "__main__":
    main()

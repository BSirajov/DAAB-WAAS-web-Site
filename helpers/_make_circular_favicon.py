#!/usr/bin/env python3
"""Build circular transparent favicon assets from images/daab-logo.png."""
from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

try:
    from _paths import ROOT
except ImportError:
    from helpers._paths import ROOT  # type: ignore

SRC = ROOT / "images" / "daab-logo.png"
OUT_PNG = ROOT / "images" / "daab-favicon.png"
OUT_ICO = ROOT / "favicon.ico"
DEPLOY_ICO = ROOT / "Deployment" / "favicon.ico"


def circularize(im: Image.Image, size: int = 128) -> Image.Image:
    """Return a square RGBA image with the logo clipped to a circle (transparent corners)."""
    im = im.convert("RGBA")
    # Fill any existing transparency with white before masking so logo stays solid.
    solid = Image.new("RGBA", im.size, (255, 255, 255, 255))
    solid.alpha_composite(im)
    solid = solid.resize((size, size), Image.Resampling.LANCZOS)

    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    # 1px inset avoids fringing on the outer ring
    draw.ellipse((1, 1, size - 2, size - 2), fill=255)

    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(solid, mask=mask)
    return out


def write_ico(circle_128: Image.Image, dest: Path) -> None:
    sizes = [(16, 16), (32, 32), (48, 48)]
    frames = [circle_128.resize(s, Image.Resampling.LANCZOS) for s in sizes]
    dest.parent.mkdir(parents=True, exist_ok=True)
    frames[0].save(
        dest,
        format="ICO",
        sizes=[(im.width, im.height) for im in frames],
        append_images=frames[1:],
    )


def main() -> int:
    if not SRC.is_file():
        raise SystemExit(f"Missing source logo: {SRC}")
    circle = circularize(Image.open(SRC), size=128)
    OUT_PNG.parent.mkdir(parents=True, exist_ok=True)
    circle.save(OUT_PNG, "PNG", optimize=True)
    write_ico(circle, OUT_ICO)
    if (ROOT / "Deployment").is_dir():
        write_ico(circle, DEPLOY_ICO)
        deploy_png = ROOT / "Deployment" / "images" / "daab-favicon.png"
        deploy_png.parent.mkdir(parents=True, exist_ok=True)
        circle.save(deploy_png, "PNG", optimize=True)
    print(f"Wrote {OUT_PNG.relative_to(ROOT)} ({OUT_PNG.stat().st_size} bytes)")
    print(f"Wrote {OUT_ICO.relative_to(ROOT)} ({OUT_ICO.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

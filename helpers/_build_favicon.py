#!/usr/bin/env python3
"""Write favicon.ico at repo root from images/daab-logo.png."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

from _paths import ROOT

SRC = ROOT / "images" / "daab-logo.png"
OUT = ROOT / "favicon.ico"


def main() -> int:
    if not SRC.is_file():
        raise SystemExit(f"Missing {SRC}")
    with Image.open(SRC) as im:
        im = im.convert("RGBA")
        im.thumbnail((32, 32), Image.Resampling.LANCZOS)
        OUT.write_bytes(b"")  # ensure overwrite
        im.save(OUT, format="ICO", sizes=[(32, 32)])
    print(f"Wrote {OUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

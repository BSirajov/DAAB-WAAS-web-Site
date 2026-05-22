"""Build Eldar Əhədov card portrait from Forum docx (image16.jpeg)."""
from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
SRC = Path(__file__).resolve().parent / "_docx_media" / "image16.jpeg"
DST = ROOT / "images" / "scientists-photos" / "eldar-ehedov.png"
TARGET = (148, 176)
BG = (247, 251, 255)


def normalize_portrait(src: Path, dst: Path) -> None:
    im = Image.open(src).convert("RGB")
    w, h = im.size
    target_ratio = TARGET[0] / TARGET[1]
    ratio = w / h
    if ratio > target_ratio:
        nw = int(h * target_ratio)
        left = (w - nw) // 2
        im = im.crop((left, 0, left + nw, h))
    else:
        nh = int(w / target_ratio)
        top = int((h - nh) * 0.08)
        top = max(0, min(top, h - nh))
        im = im.crop((0, top, w, top + nh))
    im = im.resize(TARGET, Image.Resampling.LANCZOS)
    im.save(dst, format="PNG", optimize=True)
    print("saved", dst, dst.stat().st_size, im.size)


def main() -> None:
    if not SRC.exists():
        raise SystemExit(f"missing {SRC}; run docx media extract first")
    normalize_portrait(SRC, DST)


if __name__ == "__main__":
    main()

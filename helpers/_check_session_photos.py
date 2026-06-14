#!/usr/bin/env python3
"""Analyze session table photo aspect ratios for clipping risk."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

try:
    from PIL import Image
except ImportError:
    Image = None  # type: ignore


def main() -> None:
    html_path = ROOT / "documents/preview/forum_sessions_organization.html"
    if not html_path.is_file():
        print("Run _build_sessions_preview.py first", file=sys.stderr)
        raise SystemExit(1)

    html = html_path.read_text(encoding="utf-8")
    photos = sorted(set(re.findall(r"scientists-photos/([^\"?]+)", html)))
    photo_root = ROOT / "images/scientists-photos"
    print(f"Unique photos referenced: {len(photos)}")

    if Image is None:
        print("Pillow not installed — skipping dimension analysis")
        return

    tall: list[tuple[str, int, int, float]] = []
    wide: list[tuple[str, int, int, float]] = []
    missing: list[str] = []

    for name in photos:
        path = photo_root / name
        if not path.is_file():
            missing.append(name)
            continue
        with Image.open(path) as im:
            w, h = im.size
        ratio = h / w if w else 0.0
        if ratio > 1.35:
            tall.append((name, w, h, ratio))
        elif ratio < 0.85:
            wide.append((name, w, h, ratio))

    if missing:
        print(f"Missing files ({len(missing)}):")
        for m in missing:
            print(f"  {m}")

    print(f"Tall portraits h/w > 1.35 ({len(tall)}) — cover crop risk:")
    for item in tall:
        print(f"  {item[0]}: {item[1]}x{item[2]} ({item[3]:.2f})")

    print(f"Wide images h/w < 0.85 ({len(wide)}):")
    for item in wide:
        print(f"  {item[0]}: {item[1]}x{item[2]} ({item[3]:.2f})")


if __name__ == "__main__":
    main()

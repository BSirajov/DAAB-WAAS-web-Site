#!/usr/bin/env python3
"""Report hardcoded design values outside daab-tokens.css (for design-system docs)."""
from __future__ import annotations

import re
from collections import defaultdict
from pathlib import Path

from _paths import ROOT

HEX = re.compile(r"#[0-9a-fA-F]{3,8}\b")
RGBA_BLUE = re.compile(r"rgba\(\s*0\s*,\s*105\s*,\s*180", re.I)
INLINE_STYLE_PAGES: list[str] = []

SKIP = {"daab-tokens.css"}


def scan_css() -> dict[str, list[str]]:
    hits: dict[str, list[str]] = defaultdict(list)
    for path in sorted((ROOT / "css").glob("*.css")):
        if path.name in SKIP:
            continue
        text = path.read_text(encoding="utf-8")
        hexes = set(HEX.findall(text))
        if hexes:
            hits[path.name] = sorted(hexes)[:20]
    return hits


def scan_html_inline() -> list[str]:
    pages: list[str] = []
    for base in (ROOT / "az", ROOT / "en"):
        if not base.is_dir():
            continue
        for path in base.rglob("*.html"):
            text = path.read_text(encoding="utf-8")
            if "<style>" in text.lower():
                pages.append(str(path.relative_to(ROOT)).replace("\\", "/"))
    return sorted(pages)


def main() -> None:
    print("=== CSS files with literal hex colors (excluding daab-tokens.css) ===\n")
    for name, colors in scan_css().items():
        print(f"{name}: {', '.join(colors[:12])}{'…' if len(colors) > 12 else ''}")

    print("\n=== HTML pages with inline <style> blocks ===\n")
    for p in scan_html_inline():
        print(p)

    rgba_files = []
    for path in (ROOT / "css").glob("*.css"):
        if path.name in SKIP:
            continue
        if RGBA_BLUE.search(path.read_text(encoding="utf-8")):
            rgba_files.append(path.name)
    print("\n=== CSS still using rgba(0, 105, 180, …) ===\n")
    print(", ".join(sorted(set(rgba_files))))


if __name__ == "__main__":
    main()

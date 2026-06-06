#!/usr/bin/env python3
"""Normalize prominent figure profile heroes to the DAAB site header pattern."""
from __future__ import annotations

import sys
from pathlib import Path

from _paths import ROOT
from _prominent_figure_hero import transform_page_html

FIGURES = ROOT / "az" / "prominent_figures"


def main() -> None:
    n = 0
    for group in ("azturk", "world"):
        for path in sorted((FIGURES / group).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            out, changed = transform_page_html(text)
            if changed:
                path.write_text(out, encoding="utf-8", newline="\n")
                n += 1
                print(path.relative_to(ROOT))
    print(f"Updated {n} profile hero sections")


if __name__ == "__main__":
    main()

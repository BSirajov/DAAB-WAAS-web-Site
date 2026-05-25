#!/usr/bin/env python3
"""Remove İbrət nəticəsi / Reflection blocks from forum impressions pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

KICKERS = (
    r"(?:İbrət nəticəsi|Ümumi ibrət nəticəsi|Reflection|Overall summary|Overall reflection)"
)
PAT = re.compile(
    rf'<p class="card-lead">{KICKERS}</p><p class="card-text">.*?</p>',
    re.I | re.S,
)

PATHS = (
    ROOT / "az" / "forum" / "2024" / "impressions.html",
    ROOT / "en" / "forum" / "2024" / "impressions.html",
)


def main() -> None:
    for path in PATHS:
        text = path.read_text(encoding="utf-8")
        new, n = PAT.subn("", text)
        if n:
            path.write_text(new, encoding="utf-8", newline="\n")
        print(f"{path.relative_to(ROOT)}: removed {n} moral block(s)")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract unique world-profile contribution phrases for EN translation."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

WORLD = ROOT / "az" / "prominent_figures" / "world"
PAT = re.compile(r"Onun əsas töhfəsi (.+?) ilə bağlıdır\.")


def main() -> None:
    items: list[tuple[str, str]] = []
    for p in sorted(WORLD.glob("*.html")):
        t = p.read_text(encoding="utf-8")
        m = PAT.search(t)
        if not m:
            print("MISSING", p.name)
            continue
        items.append((p.stem, m.group(1).strip()))
    print(f"Found {len(items)} contributions")
    for stem, az in items:
        print(f"    # {stem}")
        print(f'    ("{az}",')
        print(f'     ""),')


if __name__ == "__main__":
    main()

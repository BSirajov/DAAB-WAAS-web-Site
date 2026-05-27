#!/usr/bin/env python3
"""Add daab-content-hero.css to foundation, mission, membership pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

LINK = '<link href="{root}css/daab-content-hero.css?v=1" rel="stylesheet"/>\n'
PAGES = [
    "en/foundation.html",
    "az/foundation.html",
    "en/mission.html",
    "az/mission.html",
    "en/membership.html",
    "az/membership.html",
]


def asset_root(rel: str) -> str:
    depth = len(Path(rel).parts) - 1
    return "../" * depth if depth else "./"


def main() -> None:
    for rel in PAGES:
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        if "daab-content-hero.css" in text:
            continue
        root = asset_root(rel)
        tag = LINK.format(root=root)
        anchor = f'<link href="{root}css/daab-back-to-top.css?v=1" rel="stylesheet"/>'
        if anchor not in text:
            anchor = f'<link href="{root}css/daab-membership-page.css?v=2" rel="stylesheet"/>'
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + tag.strip())
            path.write_text(text, encoding="utf-8")
            print("linked", rel)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Extract unique AZ strings from presentations.html for EN phrase map."""
from __future__ import annotations

import json
import re
from pathlib import Path

from bs4 import BeautifulSoup

from _paths import ROOT

AZ = ROOT / "az" / "forum" / "2024" / "presentations.html"
OUT = ROOT / "helpers" / "_presentations_az_strings.json"


def main() -> None:
    soup = BeautifulSoup(AZ.read_text(encoding="utf-8"), "html.parser")
    texts: set[str] = set()
    for el in soup.select(
        ".card-title, .card-lead, .card-text, .program-subhead, .timeline-list a, "
        "th, td, li, .panel-copy, h1, .widget-head span, .moral-box, blockquote"
    ):
        t = " ".join(el.get_text(" ", strip=True).split())
        if t and re.search(r"[əğıöüşçƏĞİÖÜŞÇ]", t):
            texts.add(t)
    ordered = sorted(texts, key=lambda s: (-len(s), s))
    OUT.write_text(json.dumps(ordered, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"wrote {len(ordered)} strings to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

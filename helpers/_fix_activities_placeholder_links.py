#!/usr/bin/env python3
"""Remove placeholder card-source href=\"#\" from activities pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PAT = re.compile(
    r'<a\s+rel="noopener noreferrer"\s+class="card-source"\s+href="#"\s+target="_blank">\s*'
    r'(<svg.*?</svg>\s*[^<]+?)\s*</a>',
    re.DOTALL | re.IGNORECASE,
)


def fix(text: str) -> str:
    return PAT.sub(r'<span class="card-source card-source--static">\1</span>', text)


for lang in ("az", "en"):
    path = ROOT / lang / "activities.html"
    text = path.read_text(encoding="utf-8")
    updated = fix(text)
    if updated == text:
        print(f"No change: {path}")
        continue
    path.write_text(updated, encoding="utf-8")
    print(f"Fixed placeholder links: {path}")

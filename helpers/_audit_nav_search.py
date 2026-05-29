#!/usr/bin/env python3
"""Audit pages with nav for search script/CSS and nav-inner structure."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT


def audit() -> int:
    issues: list[str] = []
    paths = sorted((ROOT / "az").rglob("*.html")) + sorted((ROOT / "en").rglob("*.html"))
    for p in paths:
        rel_posix = p.relative_to(ROOT).as_posix()
        if rel_posix.endswith("application/application.html"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        if "nav-strip" not in text:
            continue
        rel = p.relative_to(ROOT).as_posix()
        if 'class="nav-inner"' not in text:
            issues.append(f"{rel}: missing .nav-inner")
        if "daab-search.js" not in text:
            issues.append(f"{rel}: missing daab-search.js")
        if "daab-search.css" not in text:
            issues.append(f"{rel}: missing daab-search.css")
        inner_count = text.count('class="nav-inner"')
        if inner_count != 1:
            issues.append(f"{rel}: expected one nav-inner, found {inner_count}")

    if issues:
        print("NAV SEARCH AUDIT — issues:")
        for line in issues:
            print(" ", line)
        return 1
    print("NAV SEARCH AUDIT — OK (all nav pages include search assets + nav-inner)")
    return 0


if __name__ == "__main__":
    raise SystemExit(audit())

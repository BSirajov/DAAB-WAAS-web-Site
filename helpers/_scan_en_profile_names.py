#!/usr/bin/env python3
"""Scan EN prominent-figure pages for Azerbaijani characters in display names."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")
EN_ROOT = ROOT / "en" / "prominent_figures"
CHECKS = [
    ("h1", re.compile(r"<h1>([^<]+)</h1>")),
    ("title", re.compile(r"<title>([^<]+)</title>")),
    ("data-daab-profile-name", re.compile(r'data-daab-profile-name="([^"]*)"'),
    ),
    ("nav-person-name", re.compile(r'class="nav-person-name">([^<]+)</div>')),
    ("sidebar full name", re.compile(r'info-label">Full name</span><span class="info-val">([^<]+)</span>')),
]


def main() -> None:
    issues: list[str] = []
    for path in sorted(EN_ROOT.rglob("*.html")):
        if path.name == "hazirlanir.html" or path.parent.name.endswith("_"):
            continue
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT)
        for label, pat in CHECKS:
            for m in pat.finditer(text):
                val = m.group(1).strip()
                if val and AZ_CHAR.search(val):
                    issues.append(f"{rel} [{label}]: {val}")
    print(f"Issues: {len(issues)}")
    for line in issues[:80]:
        print(line)


if __name__ == "__main__":
    main()

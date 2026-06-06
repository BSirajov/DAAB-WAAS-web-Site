#!/usr/bin/env python3
"""Remove hero-era-badge above profile name (between breadcrumbs and h1)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

FIGURES = ROOT / "az" / "prominent_figures"

ERA_BADGE_RE = re.compile(
    r"<div class=\"hero-era-badge\">[^<]*</div>\s*",
    re.IGNORECASE,
)


def strip_era_badge(html: str) -> tuple[str, bool]:
    new_html, n = ERA_BADGE_RE.subn("", html, count=1)
    return new_html, n > 0


def main() -> None:
    n = 0
    for group in ("azturk", "world"):
        for path in sorted((FIGURES / group).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            out, changed = strip_era_badge(text)
            if changed:
                path.write_text(out, encoding="utf-8", newline="\n")
                n += 1
    print(f"Removed hero-era-badge from {n} profile pages")


if __name__ == "__main__":
    main()

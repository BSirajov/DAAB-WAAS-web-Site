#!/usr/bin/env python3
"""Remove hero blocks now in daab-content-hero.css from page-specific stylesheets."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CSS = ROOT / "css"


def strip_between(content: str, start_pat: str, end_pat: str) -> str:
    """Remove from start_pat through line before end_pat."""
    m_start = re.search(start_pat, content, re.M)
    if not m_start:
        return content
    m_end = re.search(end_pat, content[m_start.end() :], re.M)
    if not m_end:
        return content
    end = m_start.end() + m_end.start()
    return content[: m_start.start()] + content[end:]


def strip_foundation_mission() -> None:
    for name in ("daab-foundation-page.css", "daab-mission-page.css"):
        path = CSS / name
        text = path.read_text(encoding="utf-8")
        # Drop shared hero through .panel-copy { ... }
        new = strip_between(
            text,
            r"^\.hero \{",
            r"^\.foundation-overview|^\.glass-card",
        )
        if new != text:
            path.write_text(new.lstrip(), encoding="utf-8")
            print("stripped hero from", name)


def strip_membership() -> None:
    path = CSS / "daab-membership-page.css"
    text = path.read_text(encoding="utf-8")
    # Remove minified hero lines (bare .hero{ not .membership-page)
    text = re.sub(
        r"^\.hero\{.*\n\.hero-wrap\{.*\n\.hero h1\{.*\n\.hero-panel\{.*\n",
        "",
        text,
        flags=re.M,
    )
    # Remove duplicate block comment + membership-page hero through panel-copy
    text = strip_between(
        text,
        r"/\* Membership page hero",
        r"^\.membership-page \.btn-primary",
    )
    path.write_text(text, encoding="utf-8")
    print("stripped hero from daab-membership-page.css")


def main() -> None:
    strip_foundation_mission()
    strip_membership()


if __name__ == "__main__":
    main()

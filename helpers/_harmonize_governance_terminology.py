#!/usr/bin/env python3
"""Harmonize EN governance terminology: Executive Board (not Board of Directors) for WAAS."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

DEPLOY = (ROOT / "az", ROOT / "en")

# Longest-first; only WAAS/site-chrome patterns (not third-party boards).
EN_REPLACEMENTS: list[tuple[str, str]] = [
    ("Chair of the WAAS Board of Directors", "Chair of the WAAS Executive Board"),
    ("Co-Chairman of the Board of Directors of WAAS", "Co-Chairman of the WAAS Executive Board"),
    ("Co-Chairman of WAAS Board of Directors", "Co-Chairman of the WAAS Executive Board"),
    ("Member of WAAS Board of Directors", "Member of the WAAS Executive Board"),
    ("the WAAS Board of Directors", "the WAAS Executive Board"),
    ("WAAS Board of Directors", "WAAS Executive Board"),
    ('data-nav-id="executive-board">Board of Directors<', 'data-nav-id="executive-board">Executive Board<'),
    ('"executive-board", "Board of Directors"', '"executive-board", "Executive Board"'),
    ("Board of Directors leadership", "Executive Board leadership"),
    ("Board of Directors members, biographies", "Executive Board members, biographies"),
    ("Board of Directors and leadership", "Executive Board and leadership"),
    ("Board of Directors summary", "Executive Board summary"),
    ("Board of Directors members", "Executive Board members"),
    ("<title>WAAS — Board of Directors</title>", "<title>WAAS — Executive Board</title>"),
    ("<h1>Board of Directors</h1>", "<h1>Executive Board</h1>"),
    (
        "The Chair, Co-Chairs and members of the WAAS Board of Directors,",
        "The Chair, Co-Chairs and members of the WAAS Executive Board,",
    ),
    (
        '<span class="nav-dropdown-link-title">Board of Directors</span>',
        '<span class="nav-dropdown-link-title">Executive Board</span>',
    ),
    (
        "Board of Directors</a>",
        "Executive Board</a>",
    ),
    (
        "<h3 class=\"card-title\">\n              Board of Directors\n            </h3>",
        "<h3 class=\"card-title\">\n              Executive Board\n            </h3>",
    ),
    (
        "Chair of the Board of Directors of the World Association of Azerbaijani Scientists",
        "Chair of the WAAS Executive Board",
    ),
    ("Chair of the Board of Directors of WAAS", "Chair of the WAAS Executive Board"),
    (
        "As a member of the Board of Directors of the World Association of Azerbaijani Scientists (WAAS)",
        "As a member of the WAAS Executive Board",
    ),
    (
        "Board of Directors — structure, duties and powers",
        "Executive Board — structure, duties and powers",
    ),
    ("<li>Board of Directors,</li>", "<li>Executive Board,</li>"),
    (
        "Establishment, responsibilities and powers of the Board of Directors",
        "Establishment, responsibilities and powers of the Executive Board",
    ),
    (
        "Responsibilities and powers of the Board of Directors",
        "Responsibilities and powers of the Executive Board",
    ),
]

SOURCE_FILES = (
    ROOT / "i18n" / "ui.json",
    ROOT / "js" / "daab-primary-nav.js",
    ROOT / "helpers" / "_embed_static_nav.py",
)


def patch_text(text: str) -> tuple[str, int]:
    count = 0
    for old, new in EN_REPLACEMENTS:
        if old in text:
            n = text.count(old)
            text = text.replace(old, new)
            count += n
    return text, count


def patch_ui_json() -> int:
    path = ROOT / "i18n" / "ui.json"
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        '"executiveBoard": "Board of Directors"',
        '"executiveBoard": "Executive Board"',
    )
    text = text.replace(
        '"chairRole": "Chair of the WAAS Board of Directors"',
        '"chairRole": "Chair of the WAAS Executive Board"',
    )
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return 1
    return 0


def patch_sources() -> list[str]:
    updated: list[str] = []
    for path in SOURCE_FILES:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        new_text, n = patch_text(text)
        if path.name == "_embed_static_nav.py":
            new_text2 = new_text.replace(
                '"Executive board", "Leadership and governance structure"',
                '"Executive Board", "Leadership and governance structure"',
            )
            if new_text2 != new_text:
                new_text = new_text2
                n += 1
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            updated.append(str(path.relative_to(ROOT)))
    return updated


def patch_html() -> list[str]:
    updated: list[str] = []
    for base in DEPLOY:
        if base.name != "en":
            continue
        for path in sorted(base.rglob("*.html")):
            if path.parent.name == "application":
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            new_text, n = patch_text(text)
            if n and new_text != text:
                path.write_text(new_text, encoding="utf-8", newline="\n")
                updated.append(path.relative_to(ROOT).as_posix())
    return updated


def main() -> None:
    ui = patch_ui_json()
    sources = patch_sources()
    pages = patch_html()
    print(f"ui.json: {'updated' if ui else 'unchanged'}")
    print(f"Source files updated: {len(sources)}")
    for s in sources:
        print(f"  {s}")
    print(f"EN HTML pages updated: {len(pages)}")
    for p in pages[:15]:
        print(f"  {p}")
    if len(pages) > 15:
        print(f"  ... and {len(pages) - 15} more")


if __name__ == "__main__":
    main()

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
    ("Co-Chair of the WAAS Board of Directors", "Co-Chair of the WAAS Executive Board"),
    ("Co-Chairman of the WAAS Executive Board", "Co-Chair of the WAAS Executive Board"),
    ("Member of WAAS Board of Directors", "Member of the WAAS Executive Board"),
    ("the WAAS Board of Directors", "the WAAS Executive Board"),
    ("WAAS Board of Directors", "WAAS Executive Board"),
    ("WAAS Chairman of the Board", "Chair of the WAAS Executive Board"),
    ("WAAS Board Member,", "Member of the WAAS Executive Board,"),
    ("with the WAAS Board.", "with the WAAS Executive Board."),
    ("with the WAAS Board ", "with the WAAS Executive Board "),
    (
        "World Association of Azerbaijani Scientists Board of Directors",
        "WAAS Executive Board",
    ),
    ('("İdarə Heyəti", "Board of Directors")', '("İdarə Heyəti", "Executive Board")'),
    ('("İdarə heyəti", "Board of Directors")', '("İdarə heyəti", "Executive Board")'),
    ('"🎓 Board of Directors"', '"🎓 Executive Board"'),
    ('"Board of Directors", "Leadership and governance."', '"Executive Board", "Leadership and governance."'),
    ('"Board of Directors,",', '"Executive Board,",'),
    ('("Board of Directorsnin", "of the Board of Directors")', '("Board of Directorsnin", "of the Executive Board")'),
    ("Chair of the Board of Directors of WAAS", "Chair of the WAAS Executive Board"),
    ("Chair of the Board of Directors of the World Association of Azerbaijani Scientists", "Chair of the WAAS Executive Board"),
    (
        "As a member of the Board of Directors of the World Association of Azerbaijani Scientists (WAAS)",
        "As a member of the WAAS Executive Board",
    ),
    (
        "The Chair, Co-Chairs and members of the WAAS Board of Directors,",
        "The Chair, Co-Chairs and members of the WAAS Executive Board,",
    ),
    ("Board of Directors — structure, duties and powers", "Executive Board — structure, duties and powers"),
    (
        "Establishment, responsibilities and powers of the Board of Directors",
        "Establishment, responsibilities and powers of the Executive Board",
    ),
    (
        "Responsibilities and powers of the Board of Directors",
        "Responsibilities and powers of the Executive Board",
    ),
    ("Board of Directors leadership", "Executive Board leadership"),
    ("Board of Directors members, biographies", "Executive Board members, biographies"),
    ("Board of Directors and leadership", "Executive Board and leadership"),
    ("Board of Directors summary", "Executive Board summary"),
    ("Board of Directors members", "Executive Board members"),
    ("Board of Directors Co-Chair", "Executive Board Co-Chair"),
    ("Board of Directors Chair", "Executive Board Chair"),
    ("Board of Directors member", "Executive Board member"),
    ("Board of Directors members", "Executive Board members"),
    ('data-nav-id="executive-board">Board of Directors<', 'data-nav-id="executive-board">Executive Board<'),
    ('"executive-board", "Board of Directors"', '"executive-board", "Executive Board"'),
    ('executiveBoard: "Board of Directors"', 'executiveBoard: "Executive Board"'),
    ('"executiveBoard": "Board of Directors"', '"executiveBoard": "Executive Board"'),
    ("<title>WAAS — Board of Directors</title>", "<title>WAAS — Executive Board</title>"),
    ("<h1>Board of Directors</h1>", "<h1>Executive Board</h1>"),
    (
        '<span class="nav-dropdown-link-title">Board of Directors</span>',
        '<span class="nav-dropdown-link-title">Executive Board</span>',
    ),
    ("Board of Directors</a>", "Executive Board</a>"),
    (
        '<h3 class="card-title">\n              Board of Directors\n            </h3>',
        '<h3 class="card-title">\n              Executive Board\n            </h3>',
    ),
    ("<li>Board of Directors,</li>", "<li>Executive Board,</li>"),
    ('"Executive board", "Leadership and governance structure"', '"Executive Board", "Leadership and governance structure"'),
    ("Executive board", "Executive Board"),
]

SOURCE_FILES = (
    ROOT / "i18n" / "ui.json",
    ROOT / "i18n" / "page-panel-summaries.json",
    ROOT / "i18n" / "scientists-profiles.json",
    ROOT / "i18n" / "scientists-profiles-en.json",
    ROOT / "js" / "daab-primary-nav.js",
    ROOT / "js" / "daab-breadcrumbs.js",
    ROOT / "helpers" / "_embed_static_nav.py",
)

HELPER_GLOB = "helpers/*.py"


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
    new_text, _ = patch_text(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return 1
    return 0


def patch_file(path: Path) -> bool:
    if not path.is_file():
        return False
    text = path.read_text(encoding="utf-8", errors="replace")
    new_text, _ = patch_text(text)
    if new_text != text:
        path.write_text(new_text, encoding="utf-8", newline="\n")
        return True
    return False


def patch_sources() -> list[str]:
    updated: list[str] = []
    for path in SOURCE_FILES:
        if patch_file(path):
            updated.append(str(path.relative_to(ROOT)))
    for path in sorted(ROOT.glob(HELPER_GLOB)):
        if path.name == Path(__file__).name:
            continue
        if patch_file(path):
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
            if patch_file(path):
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
    for p in pages[:20]:
        print(f"  {p}")
    if len(pages) > 20:
        print(f"  ... and {len(pages) - 20} more")


if __name__ == "__main__":
    main()

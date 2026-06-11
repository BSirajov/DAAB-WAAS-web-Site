#!/usr/bin/env python3
"""One-time helper: export Forum 2026 content/frame files from live pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

MARKER = "<!-- FORUM_2026_CONTENT -->"
NAV_PLACEHOLDER_RE = re.compile(
    r'(<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">).*?(</div>\s*</div>\s*</nav>)',
    re.S,
)
TEMPLATES = ROOT / "templates"
AZ_PAGE = ROOT / "az" / "forum" / "2026" / "index.html"
EN_PAGE = ROOT / "en" / "forum" / "2026" / "index.html"


def split_page(path: Path) -> tuple[str, str, str]:
    text = path.read_text(encoding="utf-8")
    m = re.search(
        r'^(.*?<main class="news-feed main" id="content">)\s*(.*?)\s*(</main>.*)$',
        text,
        re.S,
    )
    if not m:
        raise SystemExit(f"Could not split main in {path}")
    prefix, content, suffix = m.group(1), m.group(2).strip(), m.group(3)
    frame = prefix + "\n" + MARKER + "\n" + suffix
    frame = NAV_PLACEHOLDER_RE.sub(
        r'\1<div class="nav-divider"></div>\2',
        frame,
        count=1,
    )
    return frame, content, text


def main() -> None:
    TEMPLATES.mkdir(exist_ok=True)
    for lang, page in (("az", AZ_PAGE), ("en", EN_PAGE)):
        frame, content, _ = split_page(page)
        (TEMPLATES / f"forum-2026-frame.{lang}.html").write_text(frame, encoding="utf-8", newline="\n")
        (TEMPLATES / f"forum-2026-content.{lang}.html").write_text(content + "\n", encoding="utf-8", newline="\n")
        print(f"Wrote forum-2026-frame.{lang}.html and forum-2026-content.{lang}.html")


if __name__ == "__main__":
    main()

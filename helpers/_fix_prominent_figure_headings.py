#!/usr/bin/env python3
"""Fix heading hierarchy on prominent-figure profile pages (h1 → h2 sections → h3 prose)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

PROFILE_DIRS = (
    ROOT / "az" / "prominent_figures",
    ROOT / "en" / "prominent_figures",
)

RE_SECTION_TITLE = re.compile(
    r'<div class="section-title">(.*?)</div>',
    re.DOTALL,
)
RE_PROSE_H4 = re.compile(
    r'(<div class="prose pf-profile-article">)(.*?)(</div>)',
    re.DOTALL,
)


def fix_profile_html(text: str) -> str:
    if 'data-daab-page-id="prominent-figure"' not in text:
        return text

    def section_repl(m: re.Match[str]) -> str:
        inner = m.group(1).strip()
        if inner.startswith("<h2"):
            return m.group(0)
        return f'<h2 class="section-title">{inner}</h2>'

    text = RE_SECTION_TITLE.sub(section_repl, text)

    def prose_repl(m: re.Match[str]) -> str:
        body = m.group(2).replace("<h4>", "<h3>").replace("</h4>", "</h3>")
        return m.group(1) + body + m.group(3)

    text = RE_PROSE_H4.sub(prose_repl, text)
    return text


def main() -> int:
    updated = 0
    for base in PROFILE_DIRS:
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            original = path.read_text(encoding="utf-8")
            new = fix_profile_html(original)
            if new != original:
                path.write_text(new, encoding="utf-8", newline="\n")
                updated += 1
    print(f"Fixed heading hierarchy in {updated} prominent-figure profile(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

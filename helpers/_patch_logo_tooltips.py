#!/usr/bin/env python3
"""Add title tooltips to .page-logo home links (AZ/EN)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

LOGO_LINK = re.compile(
    r'(<div class="page-logo"><a)(\s)(?![^>]*\btitle=)([^>]*?)(>)',
    re.I | re.DOTALL,
)
NAV_JS = re.compile(r"daab-primary-nav\.js\?v=\d+")


def tip_for(path: Path, attrs: str) -> str:
    p = path.as_posix().lower()
    if "/az/" in p:
        return "Ana səhifə"
    if "/en/" in p:
        return "Home page"
    if "DAAB ana" in attrs or 'aria-label="DAAB' in attrs:
        return "Ana səhifə"
    if "WAAS home" in attrs:
        return "Home page"
    return "Home page"


def main() -> None:
    count = 0
    for path in sorted(ROOT.rglob("*.html")):
        if any(x in path.parts for x in (".git", "helpers", "documents", "cv")):
            continue
        text = path.read_text(encoding="utf-8")
        if "page-logo" not in text:
            continue

        def repl(m: re.Match[str]) -> str:
            t = tip_for(path, m.group(3))
            return f'{m.group(1)}{m.group(2)}title="{t}" {m.group(3)}{m.group(4)}'

        new = LOGO_LINK.sub(repl, text)
        new = NAV_JS.sub("daab-primary-nav.js?v=23", new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            count += 1
            print(path.relative_to(ROOT))
    print(f"Updated {count} HTML file(s).")


if __name__ == "__main__":
    main()

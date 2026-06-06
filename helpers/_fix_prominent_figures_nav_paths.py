#!/usr/bin/env python3
"""Fix nav menu hrefs on az/prominent_figures/* profile pages (../../ → az/ locale root)."""
from __future__ import annotations

from pathlib import Path

from _embed_static_nav import NAV_AZ, PLACEHOLDER_RE, prominent_nav, patch
from _paths import ROOT

FIGURES = ROOT / "az" / "prominent_figures"


def fix_menu_hrefs(text: str) -> str:
    menu = prominent_nav(NAV_AZ)
    new_text, n = PLACEHOLDER_RE.subn(
        lambda m: m.group(1) + menu + m.group(3), text, count=1
    )
    if n == 0:
        return text
    return new_text


def main() -> None:
    n = 0
    for path in sorted(FIGURES.rglob("*.html")):
        if patch(path):
            n += 1
            continue
        text = path.read_text(encoding="utf-8")
        new_text = fix_menu_hrefs(text)
        if new_text != text:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            n += 1
    print(f"Fixed nav hrefs on {n} prominent figure profile pages")


if __name__ == "__main__":
    main()

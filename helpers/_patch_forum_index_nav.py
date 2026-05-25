#!/usr/bin/env python3
"""Add standard nav-strip to az|en/forum/2024/index.html."""
from __future__ import annotations

from _embed_static_nav import forum_nav_strip
from _paths import ROOT

SECTION_NAV = '<script src="../../../js/daab-section-nav.js?v=4" defer></script>\n'


def patch(path: str, lang: str, skip_line: str) -> None:
    file = ROOT / path
    text = file.read_text(encoding="utf-8")
    nav = forum_nav_strip(lang, active_nav_id="forum-2024")
    old = f"{skip_line}\n<div data-daab-nav-placeholder=\"1\"></div>"
    if old not in text:
        raise SystemExit(f"Pattern not found in {path}")
    text = text.replace(old, f"{skip_line}\n{nav}", 1)
    if "daab-section-nav.js" not in text:
        needle = '<script src="../../../js/daab-breadcrumbs.js?v=6" defer></script>\n'
        if needle not in text:
            needle = '<script src="../../../js/daab-breadcrumbs.js?v=5" defer></script>\n'
        text = text.replace(needle, needle + SECTION_NAV, 1)
    file.write_text(text, encoding="utf-8", newline="\n")
    print(f"Patched {path}")


def main() -> None:
    patch(
        "az/forum/2024/index.html",
        "az",
        '<a class="skip" href="#content">Məzmuna keç</a>',
    )
    patch(
        "en/forum/2024/index.html",
        "en",
        '<a class="skip" href="#content">Skip to content</a>',
    )


if __name__ == "__main__":
    main()

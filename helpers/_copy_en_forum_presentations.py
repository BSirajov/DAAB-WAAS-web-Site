#!/usr/bin/env python3
"""Create en/forum/2024/presentations.html from the Azerbaijani page."""
from __future__ import annotations

from pathlib import Path

from _paths import ROOT

SRC = ROOT / "az" / "forum" / "2024" / "presentations.html"
DST = ROOT / "en" / "forum" / "2024" / "presentations.html"


def main() -> None:
    text = SRC.read_text(encoding="utf-8")
    text = text.replace('lang="az"', 'lang="en"', 1)
    text = text.replace('data-daab-lang="az"', 'data-daab-lang="en"')
    text = text.replace(
        "Foruma təqdim olunmuş məruzələr — DAAB",
        "Forum 2024 presentations — WAAS",
    )
    text = text.replace(
        "Xaricdə Yaşayan Azərbaycanlı Alimlərin I Forumuna təqdim olunmuş elmi və akademik məruzələr.",
        "Scientific and academic presentations from the First Forum of Azerbaijani Scientists Living Abroad.",
    )
    text = text.replace("Məzmuna keç", "Skip to content")
    text = text.replace('aria-label="Əsas naviqasiya"', 'aria-label="Main navigation"')
    text = text.replace('aria-label="Menyunu aç"', 'aria-label="Open menu"')
    text = text.replace('aria-label="DAAB ana səhifə"', 'aria-label="WAAS home"')
    text = text.replace(
        '<span class="nav-brand-line">Dünya Azərbaycanlı</span><span class="nav-brand-line">Alimlər Birliyi</span>',
        '<span class="nav-brand-line">World Association of</span><span class="nav-brand-line">Azerbaijani Scientists</span>',
    )
    DST.parent.mkdir(parents=True, exist_ok=True)
    DST.write_text(text, encoding="utf-8", newline="\n")
    print(f"Wrote {DST.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

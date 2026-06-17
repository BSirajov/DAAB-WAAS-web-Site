#!/usr/bin/env python3
"""Apply main-feed portrait a11y rules without rebuilding page content from DOCX."""
from __future__ import annotations

from pathlib import Path

from bs4 import BeautifulSoup

from _paths import ROOT
from _refresh_official_pages import fix_speaker_photo_alts
from _speech_photos_lib import apply_feed_portrait_a11y

PAGES = (
    (ROOT / "az" / "forum" / "2024" / "rector_speeches.html", "az"),
    (ROOT / "en" / "forum" / "2024" / "rector_speeches.html", "en"),
    (ROOT / "az" / "forum" / "2024" / "anas_leadership_speeches.html", "az"),
    (ROOT / "en" / "forum" / "2024" / "anas_leadership_speeches.html", "en"),
    (ROOT / "az" / "forum" / "2024" / "official.html", "az"),
    (ROOT / "en" / "forum" / "2024" / "official.html", "en"),
    (ROOT / "az" / "forum" / "2024" / "presentations.html", "az"),
    (ROOT / "en" / "forum" / "2024" / "presentations.html", "en"),
)


def patch_page(path: Path, lang: str) -> tuple[int, int]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    if path.name == "official.html":
        fix_speaker_photo_alts(soup, lang)
    decorative, informative = apply_feed_portrait_a11y(soup)
    path.write_text(str(soup), encoding="utf-8", newline="\n")
    return decorative, informative


def main() -> None:
    total_dec = 0
    total_inf = 0
    for path, lang in PAGES:
        if not path.is_file():
            print(f"  skip (missing): {path.relative_to(ROOT)}")
            continue
        dec, inf = patch_page(path, lang)
        total_dec += dec
        total_inf += inf
        print(
            f"  {path.relative_to(ROOT)}: {dec} decorative, {inf} informative portrait(s)"
        )
    print(f"Done — {total_dec} decorative, {total_inf} informative across speech pages.")


if __name__ == "__main__":
    main()

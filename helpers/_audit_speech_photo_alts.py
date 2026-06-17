#!/usr/bin/env python3
"""Audit main-feed forum portrait alts (speech + presentation cards)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup

from _paths import ROOT
from _speech_photos_lib import is_long_speech_heading

SPEECH_PAGES = (
    ROOT / "az" / "forum" / "2024" / "rector_speeches.html",
    ROOT / "en" / "forum" / "2024" / "rector_speeches.html",
    ROOT / "az" / "forum" / "2024" / "anas_leadership_speeches.html",
    ROOT / "en" / "forum" / "2024" / "anas_leadership_speeches.html",
    ROOT / "az" / "forum" / "2024" / "official.html",
    ROOT / "en" / "forum" / "2024" / "official.html",
    ROOT / "az" / "forum" / "2024" / "presentations.html",
    ROOT / "en" / "forum" / "2024" / "presentations.html",
)


def audit_page(path: Path) -> list[str]:
    issues: list[str] = []
    rel = path.relative_to(ROOT).as_posix()
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for article in soup.select("main.news-feed article.news-card"):
        aid = article.get("id", "?")
        title_el = article.select_one(".card-title")
        title = title_el.get_text(" ", strip=True) if title_el else ""
        long_heading = is_long_speech_heading(title)
        for img in article.select(".speech-card-photo, .presentation-card-photo"):
            alt = (img.get("alt") or "").strip()
            hidden = img.get("aria-hidden") == "true"
            if long_heading:
                if not alt:
                    issues.append(f"{rel} #{aid}: informative portrait missing alt")
                elif hidden:
                    issues.append(f"{rel} #{aid}: official portrait must not be aria-hidden")
                continue
            if alt and not hidden:
                na = re.sub(r"\s+", " ", alt).casefold()
                nt = re.sub(r"\s+", " ", title).casefold()
                if na == nt or (na and nt and (na in nt or nt in na)):
                    issues.append(
                        f"{rel} #{aid}: redundant portrait alt duplicates card-title"
                    )
            elif not alt and not hidden:
                issues.append(f"{rel} #{aid}: empty portrait alt without aria-hidden")
    return issues


def main() -> int:
    all_issues: list[str] = []
    for path in SPEECH_PAGES:
        if path.is_file():
            all_issues.extend(audit_page(path))

    print("Speech / presentation portrait alt audit\n")
    if all_issues:
        print(f"ISSUES ({len(all_issues)})")
        for item in all_issues:
            print(f"  - {item}")
        return 1

    print("OK — all main-feed portraits follow decorative vs informative rules.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""Populate story cards in live stories.html from forum_2024 Word documents."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from docx import Document

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "helpers") not in sys.path:
    sys.path.insert(0, str(ROOT / "helpers"))

from _build_stories_from_docx import (  # noqa: E402
    DOCX_AZ,
    DOCX_EN,
    OUT_AZ,
    OUT_EN,
    parse_az_docx,
    parse_en_docx,
    story_card,
    toc_items,
)


def cards_html(data: dict) -> str:
    return "".join(story_card(s, lang="az") for s in data["sections"])


def cards_html_en(data: dict) -> str:
    return "".join(story_card(s, lang="en") for s in data["sections"])


def patch_page(path: Path, cards: str, toc: str) -> None:
    text = path.read_text(encoding="utf-8")
    new_text, n = re.subn(
        r'(<main class="news-feed main" id="content">\n\n)(.*?)(\n</main>)',
        lambda m: m.group(1) + cards + m.group(3),
        text,
        count=1,
        flags=re.DOTALL,
    )
    if n != 1:
        raise SystemExit(f"Could not patch main block in {path}")
    new_text, n_toc = re.subn(
        r'(<ul class="timeline-list" id="hekayelerTOC">\n)(.*?)(\n</ul>)',
        lambda m: m.group(1) + toc + m.group(3),
        new_text,
        count=1,
        flags=re.DOTALL,
    )
    if n_toc != 1:
        raise SystemExit(f"Could not patch sidebar TOC in {path}")
    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"Patched {path.relative_to(ROOT)}")


def main() -> None:
    if not DOCX_AZ.is_file():
        raise SystemExit(f"Missing {DOCX_AZ.relative_to(ROOT)}")
    if not DOCX_EN.is_file():
        raise SystemExit(f"Missing {DOCX_EN.relative_to(ROOT)}")

    az_data = parse_az_docx(Document(str(DOCX_AZ)))
    en_data = parse_en_docx(Document(str(DOCX_EN)))

    if len(az_data["sections"]) != 4 or len(en_data["sections"]) != 4:
        raise SystemExit(
            f"Expected 4 stories; got AZ={len(az_data['sections'])} EN={len(en_data['sections'])}"
        )

    patch_page(OUT_AZ, cards_html(az_data), toc_items(az_data["sections"], lang="az"))
    patch_page(OUT_EN, cards_html_en(en_data), toc_items(en_data["sections"], lang="en"))

    for sec in az_data["sections"]:
        print(f"  AZ {sec['id']}: {len(sec['paragraphs'])} paragraphs")
    for sec in en_data["sections"]:
        print(f"  EN {sec['id']}: {len(sec['paragraphs'])} paragraphs")


if __name__ == "__main__":
    main()

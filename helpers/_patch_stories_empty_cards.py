#!/usr/bin/env python3
"""Replace story card bodies in live stories.html with empty shells (header + image only).

To restore story text from Word sources, use helpers/_populate_stories_from_docx.py instead.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "helpers") not in sys.path:
    sys.path.insert(0, str(ROOT / "helpers"))

from _build_stories_from_docx import parse_docx, story_card  # noqa: E402
from docx import Document  # noqa: E402

OUT_AZ = ROOT / "az" / "forum" / "2024" / "stories.html"
OUT_EN = ROOT / "en" / "forum" / "2024" / "stories.html"
DOCX = ROOT / "forum_2024" / "Hekayələr.docx"


def cards_html(data: dict, *, lang: str) -> str:
    return "".join(story_card(s, lang=lang) for s in data["sections"])


def patch_page(path: Path, cards: str) -> None:
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
    path.write_text(new_text, encoding="utf-8", newline="\n")
    print(f"Patched {path.relative_to(ROOT)}")


def main() -> None:
    data = parse_docx(Document(str(DOCX)))
    patch_page(OUT_AZ, cards_html(data, lang="az"))
    patch_page(OUT_EN, cards_html(data, lang="en"))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Build az/en Forum 2026 pages from templates/forum-2026-*.html sources.

Usage (from repo root):
    python helpers/_build_forum_2026_page.py
    python helpers/_extract_forum_2026_sources.py   # refresh sources from live pages

After building, re-embed static nav on Forum 2026:
    python helpers/_embed_static_nav.py
"""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

MARKER = "<!-- FORUM_2026_CONTENT -->"
TEMPLATES = ROOT / "templates"
AZ_OUT = ROOT / "az" / "forum" / "2026" / "index.html"
EN_OUT = ROOT / "en" / "forum" / "2026" / "index.html"
TEMPLATE_OUT = ROOT / "templates" / "Forum 2026.html"

SV = STYLE_VERSIONS
JV = SCRIPT_VERSIONS


def bump_asset_versions(html: str) -> str:
    for name, ver in {**SCRIPT_VERSIONS, **STYLE_VERSIONS}.items():
        html = re.sub(
            re.escape(name) + r"\?v=\d+",
            f"{name}?v={ver}",
            html,
        )
    return html


def build_page(lang: str) -> str:
    frame = (TEMPLATES / f"forum-2026-frame.{lang}.html").read_text(encoding="utf-8")
    content = (TEMPLATES / f"forum-2026-content.{lang}.html").read_text(encoding="utf-8").strip()
    if MARKER not in frame:
        raise SystemExit(f"Missing {MARKER} in forum-2026-frame.{lang}.html")
    html = frame.replace(MARKER, content, 1)
    return bump_asset_versions(html)


def main() -> None:
    for lang, out in (("az", AZ_OUT), ("en", EN_OUT)):
        src_frame = TEMPLATES / f"forum-2026-frame.{lang}.html"
        src_content = TEMPLATES / f"forum-2026-content.{lang}.html"
        if not src_frame.is_file() or not src_content.is_file():
            raise SystemExit(
                "Missing Forum 2026 templates. Run: python helpers/_extract_forum_2026_sources.py"
            )
        html = build_page(lang)
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(html, encoding="utf-8", newline="\n")
        print(f"Wrote {out.relative_to(ROOT)}")

    note = (
        "<!-- DAAB site template — synced from helpers/_build_forum_2026_page.py. "
        "Edit templates/forum-2026-content.az.html (and .en.html); live: az|en/forum/2026/index.html -->\n"
    )
    TEMPLATE_OUT.write_text(note + build_page("az"), encoding="utf-8", newline="\n")
    print(f"Wrote {TEMPLATE_OUT.relative_to(ROOT)}")

    from importlib import import_module

    embed = import_module("_embed_static_nav")
    for out in (AZ_OUT, EN_OUT):
        if embed.patch(out):
            print(f"Embedded static nav: {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

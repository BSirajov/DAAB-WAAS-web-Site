#!/usr/bin/env python3
"""Insert legal links into every footer-bottom across az/, en/, and templates."""
from __future__ import annotations

import re
from pathlib import Path

from _footer_leader_snippets import FOOTER_AZ_BOTTOM, FOOTER_EN_BOTTOM
from _paths import ROOT


def detect_lang(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix().lower()
    parts = path.relative_to(ROOT).parts
    if parts and parts[0] == "en":
        return "en"
    if "forum-2026-frame.en" in rel or rel.endswith(".en.html"):
        return "en"
    if "/en/" in f"/{rel}" or rel.startswith("en/"):
        return "en"
    return "az"


def replace_footer_bottom(text: str, lang: str) -> str | None:
    bottom = FOOTER_AZ_BOTTOM if lang == "az" else FOOTER_EN_BOTTOM
    start = text.find('<div class="footer-bottom">')
    if start == -1:
        # Some templates use a single-line footer-bottom without nested copy div
        m = re.search(
            r'<div class="footer-bottom">\s*©[^<]*</div>',
            text,
        )
        if not m:
            return None
        return text[: m.start()] + bottom + text[m.end() :]

    footer_end = text.find("</footer>", start)
    scan_end = footer_end if footer_end != -1 else len(text)
    i = start + len('<div class="footer-bottom">')
    depth = 1
    while i < scan_end and depth:
        next_open = text.find("<div", i)
        next_close = text.find("</div>", i)
        if next_close == -1:
            return None
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            i = next_close + len("</div>")
    return text[:start] + bottom + text[i:]


def iter_html() -> list[Path]:
    out: list[Path] = []
    for lang in ("az", "en"):
        root = ROOT / lang
        if root.is_dir():
            out.extend(sorted(root.rglob("*.html")))
    templates = ROOT / "templates"
    if templates.is_dir():
        out.extend(sorted(templates.rglob("*.html")))
    return out


def needs_legal_links(text: str) -> bool:
    if "footer-bottom" not in text and "footer-pro" not in text:
        return False
    if "footer-legal-links" in text and "legal-notice" in text and "#page-title" in text:
        return False
    return "footer-bottom" in text or "footer-pro" in text


def main() -> int:
    updated = 0
    skipped = 0
    unchanged = 0
    for path in iter_html():
        text = path.read_text(encoding="utf-8")
        if "footer-bottom" not in text:
            skipped += 1
            continue
        lang = detect_lang(path)
        new_text = replace_footer_bottom(text, lang)
        if new_text is None:
            print(f"SKIP (no replaceable footer-bottom): {path.relative_to(ROOT)}")
            skipped += 1
            continue
        if new_text == text:
            unchanged += 1
            continue
        path.write_text(new_text, encoding="utf-8", newline="\n")
        updated += 1
    print(f"Done — {updated} updated, {unchanged} already ok, {skipped} skipped.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

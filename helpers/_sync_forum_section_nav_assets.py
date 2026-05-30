#!/usr/bin/env python3
"""Ensure Forum 2024 pages share section-nav CSS/JS versions (reference: forum/2024/index.html)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

FORUM_DIR = ROOT / "forum" / "2024"
NAV_MEGA = (
    '<link href="../../../css/daab-nav-mega.css?v=23" rel="stylesheet"/>'
)
FORUM_SECTION_NAV_CSS = (
    '<link href="../../../css/daab-forum-section-nav.css?v=1" rel="stylesheet"/>\n'
)
SECTION_NAV_JS = '<script src="../../../js/daab-section-nav.js?v=12" defer></script>'

NAV_MEGA_RE = re.compile(
    r'<link href="\.\./\.\./\.\./css/daab-nav-mega\.css\?v=\d+" rel="stylesheet"/>'
)
SECTION_NAV_CSS_RE = re.compile(
    r'<link href="\.\./\.\./\.\./css/daab-forum-section-nav\.css\?v=\d+" rel="stylesheet"/>\n?'
)
SECTION_NAV_JS_RE = re.compile(
    r'<script(?:\s+defer="")?\s+src="\.\./\.\./\.\./js/daab-section-nav\.js\?v=\d+"(?:\s+defer)?></script>'
)


def patch_html(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    if not NAV_MEGA_RE.search(text):
        return False

    text = NAV_MEGA_RE.sub(NAV_MEGA, text, count=1)

    text = SECTION_NAV_CSS_RE.sub("", text)
    text = text.replace(NAV_MEGA + "\n", NAV_MEGA + "\n" + FORUM_SECTION_NAV_CSS, 1)

    if SECTION_NAV_JS_RE.search(text):
        text = SECTION_NAV_JS_RE.sub(SECTION_NAV_JS, text, count=1)
    elif "daab-section-nav.js" not in text:
        needle = '<script src="../../../js/daab-primary-nav.js?v='
        idx = text.find(needle)
        if idx == -1:
            return False
        line_end = text.find("</script>", idx) + len("</script>")
        text = text[:line_end] + "\n" + SECTION_NAV_JS + text[line_end:]

    if "data-daab-nav-mount" not in text:
        text = re.sub(
            r"(<html\s+)",
            r'\1data-daab-nav-mount="1" ',
            text,
            count=1,
        )

    if text == original:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    changed = 0
    for lang in ("az", "en"):
        folder = ROOT / lang / "forum" / "2024"
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.html")):
            if patch_html(path):
                print(f"patched {path.relative_to(ROOT)}")
                changed += 1
    print(f"Done — {changed} file(s) updated.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Remove duplicate hub <style> blocks from locale home pages; use daab-hub-cards.css."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

HUB_LINK = '<link href="../css/daab-hub-cards.css?v=11" rel="stylesheet"/>\n'
HUB_LINK_RE = re.compile(
    r'<link\s+href="[^"]*daab-hub-cards\.css[^"]*"\s+rel="stylesheet"\s*/>\s*',
    re.I,
)
STYLE_BLOCK = re.compile(r"<style>.*?</style>\s*", re.DOTALL | re.IGNORECASE)
HTML_TAG = re.compile(r"(<html\b)([^>]*)(>)", re.IGNORECASE)


def migrate(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    def html_repl(m: re.Match[str]) -> str:
        attrs = m.group(2)
        if "daab-hub-page" in attrs:
            return m.group(0)
        if re.search(r'\bclass="', attrs, re.I):
            attrs = re.sub(
                r'class="([^"]*)"',
                lambda cm: f'class="{cm.group(1)} daab-hub-page"',
                attrs,
                count=1,
                flags=re.I,
            )
        else:
            attrs = attrs + ' class="daab-hub-page"'
        return m.group(1) + attrs + m.group(3)

    text = HTML_TAG.sub(html_repl, text, count=1)

    if "daab-hub-cards.css" not in text:
        anchor = '<link href="../css/daab-back-to-top.css?v=1" rel="stylesheet"/>'
        if anchor in text:
            text = text.replace(anchor, anchor + "\n" + HUB_LINK.strip())
        else:
            anchor2 = '<link href="../css/daab-common.css?v=27" rel="stylesheet"/>'
            text = text.replace(anchor2, anchor2 + "\n" + HUB_LINK.strip())

    text, n = STYLE_BLOCK.subn("", text, count=1)
    if n == 0 and text == original:
        return False
    path.write_text(text, encoding="utf-8")
    return True


def migrate_forum_index(path: Path) -> bool:
    """Forum hub: only strip <style> if daab-hub-cards is already linked."""
    text = path.read_text(encoding="utf-8")
    if "daab-hub-cards.css" not in text:
        return False
    new_text, n = STYLE_BLOCK.subn("", text, count=1)
    if n == 0:
        return False
    path.write_text(new_text, encoding="utf-8")
    return True


def main() -> None:
    for name in ("az/index.html", "en/index.html"):
        p = ROOT / name
        if p.is_file() and migrate(p):
            print("migrated", name)

    for lang in ("az", "en"):
        p = ROOT / lang / "forum" / "2024" / "index.html"
        if p.is_file() and migrate_forum_index(p):
            print("migrated", p.relative_to(ROOT))


if __name__ == "__main__":
    main()

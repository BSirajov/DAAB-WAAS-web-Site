#!/usr/bin/env python3
"""Inject global sticky-chrome CSS/JS on all deploy HTML pages."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

CSS_MARKER = "daab-sticky-chrome.css"
JS_MARKER = "daab-sticky-chrome.js"
CSS_LINK = '<link href="{prefix}css/daab-sticky-chrome.css?v=1" rel="stylesheet"/>'
JS_SCRIPT = '<script src="{prefix}js/daab-sticky-chrome.js?v=1" defer></script>'
MOBILE_SCRIPT_RE = re.compile(
    r'<script[^>]*daab-mobile\.js\?v=\d+[^>]*>\s*</script>',
    re.IGNORECASE,
)


def asset_prefix(html_path: Path) -> str:
    rel = html_path.relative_to(ROOT)
    depth = len(rel.parts) - 1
    return "../" * depth if depth else ""


def inject_file(path: Path) -> bool:
    if path.name == "index.html" and path.parent == ROOT:
        return False
    text = path.read_text(encoding="utf-8")
    if "daab-gateway" in text and 'class="daab-gateway"' in text:
        return False
    if CSS_MARKER in text and JS_MARKER in text:
        return False

    prefix = asset_prefix(path)
    changed = False

    if CSS_MARKER not in text:
        m = re.search(r'(<link href="[^"]*daab-mobile\.css\?v=\d+" rel="stylesheet"/>)', text)
        if not m:
            m = re.search(r'(<link href="[^"]*daab-common\.css\?v=\d+" rel="stylesheet"/>)', text)
        if m:
            insert = m.group(1) + "\n" + CSS_LINK.format(prefix=prefix)
            text = text.replace(m.group(1), insert, 1)
            changed = True

    if JS_MARKER not in text:
        m = MOBILE_SCRIPT_RE.search(text)
        if m:
            insert = m.group(0) + "\n" + JS_SCRIPT.format(prefix=prefix)
            text = text.replace(m.group(0), insert, 1)
            changed = True

    if changed:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changed


def main() -> int:
    updated = 0
    for base in (ROOT / "az", ROOT / "en"):
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            if path.parent.name == "application" and path.parent.parent.name in ("az", "en"):
                continue
            if inject_file(path):
                print(f"  {path.relative_to(ROOT)}")
                updated += 1
    print(f"Injected sticky chrome on {updated} page(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())

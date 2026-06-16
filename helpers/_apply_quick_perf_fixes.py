#!/usr/bin/env python3
"""Quick perf fixes: logo paths, stale font preconnect, CSS import merge."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

PRECONNECT_BLOCK = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/>\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com"(?:\s+crossorigin(?:="")?)?\s*/>\s*',
    re.I,
)
PRECONNECT_BLOCK_ALT = re.compile(
    r'<link href="https://fonts\.googleapis\.com" rel="preconnect"\s*/>\s*'
    r'<link(?:\s+crossorigin(?:="")?)?\s+href="https://fonts\.gstatic\.com" rel="preconnect"\s*/>\s*',
    re.I,
)


def patch_html(text: str) -> tuple[str, bool]:
    new = text
    new = new.replace("daab-logo.png", "daab-logo.png")
    new = PRECONNECT_BLOCK.sub("", new)
    new = PRECONNECT_BLOCK_ALT.sub("", new)
    new = new.replace('type="image/svg+xml"', 'type="image/png"')
    return new, new != text


def merge_common_css() -> bool:
    common = ROOT / "css" / "daab-common.css"
    tokens = ROOT / "css" / "daab-tokens.css"
    bg = ROOT / "css" / "daab-site-background.css"
    text = common.read_text(encoding="utf-8")
    if '@import url("daab-tokens.css")' not in text:
        return False
    merged = (
        "/* === DAAB SHARED DESIGN SYSTEM === */\n"
        f"/* --- daab-tokens.css (inlined) --- */\n{tokens.read_text(encoding='utf-8').strip()}\n\n"
        f"/* --- daab-site-background.css (inlined) --- */\n{bg.read_text(encoding='utf-8').strip()}\n\n"
        + re.sub(
            r"/\* === DAAB SHARED DESIGN SYSTEM === \*/\s*"
            r'@import url\("daab-tokens\.css"\);\s*'
            r'@import url\("daab-site-background\.css"\);\s*',
            "",
            text,
            count=1,
        )
    )
    common.write_text(merged, encoding="utf-8", newline="\n")
    return True


def main() -> int:
    targets = [ROOT / "index.html", ROOT / "404.html"]
    for base in (ROOT / "az", ROOT / "en"):
        targets.extend(sorted(base.rglob("*.html")))
    html_changed = 0
    for path in targets:
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        new, changed = patch_html(text)
        if changed:
            path.write_text(new, encoding="utf-8", newline="\n")
            html_changed += 1
    css_changed = merge_common_css()
    print(f"HTML pages updated: {html_changed}")
    print(f"CSS import merge: {'yes' if css_changed else 'skipped'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

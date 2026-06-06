#!/usr/bin/env python3
"""Keep only Geniş məqalə body on prominent figure profile pages."""
from __future__ import annotations

import re
import sys
from pathlib import Path

from _paths import ROOT

FIGURES = ROOT / "az" / "prominent_figures"

RE_SIMPLIFY = re.compile(
    r"<div class=\"tabs-bar\">.*?</div>\s*"
    r"<div class=\"tab-content active\" id=\"tab-short\">.*?</div>\s*"
    r"<div class=\"tab-content\" id=\"tab-medium\">.*?</div>\s*"
    r"<div class=\"tab-content\" id=\"tab-full\"><div class=\"prose\">(.*?)</div></div>",
    re.DOTALL | re.IGNORECASE,
)

TABS_SCRIPT_RE = re.compile(
    r'\n<script src="\.\./\.\./\.\./js/daab-prominent-figure-tabs\.js\?v=\d+" defer></script>',
)


def simplify_profile_html(html: str) -> tuple[str, bool]:
    if "tab-short" not in html and "tabs-bar" not in html:
        out = TABS_SCRIPT_RE.sub("", html)
        return out, out != html

    new_html, n = RE_SIMPLIFY.subn(
        r'<div class="prose pf-profile-article">\1</div>',
        html,
        count=1,
    )
    if not n:
        print("warn: tab pattern not matched", file=sys.stderr)
        return html, False

    new_html = TABS_SCRIPT_RE.sub("", new_html)
    return new_html, True


def main() -> None:
    n = 0
    for group in ("azturk", "world"):
        for path in sorted((FIGURES / group).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            out, changed = simplify_profile_html(text)
            if changed:
                path.write_text(out, encoding="utf-8", newline="\n")
                n += 1
    print(f"Simplified tabs on {n} profile pages")


if __name__ == "__main__":
    main()

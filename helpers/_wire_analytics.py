#!/usr/bin/env python3
"""Inject daab-analytics.js on all deployable HTML pages."""
from __future__ import annotations

import re

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, iter_deploy_html

ANALYTICS = "daab-analytics.js"
VER = SCRIPT_VERSIONS[ANALYTICS]

ANCHOR_PAT = re.compile(
    r'(<script(?:\s+defer(?:="")?)?\s+src="([^"]*?)js/daab-search\.js\?v=\d+"'
    r'(?:\s+defer(?:="")?)?\s*></script>)'
)
I18N_FALLBACK_PAT = re.compile(
    r'(<script(?:\s+defer(?:="")?)?\s+src="([^"]*?)js/daab-i18n\.js\?v=\d+"'
    r'(?:\s+defer(?:="")?)?\s*></script>)'
)
TAG = f'<script src="{{prefix}}js/{ANALYTICS}?v={VER}" defer></script>'


def wire_html(text: str) -> tuple[str, bool]:
    if ANALYTICS in text:
        return text, False

    def after_search(m: re.Match[str]) -> str:
        return m.group(1) + "\n" + TAG.format(prefix=m.group(2))

    new_text, n = ANCHOR_PAT.subn(after_search, text, count=1)
    if n:
        return new_text, True

    def after_i18n(m: re.Match[str]) -> str:
        return m.group(1) + "\n" + TAG.format(prefix=m.group(2))

    new_text, n = I18N_FALLBACK_PAT.subn(after_i18n, text, count=1)
    if n:
        return new_text, True

    return text, False


def main() -> None:
    wired = 0
    skipped = 0
    for path in iter_deploy_html():
        text = path.read_text(encoding="utf-8")
        new_text, changed = wire_html(text)
        if changed:
            path.write_text(new_text, encoding="utf-8", newline="\n")
            wired += 1
        else:
            skipped += 1
    print(f"daab-analytics.js wired: {wired}")
    print(f"unchanged or already wired: {skipped}")


if __name__ == "__main__":
    main()

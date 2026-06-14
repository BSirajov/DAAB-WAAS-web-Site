#!/usr/bin/env python3
"""Wrap decorative emoji in aria-hidden spans (footers, events, widget heads, hero CTAs)."""
from __future__ import annotations

import re
import sys

from _paths import ROOT
from _site_wide_cleanup import iter_deploy_html

FOOTER_REPLACEMENTS = (
    (re.compile(r'(<div class="footer-item">)(✉)( )'), r'\1<span aria-hidden="true">\2</span>\3'),
    (re.compile(r'(<div class="footer-item">)(☎)( )'), r'\1<span aria-hidden="true">\2</span>\3'),
    (re.compile(r'(<div class="footer-item">)(🌐)( )'), r'\1<span aria-hidden="true">\2</span>\3'),
)

EVENT_SPAN_RE = re.compile(
    r'(<span)(?![^>]*aria-hidden="true")(>(?:📜|🔎|⚕️|📚|📖|🎓|🔬|🌍|🚀|🤝|✉|☎|🌐)[^<]*</span>)'
)

WIDGET_HEAD_RE = re.compile(
    r'(<(?:button|div)[^>]*class="widget-head"[^>]*>)([\U0001F300-\U0001FAFF\U00002600-\U000027BF])'
)

HERO_EMOJI_RE = re.compile(
    r'(>)([\U0001F300-\U0001FAFF\U00002600-\U000027BF])(\s*[A-Za-zƏəÖöÜüĞğŞşÇçİı])'
)


def patch_html(text: str) -> str:
    for pattern, repl in FOOTER_REPLACEMENTS:
        text = pattern.sub(repl, text)
    text = EVENT_SPAN_RE.sub(r'\1 aria-hidden="true"\2', text)
    text = WIDGET_HEAD_RE.sub(
        r'\1<span aria-hidden="true">\2</span>',
        text,
    )
    # Hero / hub CTA lines like ">🤝 Bizi" — only when emoji immediately after tag open.
    text = HERO_EMOJI_RE.sub(r'\1<span aria-hidden="true">\2</span>\3', text)
    return text


def main() -> int:
    updated = 0
    for path in iter_deploy_html():
        original = path.read_text(encoding="utf-8")
        new = patch_html(original)
        if new != original:
            path.write_text(new, encoding="utf-8", newline="\n")
            updated += 1
    print(f"Updated decorative emoji a11y in {updated} HTML file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

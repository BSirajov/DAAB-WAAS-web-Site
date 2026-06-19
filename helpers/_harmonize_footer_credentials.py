#!/usr/bin/env python3
"""One-shot: harmonise footer leadership lines and footer-title markup across live HTML."""
from __future__ import annotations

import re

from _footer_leader_snippets import FOOTER_AZ_CREDENTIAL, FOOTER_EN_CREDENTIAL
from _paths import ROOT

EN_OLD_PRIZE = "Germany — James D. Murray Prize laureate"
EN_CREDENTIAL = FOOTER_EN_CREDENTIAL
AZ_CREDENTIAL = FOOTER_AZ_CREDENTIAL

REPLACEMENTS_AZ = [
    ("Germany — James D. Murray Distinguished Professor", AZ_CREDENTIAL),
    (
        "<br/>DAAB Sədr<br/>" + AZ_CREDENTIAL,
        "<br/>DAAB İdarə Heyətinin Sədri<br/>" + AZ_CREDENTIAL,
    ),
]

REPLACEMENTS_EN = [
    (EN_OLD_PRIZE, EN_CREDENTIAL),
]

FOOTER_TITLE_RE = re.compile(
    r'<div class="footer-title">([^<]+)</div>',
    re.IGNORECASE,
)

TEL_HREF = "tel:+905551474674"
TEL_DISPLAY = "+90 555 147 46 74"

# Bare emoji in footer contact rows (multiline-friendly).
FOOTER_EMOJI_RE = re.compile(
    r'(<div class="footer-item">\s*)([✉☎🌐])(\s*)',
    re.MULTILINE,
)

# Phone as plain span → tap-to-call link.
FOOTER_PHONE_SPAN_RE = re.compile(
    r'(<span aria-hidden="true">☎</span>\s*)<span>\s*'
    + re.escape(TEL_DISPLAY)
    + r'\s*</span>',
    re.IGNORECASE,
)

FOOTER_PHONE_BARE_RE = re.compile(
    r'(<div class="footer-item">\s*)<span aria-hidden="true">☎</span>\s*<span>\s*'
    + re.escape(TEL_DISPLAY)
    + r'\s*</span>',
    re.IGNORECASE,
)


def patch_footer_contact_markup(text: str) -> str:
    text = FOOTER_EMOJI_RE.sub(r'\1<span aria-hidden="true">\2</span>\3', text)
    text = FOOTER_PHONE_SPAN_RE.sub(
        r'\1<a href="' + TEL_HREF + '">' + TEL_DISPLAY + "</a>",
        text,
    )
    text = FOOTER_PHONE_BARE_RE.sub(
        r'\1<span aria-hidden="true">☎</span> <a href="' + TEL_HREF + '">' + TEL_DISPLAY + "</a>",
        text,
    )
    # Legacy inline rows: ☎ then newline + span phone.
    text = re.sub(
        r'(<div class="footer-item">\s*)<span aria-hidden="true">☎</span>\s*<span>\s*'
        + re.escape(TEL_DISPLAY)
        + r'\s*</span>',
        r'\1<span aria-hidden="true">☎</span> <a href="' + TEL_HREF + '">' + TEL_DISPLAY + "</a>",
        text,
        flags=re.I | re.S,
    )
    text = re.sub(
        r'(<div class="footer-item">\s*)☎\s*<span>\s*'
        + re.escape(TEL_DISPLAY)
        + r'\s*</span>',
        r'\1<span aria-hidden="true">☎</span> <a href="' + TEL_HREF + '">' + TEL_DISPLAY + "</a>",
        text,
        flags=re.I | re.S,
    )
    return text


def patch_file(path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("az/"):
        for old, new in REPLACEMENTS_AZ:
            text = text.replace(old, new)
    elif rel.startswith("en/"):
        for old, new in REPLACEMENTS_EN:
            text = text.replace(old, new)
    text = FOOTER_TITLE_RE.sub(r'<h4 class="footer-title">\1</h4>', text)
    text = patch_footer_contact_markup(text)
    if text != original:
        path.write_text(text, encoding="utf-8")
        return True
    return False


def main() -> None:
    changed = 0
    for lang in ("az", "en"):
        base = ROOT / lang
        for path in sorted(base.rglob("*.html")):
            if patch_file(path):
                changed += 1
                print(f"  updated {path.relative_to(ROOT)}")
    print(f"OK — {changed} HTML file(s) updated")


if __name__ == "__main__":
    main()

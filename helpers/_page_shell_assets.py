"""Shared modern page-shell snippets for build helpers and template sync."""
from __future__ import annotations

import re

FONT_VERSION = 1

# Three-line Google Fonts block (rel="preconnect" first variant).
GOOGLE_FONTS_BLOCK_A = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/>\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com"(?:\s+crossorigin(?:="")?)?\s*/>\s*'
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/>\s*',
    re.I,
)

# Three-line block (href="https://fonts.googleapis.com" rel="preconnect" variant).
GOOGLE_FONTS_BLOCK_B = re.compile(
    r'<link href="https://fonts\.googleapis\.com" rel="preconnect"\s*/>\s*'
    r'<link crossorigin="" href="https://fonts\.gstatic\.com" rel="preconnect"\s*/>\s*'
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/>\s*',
    re.I,
)

# Standalone stylesheet link (after preconnect lines were removed separately).
GOOGLE_FONTS_CSS_ONLY = re.compile(
    r'<link href="https://fonts\.googleapis\.com/css2\?[^"]+" rel="stylesheet"\s*/>\s*',
    re.I,
)

# Leftover preconnect lines immediately before daab-fonts.css.
ORPHAN_PRECONNECT = re.compile(
    r'<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/>\s*'
    r'(?:<link rel="preconnect" href="https://fonts\.gstatic\.com"(?:\s+crossorigin(?:="")?)?\s*/>\s*)?'
    r'(?=<link href="(?:\{ASSET\}|\.\./(?:\.\./)*|\.\./|\.\./\.\./\.\./)css/daab-fonts\.css)',
    re.I,
)

CSS_ROOT_AFTER = re.compile(
    r'href="(\{ASSET\}|\.\./(?:\.\./)*)(?=css/daab-)',
)


def font_stylesheet_link(*, css_root: str) -> str:
    return f'<link href="{css_root}css/daab-fonts.css?v={FONT_VERSION}" rel="stylesheet"/>'


def infer_css_root(text: str, pos: int) -> str:
    window = text[pos : pos + 240]
    m = CSS_ROOT_AFTER.search(window)
    if m:
        return m.group(1)
    if "{ASSET}" in window:
        return "{ASSET}"
    return "../"


def replace_google_fonts(text: str) -> tuple[str, int]:
    """Replace Google Fonts blocks with self-hosted daab-fonts.css."""
    count = 0

    def repl_block(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        root = infer_css_root(text, match.end())
        return font_stylesheet_link(css_root=root) + "\n"

    for pattern in (GOOGLE_FONTS_BLOCK_A, GOOGLE_FONTS_BLOCK_B):
        text, n = pattern.subn(repl_block, text)
        count += n

    def repl_css_only(match: re.Match[str]) -> str:
        nonlocal count
        count += 1
        root = infer_css_root(text, match.end())
        return font_stylesheet_link(css_root=root) + "\n"

    text, n = GOOGLE_FONTS_CSS_ONLY.subn(repl_css_only, text)
    count += n

    text, n_orphan = ORPHAN_PRECONNECT.subn("", text)
    count += n_orphan

    text, n_pre = re.subn(
        r'<link rel="preconnect" href="https://fonts\.googleapis\.com"\s*/>\s*'
        r'<link rel="preconnect" href="https://fonts\.gstatic\.com"(?:\s+crossorigin(?:="")?)?\s*/>\s*'
        r'(\{FONT_LINK\}|\{GOOGLE_FONTS_LINK\})',
        r"\1",
        text,
        flags=re.I,
    )
    count += n_pre

    return text, count


def replace_legacy_nav_logo(text: str) -> tuple[str, int]:
    new_text, n = re.subn(r"daab-logo\.svg", "daab-logo.png", text)
    return new_text, n


def modernize_shell_source(text: str) -> tuple[str, int]:
    text, n_fonts = replace_google_fonts(text)
    text, n_logo = replace_legacy_nav_logo(text)
    return text, n_fonts + n_logo

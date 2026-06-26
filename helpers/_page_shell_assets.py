"""Shared modern page-shell snippets for build helpers and template sync."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS

FONT_VERSION = 1

# Standard deferred scripts on nav-mounted pages (hub / inner pages).
# Order matches en/index.html. Pages may add page-specific scripts after this block.
STANDARD_SHELL_SCRIPTS: tuple[str, ...] = (
    "daab-mobile.js",
    "daab-perf.js",
    "daab-sticky-chrome.js",
    "daab-back-to-top.js",
    "daab-i18n.js",
    "daab-lang-position.js",
    "daab-design-tokens.js",
    "daab-nav.js",
    "daab-primary-nav.js",
    "daab-shell.js",
    "daab-page-subtitle.js",
    "daab-search.js",
    "daab-analytics.js",
)

# Insert missing script immediately after this anchor (if present).
SCRIPT_INSERT_AFTER: dict[str, str] = {
    "daab-perf.js": "daab-mobile.js",
    "daab-design-tokens.js": "daab-lang-position.js",
    "daab-page-subtitle.js": "daab-shell.js",
}

SKIP_SHELL_PAGES = frozenset(
    {
        "membership.html",
        "membership_flyer.html",
        "sponsors_flyer.html",
    }
)

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


def iter_nav_shell_pages() -> list[Path]:
    pages: list[Path] = []
    for folder in ("az", "en"):
        base = ROOT / folder
        if not base.is_dir():
            continue
        for path in sorted(base.rglob("*.html")):
            if path.name in SKIP_SHELL_PAGES:
                continue
            text = path.read_text(encoding="utf-8")
            if 'data-daab-nav-mount="1"' in text:
                pages.append(path)
    return pages


def infer_js_root(html: str, path: Path) -> str:
    m = re.search(r'data-daab-asset-root="([^"]+)"', html)
    if m:
        return f"{m.group(1)}js/"
    depth = len(path.relative_to(ROOT).parts) - 1
    return "../" * depth + "js/"


def script_tag(js_root: str, filename: str) -> str:
    version = SCRIPT_VERSIONS.get(filename, 1)
    return f'<script src="{js_root}{filename}?v={version}" defer></script>'


def missing_shell_scripts(html: str) -> list[str]:
    return [name for name in STANDARD_SHELL_SCRIPTS if name not in html]


def insert_missing_shell_scripts(html: str, path: Path) -> tuple[str, list[str]]:
    """Insert any missing standard shell scripts. Returns (new_html, inserted_names)."""
    missing = missing_shell_scripts(html)
    if not missing:
        return html, []

    js_root = infer_js_root(html, path)
    inserted: list[str] = []
    for name in missing:
        anchor = SCRIPT_INSERT_AFTER.get(name)
        tag = script_tag(js_root, name)
        if anchor and anchor in html:
            pattern = re.compile(
                rf'(<script[^>]+{re.escape(anchor)}[^>]*>\s*</script>)',
                re.I,
            )
            new_html, n = pattern.subn(rf"\1\n{tag}", html, count=1)
            if n:
                html = new_html
                inserted.append(name)
                continue
        # Fallback: append before </head>
        html = html.replace("</head>", f"{tag}\n</head>", 1)
        inserted.append(name)
    return html, inserted


def audit_shell_scripts() -> dict[str, list[str]]:
    issues: dict[str, list[str]] = {}
    for path in iter_nav_shell_pages():
        missing = missing_shell_scripts(path.read_text(encoding="utf-8"))
        if missing:
            issues[path.relative_to(ROOT).as_posix()] = missing
    return issues


def fix_shell_scripts() -> list[tuple[str, list[str]]]:
    changed: list[tuple[str, list[str]]] = []
    for path in iter_nav_shell_pages():
        html = path.read_text(encoding="utf-8")
        new_html, inserted = insert_missing_shell_scripts(html, path)
        if inserted:
            path.write_text(new_html, encoding="utf-8", newline="\n")
            changed.append((path.relative_to(ROOT).as_posix(), inserted))
    return changed

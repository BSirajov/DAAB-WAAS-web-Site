"""Align charter/activities with daab-common shell; strip duplicate search CSS on membership."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

CHARTER_TOKEN_MAP = {
    "var(--primary-dk)": "var(--blue-900)",
    "var(--primary2)": "var(--blue-400)",
    "var(--primary)": "var(--blue-700)",
    "var(--light-bl)": "#e5f4fb",
    "var(--dark-bl)": "var(--blue-900)",
    "var(--surface)": "#ffffff",
    "var(--text3)": "#8899aa",
    "var(--text2)": "#333333",
    "var(--text)": "var(--ink)",
    "var(--border)": "var(--line)",
    "var(--radius-lg)": "var(--radius)",
}

CHARTER_HEAD_SHELL = """<link href="../css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="../css/daab-common.css?v=21" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=4" rel="stylesheet"/>
<link href="../css/daab-search.css?v=3" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=1" rel="stylesheet"/>
"""

CHARTER_HEAD_TAIL = """<link href="../css/daab-hero-summary.css?v=1" rel="stylesheet"/>
<link href="../css/daab-sidebar-widget.css?v=2" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=1" defer></script>
<script src="../js/daab-back-to-top.js?v=2" defer></script>
<link href="../css/daab-lang.css?v=9" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=11" rel="stylesheet"/>
<script src="../js/daab-i18n.js?v=12" defer></script>
<script src="../js/daab-lang-position.js?v=4" defer></script>
<script src="../js/daab-nav.js?v=8" defer></script>
<script src="../js/daab-primary-nav.js?v=8" defer></script>
<script src="../js/daab-breadcrumbs.js?v=4" defer></script>
<script src="../js/daab-shell.js?v=9" defer></script>
<script src="../js/daab-search.js?v=3" defer></script>
"""

CHARTER_LEGACY_START = re.compile(
    r"<style>\s*/\* ===== merged from style block-1 ===== \*/\s*"
    r"/\* ═+[^*]*DAAB shared design tokens[^*]*═+ \*/\s*"
    r":root\{[^}]+\}\s*"
    r"\*, \*::before, \*::after \{[^}]+\}\s*"
    r"html \{ scroll-behavior:smooth; \}\s*"
    r"body \{[^}]+\}\s*"
    r"@keyframes pulse \{[^}]+\}\s*",
    re.DOTALL,
)

CHARTER_FOOTER_BLOCK = re.compile(
    r"\s*\.footer-pro\{background:linear-gradient\(135deg,#102033,#1a6fa8\)[^}]+\}\s*"
    r"(?:\.footer-(?:inner|brand|grid|col|title|item|address|leader|bottom)[^{]*\{[^}]*\}\s*)+"
    r"@media\(max-width:900px\)\{[^}]+\}\s*"
    r"@media\(max-width:600px\)\{[^}]+\}\s*",
    re.DOTALL,
)

CHARTER_GRADIENT_BODY = re.compile(
    r"/\* ══ GRADIENT MESH BACKGROUND ══ \*/\s*"
    r"body \{[^}]+\}\s*"
    r"\.nav-strip, \.main, footer \{ position: relative; z-index: 1; \}\s*",
    re.DOTALL,
)

ACTIVITIES_LEGACY_START = re.compile(
    r"<style>\s*/\* ===== merged from style block-1 ===== \*/\s*"
    r":root\{[^}]+\}\s*"
    r"\*, \*::before, \*::after \{[^}]+\}\s*"
    r"html \{ scroll-behavior: smooth; \}\s*"
    r"body \{[^}]+\}\s*"
    r"/\* ─── HEADER ─+ \*/\s*"
    r"\.header-nav a\.active \{[^}]+\}\s*"
    r"/\* ─── HERO BAND ─+ \*/\s*"
    r"\.page-hero \{[^}]+\}\s*"
    r"\.page-hero::before \{[^}]+\}\s*"
    r"\.page-hero h1 \{[^}]+\}\s*"
    r"\.page-hero p \{[^}]+\}\s*",
    re.DOTALL,
)

MEMBERSHIP_SEARCH_MARKER = "/* Membership page hero"

CHARTER_HEAD_LINKS_BLOB = re.compile(
    r'<link href="../css/daab-hero-summary\.css\?v=1" rel="stylesheet"/>'
    r'<link href="https://fonts\.googleapis\.com"[^/]*/>'
    r'<link href="../css/daab-common\.css\?v=21" rel="stylesheet"/>'
    r'<link href="../css/daab-mobile\.css\?v=4" rel="stylesheet"/>'
    r'<link href="../css/daab-search\.css\?v=1" rel="stylesheet"/>'
    r'<link href="../css/daab-back-to-top\.css\?v=1" rel="stylesheet"/>'
    r'<link href="../css/daab-sidebar-widget\.css\?v=2" rel="stylesheet"/>'
    r'\s*<script src="../js/daab-mobile\.js\?v=1" defer></script>.*?'
    r'<script src="../js/daab-search\.js\?v=3" defer></script>',
    re.DOTALL,
)


def map_charter_tokens(css: str) -> str:
    for old, new in CHARTER_TOKEN_MAP.items():
        css = css.replace(old, new)
    return css


def fix_charter(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    # Move shell assets before <style> and drop duplicate blob after </style>
    if "<style>" in text and 'rel="stylesheet"/><link href="../css/daab-common.css' in text:
        style_idx = text.index("<style>")
        before_style = text[:style_idx]
        after_style_start = text[style_idx:]

        # Remove duplicate link/script block between </style> and </head>
        after_style_start = CHARTER_HEAD_LINKS_BLOB.sub(
            CHARTER_HEAD_TAIL,
            after_style_start,
            count=1,
        )

        if "daab-common.css?v=21" not in before_style:
            # Insert shell after <title>...</title> or description
            insert_at = before_style.rfind("</title>")
            if insert_at == -1:
                insert_at = before_style.rfind('name="description"/>')
                if insert_at != -1:
                    insert_at = before_style.find(">", insert_at) + 1
            else:
                insert_at = before_style.find(">", insert_at) + 1
            before_style = (
                before_style[:insert_at]
                + "\n"
                + CHARTER_HEAD_SHELL
                + before_style[insert_at:]
            )

        text = before_style + after_style_start

    m = re.search(r"(<style>)(.*?)(</style>)", text, re.DOTALL)
    if m:
        css = m.group(2)
        css = CHARTER_LEGACY_START.sub("", "<style>" + css).removeprefix("<style>")
        css = CHARTER_FOOTER_BLOCK.sub("\n", css)
        css = CHARTER_GRADIENT_BODY.sub(
            "\n.charter-page .main,\n.charter-page footer {\n  position: relative;\n  z-index: 1;\n}\n\n",
            css,
        )
        css = map_charter_tokens(css)
        text = text[: m.start(2)] + css + text[m.end(2) :]

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def fix_activities(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text

    m = re.search(r"(<style>)(.*?)(</style>)", text, re.DOTALL)
    if m:
        css = m.group(2)
        css = ACTIVITIES_LEGACY_START.sub("", "<style>" + css).removeprefix("<style>")
        text = text[: m.start(2)] + css + text[m.end(2) :]

    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def fix_membership(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    original = text
    start = text.find("#search-overlay.open")
    marker = text.find(MEMBERSHIP_SEARCH_MARKER)
    if start != -1 and marker != -1 and start < marker:
        text = text[:start] + text[marker:]
    if text != original:
        path.write_text(text, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for rel in (
        "az/charter.html",
        "en/charter.html",
        "az/activities.html",
        "en/activities.html",
        "az/membership.html",
        "en/membership.html",
    ):
        path = ROOT / rel
        if not path.is_file():
            continue
        changed = False
        if "charter" in rel:
            changed = fix_charter(path)
        elif "activities" in rel:
            changed = fix_activities(path)
        else:
            changed = fix_membership(path)
        if changed:
            updated.append(rel)
    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Enable dynamic primary nav on DAAB HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

NAV_MENU_RE = re.compile(
    r'(<div class="nav-menu" id="primaryNavMenu")[^>]*>.*?</div>(\s*</div>\s*</nav>)',
    re.DOTALL | re.IGNORECASE,
)

NAV_PLACEHOLDER = (
    '<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">'
    '<div class="nav-divider"></div>'
    "</div>\\2"
)

HTML_TAG_RE = re.compile(r"<html([^>]*)>", re.IGNORECASE)

SCRIPT_VERSIONS = {
    "daab-i18n.js": 11,
    "daab-lang-position.js": 3,
    "daab-nav.js": 7,
    "daab-primary-nav.js": 8,
    "daab-breadcrumbs.js": 4,
    "daab-section-nav.js": 4,
    "daab-shell.js": 7,
}

STYLE_VERSIONS = {
    "daab-nav-mega.css": 11,
    "daab-lang.css": 6,
    "daab-common.css": 18,
}

NAV_ASSETS = (
    '\n<link href="{prefix}css/daab-nav-mega.css?v=' + str(STYLE_VERSIONS["daab-nav-mega.css"]) + '" rel="stylesheet"/>'
    '\n<script src="{prefix}js/daab-i18n.js?v=' + str(SCRIPT_VERSIONS["daab-i18n.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-lang-position.js?v=' + str(SCRIPT_VERSIONS["daab-lang-position.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-nav.js?v=' + str(SCRIPT_VERSIONS["daab-nav.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-primary-nav.js?v=' + str(SCRIPT_VERSIONS["daab-primary-nav.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-breadcrumbs.js?v=' + str(SCRIPT_VERSIONS["daab-breadcrumbs.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-section-nav.js?v=' + str(SCRIPT_VERSIONS["daab-section-nav.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-shell.js?v=' + str(SCRIPT_VERSIONS["daab-shell.js"]) + '" defer></script>'
).strip()


def bump_versions(html: str) -> str:
    """Bring any existing script/style references up to current versions."""
    for name, ver in SCRIPT_VERSIONS.items():
        html = re.sub(
            r'(' + re.escape(name) + r')\?v=\d+',
            r"\1?v=" + str(ver),
            html,
        )
    for name, ver in STYLE_VERSIONS.items():
        html = re.sub(
            r'(' + re.escape(name) + r')\?v=\d+',
            r"\1?v=" + str(ver),
            html,
        )
    return html


def dedupe_scripts(html: str) -> str:
    """Remove duplicate <script src> tags that may appear after upgrades."""
    seen = set()

    def repl(m: re.Match) -> str:
        src = m.group(1)
        base = src.split("?")[0]
        if base in seen:
            return ""
        seen.add(base)
        return m.group(0)

    return re.sub(
        r'<script src="([^"]+?(?:daab-[a-z-]+\.js)[^"]*)" defer></script>\s*',
        repl,
        html,
        flags=re.I,
    )

SKIP_PARTS = {"node_modules", ".git"}


def asset_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(("az/scientists/", "en/scientists/")):
        return "../../"
    if rel.startswith(("az/", "en/")):
        return "../"
    return ""


def is_live_page(path: Path) -> bool:
    """Live pages live under /az or /en. Legacy root-level *_az.html files are
    build sources and must not be touched by the nav patcher."""
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith("az/") or rel.startswith("en/")


def should_patch(path: Path) -> bool:
    if any(p in SKIP_PARTS for p in path.parts):
        return False
    if path.suffix.lower() != ".html":
        return False
    if not is_live_page(path):
        return False
    if "primaryNavMenu" not in path.read_text(encoding="utf-8", errors="ignore"):
        return False
    return True


def ensure_nav_mount(html: str) -> str:
    def repl(m: re.Match) -> str:
        attrs = m.group(1)
        if "data-daab-nav-mount" in attrs:
            return m.group(0)
        return '<html' + attrs + ' data-daab-nav-mount="1">'

    return HTML_TAG_RE.sub(repl, html, count=1)


def replace_nav_menu(html: str) -> str:
    return NAV_MENU_RE.sub(NAV_PLACEHOLDER, html, count=1)


def inject_assets(html: str, prefix: str) -> str:
    block = NAV_ASSETS.format(prefix=prefix)
    if "daab-primary-nav.js" in html:
        html = bump_versions(html)
        if "daab-nav-mega.css" not in html:
            html = html.replace("</head>", block + "\n</head>", 1)
        html = dedupe_scripts(html)
        return html
    if "daab-nav-mega.css" in html:
        return bump_versions(html)
    html = re.sub(
        r'<script src="[^"]*daab-shell\.js[^"]*" defer></script>\s*',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script src="[^"]*daab-i18n\.js[^"]*" defer></script>\s*',
        "",
        html,
        flags=re.I,
    )
    html = re.sub(
        r'<script src="[^"]*daab-nav\.js[^"]*" defer></script>\s*',
        "",
        html,
        count=1,
        flags=re.I,
    )
    if "</head>" in html:
        html = html.replace("</head>", block + "\n</head>", 1)
    return dedupe_scripts(html)


def patch_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    html = original
    html = ensure_nav_mount(html)
    if 'id="primaryNavMenu"' in html and 'data-daab-nav-placeholder' not in html:
        html = replace_nav_menu(html)
    html = inject_assets(html, asset_prefix(path))
    if html != original:
        path.write_text(html, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> None:
    updated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if not should_patch(path):
            continue
        if patch_file(path):
            updated.append(path.relative_to(ROOT).as_posix())
    print(f"Patched {len(updated)} file(s)")
    for name in updated:
        print(f"  {name}")


if __name__ == "__main__":
    main()

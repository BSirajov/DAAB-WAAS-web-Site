#!/usr/bin/env python3
"""Slim primary nav placeholders on DAAB HTML pages.

Live navigation is built at runtime from i18n/nav.json via daab-primary-nav.js.
HTML pages keep only a minimal #primaryNavMenu placeholder (divider) so we do
not duplicate the mega-menu in every file.

Run after nav.json changes (optional — placeholder does not need nav labels):
    python helpers/_sync_primary_nav.py

Also wires required nav scripts/styles and data-daab-nav-mount on shell pages.
"""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

MINIMAL_NAV_INNER = '<div class="nav-divider"></div>'

NAV_MENU_INNER_RE = re.compile(
    r'(<div class="nav-menu"[^>]*\bid="primaryNavMenu"[^>]*>)(.*?)(</div>\s*(?:<div class="nav-actions\b|</div>\s*</nav>))',
    re.DOTALL | re.IGNORECASE,
)

HTML_TAG_RE = re.compile(r"<html([^>]*)>", re.IGNORECASE)

NAV_ASSETS = (
    '\n<link href="{prefix}css/daab-nav-mega.css?v=' + str(STYLE_VERSIONS["daab-nav-mega.css"]) + '" rel="stylesheet"/>'
    '\n<script src="{prefix}js/daab-i18n.js?v=' + str(SCRIPT_VERSIONS["daab-i18n.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-lang-position.js?v=' + str(SCRIPT_VERSIONS["daab-lang-position.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-nav.js?v=' + str(SCRIPT_VERSIONS["daab-nav.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-primary-nav.js?v=' + str(SCRIPT_VERSIONS["daab-primary-nav.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-breadcrumbs.js?v=' + str(SCRIPT_VERSIONS["daab-breadcrumbs.js"]) + '" defer></script>'
    '\n<script src="{prefix}js/daab-shell.js?v=' + str(SCRIPT_VERSIONS["daab-shell.js"]) + '" defer></script>'
).strip()

SKIP_PARTS = {"node_modules", ".git"}


def bump_versions(html: str) -> str:
    """Bring any existing script/style references up to current versions."""
    for name, ver in SCRIPT_VERSIONS.items():
        html = re.sub(
            r"(" + re.escape(name) + r")\?v=\d+",
            r"\1?v=" + str(ver),
            html,
        )
    for name, ver in STYLE_VERSIONS.items():
        html = re.sub(
            r"(" + re.escape(name) + r")\?v=\d+",
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


def asset_prefix(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith(("az/scientists/", "en/scientists/")):
        return "../../"
    if rel.startswith(("az/", "en/")):
        return "../"
    return ""


def is_live_page(path: Path) -> bool:
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


def nav_menu_inner(html: str) -> str | None:
    match = NAV_MENU_INNER_RE.search(html)
    return match.group(2) if match else None


def needs_slim_nav(html: str) -> bool:
    inner = nav_menu_inner(html)
    if inner is None:
        return False
    return inner.strip() != MINIMAL_NAV_INNER.strip()


def slim_nav_menu(html: str) -> str:
    return NAV_MENU_INNER_RE.sub(
        r"\1" + MINIMAL_NAV_INNER + r"\3",
        html,
        count=1,
    )


def ensure_nav_mount(html: str) -> str:
    def repl(m: re.Match) -> str:
        attrs = m.group(1)
        if "data-daab-nav-mount" in attrs:
            return m.group(0)
        return '<html' + attrs + ' data-daab-nav-mount="1">'

    return HTML_TAG_RE.sub(repl, html, count=1)


def ensure_nav_placeholder_attr(html: str) -> str:
    return re.sub(
        r'(<div class="nav-menu" id="primaryNavMenu")((?![^>]*data-daab-nav-placeholder)[^>]*)>',
        r'\1 data-daab-nav-placeholder="1"\2>',
        html,
        count=1,
        flags=re.I,
    )


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
    if 'id="primaryNavMenu"' in html:
        html = ensure_nav_placeholder_attr(html)
    if needs_slim_nav(html):
        html = slim_nav_menu(html)
    html = inject_assets(html, asset_prefix(path))
    if html != original:
        path.write_text(html, encoding="utf-8", newline="\n")
        return True
    return False


def main() -> int:
    updated: list[str] = []
    bloated: list[str] = []
    for path in sorted(ROOT.rglob("*.html")):
        if not should_patch(path):
            continue
        if patch_file(path):
            updated.append(path.relative_to(ROOT).as_posix())
        text = path.read_text(encoding="utf-8")
        if needs_slim_nav(text):
            bloated.append(path.relative_to(ROOT).as_posix())
    print(f"Slim nav placeholder: {len(updated)} file(s) updated")
    for name in updated[:20]:
        print(f"  {name}")
    if len(updated) > 20:
        print(f"  … and {len(updated) - 20} more")
    if bloated:
        print(f"WARNING: {len(bloated)} page(s) still have embedded mega-menu")
        for name in bloated[:10]:
            print(f"  {name}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

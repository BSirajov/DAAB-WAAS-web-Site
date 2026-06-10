#!/usr/bin/env python3
"""Apply site-wide performance optimizations to deploy HTML pages."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT
from _site_wide_cleanup import STYLE_VERSIONS, SCRIPT_VERSIONS, iter_deploy_html

BLOCKING_SCRIPT_NAMES = (
    "scientists-catalog-data",
    "scientists-catalog-data-en",
    "daab-collation",
    "scientists-list-preview",
    "daab-scientists-toolbar-mobile",
    "html2canvas",
    "jspdf",
)

PERF_CSS_NAME = "daab-perf.css"
PERF_JS_NAME = "daab-perf.js"


def _strip_perf_assets(html: str) -> str:
    html = re.sub(r'<link\s+href="[^"]*daab-perf\.css[^"]*"\s+rel="stylesheet"\s*/>\s*', "", html)
    html = re.sub(r'<script\s+[^>]*daab-perf\.js[^>]*></script>\s*', "", html)
    return html


def _asset_roots(html: str) -> tuple[str | None, str | None]:
    css_m = re.search(r'<link\s+href="([^"]*/)css/daab-common\.css', html)
    js_m = re.search(
        r'<script\s+src="([^"]*/)js/daab-(?:mobile|i18n|perf)\.js',
        html,
    )
    css_root = css_m.group(1) if css_m else None
    js_root = js_m.group(1) if js_m else css_root
    return css_root, js_root


def inject_perf_assets(html: str) -> str:
    html = _strip_perf_assets(html)
    css_root, js_root = _asset_roots(html)
    if not css_root or not js_root:
        return html

    css_tag = (
        f'<link href="{css_root}css/{PERF_CSS_NAME}?v={STYLE_VERSIONS[PERF_CSS_NAME]}" rel="stylesheet"/>'
    )
    js_tag = (
        f'<script src="{js_root}js/{PERF_JS_NAME}?v={SCRIPT_VERSIONS[PERF_JS_NAME]}" defer></script>'
    )

    html = re.sub(
        r'(<link\s+href="[^"]*daab-common\.css[^"]*"\s+rel="stylesheet"\s*/>)',
        r"\1\n" + css_tag,
        html,
        count=1,
    )

    mobile = re.search(r'<script\s+src="[^"]*daab-mobile\.js[^"]*"\s+defer></script>', html)
    if mobile:
        html = html.replace(mobile.group(0), mobile.group(0) + "\n" + js_tag, 1)
    else:
        i18n = re.search(r'<script\s+src="[^"]*daab-i18n\.js[^"]*"\s+defer></script>', html)
        if i18n:
            html = html.replace(i18n.group(0), js_tag + "\n" + i18n.group(0), 1)

    return html


def defer_blocking_scripts(html: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if " defer" in tag or 'type="module"' in tag:
            return tag
        inner = match.group(1)
        if not any(name in inner for name in BLOCKING_SCRIPT_NAMES):
            return tag
        return f'<script defer src="{inner}"></script>'

    return re.sub(
        r'<script\s+src="([^"]+\.js[^"]*)"\s*></script>',
        repl,
        html,
    )


def add_lazy_to_images(html: str) -> str:
    skip_classes = ("nav-brand-logo",)

    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if "loading=" in tag:
            return tag
        if any(cls in tag for cls in skip_classes):
            return tag
        if 'fetchpriority="high"' in tag:
            return tag
        if "data-thumb-src" in tag:
            return tag
        if 'decoding="' not in tag:
            tag = tag.replace("<img ", '<img decoding="async" ', 1)
        return tag.replace("<img ", '<img loading="lazy" fetchpriority="low" ', 1)

    return re.sub(r"<img\s[^>]*?/?>", repl, html, flags=re.IGNORECASE)


def process_file(path: Path) -> bool:
    original = path.read_text(encoding="utf-8")
    text = original
    text = inject_perf_assets(text)
    text = defer_blocking_scripts(text)
    text = add_lazy_to_images(text)
    if text == original:
        return False
    path.write_text(text, encoding="utf-8", newline="\n")
    return True


def main() -> None:
    updated = 0
    for path in iter_deploy_html():
        if process_file(path):
            updated += 1
            print(path.relative_to(ROOT))
    print(f"Updated {updated} file(s)")


if __name__ == "__main__":
    main()

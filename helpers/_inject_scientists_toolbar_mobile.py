"""Wrap scientist catalogue toolbars for collapsible filters (all viewports)."""
from __future__ import annotations

import re

from _paths import ROOT

PAGES = (
    ROOT / "az" / "scientists" / "profiles.html",
    ROOT / "en" / "scientists" / "profiles.html",
    ROOT / "az" / "scientists" / "list.html",
    ROOT / "en" / "scientists" / "list.html",
)

CSS_V = "9"
JS_V = "3"

TOOLBAR_RE = re.compile(
    r'<div class="toolbar(?P<sticky> toolbar--sticky)?(?P<extra> catalog-toolbar)?"(?P<attrs>[^>]*)>\s*'
    r'(?P<search><div class="search-wrap">.*?</div>)\s*'
    r'(?P<filters><div class="filter-group">.*?</div>)\s*'
    r"</div>",
    re.DOTALL | re.IGNORECASE,
)

TOGGLE_AZ = (
    '<button type="button" class="catalog-toolbar__toggle" aria-expanded="false" '
    'aria-controls="catalogFilterPanel" aria-label="Filtrləri göstər">'
    '<svg class="catalog-toolbar__toggle-icon" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><path d="M3 5h18l-7 9v5l-4-2v-3L3 5z"/></svg>'
    '<span class="catalog-toolbar__toggle-text">Filtrlər</span>'
    '<span class="catalog-toolbar__badge" hidden></span>'
    "</button>"
)

TOGGLE_EN = (
    '<button type="button" class="catalog-toolbar__toggle" aria-expanded="false" '
    'aria-controls="catalogFilterPanel" aria-label="Show filters">'
    '<svg class="catalog-toolbar__toggle-icon" viewBox="0 0 24 24" fill="none" '
    'stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" '
    'aria-hidden="true"><path d="M3 5h18l-7 9v5l-4-2v-3L3 5z"/></svg>'
    '<span class="catalog-toolbar__toggle-text">Filters</span>'
    '<span class="catalog-toolbar__badge" hidden></span>'
    "</button>"
)


def wrap_toolbar(match: re.Match[str], toggle: str) -> str:
    sticky = match.group("sticky") or ""
    attrs = match.group("attrs") or ""
    search = match.group("search")
    filters = match.group("filters")
    extra = ""
    if "catalog-toolbar" not in attrs:
        extra = " catalog-toolbar"
    return (
        f'<div class="toolbar{sticky}{extra}"{attrs}>\n'
        f'<div class="catalog-toolbar__head">\n{search}\n{toggle}\n</div>\n'
        f'<div class="catalog-toolbar__panel" id="catalogFilterPanel">\n'
        f'<div class="catalog-toolbar__panel-inner">\n{filters}\n</div>\n'
        f"</div>\n</div>"
    )


def inject_assets(text: str, prefix: str) -> tuple[str, list[str]]:
    changes: list[str] = []
    css_needle = "scientists-catalog-toolbar.css?v="
    if css_needle in text:
        text, n = re.subn(
            r"scientists-catalog-toolbar\.css\?v=\d+",
            f"scientists-catalog-toolbar.css?v={CSS_V}",
            text,
            count=1,
        )
        if n:
            changes.append("css-v")
    js_tag = f'<script src="{prefix}js/daab-scientists-toolbar-mobile.js?v={JS_V}"></script>'
    js_needle = "daab-scientists-toolbar-mobile.js"
    if js_needle in text:
        text, n = re.subn(
            r"daab-scientists-toolbar-mobile\.js\?v=\d+",
            f"daab-scientists-toolbar-mobile.js?v={JS_V}",
            text,
            count=1,
        )
        if n:
            changes.append("js-v")
    elif "scientists-cv-filters.js" in text:
        text = text.replace(
            '<script src="' + prefix + "js/scientists-cv-filters.js",
            js_tag + "\n" + '<script src="' + prefix + "js/scientists-cv-filters.js",
            1,
        )
        changes.append("js")
    elif "</body>" in text:
        text = text.replace("</body>", js_tag + "\n</body>", 1)
        changes.append("js")

    cv_needle = prefix + "js/scientists-cv-filters.js"
    if cv_needle in text:
        text2, n2 = re.subn(
            r"scientists-cv-filters\.js\?v=\d+",
            "scientists-cv-filters.js?v=15",
            text,
            count=1,
        )
        if n2:
            text = text2
            changes.append("cv-filters-v")
    return text, changes


def process(path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    changes: list[str] = []
    rel = path.relative_to(ROOT).as_posix()
    prefix = "../../" if "scientists/" in rel else "../"
    toggle = TOGGLE_EN if rel.startswith("en/") else TOGGLE_AZ

    if "catalog-toolbar__head" not in text:
        new_text, n = TOOLBAR_RE.subn(lambda m: wrap_toolbar(m, toggle), text, count=1)
        if n:
            text = new_text
            changes.append("toolbar-wrap")

    text2, n = re.subn(r'\btoolbar--sticky\b\s*', "", text)
    if n:
        text = text2
        changes.append("no-sticky")

    text, asset_changes = inject_assets(text, prefix)
    changes.extend(asset_changes)

    if changes:
        path.write_text(text, encoding="utf-8", newline="\n")
    return changes


def main() -> int:
    updated: list[str] = []
    for path in PAGES:
        if not path.is_file():
            continue
        changes = process(path)
        if changes:
            updated.append(f"{path.relative_to(ROOT).as_posix()} ({', '.join(changes)})")
    print(f"Updated {len(updated)} file(s):")
    for line in updated:
        print(f"  {line}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

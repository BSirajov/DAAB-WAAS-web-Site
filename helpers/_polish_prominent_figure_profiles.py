#!/usr/bin/env python3
"""Polish prominent-figure profile heroes (tags, symbol placement)."""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT

FIGURES = ROOT / "az" / "prominent_figures"

GROUP_TAG_OLD = "Azərbaycan və türk dünyası"
GROUP_TAG_NEW = "Azərbaycan və türk dünyası"

GORLEMELI_TAG = '\n<span class="hero-tag">Görkəmli şəxsiyyət</span>'

# Regional flag emojis in hero symbol often render as country codes (e.g. AZ) on Windows.
FLAG_SYMBOL_REPLACEMENTS = {
    "🇦🇿": "🏛️",
    "🇹🇷": "🕌",
}

HERO_MOVE_SYMBOL = re.compile(
    r"(<header class=\"hero pf-profile-hero\"><div class=\"hero-inner shell pf-profile-hero__inner\">"
    r"<section class=\"hero-copy\">(?:<div class=\"hero-era-badge\">[^<]*</div>\s*)?"
    r"(?:<div class=\"pf-profile-hero__title-row\">)?"
    r"(?:<aside class=\"pf-hero-symbol\" aria-hidden=\"true\"><span class=\"pf-hero-symbol__icon\">[^<]*</span></aside>)?"
    r"\s*(<h1>[^<]*</h1>)"
    r"(\s*<div class=\"page-hero-subtitle[^\"]*\">[^<]*</div>\s*"
    r"<p class=\"pf-hero-dates\">[^<]*</p>\s*<div class=\"hero-tags\">.*?</div>)"
    r"\s*</section><aside class=\"pf-hero-symbol\" aria-hidden=\"true\">"
    r"<span class=\"pf-hero-symbol__icon\">([^<]*)</span></aside></div></header>",
    re.DOTALL,
)


def polish_profile_html(html: str) -> tuple[str, bool]:
    changed = False

    if GORLEMELI_TAG in html:
        html = html.replace(GORLEMELI_TAG, "")
        changed = True

    if GROUP_TAG_OLD in html:
        html = html.replace(GROUP_TAG_OLD, GROUP_TAG_NEW)
        changed = True

    for old, new in FLAG_SYMBOL_REPLACEMENTS.items():
        needle = f'<span class="pf-hero-symbol__icon">{old}</span>'
        if needle in html:
            html = html.replace(needle, f'<span class="pf-hero-symbol__icon">{new}</span>')
            changed = True

    if "pf-profile-hero__title-row" not in html:

        def move_symbol(m: re.Match[str]) -> str:
            emoji = m.group(4).strip()
            for old, new in FLAG_SYMBOL_REPLACEMENTS.items():
                if emoji == old:
                    emoji = new
            return (
                f"{m.group(1)}"
                f'<div class="pf-profile-hero__title-row">'
                f'<aside class="pf-hero-symbol" aria-hidden="true">'
                f'<span class="pf-hero-symbol__icon">{emoji}</span></aside>'
                f"{m.group(2)}</div>"
                f"{m.group(3)}</section></div></header>"
            )

        new_html, n = HERO_MOVE_SYMBOL.subn(move_symbol, html, count=1)
        if n:
            html = new_html
            changed = True

    return html, changed


TITLE_ROW_REORDER = re.compile(
    r'<div class="pf-profile-hero__title-row"><h1>([^<]*)</h1>'
    r'<aside class="pf-hero-symbol" aria-hidden="true">'
    r'<span class="pf-hero-symbol__icon">([^<]*)</span></aside></div>'
)


def reorder_title_row_icon(html: str) -> tuple[str, bool]:
    new_html, n = TITLE_ROW_REORDER.subn(
        r'<div class="pf-profile-hero__title-row">'
        r'<aside class="pf-hero-symbol" aria-hidden="true">'
        r'<span class="pf-hero-symbol__icon">\2</span></aside>'
        r"<h1>\1</h1></div>",
        html,
        count=1,
    )
    return new_html, n > 0


def main() -> None:
    n = 0
    for group in ("azturk", "world"):
        for path in sorted((FIGURES / group).glob("*.html")):
            text = path.read_text(encoding="utf-8")
            out, changed = polish_profile_html(text)
            out2, reordered = reorder_title_row_icon(out)
            if reordered:
                out = out2
                changed = True
            if changed:
                path.write_text(out, encoding="utf-8", newline="\n")
                n += 1
    print(f"Polished {n} profile pages")


if __name__ == "__main__":
    main()

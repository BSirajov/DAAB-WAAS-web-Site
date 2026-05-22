"""Add country under names, inline meta rows, flatten catalog grid."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT
CV = ROOT / "scientists_card_view_az.html"
DATA_JS = ROOT / "js" / "scientists-catalog-data.js"

CODE_TO_NAME = {
    "abs": "ABŞ",
    "de": "Almaniya",
    "at": "Avstriya",
    "uk": "Birləşmiş Krallıq",
    "kr": "Koreya",
    "ee": "Estoniya",
    "fr": "Fransa",
    "ge": "Gürcüstan",
    "il": "İsrail",
    "se": "İsveç",
    "it": "İtaliya",
    "ca": "Kanada",
    "mx": "Meksika",
    "eg": "Misir",
    "om": "Oman",
    "pl": "Polşa",
    "kz": "Qazaxıstan",
    "kg": "Qırğızıstan",
    "ru": "Rusiya Federasiyası",
    "sa": "Səudiyyə Ərəbistanı",
    "tr": "Türkiyə",
    "ua": "Ukrayna",
    "jp": "Yaponiya",
}

META_RE = re.compile(
    r'<div class="card-meta">'
    r'<span class="card-meta-label">İxtisas</span>'
    r'<span class="card-meta-ixtilas">([^<]*)</span>'
    r'<span class="card-meta-label">E-poçt</span>'
    r'((?:<a class="card-email"[^>]*>[^<]*</a>)|(?:<span class="card-email[^"]*"[^>]*>[^<]*</span>))'
    r"</div>",
    re.I,
)

HEADER_RE = re.compile(
    r'(<div class="card-header">\s*<span class="card-name">.*?</span>\s*)(</div>)',
    re.S,
)


def load_email_country() -> dict[str, str]:
    text = DATA_JS.read_text(encoding="utf-8")
    data = json.loads(text.split("=", 1)[1].strip().rstrip(";"))
    out: dict[str, str] = {}
    for row in data:
        email = (row.get("email") or "").strip().lower()
        country = (row.get("yasadigi_olke") or "").strip()
        if email and country:
            out[email] = country
    return out


def country_for_card(card_html: str, by_email: dict[str, str]) -> str:
    m = re.search(r'data-country="([^"]+)"', card_html)
    code = m.group(1) if m else ""
    em = re.search(r'data-email="([^"]*)"', card_html)
    if em:
        c = by_email.get(em.group(1).strip().lower())
        if c:
            return c
    return CODE_TO_NAME.get(code, code)


def inline_meta(card_html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        ixt = m.group(1)
        email = m.group(2)
        return (
            '<div class="card-meta">'
            '<div class="card-meta-row">'
            '<span class="card-meta-label">İxtisas:</span>'
            f'<span class="card-meta-ixtilas">{ixt}</span>'
            "</div>"
            '<div class="card-meta-row">'
            '<span class="card-meta-label">E-poçt:</span>'
            f"{email}"
            "</div>"
            "</div>"
        )

    return META_RE.sub(repl, card_html)


def add_country_header(card_html: str, country: str) -> str:
    esc = country.replace("&", "&amp;")
    country_line = f'<p class="card-country">{esc}</p>'
    if "card-country" in card_html:
        card_html = re.sub(
            r'<p class="card-country">[^<]*</p>\s*',
            "",
            card_html,
        )
    if 'data-country-name="' not in card_html:
        card_html = card_html.replace(
            'data-country="',
            f'data-country-name="{esc}" data-country="',
            1,
        )
    else:
        card_html = re.sub(
            r'data-country-name="[^"]*"',
            f'data-country-name="{esc}"',
            card_html,
            count=1,
        )

    def header_repl(m: re.Match[str]) -> str:
        return m.group(1) + country_line + "\n    " + m.group(2)

    return HEADER_RE.sub(header_repl, card_html, count=1)


def main() -> None:
    by_email = load_email_country()
    text = CV.read_text(encoding="utf-8")

    cards: list[str] = []
    chunks = re.split(r'(?=<div class="card")', text)
    for chunk in chunks[1:]:
        if not chunk.strip().startswith("<div"):
            continue
        country = country_for_card(chunk, by_email)
        chunk = inline_meta(chunk)
        chunk = add_country_header(chunk, country)
        cards.append(chunk.strip())

    print(f"Processed {len(cards)} cards")

    start = text.find('<section class="country-section"')
    end = text.find('<div class="no-results"')
    if start < 0 or end < 0:
        raise SystemExit("Could not find catalog boundaries")

    catalog = (
        '<section class="catalog-section" id="scientists-catalog">\n'
        '  <div class="cards-grid">\n    '
        + "\n\n".join(cards)
        + "\n  </div>\n</section>\n  "
    )
    text = text[:start] + catalog + text[end:]
    CV.write_text(text, encoding="utf-8")
    print("Wrote", CV.name)


if __name__ == "__main__":
    main()

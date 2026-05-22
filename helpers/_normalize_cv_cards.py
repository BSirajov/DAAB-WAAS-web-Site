"""Normalize all CV cards to match the first reference card structure."""
from __future__ import annotations

import html
import json
import re
import unicodedata
from pathlib import Path

from _paths import ROOT

CV = ROOT / "scientists_card_view_az.html"
AZ = ROOT / "scientists_list_view_az.html"

COUNTRY_CODE_TO_NAME = {
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


def esc_attr(s: str) -> str:
    return html.escape(s or "", quote=True)


def norm_search(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def extract_cards(text: str) -> tuple[list[str], int, int, str]:
    """Split catalog into top-level card blocks by open tag positions."""
    section_m = re.search(
        r'<section class="catalog-section" id="scientists-catalog">',
        text,
    )
    if not section_m:
        raise SystemExit("catalog section not found")
    section_start = section_m.start()
    grid_start = text.find('<div class="cards-grid">', section_start)
    grid_end = text.find('<div class="no-results"', section_start)
    if grid_start < 0 or grid_end < 0:
        raise SystemExit("catalog boundaries not found")
    grid = text[grid_start:grid_end]
    opens = [m.start() for m in re.finditer(r'<div class="card" data-country-name', grid)]
    cards = []
    for i, pos in enumerate(opens):
        end = opens[i + 1] if i + 1 < len(opens) else len(grid)
        cards.append(grid[pos:end].strip())
    no_results = text.find('<div class="no-results"', section_start)
    if no_results < 0:
        raise SystemExit("no-results not found")
    return cards, section_start, no_results, text


def parse_card(chunk: str) -> dict:
    attrs = {}
    m = re.match(r'<div class="card"([^>]*)>', chunk)
    if m:
        for key in ("data-country-name", "data-country", "data-email", "data-ixtilas", "data-degree"):
            am = re.search(rf'{key}="([^"]*)"', m.group(1))
            if am:
                attrs[key] = html.unescape(am.group(1))

    avatar = re.search(
        r'<div class="card-avatar[^"]*">(.*?)</div>',
        chunk,
        re.S,
    )
    cred_m = re.search(r'<span class="cred">([^<]*)</span>', chunk)
    name_m = re.search(r'<span class="card-name">(.*?)</span>\s*<p class="card-country">', chunk, re.S)
    if not name_m:
        name_m = re.search(r'<span class="card-name">(.*?)</span>', chunk, re.S)
    country_m = re.search(r'<p class="card-country">([^<]*)</p>', chunk)
    title_m = re.search(r'<p class="card-title">([^<]*)</p>', chunk)

    ixt_m = re.search(r'<span class="card-meta-ixtilas">([^<]*)</span>', chunk)
    email_m = re.search(
        r'<a class="card-email" href="mailto:([^"]*)"[^>]*>([^<]*)</a>',
        chunk,
    )
    email_empty = re.search(r'<span class="card-email card-email--empty">([^<]*)</span>', chunk)

    cred = cred_m.group(1).strip() if cred_m else ""
    name_plain = ""
    if name_m:
        name_plain = re.sub(r"<span class=\"cred\">.*", "", name_m.group(1), flags=re.S)
        name_plain = re.sub(r"<[^>]+>", "", name_plain).strip()

    bio = ""
    bio_marker = '<div class="card-bio">'
    bio_idx = chunk.find(bio_marker)
    if bio_idx >= 0:
        bio_start = bio_idx + len(bio_marker)
        end_m = re.search(r"</div>\s*</div>\s*</div>\s*$", chunk, re.S)
        if end_m:
            bio = chunk[bio_start : end_m.start()].strip()
        else:
            bio = chunk[bio_start:].strip()

    return {
        "attrs": attrs,
        "avatar_inner": avatar.group(1).strip() if avatar else "",
        "name_plain": name_plain,
        "cred": cred,
        "country": (country_m.group(1).strip() if country_m else attrs.get("data-country-name", "")),
        "title": title_m.group(1).strip() if title_m else "",
        "ixtilas": (ixt_m.group(1).strip() if ixt_m else attrs.get("data-ixtilas", "")),
        "email": email_m.group(1).strip() if email_m else "",
        "email_label": (email_m.group(2).strip() if email_m else (email_empty.group(1).strip() if email_empty else "—")),
        "bio": bio,
    }


def build_search_blob(parsed: dict) -> str:
    name_plain = parsed["name_plain"]
    if parsed["cred"]:
        name_plain = f"{name_plain} {parsed['cred']}"
    parts = [
        name_plain,
        parsed["attrs"].get("data-degree", ""),
        parsed["title"],
        parsed["country"],
        parsed["email"],
        parsed["ixtilas"],
        name_plain,
        parsed["attrs"].get("data-country", ""),
        parsed["attrs"].get("data-degree", ""),
        parsed["email"],
        parsed["ixtilas"],
    ]
    return norm_search(" ".join(p for p in parts if p))


def render_card(parsed: dict) -> str:
    a = parsed["attrs"]
    country_name = parsed["country"] or a.get("data-country-name", "")
    country_code = a.get("data-country", "")
    email = parsed["email"] or a.get("data-email", "")
    ixt = parsed["ixtilas"] or a.get("data-ixtilas", "")
    degree = a.get("data-degree", "")
    search = build_search_blob(parsed)

    if email and parsed["email_label"] != "—":
        email_row = (
            f'<div class="card-meta-row">'
            f'<span class="card-meta-label">E-poçt:</span>'
            f'<a class="card-email" href="mailto:{esc_attr(email)}">{html.escape(parsed["email_label"])}</a>'
            f"</div>"
        )
    else:
        email_row = (
            '<div class="card-meta-row">'
            '<span class="card-meta-label">E-poçt:</span>'
            '<span class="card-email card-email--empty">—</span>'
            "</div>"
        )

    cred_html = (
        f' <span class="cred">{html.escape(parsed["cred"])}</span>'
        if parsed["cred"]
        else ""
    )
    bio_inner = parsed["bio"]
    bio_block = f'    <div class="card-bio">{bio_inner}</div>' if bio_inner else '    <div class="card-bio"></div>'

    return f'''<div class="card" data-country-name="{esc_attr(country_name)}" data-country="{esc_attr(country_code)}" data-search="{esc_attr(search)}" data-email="{esc_attr(email)}" data-ixtilas="{esc_attr(ixt)}" data-degree="{esc_attr(degree)}">
  <div class="card-avatar card-photo">{parsed["avatar_inner"]}</div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-name">{html.escape(parsed["name_plain"])}{cred_html}</span>
      <p class="card-country">{html.escape(country_name)}</p>
    </div>
    <p class="card-title">{html.escape(parsed["title"])}</p>
    <div class="card-meta">
      <div class="card-meta-row"><span class="card-meta-label">İxtisas:</span><span class="card-meta-ixtilas">{html.escape(ixt)}</span></div>
      {email_row}
    </div>
{bio_block}
  </div>
</div>'''


def main() -> None:
    text = CV.read_text(encoding="utf-8")
    cards_raw, section_start, no_results_pos, full = extract_cards(text)
    print(f"Found {len(cards_raw)} raw card blocks")

    rebuilt = []
    issues = []
    for i, chunk in enumerate(cards_raw):
        try:
            parsed = parse_card(chunk)
            rebuilt.append(render_card(parsed))
        except Exception as e:
            issues.append((i + 1, str(e)))

    if issues:
        print("Parse issues:", issues[:10])

    catalog = (
        '<section class="catalog-section" id="scientists-catalog">\n'
        "  <div class=\"cards-grid\">\n\n"
        + "\n\n".join(rebuilt)
        + "\n\n  </div>\n</section>\n  "
    )

    new_text = full[:section_start] + catalog + full[no_results_pos:]
    # fix double-encoded entities in data-search from old file
    new_text = re.sub(r"&amp;(?:amp;)+", "&amp;", new_text)
    new_text = re.sub(r"&amp;quot;", "&quot;", new_text)

    CV.write_text(new_text, encoding="utf-8")
    print(f"Wrote {len(rebuilt)} normalized cards")


if __name__ == "__main__":
    main()

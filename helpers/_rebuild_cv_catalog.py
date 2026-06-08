"""Rebuild az/scientists/profiles.html catalog from book + catalog data."""
from __future__ import annotations

import html
import importlib.util
import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from _paths import ROOT, HELPERS, AZ_SCIENTISTS_PROFILES

CV = AZ_SCIENTISTS_PROFILES
DATA_JS = ROOT / "js" / "scientists-catalog-data.js"
PHOTOS = ROOT / "images" / "scientists-photos"

COUNTRY_NAME_TO_CODE = {
    "ABŞ": "abs",
    "Almaniya": "de",
    "Avstriya": "at",
    "Birləşmiş Krallıq": "uk",
    "Koreya": "kr",
    "Estoniya": "ee",
    "Fransa": "fr",
    "Gürcüstan": "ge",
    "İsrail": "il",
    "İsveç": "se",
    "İtaliya": "it",
    "Kanada": "ca",
    "Meksika": "mx",
    "Misir": "eg",
    "Oman": "om",
    "Polşa": "pl",
    "Qazaxıstan": "kz",
    "Qırğızıstan": "kg",
    "Rusiya Federasiyası": "ru",
    "Səudiyyə Ərəbistanı": "sa",
    "Türkiyə": "tr",
    "Ukrayna": "ua",
    "Yaponiya": "jp",
}

CRED_LABEL = {
    "PhD": "Ph.D.",
    "Prof.Dr.": "Prof. Dr.",
    "Ed.D.": "Ed.D.",
    "Dr.": "Dr.",
}

DISPLAY_ALIASES = {
    "AFI NA MEMMEDLI BARMANBAY": "Afina Barmanbay",
    "AFINA MEMMEDLI BARMANBAY": "Afina Barmanbay",
    "MEQBULE SEBZIYEVA": "Məqbulə Səbziyeva",
    "MEGBULE SEBZIYEVA": "Məqbulə Səbziyeva",
    "MEHDI GENCELI ISMAYILOV": "Mehdi İsmayilov (Gəncəli)",
    "GAFAR CAXMAGLI MEHDIYEV": "Qafar Mehdiyev (Çaxmaxçı)",
}


def load_book_module():
    spec = importlib.util.spec_from_file_location(
        "book_sync", HELPERS / "_sync_scientists_from_book.py"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).upper().strip()
    s = re.sub(r"[^A-Z0-9ƏŞÇĞÖÜİ\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s)
    for a, b in [("İ", "I"), ("Ə", "E"), ("Ş", "S"), ("Ç", "C"), ("Ğ", "G"), ("Ö", "O"), ("Ü", "U"), ("Q", "G")]:
        s = s.replace(a, b)
    return s.strip()


def esc_attr(s: str) -> str:
    return html.escape((s or "").strip(), quote=True)


def load_catalog_data() -> list[dict]:
    text = DATA_JS.read_text(encoding="utf-8")
    data = json.loads(text.split("=", 1)[1].strip().rstrip(";"))
    return sorted(data, key=lambda r: r.get("say", 0))


def photo_lookup() -> dict[str, str]:
    files = {p.stem: p.name for p in PHOTOS.glob("*") if p.suffix.lower() in (".png", ".jpg", ".jpeg")}
    by_norm = {norm(k.replace("-", " ")): k for k in files}
    return files, by_norm


def find_photo(display_name: str, files: dict[str, str], by_norm: dict[str, str]) -> str:
    key = norm(display_name)
    if key in DISPLAY_ALIASES:
        display_name = DISPLAY_ALIASES[key]
        key = norm(display_name)
    if key in by_norm:
        return files[by_norm[key]]
    best_stem = None
    best = 0.0
    for stem in files:
        score = SequenceMatcher(None, key, norm(stem.replace("-", " "))).ratio()
        if score > best:
            best = score
            best_stem = stem
    if best_stem and best >= 0.55:
        return files[best_stem]
    return "img_001_p61.jpeg"


def norm_search(s: str) -> str:
    return re.sub(r"\s+", " ", s.lower()).strip()


def az_upper_name(name: str) -> str:
    """Uppercase for card headings; map ASCII I to Azerbaijani İ."""
    s = unicodedata.normalize("NFKC", name.strip()).upper()
    return s.replace("I", "İ")


def build_search(row: dict, title: str, country: str, code: str, display: str, cred: str) -> str:
    email = (row.get("email") or "").strip()
    ixt = (row.get("ixtilas") or "").strip()
    deg = (row.get("elmi_derece") or "").strip()
    parts = [
        display,
        cred,
        deg,
        title,
        country,
        email,
        ixt,
        display,
        code,
        deg,
        email,
        ixt,
    ]
    return norm_search(" ".join(p for p in parts if p))


def render_card(row: dict, profile: dict, book) -> str:
    display = (row.get("ad_soyad") or profile["name"]).strip()
    country = (row.get("yasadigi_olke") or "").strip()
    code = COUNTRY_NAME_TO_CODE.get(country, "")
    email = (row.get("email") or "").strip().strip("\u00a0")
    ixt = (row.get("ixtilas") or "").strip()
    degree = (row.get("elmi_derece") or "").strip()
    cred = CRED_LABEL.get(degree, degree)
    title, _org = book.split_title_org(profile["header_lines"])
    bio_html = book.build_bio_html(profile["body_lines"])

    files, by_norm = photo_lookup()
    photo = find_photo(display, files, by_norm)
    alt = html.escape(display)
    search = build_search(row, title, country, code, display, cred)

    if email:
        email_row = (
            '      <div class="card-meta-row"><span class="card-meta-label">İxtisas:</span>'
            f'<span class="card-meta-ixtilas">{html.escape(ixt)}</span></div>\n'
            '      <div class="card-meta-row"><span class="card-meta-label">E-poçt:</span>'
            f'<a class="card-email" href="mailto:{esc_attr(email)}">{html.escape(email)}</a></div>'
        )
    else:
        email_row = (
            '      <div class="card-meta-row"><span class="card-meta-label">İxtisas:</span>'
            f'<span class="card-meta-ixtilas">{html.escape(ixt)}</span></div>\n'
            '      <div class="card-meta-row"><span class="card-meta-label">E-poçt:</span>'
            '<span class="card-email card-email--empty">—</span></div>'
        )

    cred_html = f' <span class="cred">{html.escape(cred)}</span>' if cred else ""
    name_upper = html.escape(az_upper_name(display))

    return f'''<div class="card" data-country-name="{esc_attr(country)}" data-country="{esc_attr(code)}" data-search="{esc_attr(search)}" data-email="{esc_attr(email)}" data-ixtilas="{esc_attr(ixt)}" data-degree="{esc_attr(degree)}">
  <div class="card-avatar card-photo"><img src="images/scientists-photos/{html.escape(photo)}" alt="{alt}" loading="lazy"/></div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-name">{name_upper}{cred_html}</span>
      <p class="card-country">{html.escape(country)}</p>
    </div>
    <p class="card-title">{html.escape(title)}</p>
    <div class="card-meta">
      {email_row}
    </div>
    {bio_html}
  </div>
</div>'''


def main() -> None:
    book = load_book_module()
    chapter = book.extract_chapter()
    profiles = book.parse_profiles_by_order(chapter)
    rows = load_catalog_data()
    if len(profiles) != 83 or len(rows) != 83:
        raise SystemExit(f"Expected 83 profiles/rows, got {len(profiles)}/{len(rows)}")

    cards = [render_card(row, prof, book) for row, prof in zip(rows, profiles)]

    shell = CV.read_text(encoding="utf-8")
    start = shell.find('<section class="catalog-section" id="scientists-catalog">')
    end = shell.find('<div class="no-results"')
    if start < 0 or end < 0:
        raise SystemExit("CV shell missing catalog section")

    catalog = (
        '<section class="catalog-section" id="scientists-catalog">\n'
        '  <div class="cards-grid">\n\n'
        + "\n\n".join(cards)
        + "\n\n  </div>\n</section>\n  "
    )
    CV.write_text(shell[:start] + catalog + shell[end:], encoding="utf-8")
    print(f"Rebuilt {len(cards)} cards in {CV.name}")


if __name__ == "__main__":
    main()

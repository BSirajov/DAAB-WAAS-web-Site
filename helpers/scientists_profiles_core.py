"""Render scientist profile cards from i18n/scientists-profiles.json."""
from __future__ import annotations

import html
import json
import re
import unicodedata
from pathlib import Path

try:
    from _paths import ROOT, AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES
    from i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN
    from i18n_person_names_en import az_upper_name_latin, latin_display_name
except ImportError:
    from helpers._paths import ROOT, AZ_SCIENTISTS_PROFILES, EN_SCIENTISTS_PROFILES  # type: ignore
    from helpers.i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN  # type: ignore
    from helpers.i18n_person_names_en import az_upper_name_latin, latin_display_name  # type: ignore

PROFILES_JSON = ROOT / "i18n" / "scientists-profiles.json"

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

META_LABELS = {
    "az": {"field": "İxtisas:", "email": "E-poçt:"},
    "en": {"field": "Field:", "email": "Email:"},
}

QR_LABELS = {
    "az": {
        "aria": "Profil linkinin QR kodu",
        "title": "Bu alimin profil səhifəsinə keçid",
    },
    "en": {
        "aria": "QR code for profile link",
        "title": "Link to this scientist's profile page",
    },
}

SITE_BASE = "https://daab-waas.com"


def esc_attr(s: str) -> str:
    return html.escape((s or "").strip(), quote=True)


def az_upper_name(name: str) -> str:
    s = unicodedata.normalize("NFKC", name.strip()).upper()
    return s.replace("I", "İ")


def norm_search(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def slug_from_photo(photo: str) -> str:
    return Path((photo or "").strip()).stem or ""


def profile_deep_link(lang: str, slug: str, *, base: str = SITE_BASE) -> str:
    locale = "az" if lang == "az" else "en"
    return f"{base.rstrip('/')}/{locale}/scientists/profiles.html#{slug}"


def load_profiles() -> list[dict]:
    data = json.loads(PROFILES_JSON.read_text(encoding="utf-8"))
    rows = data.get("profiles") or []
    return sorted(rows, key=lambda r: r.get("say", 0))


def save_profiles(profiles: list[dict]) -> None:
    PROFILES_JSON.parent.mkdir(parents=True, exist_ok=True)
    payload = {"version": 1, "profiles": sorted(profiles, key=lambda r: r.get("say", 0))}
    PROFILES_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def profile_country_code(profile: dict, lang: str) -> str:
    code = (profile.get("country_code") or "").strip()
    if code:
        return code
    country = profile.get("country_az") or profile.get("country") or ""
    return COUNTRY_NAME_TO_CODE.get(country, "")


def profile_country(profile: dict, lang: str) -> str:
    if lang == "en":
        return profile.get("country_en") or COUNTRY_EN.get(profile.get("country_az", ""), profile.get("country_az", ""))
    return profile.get("country_az") or profile.get("country") or ""


def profile_field(profile: dict, lang: str) -> str:
    if lang == "en":
        return profile.get("field_en") or FIELD_EN.get(profile.get("field_az", ""), profile.get("field_az", ""))
    return profile.get("field_az") or profile.get("field") or ""


def profile_name(profile: dict, lang: str) -> str:
    base = profile.get("name") or profile.get("name_az") or ""
    if lang == "en":
        return profile.get("name_en") or latin_display_name(base)
    return base


def profile_title(profile: dict, lang: str) -> str:
    if lang == "en":
        return profile.get("title_en") or profile.get("title_az") or profile.get("title") or ""
    return profile.get("title_az") or profile.get("title") or ""


def profile_bio(profile: dict, lang: str) -> str:
    if lang == "en":
        return profile.get("bio_html_en") or profile.get("bio_html_az") or profile.get("bio_html") or ""
    return profile.get("bio_html_az") or profile.get("bio_html") or ""


def build_search_blob(profile: dict, lang: str) -> str:
    degree = (profile.get("degree") or "").strip()
    cred = CRED_LABEL.get(degree, degree)
    name = profile_name(profile, lang)
    if cred:
        name = f"{name} {cred}"
    country = profile_country(profile, lang)
    field = profile_field(profile, lang)
    email = (profile.get("email") or "").strip()
    code = profile_country_code(profile, lang)
    title = profile_title(profile, lang)
    parts = [name, degree, title, country, email, field, code, degree, email, field]
    return norm_search(" ".join(p for p in parts if p))


def render_card(profile: dict, lang: str, *, asset_prefix: str = "../../") -> str:
    email = (profile.get("email") or "").strip()
    degree = (profile.get("degree") or "").strip()
    cred = CRED_LABEL.get(degree, degree)
    country = profile_country(profile, lang)
    field = profile_field(profile, lang)
    code = profile_country_code(profile, lang)
    search = build_search_blob(profile, lang)
    title = profile_title(profile, lang)
    bio_html = profile_bio(profile, lang)
    labels = META_LABELS[lang]
    photo = (profile.get("photo") or "img_001_p61.jpeg").strip()
    slug = slug_from_photo(photo)
    name_display = profile_name(profile, lang)
    name_heading = az_upper_name_latin(name_display) if lang == "en" else az_upper_name(name_display)

    if email:
        email_row = (
            f'      <div class="card-meta-row"><span class="card-meta-label">{labels["field"]}</span>'
            f'<span class="card-meta-ixtilas">{html.escape(field)}</span></div>\n'
            f'      <div class="card-meta-row"><span class="card-meta-label">{labels["email"]}</span>'
            f'<a class="card-email" href="mailto:{esc_attr(email)}">{html.escape(email)}</a></div>'
        )
    else:
        email_row = (
            f'      <div class="card-meta-row"><span class="card-meta-label">{labels["field"]}</span>'
            f'<span class="card-meta-ixtilas">{html.escape(field)}</span></div>\n'
            f'      <div class="card-meta-row"><span class="card-meta-label">{labels["email"]}</span>'
            f'<span class="card-email card-email--empty">—</span></div>'
        )

    cred_html = f' <span class="cred">{html.escape(cred)}</span>' if cred else ""
    alt = html.escape(name_display)
    qr_labels = QR_LABELS[lang]
    profile_href = f"#{html.escape(slug)}"
    qr_src = f"{asset_prefix}images/qr/{lang}/{html.escape(slug)}.png?v=1"

    return f'''<div class="card" id="{html.escape(slug)}" tabindex="-1" data-country-name="{esc_attr(country)}" data-country="{esc_attr(code)}" data-search="{esc_attr(search)}" data-email="{esc_attr(email)}" data-ixtilas="{esc_attr(field)}" data-degree="{esc_attr(degree)}">
  <div class="card-portrait">
    <div class="card-avatar card-photo"><img src="{asset_prefix}images/scientists-photos/{html.escape(photo)}" alt="{alt}" loading="lazy"/></div>
    <a class="card-qr-link" href="{profile_href}" title="{esc_attr(qr_labels["title"])}" aria-label="{esc_attr(qr_labels["aria"])}">
      <img class="card-qr" src="{qr_src}" width="80" height="80" alt="" decoding="async" loading="lazy"/>
    </a>
  </div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-name">{html.escape(name_heading)}{cred_html}</span>
      <p class="card-country">{html.escape(country)}</p>
    </div>
    <p class="card-title">{html.escape(title)}</p>
    <div class="card-meta">
{email_row}
    </div>
    <div class="card-bio">{bio_html}</div>
  </div>
</div>'''


def build_catalog_section(profiles: list[dict], lang: str, *, asset_prefix: str = "../../") -> str:
    cards = [render_card(p, lang, asset_prefix=asset_prefix) for p in profiles]
    return (
        '<section class="catalog-section" id="scientists-catalog">\n'
        '  <div class="cards-grid">\n\n'
        + "\n\n".join(cards)
        + '\n\n  </div>\n</section>\n  '
    )


def replace_catalog_in_page(page_path: Path, catalog_html: str) -> None:
    text = page_path.read_text(encoding="utf-8")
    page_path.write_text(replace_catalog_in_html(text, catalog_html), encoding="utf-8", newline="\n")


def replace_catalog_in_html(text: str, catalog_html: str) -> str:
    start_m = re.search(r'<section class="catalog-section" id="scientists-catalog">', text)
    if not start_m:
        raise SystemExit("catalog section not found")
    start = start_m.start()
    # Anchor on no-results, not the first </section>, so legacy wrapper markup is removed.
    end_m = re.search(r'<div class="no-results"', text[start:])
    if not end_m:
        raise SystemExit("catalog end not found")
    end = start + end_m.start()
    return text[:start] + catalog_html.rstrip() + "\n  " + text[end:]


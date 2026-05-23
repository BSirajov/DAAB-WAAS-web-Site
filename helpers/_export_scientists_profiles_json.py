"""One-time / refresh export: AZ profile cards -> i18n/scientists-profiles.json."""
from __future__ import annotations

import json
import re
from pathlib import Path

try:
    from _paths import ROOT, AZ_SCIENTISTS_PROFILES
    from _normalize_cv_cards import extract_cards, parse_card
    from i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN
    from i18n_person_names_en import latin_display_name
    from scientists_profiles_core import PROFILES_JSON, save_profiles
except ImportError:
    from helpers._paths import ROOT, AZ_SCIENTISTS_PROFILES  # type: ignore
    from helpers._normalize_cv_cards import extract_cards, parse_card  # type: ignore
    from helpers.i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN  # type: ignore
    from helpers.i18n_person_names_en import latin_display_name  # type: ignore
    from helpers.scientists_profiles_core import PROFILES_JSON, save_profiles  # type: ignore

CATALOG_JS = ROOT / "js" / "scientists-catalog-data.js"
EN_CACHE = ROOT / "i18n" / "scientists-profiles-en.json"


def load_catalog_rows() -> dict[str, dict]:
    text = CATALOG_JS.read_text(encoding="utf-8")
    m = re.search(r"window\.SCIENTISTS_CATALOG_DATA\s*=\s*(\[.*?\]);", text, re.S)
    if not m:
        raise SystemExit(f"Could not parse {CATALOG_JS}")
    rows = json.loads(m.group(1))
    by_email: dict[str, dict] = {}
    for row in rows:
        email = (row.get("email") or "").strip().lower()
        if email:
            by_email[email] = row
    return by_email


def extract_photo(avatar_inner: str) -> str:
    m = re.search(r'src="[^"]*/([^"/]+\.(?:png|jpe?g|webp))"', avatar_inner, re.I)
    if m:
        return m.group(1)
    m = re.search(r'src="([^"]+)"', avatar_inner)
    if m:
        return Path(m.group(1)).name
    return "img_001_p61.jpeg"


def main() -> None:
    az_html = AZ_SCIENTISTS_PROFILES.read_text(encoding="utf-8")
    cards_raw, _, _, _ = extract_cards(az_html)
    catalog = load_catalog_rows()
    en_cache = json.loads(EN_CACHE.read_text(encoding="utf-8")) if EN_CACHE.is_file() else {}
    en_profiles = en_cache.get("profiles") or {}

    profiles: list[dict] = []
    for chunk in cards_raw:
        parsed = parse_card(chunk)
        email = (parsed["email"] or parsed["attrs"].get("data-email") or "").strip().lower()
        cat = catalog.get(email, {})
        en = en_profiles.get(email) or en_profiles.get(parsed["email"]) or {}

        name = (cat.get("ad_soyad") or parsed["name_plain"]).strip()
        country_az = parsed["country"] or parsed["attrs"].get("data-country-name", "")
        field_az = parsed["ixtilas"] or parsed["attrs"].get("data-ixtilas", "")

        profile = {
            "say": cat.get("say") or len(profiles) + 1,
            "email": email or parsed["email"],
            "name": name,
            "name_en": latin_display_name(name),
            "photo": extract_photo(parsed["avatar_inner"]),
            "country_az": country_az,
            "country_code": parsed["attrs"].get("data-country", ""),
            "field_az": field_az,
            "degree": parsed["attrs"].get("data-degree") or cat.get("elmi_derece") or parsed["cred"],
            "title_az": parsed["title"],
            "bio_html_az": parsed["bio"],
            "country_en": en.get("country") or COUNTRY_EN.get(country_az, country_az),
            "field_en": en.get("ixtilas") or FIELD_EN.get(field_az, field_az),
            "title_en": en.get("title") or "",
            "bio_html_en": en.get("bio_html") or "",
        }
        profiles.append(profile)

    profiles.sort(key=lambda p: p.get("say", 0))
    save_profiles(profiles)
    print(f"Exported {len(profiles)} profiles -> {PROFILES_JSON.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

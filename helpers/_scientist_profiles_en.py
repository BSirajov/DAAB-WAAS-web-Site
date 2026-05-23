"""Translate scientist profile cards for en/scientists/profiles.html."""
from __future__ import annotations

import argparse
import html
import json
import re
import time
import unicodedata
from pathlib import Path

from _paths import ROOT

try:
    from i18n_scientists_maps_en import (
        BIO_SECTION_HEADINGS_EN,
        COUNTRY_EN,
        FIELD_EN,
    )
    from i18n_person_names_en import az_upper_name_latin, latin_display_name
    from _normalize_cv_cards import extract_cards, parse_card
except ImportError:
    from helpers.i18n_scientists_maps_en import (  # type: ignore
        BIO_SECTION_HEADINGS_EN,
        COUNTRY_EN,
        FIELD_EN,
    )
    from helpers.i18n_person_names_en import az_upper_name_latin, latin_display_name  # type: ignore
    from helpers._normalize_cv_cards import extract_cards, parse_card  # type: ignore

AZ_PROFILES = ROOT / "az" / "scientists" / "profiles.html"
CACHE_PATH = ROOT / "i18n" / "scientists-profiles-en.json"
PROFILES_JSON = ROOT / "i18n" / "scientists-profiles.json"

P_RE = re.compile(r"<p(?P<attrs>[^>]*)>(?P<body>.*?)</p>", re.DOTALL | re.IGNORECASE)
LI_RE = re.compile(r"<li(?P<attrs>[^>]*)>(?P<body>.*?)</li>", re.DOTALL | re.IGNORECASE)


def esc_attr(s: str) -> str:
    return html.escape((s or "").strip(), quote=True)


def strip_tags(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "")


def az_upper_name(name: str) -> str:
    return az_upper_name_latin(name)


def map_country(country: str) -> str:
    return COUNTRY_EN.get(country.strip(), country.strip())


def map_field(field: str) -> str:
    return FIELD_EN.get(field.strip(), field.strip())


def norm_search(s: str) -> str:
    return re.sub(r"\s+", " ", (s or "").lower()).strip()


def get_translator():
    from deep_translator import GoogleTranslator

    return GoogleTranslator(source="auto", target="en")


def translate_text(translator, text: str) -> str:
    text = (text or "").strip()
    if not text:
        return text
    if text in BIO_SECTION_HEADINGS_EN:
        return BIO_SECTION_HEADINGS_EN[text]
    chunk_size = 4500
    if len(text) <= chunk_size:
        try:
            return translator.translate(text)
        except Exception:
            time.sleep(1.5)
            return translator.translate(text)
    parts: list[str] = []
    for i in range(0, len(text), chunk_size):
        chunk = text[i : i + chunk_size]
        try:
            parts.append(translator.translate(chunk))
        except Exception:
            time.sleep(1.5)
            parts.append(translator.translate(chunk))
        time.sleep(0.15)
    return " ".join(parts)


def _translate_tagged_block(translator, match: re.Match[str], tag: str) -> str:
    attrs = match.group("attrs")
    body = match.group("body")
    plain = html.unescape(strip_tags(body)).strip()
    if not plain:
        return match.group(0)
    if tag == "p" and "bio-section-title" in attrs:
        en = BIO_SECTION_HEADINGS_EN.get(plain, translate_text(translator, plain))
    else:
        en = translate_text(translator, plain)
    return f"<{tag}{attrs}>{html.escape(en)}</{tag}>"


def translate_bio_html(translator, bio_html: str) -> str:
    if not bio_html.strip():
        return bio_html

    bio_html = P_RE.sub(lambda m: _translate_tagged_block(translator, m, "p"), bio_html)
    bio_html = LI_RE.sub(lambda m: _translate_tagged_block(translator, m, "li"), bio_html)
    return bio_html


def build_search(parsed: dict, country_en: str, field_en: str) -> str:
    name = latin_display_name(parsed["name_plain"])
    if parsed["cred"]:
        name = f"{name} {parsed['cred']}"
    parts = [
        name,
        parsed["attrs"].get("data-degree", ""),
        parsed.get("title_en") or parsed["title"],
        country_en,
        parsed["email"],
        field_en,
        parsed["attrs"].get("data-country", ""),
        parsed["attrs"].get("data-degree", ""),
        parsed["email"],
        field_en,
    ]
    return norm_search(" ".join(p for p in parts if p))


def render_card_en(parsed: dict) -> str:
    attrs = parsed["attrs"]
    country_en = parsed["country_en"]
    field_en = parsed["field_en"]
    email = parsed["email"] or attrs.get("data-email", "")
    degree = attrs.get("data-degree", "")
    title_en = parsed["title_en"]
    bio_html = parsed["bio_en"]
    search = build_search(parsed, country_en, field_en)

    email_row = (
        '      <div class="card-meta-row"><span class="card-meta-label">Field:</span>'
        f'<span class="card-meta-ixtilas">{html.escape(field_en)}</span></div>\n'
        '      <div class="card-meta-row"><span class="card-meta-label">Email:</span>'
        + (
            f'<a class="card-email" href="mailto:{esc_attr(email)}">{html.escape(email)}</a></div>'
            if email
            else '<span class="card-email card-email--empty">—</span></div>'
        )
    )

    cred_html = (
        f' <span class="cred">{html.escape(parsed["cred"])}</span>' if parsed["cred"] else ""
    )
    name_upper = html.escape(az_upper_name_latin(parsed["name_plain"]))
    avatar_inner = parsed["avatar_inner"]
    if 'alt="' in avatar_inner:
        alt_m = re.search(r'alt="([^"]*)"', avatar_inner)
        if alt_m:
            avatar_inner = avatar_inner.replace(
                alt_m.group(0),
                f'alt="{html.escape(latin_display_name(html.unescape(alt_m.group(1))))}"',
                1,
            )

    return f'''<div class="card" data-country-name="{esc_attr(country_en)}" data-country="{esc_attr(attrs.get("data-country", ""))}" data-search="{esc_attr(search)}" data-email="{esc_attr(email)}" data-ixtilas="{esc_attr(field_en)}" data-degree="{esc_attr(degree)}">
  <div class="card-avatar card-photo">{avatar_inner}</div>
  <div class="card-body">
    <div class="card-header">
      <span class="card-name">{name_upper}{cred_html}</span>
      <p class="card-country">{html.escape(country_en)}</p>
    </div>
    <p class="card-title">{html.escape(title_en)}</p>
    <div class="card-meta">
{email_row}
    </div>
    <div class="card-bio">{bio_html}</div>
  </div>
</div>'''


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {"version": 1, "profiles": {}}
    return json.loads(CACHE_PATH.read_text(encoding="utf-8"))


def save_cache(cache: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def profile_key(parsed: dict) -> str:
    email = (parsed.get("email") or parsed["attrs"].get("data-email") or "").strip().lower()
    if email:
        return email
    return parsed["name_plain"].casefold()


def enrich_parsed(parsed: dict, cache_entry: dict | None, translator=None) -> dict:
    country_en = map_country(parsed["country"])
    field_en = map_field(parsed["ixtilas"])

    title_en = parsed["title"]
    bio_en = parsed["bio"]

    if cache_entry:
        title_en = cache_entry.get("title") or title_en
        bio_en = cache_entry.get("bio_html") or bio_en
        country_en = cache_entry.get("country") or country_en
        field_en = cache_entry.get("ixtilas") or field_en
    elif translator is not None:
        if title_en.strip():
            title_en = translate_text(translator, title_en)
        if bio_en.strip():
            bio_en = translate_bio_html(translator, bio_en)

    out = dict(parsed)
    out["country_en"] = country_en
    out["field_en"] = field_en
    out["title_en"] = title_en
    out["bio_en"] = bio_en
    return out


def build_catalog_section(az_html: str, cache: dict, translator=None) -> str:
    cards_raw, _, _, _ = extract_cards(az_html)
    profiles = cache.get("profiles", {})
    rebuilt: list[str] = []

    for chunk in cards_raw:
        parsed = parse_card(chunk)
        key = profile_key(parsed)
        entry = profiles.get(key)
        enriched = enrich_parsed(parsed, entry, translator)
        rebuilt.append(render_card_en(enriched))

    return (
        '<section class="catalog-section" id="scientists-catalog">\n'
        '  <div class="cards-grid">\n\n'
        + "\n\n".join(rebuilt)
        + '\n\n  </div>\n</section>\n  '
    )


def build_cache(refresh: bool = False) -> None:
    az_html = AZ_PROFILES.read_text(encoding="utf-8")
    cards_raw, _, _, _ = extract_cards(az_html)
    cache = load_cache()
    profiles = cache.setdefault("profiles", {})
    translator = get_translator() if refresh else None

    for i, chunk in enumerate(cards_raw, 1):
        parsed = parse_card(chunk)
        key = profile_key(parsed)
        existing = profiles.get(key)
        needs_title = not existing or not existing.get("title")
        needs_bio = not existing or not existing.get("bio_html")
        if refresh or needs_title or needs_bio:
            if translator is None:
                translator = get_translator()
            title_en = translate_text(translator, parsed["title"]) if parsed["title"].strip() else ""
            bio_en = translate_bio_html(translator, parsed["bio"]) if parsed["bio"].strip() else ""
            profiles[key] = {
                "title": title_en,
                "bio_html": bio_en,
                "country": map_country(parsed["country"]),
                "ixtilas": map_field(parsed["ixtilas"]),
            }
            print(f"[{i}/{len(cards_raw)}] translated {parsed['name_plain']}")
            time.sleep(0.2)
        else:
            print(f"[{i}/{len(cards_raw)}] cached {parsed['name_plain']}")

    save_cache(cache)
    print(f"Saved {len(profiles)} profiles -> {CACHE_PATH.relative_to(ROOT)}")

    try:
        from _export_scientists_profiles_json import main as export_profiles_json
        from _build_scientists_profiles import build_az, build_en
    except ImportError:
        from helpers._export_scientists_profiles_json import main as export_profiles_json  # type: ignore
        from helpers._build_scientists_profiles import build_az, build_en  # type: ignore

    export_profiles_json()
    build_az()
    build_en()
    print("Synced unified JSON and rebuilt az/en catalogs")


def apply_to_html(html: str) -> str:
    try:
        from scientists_profiles_core import build_catalog_section, load_profiles, replace_catalog_in_html
    except ImportError:
        from helpers.scientists_profiles_core import (  # type: ignore
            build_catalog_section,
            load_profiles,
            replace_catalog_in_html,
        )
    if not PROFILES_JSON.is_file():
        raise SystemExit(
            f"Missing {PROFILES_JSON.relative_to(ROOT)} — run: python helpers/_export_scientists_profiles_json.py"
        )
    profiles = load_profiles()
    catalog = build_catalog_section(profiles, "en", asset_prefix="../../")
    return replace_catalog_in_html(html, catalog)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--build-cache", action="store_true", help="Translate AZ profile cards into i18n cache")
    parser.add_argument("--refresh", action="store_true", help="Re-translate all cached profiles")
    args = parser.parse_args()
    if args.build_cache:
        build_cache(refresh=args.refresh)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()

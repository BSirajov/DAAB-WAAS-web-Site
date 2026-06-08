#!/usr/bin/env python3
"""Extract metadata from prominent figure profiles into js/prominent-figures-catalog-data.js."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

from _paths import ROOT
from _prominent_figure_en_strings import (
    CATEGORY_LABEL_EN,
    translate_country,
    translate_field,
    translate_period,
    translate_region,
)
from _prominent_figure_names_en import apply_english_names, english_name
from _prominent_figure_pronouns_en import apply_singular_pronouns

FIGURES_ROOT_AZ = ROOT / "az" / "prominent_figures"
FIGURES_ROOT_EN = ROOT / "en" / "prominent_figures"
OUT_AZ = ROOT / "js" / "prominent-figures-catalog-data.js"
OUT_EN = ROOT / "js" / "prominent-figures-catalog-data-en.js"

RE_NAME = re.compile(r"<h1>([^<]+)</h1>")
RE_DATES = re.compile(r'<p class="pf-hero-dates">([^<]+)</p>')
RE_ERA = re.compile(r'<div class="hero-era-badge">([^<]+)</div>')
RE_SHORT = re.compile(
    r'class="prose pf-profile-article">.*?<p>([^<]{20,400})</p>',
    re.DOTALL,
)
RE_EMOJI = re.compile(r'<span class="pf-hero-symbol__icon">([^<]+)</span>')
RE_GOLD = re.compile(r'<span class="hero-tag gold">([^<]+)</span>')
RE_FIELD = re.compile(
    r'info-label">(?:Sahə|Field)</span><span class="info-val">([^<]+)</span>'
)
RE_BIRTH = re.compile(
    r'info-label">(?:Doğum tarixi|Year of birth)</span><span class="info-val">([^<]+)</span>'
)
RE_YEAR = re.compile(r"(\d{3,4})")

CATEGORY_LABELS = {
    "azturk": "Azərbaycan və türk dünyası",
    "world": "Dünya alimləri",
}


def parse_field(raw: str) -> tuple[str, str]:
    parts = [p.strip() for p in raw.split(",") if p.strip()]
    if len(parts) >= 2:
        return parts[0], parts[-1]
    if parts:
        return parts[0], parts[0]
    return "", ""


def parse_era(raw: str) -> tuple[str, str]:
    text = html.unescape(raw.strip())
    if "·" in text:
        left, right = [s.strip() for s in text.split("·", 1)]
        return left, right
    return text, ""


def birth_year(dates: str, birth_val: str) -> int | None:
    for src in (birth_val, dates):
        if not src:
            continue
        m = RE_YEAR.search(src.replace("BCE", "").replace("bce", ""))
        if m:
            try:
                return int(m.group(1))
            except ValueError:
                pass
    return None


RE_ROMAN_CENTURY = re.compile(
    r"\b([IVXLCDM]{1,4})\s*(?:(?:-ci|-cü|-cu|-cü|-nci|-ncü|-ncu|-ncü)\s*)?əsr\b",
    re.IGNORECASE,
)
RE_ORDINAL_CENTURY = re.compile(
    r"\b(\d{1,2})(?:st|nd|rd|th)\s*[-–]?\s*(?:\d{1,2})?\s*(?:st|nd|rd|th)?\s*century\b",
    re.IGNORECASE,
)
RE_ARABIC_CENTURY = re.compile(r"\b(\d{1,2})\s*(?:-ci|-cü|-cu|-cü|-nci|-ncü|-ncu|-ncü)\s*əsr\b", re.IGNORECASE)


def _roman_to_int(value: str) -> int | None:
    numerals = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    text = value.upper()
    if not text or any(ch not in numerals for ch in text):
        return None
    total = 0
    prev = 0
    for ch in reversed(text):
        num = numerals[ch]
        if num < prev:
            total -= num
        else:
            total += num
            prev = num
    return total or None


def century_start_year(century: int) -> int:
    return max(1, (century - 1) * 100 + 1)


def parse_century_year(text: str) -> int | None:
    raw = html.unescape(text or "").strip()
    if not raw:
        return None
    m = RE_ROMAN_CENTURY.search(raw)
    if m:
        century = _roman_to_int(m.group(1))
        return century_start_year(century) if century else None
    m = RE_ARABIC_CENTURY.search(raw)
    if m:
        return century_start_year(int(m.group(1)))
    m = RE_ORDINAL_CENTURY.search(raw)
    if m:
        return century_start_year(int(m.group(1)))
    if "century" in raw.lower():
        m = RE_YEAR.search(raw)
        if m:
            return century_start_year(int(m.group(1)))
    return None


def fallback_year(text: str) -> int | None:
    raw = html.unescape(text or "").strip()
    if not raw:
        return None
    m = re.search(r"\b(\d{3,4})\b", raw)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{1,2})\s*[-–]", raw)
    if m:
        return int(m.group(1))
    m = re.search(r"\b(\d{1,2})\s*(?:ce|bce)\b", raw, re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None


def infer_period(dates: str, birth_val: str, year: int | None) -> str:
    """Historical era label for catalogue filters and table view."""
    combined = f"{dates} {birth_val}".strip()
    lower = combined.lower()
    if any(token in lower for token in ("bce", "e.ə", "ə.e", "e.e", "milli", "əfsanəvi", "legendary")):
        return "Antik dövr"
    resolved = year if year is not None else fallback_year(combined)
    if resolved is None:
        resolved = parse_century_year(combined)
    if resolved is None:
        return ""
    if resolved < 500:
        return "Antik dövr"
    if resolved < 1500:
        return "Orta əsrlər"
    if resolved < 1800:
        return "Yeni dövr"
    return "Müasir dövr"


def parse_profile(path: Path, category: str) -> dict | None:
    text = path.read_text(encoding="utf-8", errors="replace")
    name_m = RE_NAME.search(text)
    if not name_m:
        return None
    name = html.unescape(name_m.group(1).strip())
    dates = html.unescape(RE_DATES.search(text).group(1).strip()) if RE_DATES.search(text) else ""
    era_raw = RE_ERA.search(text).group(1) if RE_ERA.search(text) else ""
    region, period = parse_era(html.unescape(era_raw))
    short_m = RE_SHORT.search(text)
    summary = html.unescape(short_m.group(1).strip()) if short_m else ""
    emoji_m = RE_EMOJI.search(text)
    emoji = html.unescape(emoji_m.group(1).strip()) if emoji_m else "⭐"
    country = (
        html.unescape(RE_GOLD.search(text).group(1).strip()) if RE_GOLD.search(text) else ""
    )
    field_raw = (
        html.unescape(RE_FIELD.search(text).group(1).strip()) if RE_FIELD.search(text) else ""
    )
    _, field = parse_field(field_raw)
    if not field and field_raw:
        field = field_raw
    birth_val = (
        html.unescape(RE_BIRTH.search(text).group(1).strip())
        if RE_BIRTH.search(text)
        else ""
    )
    slug = path.stem
    href = f"prominent_figures/{category}/{slug}.html"
    by = birth_year(dates, birth_val)
    if not period:
        period = infer_period(dates, birth_val, by)
    return {
        "id": slug,
        "name": name,
        "dates": dates,
        "summary": summary,
        "emoji": emoji,
        "country": country,
        "field": field,
        "region": region,
        "period": period,
        "category": category,
        "categoryLabel": CATEGORY_LABELS[category],
        "href": href,
        "birthYear": by,
    }


def localize_row_en(row: dict) -> dict:
    out = dict(row)
    slug = row.get("id") or ""
    en_name = english_name(slug, row.get("name") or "")
    out["name"] = en_name
    out["categoryLabel"] = CATEGORY_LABEL_EN.get(row["category"], row.get("categoryLabel", ""))
    out["field"] = translate_field(row.get("field") or "")
    out["period"] = translate_period(row.get("period") or "")
    out["region"] = translate_region(row.get("region") or "")
    out["country"] = translate_country(row.get("country") or "")
    if row.get("summary") and re.search(r"[əğıöüşçƏĞİÖÜŞÇ]", row["summary"]):
        field = out["field"]
        if row["category"] == "world":
            out["summary"] = (
                f"{en_name} is among the prominent figures who shaped {field or 'this field'} "
                "and left a lasting mark on world science."
            )
        else:
            country = translate_country(row.get("country") or row.get("region") or "the Turkic world")
            out["summary"] = (
                f"{en_name} was a prominent representative of {country} whose work in "
                f"{field or 'science, culture, and public life'} occupies an important "
                "place in the shared heritage of the Turkic world."
            )
    elif out.get("summary"):
        out["summary"] = apply_english_names(out["summary"], slug)
    if out.get("summary"):
        out["summary"] = apply_singular_pronouns(out["summary"])
    return out


def collect_rows(figures_root: Path, category_labels: dict[str, str], *, en: bool) -> list[dict]:
    rows: list[dict] = []
    for category in ("azturk", "world"):
        folder = figures_root / category
        if not folder.is_dir():
            continue
        for path in sorted(folder.glob("*.html")):
            if path.name == "hazirlanir.html" or path.stem.endswith("_EN"):
                continue
            row = parse_profile(path, category)
            if not row:
                continue
            row["categoryLabel"] = category_labels[category]
            if en:
                row = localize_row_en(row)
            rows.append(row)
    rows.sort(key=lambda r: r["name"].casefold())
    return rows


def write_catalog(rows: list[dict], var_name: str, out_path: Path) -> None:
    payload = json.dumps(rows, ensure_ascii=False, indent=2)
    out_path.write_text(f"window.{var_name} = {payload};\n", encoding="utf-8", newline="\n")
    print(f"Wrote {len(rows)} profiles to {out_path.relative_to(ROOT)}")


def main() -> None:
    az_rows = collect_rows(FIGURES_ROOT_AZ, CATEGORY_LABELS, en=False)
    write_catalog(az_rows, "PROMINENT_FIGURES_CATALOG", OUT_AZ)
    if FIGURES_ROOT_EN.is_dir():
        en_rows = collect_rows(FIGURES_ROOT_EN, CATEGORY_LABEL_EN, en=True)
        write_catalog(en_rows, "PROMINENT_FIGURES_CATALOG_EN", OUT_EN)
    else:
        print(f"Skip EN catalog: {FIGURES_ROOT_EN.relative_to(ROOT)} not found (run _build_en_prominent_figures.py)")


if __name__ == "__main__":
    main()

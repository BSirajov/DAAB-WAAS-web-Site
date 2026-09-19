#!/usr/bin/env python3
"""Build per-country city JSON for DAAB forms from GeoNames cities500.

Every form country gets a complete city list (populated places + admin seats)
with the capital pinned first. Re-run after changing DAAB_COUNTRY_CODES.
"""
from __future__ import annotations

import json
import re
import unicodedata
import zipfile
from pathlib import Path

from _paths import HELPERS, ROOT

CACHE = HELPERS / "_geo_cache"
CITIES_ZIP = CACHE / "cities500.zip"
COUNTRY_INFO = CACHE / "countryInfo.txt"
OUT_DIR = ROOT / "js" / "cities"
DEPLOY_DIR = ROOT / "Deployment" / "js" / "cities"
COUNTRY_CODES_JS = ROOT / "js" / "daab-country-codes.js"

# Extra English / local capital spellings GeoNames may omit as the primary name.
EXTRA_CAPITALS: dict[str, list[str]] = {
    "AG": ["Saint John's", "St. John's"],
    "AT": ["Vienna", "Wien"],
    "BO": ["Sucre", "La Paz"],
    "CI": ["Yamoussoukro", "Abidjan"],
    "CZ": ["Prague", "Praha"],
    "EG": ["Cairo", "Qahirə", "Kairo"],
    "FM": ["Palikir"],
    "LK": ["Sri Jayawardenepura Kotte", "Colombo"],
    "MD": ["Chișinău", "Chisinau"],
    "NL": ["Amsterdam", "The Hague"],
    "PS": ["Ramallah", "East Jerusalem"],
    "SY": ["Damascus", "Dimashq", "Dəməşq"],
    "SZ": ["Mbabane", "Lobamba"],
    "TZ": ["Dodoma", "Dar es Salaam"],
    "US": ["Washington", "Washington, D.C.", "Washington DC"],
    "VA": ["Vatican City"],
    "XK": ["Pristina", "Prishtina", "Priština"],
    "ZA": ["Pretoria", "Cape Town", "Bloemfontein"],
}


def fold(text: str) -> str:
    az = str.maketrans("əıöüuğşçƏİÖÜĞŞÇ", "eiouugscEIOUGSC")
    s = unicodedata.normalize("NFKD", (text or "").translate(az)).lower()
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", " ", s).strip()


def load_iso_codes() -> list[str]:
    text = COUNTRY_CODES_JS.read_text(encoding="utf-8")
    match = re.search(r"var CODES = \[(.*?)\];", text, re.S)
    if not match:
        raise SystemExit("Could not parse DAAB_COUNTRY_CODES")
    return [c.strip().strip('"') for c in match.group(1).split(",") if c.strip()]


def load_capitals() -> dict[str, str]:
    capitals: dict[str, str] = {}
    for line in COUNTRY_INFO.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        parts = line.split("\t")
        if len(parts) < 6:
            continue
        iso, capital = parts[0].strip().upper(), parts[5].strip()
        if iso and capital:
            capitals[iso] = capital
    return capitals


def add_city(bucket: dict[str, str], name: str) -> None:
    name = str(name or "").strip()
    if not name:
        return
    key = fold(name)
    if not key or key in bucket:
        return
    bucket[key] = name


def load_cities_by_country(codes: set[str]) -> dict[str, dict[str, str]]:
    by_country: dict[str, dict[str, str]] = {code: {} for code in codes}
    with zipfile.ZipFile(CITIES_ZIP) as zf:
        member = next(n for n in zf.namelist() if n.endswith(".txt") or n == "cities500")
        with zf.open(member) as fh:
            for raw in fh:
                line = raw.decode("utf-8", errors="replace")
                cols = line.split("\t")
                if len(cols) < 9:
                    continue
                code = cols[8].strip().upper()
                if code not in by_country:
                    continue
                bucket = by_country[code]
                add_city(bucket, cols[1])
                add_city(bucket, cols[2])
    return by_country


def ordered_city_list(code: str, bucket: dict[str, str], capital: str) -> list[str]:
    pins: list[str] = []
    if capital:
        pins.append(capital)
    pins.extend(EXTRA_CAPITALS.get(code, []))
    seen: set[str] = set()
    out: list[str] = []
    for name in pins:
        key = fold(name)
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(bucket.get(key, name))
    rest = [name for key, name in bucket.items() if key not in seen]
    rest.sort(key=lambda n: fold(n))
    out.extend(rest)
    return out


def write_json(path: Path, cities: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cities, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")


def main() -> None:
    if not CITIES_ZIP.exists() or not COUNTRY_INFO.exists():
        raise SystemExit(
            "Missing GeoNames dumps. Download cities500.zip and countryInfo.txt into helpers/_geo_cache/"
        )
    codes = load_iso_codes()
    code_set = set(codes)
    capitals = load_capitals()
    by_country = load_cities_by_country(code_set)

    empty: list[str] = []
    missing_capital: list[str] = []
    total = 0
    for code in codes:
        cities = ordered_city_list(code, by_country.get(code, {}), capitals.get(code, ""))
        if not cities:
            empty.append(code)
        cap = capitals.get(code, "")
        extras = EXTRA_CAPITALS.get(code, [])
        if cap and fold(cap) not in {fold(c) for c in cities} and not extras:
            missing_capital.append(f"{code}:{cap}")
        write_json(OUT_DIR / f"{code}.json", cities)
        write_json(DEPLOY_DIR / f"{code}.json", cities)
        total += len(cities)

    print(f"Wrote {len(codes)} country city files ({total} names) to {OUT_DIR}")
    if empty:
        raise SystemExit("Empty city lists: " + ", ".join(empty))
    if missing_capital:
        print("Capitals not matched in GeoNames (pinned from countryInfo): " + ", ".join(missing_capital))


if __name__ == "__main__":
    main()

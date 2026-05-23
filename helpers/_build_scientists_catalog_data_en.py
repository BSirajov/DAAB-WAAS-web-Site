"""Generate js/scientists-catalog-data-en.js from the AZ catalogue data."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

try:
    from i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN, GENDER_EN
    from i18n_person_names_en import latin_display_name
except ImportError:
    from helpers.i18n_scientists_maps_en import COUNTRY_EN, FIELD_EN, GENDER_EN  # type: ignore
    from helpers.i18n_person_names_en import latin_display_name  # type: ignore

DATA_AZ = ROOT / "js" / "scientists-catalog-data.js"
DATA_EN = ROOT / "js" / "scientists-catalog-data-en.js"


def load_az_rows() -> list[dict]:
    text = DATA_AZ.read_text(encoding="utf-8")
    return json.loads(text.split("=", 1)[1].strip().rstrip(";"))


def translate_row(row: dict) -> dict:
    out = dict(row)
    country = (row.get("yasadigi_olke") or "").strip()
    field = (row.get("ixtilas") or "").strip()
    gender = (row.get("cinsi") or "").strip()
    name = (row.get("ad_soyad") or "").strip()
    if name:
        out["ad_soyad"] = latin_display_name(name)
    if country in COUNTRY_EN:
        out["yasadigi_olke"] = COUNTRY_EN[country]
    if field in FIELD_EN:
        out["ixtilas"] = FIELD_EN[field]
    if gender in GENDER_EN:
        out["cinsi"] = GENDER_EN[gender]
    return out


def main() -> None:
    rows = [translate_row(r) for r in load_az_rows()]
    body = json.dumps(rows, ensure_ascii=False, indent=2)
    DATA_EN.write_text(
        f"window.SCIENTISTS_CATALOG_DATA = {body};\n",
        encoding="utf-8",
    )
    print(f"Wrote {len(rows)} rows -> {DATA_EN.relative_to(ROOT)}")


if __name__ == "__main__":
    main()

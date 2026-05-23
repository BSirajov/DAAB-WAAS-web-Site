"""Compare scientist name order between list catalogue and profile cards."""
from __future__ import annotations

import json
import re

from _paths import AZ_SCIENTISTS_LIST, AZ_SCIENTISTS_PROFILES, ROOT


def norm(s: str) -> str:
    s = s.upper().strip()
    s = re.sub(r"\s+", " ", s)
    for a, b in [("İ", "I"), ("Ə", "E"), ("Ş", "S"), ("Ç", "C"), ("Ğ", "G"), ("Ö", "O"), ("Ü", "U")]:
        s = s.replace(a, b)
    return s


def load_catalog_names() -> list[str]:
    data_js = ROOT / "js" / "scientists-catalog-data.js"
    text = data_js.read_text(encoding="utf-8")
    m = re.search(r"window\.SCIENTISTS_CATALOG_DATA\s*=\s*(\[.*?\]);", text, re.S)
    if not m:
        raise SystemExit(f"Could not parse catalogue array in {data_js}")
    rows = json.loads(m.group(1))
    return [norm(r.get("ad_soyad", "")) for r in rows]


def load_profile_names() -> list[str]:
    text = AZ_SCIENTISTS_PROFILES.read_text(encoding="utf-8")
    raw = re.findall(r'class="card-name">([^<]+)', text)
    return [norm(re.sub(r"<span.*", "", n)) for n in raw]


def main() -> int:
    if not AZ_SCIENTISTS_LIST.is_file():
        raise SystemExit(f"Missing {AZ_SCIENTISTS_LIST}")
    if not AZ_SCIENTISTS_PROFILES.is_file():
        raise SystemExit(f"Missing {AZ_SCIENTISTS_PROFILES}")

    data_names = load_catalog_names()
    card_names = load_profile_names()
    mism = [
        (i + 1, card_names[i], data_names[i])
        for i in range(min(len(card_names), len(data_names)))
        if card_names[i] != data_names[i]
    ]
    print("cards", len(card_names), "catalog", len(data_names), "mismatches", len(mism))
    for x in mism[:20]:
        print(x)
    return 1 if mism else 0


if __name__ == "__main__":
    raise SystemExit(main())

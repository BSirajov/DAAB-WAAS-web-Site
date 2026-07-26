"""Compare scientist name order between list catalogue and profile cards.

Profiles pages may be client-rendered (data-daab-profiles-client=1), in which
case names are not present as static HTML. In that mode, compare catalogue
`ad_soyad` order against i18n/scientists-profiles.json `name` order (by say).
"""
from __future__ import annotations

import json
import re

from _paths import AZ_SCIENTISTS_LIST, AZ_SCIENTISTS_PROFILES, ROOT

PROFILES_JSON = ROOT / "i18n" / "scientists-profiles.json"


def norm(s: str) -> str:
    s = s.upper().strip()
    s = re.sub(r"\s+", " ", s)
    for a, b in [("İ", "I"), ("Ə", "E"), ("Ş", "S"), ("Ç", "C"), ("Ğ", "G"), ("Ö", "O"), ("Ü", "U")]:
        s = s.replace(a, b)
    return s


def is_client_render_profiles(html: str) -> bool:
    return 'data-daab-profiles-client="1"' in html or "data-daab-profiles-client='1'" in html


def load_catalog_rows() -> list[dict]:
    data_js = ROOT / "js" / "scientists-catalog-data.js"
    text = data_js.read_text(encoding="utf-8")
    m = re.search(r"window\.SCIENTISTS_CATALOG_DATA\s*=\s*(\[.*?\]);", text, re.S)
    if not m:
        raise SystemExit(f"Could not parse catalogue array in {data_js}")
    rows = json.loads(m.group(1))
    rows.sort(key=lambda r: int(r.get("say") or 0))
    return rows


def load_catalog_names() -> list[str]:
    return [norm(r.get("ad_soyad", "")) for r in load_catalog_rows()]


def load_profile_names_from_html(html: str) -> list[str]:
    raw = re.findall(r'class="card-name">([^<]+)', html)
    return [norm(re.sub(r"<span.*", "", n)) for n in raw]


def load_profile_names_from_json() -> list[str]:
    if not PROFILES_JSON.is_file():
        raise SystemExit(f"Missing {PROFILES_JSON}")
    data = json.loads(PROFILES_JSON.read_text(encoding="utf-8"))
    profiles = list(data.get("profiles") or [])
    profiles.sort(key=lambda p: int(p.get("say") or 0))
    return [norm(p.get("name") or p.get("name_az") or "") for p in profiles]


def main() -> int:
    if not AZ_SCIENTISTS_LIST.is_file():
        raise SystemExit(f"Missing {AZ_SCIENTISTS_LIST}")
    if not AZ_SCIENTISTS_PROFILES.is_file():
        raise SystemExit(f"Missing {AZ_SCIENTISTS_PROFILES}")

    html = AZ_SCIENTISTS_PROFILES.read_text(encoding="utf-8")
    data_names = load_catalog_names()
    client_render = is_client_render_profiles(html)

    if client_render:
        card_names = load_profile_names_from_json()
        mode = "client-render (profiles.json)"
    else:
        card_names = load_profile_names_from_html(html)
        mode = "static HTML"

    print(f"mode: {mode}")
    print("cards", len(card_names), "catalog", len(data_names), end="")

    if not data_names:
        print(" mismatches 0")
        print("ERROR: catalogue is empty")
        return 1

    if not card_names:
        print(" mismatches 0")
        print("ERROR: no profile names found while catalogue has entries")
        return 1

    if len(card_names) != len(data_names):
        print(f" mismatches (count mismatch)")
        print(
            f"ERROR: profile count {len(card_names)} != catalogue count {len(data_names)}"
        )
        return 1

    mism = [
        (i + 1, card_names[i], data_names[i])
        for i in range(len(card_names))
        if card_names[i] != data_names[i]
    ]
    print(" mismatches", len(mism))
    for x in mism[:20]:
        print(x)
    return 1 if mism else 0


if __name__ == "__main__":
    raise SystemExit(main())

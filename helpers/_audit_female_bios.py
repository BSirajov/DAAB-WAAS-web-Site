"""Audit feminine pronoun usage in female scientist profiles."""
from __future__ import annotations

import json
import re
from pathlib import Path

from _paths import ROOT

pat_en = re.compile(r"\b(He|he|His|his|him|Him|himself|Himself)\b")


def main() -> None:
    profiles = json.loads((ROOT / "i18n" / "scientists-profiles.json").read_text(encoding="utf-8"))[
        "profiles"
    ]
    raw = (ROOT / "js" / "scientists-catalog-data.js").read_text(encoding="utf-8")
    data = json.loads(raw.split("=", 1)[1].strip().rstrip(";"))
    female = {r["email"]: r for r in data if r.get("cinsi") == "qadın"}
    for p in profiles:
        if p["email"] not in female:
            continue
        en = p.get("bio_html_en") or ""
        az = p.get("bio_html_az") or ""
        hits_en = pat_en.findall(en)
        hits_az_o = re.findall(r"\b(o,|Onun|onun)\b", az, re.I)
        print(
            f"{p['say']:3} {p['name'][:40]:40} EN_masc:{len(hits_en):3} AZ_O:{len(hits_az_o):2}"
        )


if __name__ == "__main__":
    main()

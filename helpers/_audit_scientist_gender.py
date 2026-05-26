"""Audit masculine pronouns in female scientist profiles (EN + AZ hints)."""
from __future__ import annotations

import json
import re

from _paths import ROOT

EN_PAT = re.compile(r"\b(He|he|His|his|him|Him|himself|Himself)\b")
# Suspicious invented feminine job titles
BAD_AZ = re.compile(r"\b(dosentə|Dosentə|professorə|Professorə)\b")


def main() -> None:
    profiles = json.loads(
        (ROOT / "i18n" / "scientists-profiles.json").read_text(encoding="utf-8")
    )["profiles"]
    raw = (ROOT / "js" / "scientists-catalog-data.js").read_text(encoding="utf-8")
    catalog = json.loads(raw.split("=", 1)[1].strip().rstrip(";"))
    female_says = {r["say"] for r in catalog if r.get("cinsi") == "qadın"}
    male_says = {r["say"] for r in catalog if r.get("cinsi") == "kişi"}

    print(f"Female in catalogue: {len(female_says)} | Male: {len(male_says)}\n")
    issues = []
    for p in profiles:
        say = p["say"]
        en = p.get("bio_html_en") or ""
        az = p.get("bio_html_az") or ""
        en_hits = EN_PAT.findall(en)
        bad_az = BAD_AZ.findall(az + " " + (p.get("title_az") or ""))
        if say in female_says and en_hits:
            issues.append((say, p["name"], "EN", len(en_hits), en_hits[:5]))
        if say in female_says and bad_az:
            issues.append((say, p["name"], "AZ_BAD", bad_az))
        if say in male_says and en_hits:
            # flag possible female mis-tagged male only if many hits + female name heuristic
            pass

    if not issues:
        print("No EN masculine pronouns in female profiles; no dosentə/professorə.")
    else:
        for row in issues:
            print(row)

    # Male profiles with she/her (possible mis-tag)
    SHE_PAT = re.compile(r"\b(She|she|Her|her)\b")
    print("\n--- Male catalogue rows with she/her in EN bio ---")
    for p in profiles:
        if p["say"] not in male_says:
            continue
        en = p.get("bio_html_en") or ""
        hits = SHE_PAT.findall(en)
        if hits:
            print(f"  say {p['say']:3} {p['name'][:40]:40} she/her count: {len(hits)}")


if __name__ == "__main__":
    main()

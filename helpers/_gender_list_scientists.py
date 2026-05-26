"""One-off: list scientist genders from names (+ bio when unambiguous)."""
import json
import re
from collections import Counter
from pathlib import Path

from _paths import ROOT

PROFILES_JSON = ROOT / "i18n" / "scientists-profiles.json"

# Explicit overrides (first name lowercased)
MALE_FIRST = {
    "asəf", "asef", "aytəkin", "aytekin", "elşad", "toğrul", "məsud", "mirzə",
    "rasim", "rauf", "yaşar", "bəxtiyar", "kamal", "murad", "qərib", "vəhid",
    "xaqani", "lev", "mark", "ilham", "rıza", "natiq", "seymur", "şəhriyar",
    "akif", "tofiq", "eldar", "əliheydər", "emil", "ismayıl", "kamran", "nizami",
    "suleyman", "vahid", "zahid", "azər", "elvin", "cavid", "əmirullah", "hacıəli",
    "ilkin", "ismixan", "mehdi", "mehmet", "oruc", "qafar", "ramin", "şahin",
    "saleh", "teymur", "varqa", "arif", "xəlil", "ağamalı", "agamali",
    "əhməd", "rövşən", "rovshan", "şuay", "elçin", "vəfa", "əhməd",
}

FEMALE_FIRST = {
    "cəmilə", "cemile", "sevinc", "sevda", "xədicə", "xedicə", "dinara",
    "aynur", "günel", "gunel", "reyhan", "aygül", "aygul", "səadət", "saadat",
    "zərifə", "zerife", "səbinə", "sebine", "sabina", "yulduz", "səidə", "seida",
    "arzu", "nigar", "afina", "maqbula", "maqbulə", "makbulə", "gulnar",
    "gulnara", "gulshan", "gülşən", "gulcin", "gülçin",
}

FEMALE_SURNAME_SUFFIXES = ("ova", "eva", "əva", "yeva", "iyeva")

FEMALE_EN = re.compile(
    r"\b(She |Her |she works|she teaches|she has edited|Under her supervision)\b",
    re.I,
)


def first_name(name: str) -> str:
    token = re.sub(r"[^a-zA-ZəğıöüşçƏĞİÖÜŞÇ\s-]", "", (name or "").lower()).split()
    return token[0] if token else ""


def from_name(name: str) -> str | None:
    fn = first_name(name)
    if fn in MALE_FIRST:
        return "male"
    if fn in FEMALE_FIRST:
        return "female"
    parts = re.sub(r"[^a-zA-ZəğıöüşçƏĞİÖÜŞÇ\s-]", "", (name or "").lower()).split()
    for part in parts[1:]:
        if any(part.endswith(suf) for suf in FEMALE_SURNAME_SUFFIXES):
            return "female"
    return None


def from_bio_female_only(en: str) -> bool:
    """True only when EN bio clearly uses feminine pronouns (no 'he')."""
    en = en or ""
    if not FEMALE_EN.search(en):
        return False
    if re.search(r"\b(He |His |he is|he was|he has|he teaches|he works)\b", en, re.I):
        return False
    return True


def main() -> None:
    profiles = json.loads(PROFILES_JSON.read_text(encoding="utf-8"))["profiles"]
    rows = []
    for p in sorted(profiles, key=lambda x: x.get("say", 0)):
        name = p.get("name", "")
        g = from_name(name) or from_name(p.get("name_en", ""))
        if not g and from_bio_female_only(p.get("bio_html_en", "")):
            g = "female"
        if not g:
            g = "male"  # default for remaining typical AZ male roster
            source = "default-male"
        else:
            source = "name" if from_name(name) else "bio"
        rows.append({"say": p["say"], "name": name, "name_en": p.get("name_en", name), "gender": g, "source": source})

    for r in rows:
        print(f"{r['say']:3}  {r['gender']:8}  {r['name']}")

    print("---")
    print(Counter(r["gender"] for r in rows))
    females = [r for r in rows if r["gender"] == "female"]
    print(f"Female count: {len(females)}")


if __name__ == "__main__":
    main()

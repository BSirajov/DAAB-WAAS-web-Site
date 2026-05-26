"""Fix masculine pronouns in female scientist profile bios (EN + AZ)."""
from __future__ import annotations

import json
import re

from _paths import ROOT

# Protect third-party masculine pronouns before bulk EN replace
EN_PROTECT_PHRASES = [
    "Antoni Van Noordt and his work",
]

# EN: word-boundary replacements (order: longer / capitalized first)
EN_REPLACEMENTS: list[tuple[str, str]] = [
    (r"\bHimself\b", "Herself"),
    (r"\bhimself\b", "herself"),
    (r"\bHis\b", "Her"),
    (r"\bhis\b", "her"),
    (r"\bHim\b", "Her"),
    (r"\bhim\b", "her"),
    (r"\bHe\b", "She"),
    (r"\bhe\b", "she"),
]

EN_ITS_FIXES: list[tuple[str, str]] = [
    (r"\bIts activities\b", "Her activities"),
    (r"\bIts H-index\b", "Her H-index"),
    (r"\bits H-index\b", "her H-index"),
    (r"\bIts main\b", "Her main"),
    (r"\bits main\b", "her main"),
    (r"\bIts activity\b", "Her activity"),
    (r"\bits activity\b", "her activity"),
]

EN_EXTRA: list[tuple[str, str]] = [
    (r"\bHe specializes\b", "She specializes"),
    (r"\bhe specializes\b", "she specializes"),
    (r"\bIn addition, it also\b", "In addition, she also"),
    (r"\bin addition, it also\b", "in addition, she also"),
    (r"\bThe company he works for\b", "The company she works for"),
    (r"\bthe company he works for\b", "the company she works for"),
]

# Per-say title / bio overrides (after automated pass)
PROFILE_OVERRIDES: dict[int, dict[str, str]] = {
    39: {
        "bio_html_en": (
            '<p class="bio bio-lead">She is the author of seven journal articles, two '
            "methodical works and one educational book. She held five seminars at Oman "
            "Royal Opera House and one seminar at Sultan Qaboos University. She is the "
            "developer of more than 20 programs, as well as the author and artistic director "
            "of about 20 different projects, competitions and concerts.</p>"
            '<p class="bio">She has spoken at the embassies of Japan, Turkey, France and '
            "Russia on many occasions and has been awarded letters of thanks and certificates "
            "for her activities. She took part in the implementation of the following two "
            "large-scale concert programs:</p>"
            '<p class="bio">• May 31, 2024 – a concert program organized for an audience of '
            'about 250 people called &quot;Cradle of Eastern Culture&quot; held in Shusha.</p>'
            '<p class="bio">• May 30, 2025 – a concert program dedicated to Oman–Azerbaijan '
            "friendship and organized for an audience of about 300 people.</p>"
            '<p class="bio">Articles about Dr. Saida Khalilova&#x27;s creativity and work have '
            "been published many times in influential media outlets in Oman.</p>"
        ),
    },
}

CATALOG_CINSI_FIXES: dict[int, str] = {}  # say -> cinsi overrides when catalogue is wrong
CATALOG_EMAIL_FIX = {39: "dr.saidakhalilova@gmail.com"}

TITLE_FIXES_EXTRA: dict[int, dict[str, str]] = {
    2: {
        "title_az": "Asistent Tədqiqat Professoru, Vaşinqton Universiteti (St. Louis)",
        "title_en": "Assistant Research Professor, Washington University (St. Louis)",
    },
    30: {
        "title_az": "DAAB İdarə Heyətinin üzvü, mətbuat katibi",
    },
}


def _protect_en(text: str) -> tuple[str, dict[str, str]]:
    tokens: dict[str, str] = {}
    for i, phrase in enumerate(EN_PROTECT_PHRASES):
        token = f"__PROTECT_{i}__"
        if phrase in text:
            text = text.replace(phrase, token)
            tokens[token] = phrase
    return text, tokens


def _unprotect_en(text: str, tokens: dict[str, str]) -> str:
    for token, phrase in tokens.items():
        text = text.replace(token, phrase)
    return text


def fix_en_bio(text: str) -> str:
    if not text:
        return text
    text, tokens = _protect_en(text)
    for pat, repl in EN_ITS_FIXES + EN_EXTRA + EN_REPLACEMENTS:
        text = re.sub(pat, repl, text)
    return _unprotect_en(text, tokens)


def fix_az_bio(text: str) -> str:
    if not text:
        return text
    text = re.sub(r"(?<=[.>])\s*o,", " O,", text)
    text = re.sub(r"^o,", "O,", text)
    return text


def load_catalog() -> list[dict]:
    raw = (ROOT / "js" / "scientists-catalog-data.js").read_text(encoding="utf-8")
    return json.loads(raw.split("=", 1)[1].strip().rstrip(";"))


def save_catalog(rows: list[dict]) -> None:
    path = ROOT / "js" / "scientists-catalog-data.js"
    body = json.dumps(rows, ensure_ascii=False, indent=2)
    path.write_text(f"window.SCIENTISTS_CATALOG_DATA = {body};\n", encoding="utf-8")


def main() -> None:
    data_path = ROOT / "i18n" / "scientists-profiles.json"
    doc = json.loads(data_path.read_text(encoding="utf-8"))
    profiles = doc["profiles"]

    raw = (ROOT / "js" / "scientists-catalog-data.js").read_text(encoding="utf-8")
    catalog = json.loads(raw.split("=", 1)[1].strip().rstrip(";"))
    female_says = {r["say"] for r in catalog if r.get("cinsi") == "qadın"}

    changed = 0
    for p in profiles:
        if p["say"] not in female_says:
            continue
        overrides = PROFILE_OVERRIDES.get(p["say"], {})
        en_old = p.get("bio_html_en") or ""
        az_old = p.get("bio_html_az") or ""
        en_new = overrides.get("bio_html_en") or fix_en_bio(en_old)
        az_new = fix_az_bio(az_old)
        if en_new != en_old:
            p["bio_html_en"] = en_new
            changed += 1
            print(f"EN fixed: say {p['say']} {p['name']}")
        if az_new != az_old:
            p["bio_html_az"] = az_new
            changed += 1
            print(f"AZ fixed: say {p['say']} {p['name']}")
        for key, val in TITLE_FIXES_EXTRA.get(p["say"], {}).items():
            if p.get(key) != val:
                p[key] = val
                changed += 1
                print(f"title fixed: say {p['say']} {key}")

    data_path.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"profiles.json field updates: {changed}")

    cat_changed = False
    for row in catalog:
        if row["say"] in CATALOG_CINSI_FIXES:
            new_val = CATALOG_CINSI_FIXES[row["say"]]
            if row.get("cinsi") != new_val:
                row["cinsi"] = new_val
                cat_changed = True
                print(f"catalog cinsi say {row['say']} -> {new_val}")
        if row["say"] in CATALOG_EMAIL_FIX:
            new_email = CATALOG_EMAIL_FIX[row["say"]]
            if row.get("email", "").lower() != new_email:
                row["email"] = new_email
                cat_changed = True
                print(f"catalog email say {row['say']} -> {new_email}")
    if cat_changed:
        save_catalog(catalog)


if __name__ == "__main__":
    main()

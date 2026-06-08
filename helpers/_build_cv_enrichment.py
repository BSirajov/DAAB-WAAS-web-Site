"""Match CV cards to az/scientists/list.html DATA by name; add email/ixtilas."""
from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path

from _paths import ROOT, AZ_SCIENTISTS_LIST, AZ_SCIENTISTS_PROFILES

AZ = AZ_SCIENTISTS_LIST
CV = AZ_SCIENTISTS_PROFILES

COUNTRY_CODE_TO_NAME = {
    "abs": "ABŞ",
    "de": "Almaniya",
    "at": "Avstriya",
    "uk": "Birləşmiş Krallıq",
    "kr": "Koreya",
    "ee": "Estoniya",
    "fr": "Fransa",
    "ge": "Gürcüstan",
    "il": "İsrail",
    "se": "İsveç",
    "it": "İtaliya",
    "ca": "Kanada",
    "mx": "Meksika",
    "eg": "Misir",
    "om": "Oman",
    "pl": "Polşa",
    "kz": "Qazaxıstan",
    "kg": "Qırğızıstan",
    "ru": "Rusiya Federasiyası",
    "sa": "Səudiyyə Ərəbistanı",
    "tr": "Türkiyə",
    "ua": "Ukrayna",
    "jp": "Yaponiya",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKC", s).upper().strip()
    s = re.sub(r"[^A-Z0-9ƏŞÇĞÖÜİ\s\-]", " ", s)
    s = re.sub(r"\s+", " ", s)
    for a, b in [("İ", "I"), ("Ə", "E"), ("Ş", "S"), ("Ç", "C"), ("Ğ", "G"), ("Ö", "O"), ("Ü", "U"), ("Q", "G")]:
        s = s.replace(a, b)
    return s.strip()


DISPLAY_ALIASES = {
    "AFI NA MEMMEDLI BARMANBAY": "Afina Barmanbay",
    "AFINA MEMMEDLI BARMANBAY": "Afina Barmanbay",
    "MEQBULE SEBZIYEVA": "Makbule Sabziyeva",
    "MEGBULE SEBZIYEVA": "Makbule Sabziyeva",
    "MEGBULE SEBZI YEVA": "Makbule Sabziyeva",
    "MEHDI GENCELI ISMAYILOV": "Mehdi Ismayilov (Gəncəli)",
    "GAFAR CAXMAGLI MEHDIYEV": "Qafar Mehdiyev (Çaxmaxçı)",
    "GAFAR CAXMAGLI MEHDI YEV": "Qafar Mehdiyev (Çaxmaxçı)",
}


def esc_attr(s: str) -> str:
    return s.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;")


def load_data() -> list[dict]:
    text = AZ.read_text(encoding="utf-8")
    m = re.search(r"const DATA = (\[.*?\]);", text, re.S)
    return json.loads(m.group(1))


def card_display_name(chunk: str) -> str:
    alt = re.search(r'alt="([^"]+)"', chunk)
    if alt:
        return alt.group(1).strip()
    m = re.search(r'class="card-name">([^<]+)', chunk)
    if m:
        return re.sub(r"<span[^>]*>.*", "", m.group(1), flags=re.S).strip()
    return ""


def find_row(by_norm: dict[str, dict], display: str, used: set[str]) -> dict | None:
    key = norm(display)
    if key in DISPLAY_ALIASES:
        display = DISPLAY_ALIASES[key]
        key = norm(display)
    if key in by_norm and key not in used:
        return by_norm[key]
    # try without middle initials (LEV V. EPPELBAUM -> LEV EPPELBAUM)
    parts = key.split()
    if len(parts) > 2:
        compact = " ".join([parts[0]] + [p for p in parts[1:] if len(p) > 1])
        if compact in by_norm and compact not in used:
            return by_norm[compact]
    best = None
    best_score = 0.0
    for k, row in by_norm.items():
        if k in used:
            continue
        score = SequenceMatcher(None, key, k).ratio()
        if score > best_score:
            best_score = score
            best = row
    if best_score >= 0.82:
        return best
    return None


def strip_existing_meta(chunk: str) -> str:
    chunk = re.sub(r'<div class="card-meta">.*?</div>', "", chunk, flags=re.S)
    chunk = re.sub(
        r'\s*data-email="[^"]*"\s*data-ixtilas="[^"]*"\s*data-degree="[^"]*"',
        "",
        chunk,
    )
    return chunk


def main() -> None:
    data = load_data()
    by_norm: dict[str, dict] = {}
    for row in data:
        by_norm[norm(row["ad_soyad"])] = row

    js_path = ROOT / "js" / "scientists-catalog-data.js"
    js_path.write_text(
        "window.SCIENTISTS_CATALOG_DATA = "
        + json.dumps(data, ensure_ascii=False, indent=2)
        + ";\n",
        encoding="utf-8",
    )

    cv_text = CV.read_text(encoding="utf-8")
    chunks = re.split(r'(?=<div class="card")', cv_text)
    out = [chunks[0]]
    used_keys: set[str] = set()
    matched = 0

    for chunk in chunks[1:]:
        chunk = strip_existing_meta(chunk)
        display = card_display_name(chunk)
        row = find_row(by_norm, display, used_keys)
        if not row:
            out.append(chunk)
            print("WARN no match:", display)
            continue
        used_keys.add(norm(row["ad_soyad"]))
        matched += 1

        cm = re.search(r'data-country="([^"]+)" data-search="([^"]*)"', chunk)
        if not cm:
            out.append(chunk)
            continue
        country = cm.group(1)
        email = (row.get("email") or "").strip()
        ixt = (row.get("ixtilas") or "").strip()
        deg = (row.get("elmi_derece") or "").strip()
        hay = " ".join(
            filter(
                None,
                [
                    cm.group(2),
                    email.lower(),
                    ixt.lower(),
                    row.get("ad_soyad", "").lower(),
                    row.get("yasadigi_olke", "").lower(),
                    deg.lower(),
                    COUNTRY_CODE_TO_NAME.get(country, "").lower(),
                ],
            )
        )
        hay = re.sub(r"\s+", " ", hay).strip()
        chunk = re.sub(
            r'data-country="[^"]+" data-search="[^"]*"',
            (
                f'data-country="{country}" data-search="{esc_attr(hay)}" '
                f'data-email="{esc_attr(email)}" data-ixtilas="{esc_attr(ixt)}" '
                f'data-degree="{esc_attr(deg)}"'
            ),
            chunk,
            count=1,
        )
        title_m = re.search(r'<p class="card-title">.*?</p>', chunk, re.S)
        if title_m:
            if email:
                em = f'<a class="card-email" href="mailto:{esc_attr(email)}">{esc_attr(email)}</a>'
            else:
                em = '<span class="card-email card-email--empty">—</span>'
            meta = (
                '<div class="card-meta">'
                '<span class="card-meta-label">İxtisas</span>'
                f'<span class="card-meta-ixtilas">{esc_attr(ixt) or "—"}</span>'
                '<span class="card-meta-label">E-poçt</span>'
                f"{em}"
                "</div>"
            )
            chunk = chunk.replace(title_m.group(0), title_m.group(0) + meta, 1)
        out.append(chunk)

    CV.write_text("".join(out), encoding="utf-8")
    print(f"Matched {matched}/83 cards, wrote {js_path.name}")


if __name__ == "__main__":
    main()

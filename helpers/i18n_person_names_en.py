"""Latin personal-name forms for English pages."""
from __future__ import annotations

import json
import re
import unicodedata
from difflib import SequenceMatcher
from functools import lru_cache
from pathlib import Path

try:
    from _paths import ROOT
except ImportError:
    from helpers._paths import ROOT  # type: ignore

PHOTOS = ROOT / "images" / "scientists-photos"
DATA_JS = ROOT / "js" / "scientists-catalog-data.js"
CACHE_PATH = ROOT / "i18n" / "person-names-en.json"

AZ_CHARS = str.maketrans(
    {
        "ə": "e",
        "Ə": "E",
        "ı": "i",
        "I": "I",
        "ö": "o",
        "Ö": "O",
        "ü": "u",
        "Ü": "U",
        "ş": "s",
        "Ş": "S",
        "ç": "c",
        "Ç": "C",
        "ğ": "g",
        "Ğ": "G",
        "İ": "I",
        "q": "g",
        "Q": "G",
        "x": "kh",
        "X": "Kh",
    }
)

# Established Latin spellings that differ from filename heuristics.
PERSON_NAME_OVERRIDES: dict[str, str] = {
    "Məsud Əfəndiyev": "Messoud Efendiyev",
    "MƏSUD ƏFƏNDİYEV": "MESSOUD EFENDIYEV",
    "Prof. Dr. Məsud Əfəndiyev": "Prof. Dr. Messoud Efendiyev",
    "Məsud Əfəndiyev, Prof. Dr.": "Messoud Efendiyev, Prof. Dr.",
    "Məsud Əfəndiyev — NDU": "Messoud Efendiyev — NDU",
    "Bəxtiyar Siracov": "Bakhtiyar Sirajov",
    "BƏXTİYAR SIRACOV": "BAKHTIYAR SIRAJOV",
    "Bəxtiyar Siracov, Dr.": "Bakhtiyar Sirajov, Dr.",
    "Seymur Nəsirov": "Seymur Nasirov",
    "Seymur Nəsirov, Dr.": "Seymur Nasirov, Dr.",
    "Səadət Kərimi": "Saadat Karimi",
    "Səadət Kərimi, Prof. Dr.": "Saadat Karimi, Prof. Dr.",
    "Toğrul İsmayıl": "Togrul Ismayil",
    "Toğrul İsmayıl, Prof. Dr.": "Togrul Ismayil, Prof. Dr.",
    "Toğrul Kərimov": "Togrul Karimov",
    "Toğrul Kərimov, Dr.": "Togrul Karimov, Dr.",
    "Yulduz Rəhimov": "Yulduz Rahimov",
    "Yulduz Rəhimov, Prof. Dr.": "Yulduz Rahimov, Prof. Dr.",
    "Emil Əhmədov": "Emil Ahmadov",
    "Emil Əhmədov, Prof. Dr.": "Emil Ahmadov, Prof. Dr.",
    "Nigar Məsumova": "Nigar Masimova",
    "Nigar Məsumova, Dr.": "Nigar Masimova, Dr.",
    "Sevinc Məmmədova": "Sevinj Mammadova",
    "Sevinc Məmmədova, Dr.": "Sevinj Mammadova, Dr.",
    "Mehdi İsmayilov (Gəncəli)": "Mehdi Ismayilov (Gancali)",
    "MEHDI İSMAYILOV (GƏNCƏLİ)": "MEHDI ISMAYILOV (GANCALI)",
    "Qafar Mehdiyev (Çaxmaxçı)": "Gafar Mehdiyev (Chakhmatchi)",
    "QAFAR MEHDİYEV (ÇAXMAXÇİ)": "GAFAR MEHDIYEV (CHAKHMATCHI)",
    "Məqbulə Səbziyeva": "Makbule Sabziyeva",
    "MƏQBULƏ SƏBZİYEVA": "MAKBULE SABZIYEVA",
    "Cəmilə Cavadova-Spitzberg": "Jamila Javadova-Spitzberg",
    "CƏMİLƏ CAVADOVA-SPİTZBERG": "JAMILA JAVADOVA-SPITZBERG",
    "Riza Moridi": "Reza Moridi",
    "RİZA MORİDİ": "REZA MORIDI",
    "Mark Vilen Applebaum": "Mark Applebaum",
    "MARK VİLEN APPLEBAUM": "MARK APPLEBAUM",
    "Lev V. Eppelbaum": "Lev V. Eppelbaum",
    "Asəf Salamov": "Asaf Salamov",
    "ASƏF SALAMOV": "ASAF SALAMOV",
    "Aytəkin Hüseynli": "Aytekin Huseynli",
    "AYTƏKİN HÜSEYNLİ": "AYTEKIN HUSEYNLI",
    "Elşad Allahyarov": "Elshad Allahyarov",
    "ELŞAD ALLAHYAROV": "ELSHAD ALLAHYAROV",
    "Şuay Abdullayev": "Shuay Abdullayev",
    "ŞUAY ABDULLAYEV": "SHUAY ABDULLAYEV",
    "Toğrul Talişinski": "Togrul Talishinski",
    "TOĞRUL TALİŞİNSKİ": "TOGRUL TALISHINSKI",
    "Xədicə Zeynalova": "Khadija Zeynalova",
    "Xıdır Kazımov": "Khidir Kazimov",
    "Cahid Kazımov": "Jahid Kazimov",
    "Emin Rüstəmov": "Emin Rustamov",
    "Pərviz Məmmədzadə": "Parviz Mammadzade",
    "Rüfət Sarabin": "Rufat Sarabin",
    "Ülkər Səttarova": "Ulker Sattarova",
    "Vəsilə Zeynalova": "Vasila Zeynalova",
    "Aqşin Əliyev": "Aghshin Aliyev",
    "Əli Əsgərov": "Ali Asgarov",
    "Əmirullah Mehmetov": "Amirullah Mehmetov",
    "Əsgər Ələkbərov": "Asgar Alekberov",
    "Heydər İmanov": "Heydar Imanov",
    "Mahmud Hacıxəlilov": "Mahmud Hajikhalilov",
    "Mehdi İsmayılov": "Mehdi Ismayilov",
    "Mübariz Qarayev": "Mubariz Garayev",
    "Ramin Sadık": "Ramin Sadig",
    "Rövşən İbrahimov": "Rovshan Ibrahimov",
    "Seymur Nəsirov": "Seymur Nasirov",
    "Toğrul İsmayıl": "Togrul Ismayil",
    "Vüqar İmanbəyli": "Vugar Imanbeyli",
    "Xaqani Qayıblı": "Khagani Gayibli",
    "Xəlil Kələntər": "Khalil Kelenter",
    "Zaur Sadıqbəyli": "Zaur Sadigbeyli",
    "Rasim Cənnətəliyev": "Rasim Jannataliyev",
    "İsmayıl Əliyev": "Ismayil Aliyev",
    "İlkın Gulusoy": "Ilkin Gulusoy",
    "İsmixan Bayramov": "Ismikhan Bayramov",
    "İlham Axundov": "Ilham Akhundov",
    "İsmayıl Əliyev": "Ismayil Aliyev",
}


def norm_key(name: str) -> str:
    s = unicodedata.normalize("NFKC", name).upper().strip()
    s = re.sub(r"[^A-Z0-9ƏŞÇĞÖÜİ\s\-().]", " ", s)
    s = re.sub(r"\s+", " ", s)
    for a, b in [("İ", "I"), ("Ə", "E"), ("Ş", "S"), ("Ç", "C"), ("Ğ", "G"), ("Ö", "O"), ("Ü", "U"), ("Q", "G")]:
        s = s.replace(a, b)
    return s.strip()


def photo_stem_to_latin(stem: str) -> str:
    stem = re.sub(r"\s+\d+$", "", stem.strip())
    parts = [p for p in stem.split("-") if p]
    if len(parts) == 3 and len(parts[1]) == 1:
        return f"{parts[0].title()} {parts[1].upper()}. {parts[2].title()}"
    return " ".join(p.title() for p in parts)


def transliterate_az_name(name: str) -> str:
    if not name:
        return name
    if name in PERSON_NAME_OVERRIDES:
        return PERSON_NAME_OVERRIDES[name]
    out = name.translate(AZ_CHARS)
    out = re.sub(r"\(\s*Gəncəli\s*\)", "(Gancali)", out, flags=re.I)
    out = re.sub(r"\(\s*Çaxmaxçı\s*\)", "(Chakhmatchi)", out, flags=re.I)
    return out


def az_upper_name_latin(name: str) -> str:
    base = latin_display_name(name)
    return unicodedata.normalize("NFKC", base).upper()


def latin_display_name(name: str) -> str:
    name = (name or "").strip()
    if not name:
        return name
    if name in PERSON_NAME_OVERRIDES:
        return PERSON_NAME_OVERRIDES[name]
    return transliterate_az_name(name)


def _load_catalog_rows() -> list[dict]:
    text = DATA_JS.read_text(encoding="utf-8")
    return json.loads(text.split("=", 1)[1].strip().rstrip(";"))


def _photo_maps() -> tuple[dict[str, str], dict[str, str]]:
    files = {
        p.stem: p.name
        for p in PHOTOS.glob("*")
        if p.suffix.lower() in (".png", ".jpg", ".jpeg")
    }
    by_norm = {norm_key(stem.replace("-", " ")): stem for stem in files}
    return files, by_norm


def _latin_from_photo(az_name: str, files: dict[str, str], by_norm: dict[str, str]) -> str | None:
    key = norm_key(az_name)
    stem = by_norm.get(key)
    if not stem:
        best_stem = None
        best = 0.0
        for candidate, s in by_norm.items():
            score = SequenceMatcher(None, key, candidate).ratio()
            if score > best:
                best = score
                best_stem = s
        if best >= 0.82:
            stem = best_stem
    if stem:
        return photo_stem_to_latin(stem)
    return None


def build_name_map() -> dict[str, str]:
    mapping: dict[str, str] = dict(PERSON_NAME_OVERRIDES)
    files, by_norm = _photo_maps()

    for row in _load_catalog_rows():
        az = (row.get("ad_soyad") or "").strip()
        if not az or re.search(r"[А-Яа-яЁё]", az):
            continue
        latin = _latin_from_photo(az, files, by_norm) or transliterate_az_name(az)
        mapping[az] = latin
        mapping[az.upper()] = latin.upper()
        if "-" in az:
            mapping[re.sub(r"\s+", " ", az)] = latin

    # Common title suffixes on board cards.
    for az, latin in list(mapping.items()):
        if "," in az:
            continue
        for suffix in (", Prof. Dr.", ", Dr.", ", Prof.", " — NDU"):
            if az + suffix not in mapping:
                mapping[az + suffix] = latin + suffix

    return mapping


def build_replacement_pairs() -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    seen: set[str] = set()
    for az, latin in build_name_map().items():
        if az == latin or not az.strip() or az in seen:
            continue
        if not re.search(r"[əıöüşçğƏİÖÜŞÇĞ]", az):
            continue
        seen.add(az)
        pairs.append((az, latin))
    pairs.sort(key=lambda item: len(item[0]), reverse=True)
    return pairs


@lru_cache(maxsize=1)
def replacement_pairs() -> tuple[tuple[str, str], ...]:
    if CACHE_PATH.exists():
        data = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
        pairs = [(k, v) for k, v in data.get("names", {}).items() if k != v]
        pairs.sort(key=lambda item: len(item[0]), reverse=True)
        return tuple(pairs)
    return tuple(build_replacement_pairs())


def write_cache() -> None:
    names = build_name_map()
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    CACHE_PATH.write_text(
        json.dumps({"version": 1, "names": names}, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def apply_person_name_latin(html: str) -> str:
    for az, latin in replacement_pairs():
        html = html.replace(az, latin)
    return html

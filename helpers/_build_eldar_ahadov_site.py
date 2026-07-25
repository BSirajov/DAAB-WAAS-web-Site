#!/usr/bin/env python3
"""Build Eldar Əhədov literary pages (AZ/EN) from cached Google Sites HTML.

    python helpers/_build_eldar_ahadov_site.py
    python helpers/_build_eldar_ahadov_site.py --download-images

Source HTML lives in helpers/_eldar_ahadov_source/ (copied from the scrape).
Images are written to az/scientists/eldar-ahadov-media-thumbnails/.
"""
from __future__ import annotations

import argparse
import copy
import html
import http.cookiejar
import io
import json
import re
import shutil
import urllib.request
from pathlib import Path

from bs4 import BeautifulSoup, Tag
from PIL import Image

from _eldar_ahadov_en_strings import (
    EN_CANONICAL_H2,
    EN_NAV_TITLES,
    EN_OZUM_AWARDS_ITEMS,
    EN_OZUM_AWARDS_TITLE,
    EN_OZUM_BERENGARTEN,
    EN_OZUM_BIO_PARAS,
    TRANSLATIONS,
)
from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

SOURCE_DIR = ROOT / "helpers" / "_eldar_ahadov_source"
THUMB_DIR = ROOT / "az" / "scientists" / "eldar-ahadov-media-thumbnails"
ELDAR_CSS = "daab-eldar-ahadov.css"
ELDAR_CSS_VER = int(STYLE_VERSIONS.get(ELDAR_CSS, 1))

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

LIVE_URLS = {
    "ozum": "https://sites.google.com/view/eldar-ahadov/%C3%B6z%C3%BCm-haqq%C4%B1nda",
    "poeziya": "https://sites.google.com/view/eldar-ahadov/poeziya",
    "poetik": "https://sites.google.com/view/eldar-ahadov/poetik-dastanlar-v%C9%99-%C9%99fsan%C9%99l%C9%99r",
    "bedii": "https://sites.google.com/view/eldar-ahadov/b%C9%99dii-n%C9%99sr",
    "esse": "https://sites.google.com/view/eldar-ahadov/esse",
}

# Shared Google Sites header logo — skip as content image.
SKIP_IMG_MARKERS = (
    "AG8ngQVnpiLlGcrr3_u6HCtPAYn1VvUPatMZTW2WJBK7yQOaMkECv_cSyFHRH4sJocaXs0JBf_Qey8m4C69Yn",
)

MIN_IMG_BYTES = 4_000
MIN_IMG_EDGE = 80

PAGES = [
    {
        "key": "ozum",
        "source": "ozum.html",
        "slug": "eldar-ahadov",
        "page_id": "eldar-ahadov",
        "nav_title": "Özüm haqqında",
        "img_prefix": "ozum",
        "canonical_h2": [],
        "float_first_img": "portrait",
        "is_poetry": False,
    },
    {
        "key": "poeziya",
        "source": "poeziya.html",
        "slug": "eldar-ahadov-poeziya",
        "page_id": "eldar-ahadov-poeziya",
        "nav_title": "Poeziya",
        "img_prefix": "poeziya",
        "canonical_h2": [
            "AGAC",
            "ANLARSAN",
            "AZAN",
            "BİR DƏ O YERƏ QAYIDARAM MƏN",
            "BİR GÜN SƏNDƏN HAMI DÖNSƏ",
            "GƏNCLİK VƏ QOCALIQ",
            "HƏKİM ÇAĞIRMAQ",
            "İNSAN OLAQ",
            "İŞIĞIN KÖLGƏSİ YOXDUR",
            "KAĞIZDAN ATA",
            "MƏNİ TƏRK ELƏMƏ",
            "MƏNİM ŞƏHİDLƏRİM",
            "MÖCÜZƏ",
            "QAR YAĞIR",
            "SƏNDƏN SAVAYI",
            "XOŞ SÖZ",
        ],
        "float_first_img": "figure",
        "is_poetry": True,
    },
    {
        "key": "poetik",
        "source": "poetik.html",
        "slug": "eldar-ahadov-poetik-dastanlar",
        "page_id": "eldar-ahadov-poetik-dastanlar",
        "nav_title": "Poetik dastanlar və əfsanələr",
        "img_prefix": "poetik",
        "canonical_h2": [
            "AZƏRBAYCAN DASTANI - XARI BÜLBÜL",
            "XARI BÜLBÜL DASTANINDA QEYD OLUNAN ADLARIN GÖSTƏRİCİSİ",
        ],
        "float_first_img": "figure",
        "is_poetry": True,
    },
    {
        "key": "bedii",
        "source": "bedii.html",
        "slug": "eldar-ahadov-bedii-nesr",
        "page_id": "eldar-ahadov-bedii-nesr",
        "nav_title": "Bədii nəsr",
        "img_prefix": "bedii",
        "canonical_h2": [
            "VƏTƏN HİSSLƏRİ",
            "XƏDİCƏ",
            "CIDIR DÜZÜ",
            "NUR",
            "FISDIQ AĞACI",
            "HARAM",
            "MƏN KİMDƏN ARTIĞAM Kİ ...",
            "OĞLU",
            "SİZİNLƏ VİDALAŞMIRAM",
            "ANAMIN DOLMASI",
        ],
        "float_first_img": None,
        "is_poetry": False,
    },
    {
        "key": "esse",
        "source": "esse.html",
        "slug": "eldar-ahadov-esse",
        "page_id": "eldar-ahadov-esse",
        "nav_title": "Esse",
        "img_prefix": "esse",
        "canonical_h2": ["MƏRHƏMƏT ABİDƏSİ"],
        "float_first_img": "figure",
        "is_poetry": False,
    },
]

NAV_ITEMS = [(p["slug"], p["nav_title"]) for p in PAGES]

# Authoritative “Özüm haqqında” bio (replaces scraped Google Sites paragraphs).
OZUM_BIO_PARAS = [
    "Eldar Əlixas oğlu Əhədov",
    (
        "19 iyul 1960-cı ildə Bakıda anadan olub, Sankt-Peterburq Mədən Universitetini bitirib "
        "və TNK-BP (Tümen Neft Şirkəti - British Petroleum) birgə müəssisəsində, daha sonra isə "
        "Rosneft-də baş mütəxəssis vəzifəsində çalışıb."
    ),
    (
        "Arktika və Sibirin səyyahı və tədqiqatçısı olan o, azərbaycan, ingilis, ispan, italyan, "
        "çin, rus və serb dillərində nəşr olunmuş 110 kitabın — bədii ədəbiyyat, şeir, tədqiqat "
        "və elmi məqalələrin — müəllifidir. Onun kitabları Azərbaycan, Misir, Hindistan, Kanada, "
        "Çin, Meksika, Rusiya, Serbiya, ABŞ və Türkiyədə nəşr olunub. O, Azərbaycan Yazıçılar "
        "Birliyinin fəxri üzvü (2021), Beynəlxalq Ədəbiyyat, İncəsənət, Mədəniyyət və Sosial "
        "Elmlər Akademiyasının akademiki (2025, Özbəkistan), Rusiya Yazıçılar Birliyinin üzvü "
        "(2000), Rusiya Yazıçılar Birliyinin Krasnoyarsk bölməsinin idarə heyətinin üzvü, "
        "Rusiya Milli Coğrafiya Cəmiyyətinin üzvü (2016), PEN International-ın üzvü, Dünya "
        "Xalqları Assambleyası Ədəbi Şurasının həmsədri (2020), Dünya Yazıçılar Təşkilatının "
        "Koordinasiya Şurasının rəhbəri (2024), Rusiya Coğrafiya Cəmiyyətinin Krasnoyarsk "
        "bölməsinin Toponimiya Komissiyasının sədri (2024), \"Reader's Choice\" jurnalının "
        "icraçı redaktorudur (Mumbay, Hindistan, 2024-2026)."
    ),
]


def apply_ozum_bio_override(blocks: list[dict], lang: str = "az") -> list[dict]:
    """Replace the opening bio paragraphs with the curated text."""
    paras = EN_OZUM_BIO_PARAS if lang == "en" else OZUM_BIO_PARAS
    name_keys = {
        _title_key(OZUM_BIO_PARAS[0]),
        _title_key(EN_OZUM_BIO_PARAS[0]),
    }
    for i, b in enumerate(blocks):
        if b.get("kind") != "p" or _title_key(b.get("text", "")) not in name_keys:
            continue
        # Replace name + the following two scraped bio paragraphs.
        end = i + 1
        while end < len(blocks) and blocks[end].get("kind") == "p" and end < i + 3:
            end += 1
        replacement = [{"kind": "p", "text": t} for t in paras]
        return blocks[:i] + replacement + blocks[end:]
    # If name line missing, prepend after first figure when present.
    insert_at = 0
    for i, b in enumerate(blocks):
        if b.get("kind") == "figure":
            insert_at = i + 1
            break
    replacement = [{"kind": "p", "text": t} for t in paras]
    return blocks[:insert_at] + replacement + blocks[insert_at:]


OZUM_AWARDS_TITLE = "ƏN ƏHƏMİYYƏTLİ MÜKAFATLAR"
OZUM_AWARDS_ITEMS = [
    'Dünya Yazıçılar Təşkilatının "Dünya ədəbiyyatının inkişafına verdiyi töhfəyə görə" Gümüş Medalı (2024, Abuja, Nigeriya);',
    "Naji Naaman Beynəlxalq Mükafatı Laureatı (2024, Livan);",
    '"Xarici dilə əsaslanan əsərlərin yaradılmasında milli kimliyin qorunması" kateqoriyasında Avrasiya Ədəbiyyat Festivalının Gümüş Medalı (2019, Bakı, Azərbaycan);',
    "Ümumrusiya Ədəbiyyat Müsabiqəsi və Festivalının Gümüş Medalı (2019, Tümen, Rusiya);",
    '"Sülh naminə" beynəlxalq onlayn müsabiqəsinin Poeziya kateqoriyasında Birinci Mükafat - Sənətdə Xeyriyyəçilik (2013, Moskva);',
    '"Sülh naminə" beynəlxalq onlayn müsabiqəsinin Nəsr kateqoriyasında İkinci Mükafat - Sənətdə Xeyriyyəçilik (2012, Moskva);',
    "Krasnoyarsk diyarı qubernatorunun mədəniyyət sahəsində fərdi qrantı (2008, Krasnoyarsk);",
    'Yamalo-Nenets Muxtar Dairəsi Qubernatorunun "Bədii və qeyri-bədii əsərlər" kateqoriyasında ədəbi pul mükafatı (2017, Salexard, Yamalo-Nenets Muxtar Dairəsi);',
    'Yamalo-Nenets Muxtar Dairəsinin Qanunvericilik Məclisinin "Yamalo-Nenets Muxtar Dairəsinin mədəni inkişafına verdiyi töhfəyə görə" təşəkkür məktubu (2022, Salexard);',
    'Krasnoyarsk diyarı qubernatorunun "Vicdanlı işinə, yüksək peşəkarlığına və Krasnoyarsk diyarında mədəniyyətin inkişafına verdiyi töhfəyə görə" təşəkkür məktubu (2025);',
    'Krasnoyarsk diyarı Mədəniyyət Nazirliyinin "Vicdanlı işinə və Krasnoyarsk diyarında mədəniyyətin inkişafına verdiyi şəxsi töhfəyə görə" fəxri fərmanı (2020);',
    '"Məhəmməd Peyğəmbər - aləmlərə mərhəmət" müsabiqəsində ikinci yerə görə Rusiya Müftilər Şurasının pul mükafatı (2011, Moskva);',
    "ZA-ZA Verlag Nəşriyyatının Beynəlxalq Ədəbi Müsabiqəsinin Esse kateqoriyasında qalib diplomu (2018, Düsseldorf, Almaniya);",
    "İtalyan dilində Vincenzo Padula Beynəlxalq Ədəbi Müsabiqəsinin qalibi diplomu (2022, Saracena, Kalabriya bölgəsi, İtaliya);",
    'Rusiya Mədən Mütəxəssisləri Birliyinin "Geodeziyanın inkişafına, yeraltı sərvətlərin səmərəli istifadəsinin və qorunmasının təmin edilməsinə əhəmiyyətli töhfəsinə görə" gümüş nişanı (Moskva, 4 may 2016-cı il tarixli 07/08 nömrəli əmr);',
    'Tümen regional geodeziya mərkəzinin "Rusiyada Geodeziya və Kartoqrafiya Xidmətinin 100 ili" medalı (19 mart 2019-cu il, Tümen);',
    'Beynəlxalq İctimai Diplomatiya Elit Birliyinin "Rusiyanın və Türk Dünyasının Görkəmli Yazıçısı" medalı (2020, Qazaxıstan);',
    'Sultan Baybars "Beynəlxalq Ədəbi Hərəkata Görkəmli Xidmətinə görə" medalı (2024, Qazaxıstan);',
    "2007-ci il Rusiyanın Gümüş Qələmi Müsabiqəsinin qalibinin gümüş nişanı.",
]


def apply_ozum_awards_override(blocks: list[dict], lang: str = "az") -> list[dict]:
    """Replace the awards heading + list with the curated awards section."""
    title = EN_OZUM_AWARDS_TITLE if lang == "en" else OZUM_AWARDS_TITLE
    items = EN_OZUM_AWARDS_ITEMS if lang == "en" else OZUM_AWARDS_ITEMS
    # Keep AZ-based anchors stable across languages.
    awards_anchor = slugify_anchor(OZUM_AWARDS_TITLE)
    awards_keys = {
        _title_key("ƏN ƏHƏMİYYƏTLİ MÜKAFATLARIM"),
        _title_key(OZUM_AWARDS_TITLE),
        _title_key(EN_OZUM_AWARDS_TITLE),
    }
    for i, b in enumerate(blocks):
        if b.get("kind") != "h2" or _title_key(b.get("text", "")) not in awards_keys:
            continue
        end = i + 1
        if end < len(blocks) and blocks[end].get("kind") in ("ul", "analysis_ul"):
            end += 1
        replacement = [
            {
                "kind": "h2",
                "text": title,
                "anchor": awards_anchor,
            },
            {"kind": "ul", "items": list(items)},
        ]
        return blocks[:i] + replacement + blocks[end:]
    return blocks


def _ozum_block_text(b: dict) -> str:
    if b.get("kind") == "ext":
        return f"{b.get('text', '')} {b.get('href', '')}"
    return b.get("text", "") or ""


def apply_ozum_strip_berengarten(blocks: list[dict]) -> list[dict]:
    """Remove the Richard Berengarten tribute (AZ/EN/RU) after the awards list."""
    markers = (
        "rus dilində yazan görkəmli",
        "outstanding azerbaijani poet",
        "prominent azerbaijani poet",
        "эльдар ахадов",
        "təxəyyülpərəst",
        "riçard berengarten",
        "richard berengarten",
        "ричард беренгартен",
        "berengarten",
        "imaginationalist",
        "имажинационалист",
        "visionary",
        "----------------",
    )
    start = None
    for i, b in enumerate(blocks):
        if b.get("kind") not in ("p", "ext", "credit"):
            continue
        key = _ozum_block_text(b).casefold()
        if any(m in key for m in markers):
            start = i
            break
    if start is None:
        return blocks
    # Drop tribute through the end; keep any trailing figures before start only.
    return blocks[:start]


OZUM_BERENGARTEN_AZ = (
    "Eldar Əhədov - rus dilində yazan görkəmli Azərbaycan şairidir. Əhədov çeşidli "
    "simaları özündə ehtiva edir. O, həm alim, həm geoloq, həm Arktika tədqiqatçısı, "
    "həm qazmaçı, həm dilçi, həm tənqidçi, həm maarifçi və həm də müəllimdir. Şair həm "
    "ətrafımızda, həm də daxilimizdə olan fiziki kainatı tərənnüm etməklə yanaşı, eyni "
    "anda həm sonsuz, həm də mikroskopik dünyamızın qarşımıza qoyduğu sirli metafizik "
    "məsələləri araşdırmaqla məşğul olur. Şairin ruhu ehtiraslı intellektual axtarış, "
    "şəfqət və səxavətin vəhdətindən ibarətdir. Onun şeirləri əzab və sevinc hissləri "
    "aşılamaqla bərabər, ilk növbədə ümid saçması ilə səciyyələnir. Bu cəhətlərinə görə, "
    "Əhədov yalnız müasir dövrümüzün nümunəvi bir insanı deyil, həm də dövrümüz və "
    "gələcəyimiz üçün bir örnəkdir. O, təkcə beynəlmiləlçi deyil, həm də təxəyyülpərəstdir."
)


def apply_ozum_append_berengarten(blocks: list[dict], lang: str = "az") -> list[dict]:
    """Append the curated Berengarten tribute with link + date below."""
    if lang == "en":
        quote, link_label, date = EN_OZUM_BERENGARTEN
    else:
        quote, link_label, date = (
            OZUM_BERENGARTEN_AZ,
            "Riçard Berengarten",
            "Kembric, İyun 2020",
        )
    return blocks + [
        {"kind": "p", "text": quote},
        {
            "kind": "ext",
            "href": "https://en.wikipedia.org/wiki/Richard_Berengarten",
            "text": link_label,
        },
        {"kind": "credit", "text": date},
    ]


STRINGS = {
    "az": {
        "lang": "az",
        "locale": "az_AZ",
        "skip": "Məzmuna keç",
        "nav_home_title": "Ana səhifə",
        "nav_home_aria": "DAAB ana səhifə",
        "brand": "Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi",
        "brand_menu_aria": "Əsas naviqasiya",
        "menu_open": "Menyunu aç",
        "crumb_home": "Ana səhifə",
        "crumb_scientists": "Alimlərimiz",
        "crumb_aria": "Səhifə yolu",
        "author": "Eldar Əhədov",
        "section_nav_aria": "Ədəbi bölmələr",
        "panel_title": "Bu səhifə haqqında",
        "footer_org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "footer_contact": "Əlaqə",
        "footer_addr": "Ünvan",
        "footer_lead_h": "Rəhbərlik",
        "footer_addr_body": (
            "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>"
            "Kadıköy, İstanbul, Türkiyə"
        ),
        "footer_lead_body": (
            "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>"
            "DAAB İdarə Heyətinin Sədri<br/>"
            "Almaniya — James D. Murray mükafatlı professoru"
        ),
        "footer_rights": "© 2026 DAAB — Bütün hüquqlar qorunur",
        "meta": {
            "eldar-ahadov": (
                "Özüm haqqında",
                "Eldar Əhədovun bioqrafiyası, mükafatları və Riçard Berengartenin rəyi.",
                "Yazıçı və şair Eldar Əhədov — bioqrafiya və mükafatlar",
            ),
            "eldar-ahadov-poeziya": (
                "Poeziya",
                "Eldar Əhədovun şeirləri, təsvir və şeir təhlilləri ilə.",
                "Eldar Əhədov — poeziya toplusu",
            ),
            "eldar-ahadov-poetik-dastanlar": (
                "Poetik dastanlar və əfsanələr",
                "Eldar Əhədovun «Xarı bülbül» dastanı və adlar göstəricisi.",
                "Poetik dastanlar və əfsanələr",
            ),
            "eldar-ahadov-bedii-nesr": (
                "Bədii nəsr",
                "Eldar Əhədovun bədii nəsr əsərləri və video materiallar.",
                "Bədii nəsr hekayələri",
            ),
            "eldar-ahadov-esse": (
                "Esse",
                "Eldar Əhədovun esse yazıları.",
                "Esse — Mərhəmət abidəsi",
            ),
        },
    },
    "en": {
        "lang": "en",
        "locale": "en_US",
        "skip": "Skip to content",
        "nav_home_title": "Home",
        "nav_home_aria": "WAAS home",
        "brand": "World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists",
        "brand_menu_aria": "Primary navigation",
        "menu_open": "Open menu",
        "crumb_home": "Home",
        "crumb_scientists": "Scientists",
        "crumb_aria": "Breadcrumb",
        "author": "Eldar Ahadov",
        "section_nav_aria": "Literary sections",
        "panel_title": "About this page",
        "footer_org": "World Association of Azerbaijani Scientists",
        "footer_contact": "Contact",
        "footer_addr": "Address",
        "footer_lead_h": "Leadership",
        "footer_addr_body": (
            "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>"
            "Kadıköy, İstanbul, Türkiye"
        ),
        "footer_lead_body": (
            "<strong>Prof. Dr. Messoud Efendiyev</strong><br/>"
            "Chair of the WAAS Executive Board<br/>"
            "Germany — James D. Murray Distinguished Professor"
        ),
        "footer_rights": "© 2026 WAAS — All Rights Reserved",
        "meta": {
            "eldar-ahadov": (
                "About me",
                "Biography, awards, and Richard Berengarten’s tribute to Eldar Ahadov.",
                "Writer and poet Eldar Ahadov — biography and awards",
            ),
            "eldar-ahadov-poeziya": (
                "Poetry",
                "Poems by Eldar Ahadov with illustration and poem analyses. Verse remains in Azerbaijani.",
                "Eldar Ahadov — poetry collection",
            ),
            "eldar-ahadov-poetik-dastanlar": (
                "Poetic epics and legends",
                "Eldar Ahadov’s “Khari Bulbul” epic and name index. Epic verse remains in Azerbaijani.",
                "Poetic epics and legends",
            ),
            "eldar-ahadov-bedii-nesr": (
                "Literary prose",
                "Prose works by Eldar Ahadov with video links.",
                "Literary prose stories",
            ),
            "eldar-ahadov-esse": (
                "Essay",
                "Essays by Eldar Ahadov.",
                "Essay — Monument of Mercy",
            ),
        },
    },
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def v(name: str, mapping: dict) -> int:
    return int(mapping.get(name, 1))


def clean_img_url(url: str) -> str:
    url = url.replace("\\/", "/")
    url = re.sub(r"\);.*$", "", url)
    url = re.sub(r";z-index:.*$", "", url)
    return url.rstrip(");\"'")


def should_skip_url(url: str) -> bool:
    return any(m in url for m in SKIP_IMG_MARKERS)


def normalize_ws(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    return text.strip()


_TRANSLATIONS_NORM: dict[str, str] | None = None
_TRANSLATIONS_CF: dict[str, str] | None = None


def _translation_maps() -> tuple[dict[str, str], dict[str, str]]:
    global _TRANSLATIONS_NORM, _TRANSLATIONS_CF
    if _TRANSLATIONS_NORM is None:
        _TRANSLATIONS_NORM = {normalize_ws(k): v for k, v in TRANSLATIONS.items()}
        _TRANSLATIONS_CF = {
            normalize_ws(k).casefold(): v for k, v in TRANSLATIONS.items()
        }
    return _TRANSLATIONS_NORM, _TRANSLATIONS_CF


def tr(text: str) -> str:
    """Translate AZ literary text to English; return original if no mapping."""
    if not text:
        return text
    key = normalize_ws(text)
    by_norm, by_cf = _translation_maps()
    if key in by_norm:
        return by_norm[key]
    if key in TRANSLATIONS:
        return TRANSLATIONS[key]
    cf = key.casefold()
    if cf in by_cf:
        return by_cf[cf]
    return text


def localize_blocks(blocks: list[dict], lang: str) -> list[dict]:
    """Return blocks with translatable fields localized for lang."""
    if lang != "en":
        return blocks
    out: list[dict] = []
    for b in blocks:
        kind = b.get("kind")
        if kind in ("poem", "figure"):
            out.append(b)
            continue
        nb = dict(b)
        if kind in (
            "p",
            "h1",
            "h2",
            "index",
            "credit",
            "analysis_title",
            "analysis_p",
        ):
            nb["text"] = tr(b.get("text", ""))
            # Keep AZ-derived anchors stable on headings.
            if kind == "h2" and "anchor" not in nb:
                nb["anchor"] = slugify_anchor(b.get("text", ""))
            out.append(nb)
            continue
        if kind in ("video", "ext"):
            nb["text"] = tr(b.get("text", ""))
            out.append(nb)
            continue
        if kind in ("ul", "analysis_ul"):
            nb["items"] = [tr(it) for it in b.get("items", [])]
            out.append(nb)
            continue
        out.append(nb)
    return out


def heading_text(el: Tag, canonical: list[str] | None = None) -> str:
    """Join letter spans without inserting spaces; keep real word spaces."""
    raw = "".join(el.strings)
    raw = normalize_ws(raw.replace("\n", " "))
    if not canonical:
        return raw
    compact = re.sub(r"\s+", "", raw).casefold()
    for c in canonical:
        if re.sub(r"\s+", "", c).casefold() == compact:
            return c
    # Missing-space salvage: e.g. BİRGÜN… → BİR GÜN…
    for c in canonical:
        if re.sub(r"\s+", "", c).casefold() == compact:
            return c
        if compact.startswith(re.sub(r"\s+", "", c).casefold()):
            return c
    return raw


def slugify_anchor(title: str) -> str:
    s = title.casefold()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"[\s_]+", "-", s).strip("-")
    return s or "section"


def az_lower(text: str) -> str:
    """Lowercase with Azerbaijani I/İ handling."""
    return text.replace("I", "ı").replace("İ", "i").lower()


def az_upper_first(ch: str) -> str:
    if ch == "i":
        return "İ"
    if ch == "ı":
        return "I"
    return ch.upper()


def az_sentence_case(text: str) -> str:
    """First alphabetic character upper, remainder lower (Azerbaijani-aware)."""
    s = normalize_ws(text)
    if not s:
        return s
    lower = az_lower(s)
    for i, ch in enumerate(lower):
        if ch.isalpha():
            return lower[:i] + az_upper_first(ch) + lower[i + 1 :]
    return lower


def _title_key(title: str) -> str:
    return normalize_ws(title).casefold()


def _title_tokens(title: str) -> frozenset[str]:
    return frozenset(re.findall(r"\w+", title.casefold(), flags=re.UNICODE))


def resolve_poem_anchor(title: str, poems: list[tuple[str, str]]) -> str | None:
    """Map an index title to a poem article id (exact, slug, or same-word-set)."""
    key = _title_key(title)
    for poem_title, anchor in poems:
        if _title_key(poem_title) == key:
            return anchor

    candidates = [
        (poem_title, anchor)
        for poem_title, anchor in poems
        if _title_key(poem_title)
        not in {"poeziya", "bədii nəsr", "esse", "poetik dastanlar və əfsanələr"}
    ]
    want_slug = slugify_anchor(title)
    for poem_title, anchor in candidates:
        if slugify_anchor(poem_title) == want_slug:
            return anchor

    tokens = _title_tokens(title)
    if len(tokens) >= 3:
        matches = [
            (poem_title, anchor)
            for poem_title, anchor in candidates
            if _title_tokens(poem_title) == tokens
        ]
        if len(matches) == 1:
            return matches[0][1]
    return None


def is_title_index_line(text: str) -> bool:
    """True for TOC lines like '"AGAC"; "ANLARSAN"; …', not ordinary prose with quotes."""
    titles = re.findall(r'"([^"]+)"', text)
    if len(titles) < 4:
        return False
    if any(len(t.strip()) > 90 for t in titles):
        return False
    leftover = text
    for t in titles:
        leftover = leftover.replace(f'"{t}"', "")
    leftover = re.sub(r"[;\s.…,]+", "", leftover)
    return len(leftover) <= 8 and text.count(";") >= max(1, len(titles) - 2)


def format_title_index_line(titles: list[str]) -> str:
    """Internal quoted form kept for legacy parsing of scraped index lines."""
    return "; ".join(f'"{t}"' for t in titles) + ";"


def render_title_index_links(
    titles: list[str],
    poems: list[tuple[str, str]],
    *,
    sentence_case: bool = False,
) -> str:
    """Render TOC titles as in-page links (no quotation marks)."""
    parts: list[str] = []
    for i, title in enumerate(titles):
        display = az_sentence_case(title) if sentence_case else title
        label = esc(display)
        anchor = resolve_poem_anchor(title, poems)
        if anchor:
            parts.append(
                f'<a class="eldar-index-link" href="#{esc(anchor)}">{label}</a>'
            )
        else:
            parts.append(label)
        if i < len(titles) - 1:
            parts.append("; ")
    return "".join(parts)


def render_poem_index_html(
    text: str,
    poems: list[tuple[str, str]],
    *,
    sentence_case: bool = False,
) -> str:
    """Turn quoted poem/prose titles in a scraped index line into in-page links."""
    titles = re.findall(r'"([^"]+)"', text)
    if titles:
        return render_title_index_links(
            titles, poems, sentence_case=sentence_case
        )
    return esc(text)


def collect_image_urls(soup: BeautifulSoup) -> list[str]:
    root = soup.select_one("div.UtePc.RCETm.yxgWrb") or soup
    urls: list[str] = []

    def add(u: str) -> None:
        u = clean_img_url(u)
        if not u.startswith("https://lh") or should_skip_url(u):
            return
        if u not in urls:
            urls.append(u)

    for img in root.find_all("img"):
        src = img.get("src") or ""
        if "googleusercontent.com" in src:
            add(src)
    for el in root.find_all(True):
        style = el.get("style") or ""
        m = re.search(
            r"url\((?:&quot;|\"|')?(https://lh\d\.googleusercontent\.com/sitesv/[^)\"'&]+)",
            style,
        )
        if m:
            add(html.unescape(m.group(1)))
    return urls


def _http_opener() -> urllib.request.OpenerDirector:
    cj = http.cookiejar.CookieJar()
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))


def fetch_fresh_image_urls(opener: urllib.request.OpenerDirector, key: str) -> list[str]:
    """Visit the live Google Sites page to obtain working image tokens."""
    live = LIVE_URLS[key]
    req = urllib.request.Request(
        live,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "az,en;q=0.8",
        },
    )
    with opener.open(req, timeout=90) as resp:
        html_text = resp.read().decode("utf-8", "replace")
    soup = BeautifulSoup(html_text, "html.parser")
    return collect_image_urls(soup)


def download_images(
    url_map: dict[str, list[str]],
    force: bool = False,
    *,
    refresh_urls: bool = True,
) -> dict[str, list[str]]:
    """Download content images; return {page_key: [local filenames]}."""
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    result: dict[str, list[str]] = {}
    opener = _http_opener()

    for key, cached_urls in url_map.items():
        prefix = next(p["img_prefix"] for p in PAGES if p["key"] == key)
        urls = cached_urls
        if refresh_urls:
            try:
                fresh = fetch_fresh_image_urls(opener, key)
                if fresh:
                    # Prefer fresh tokens; keep count aligned with cached when possible.
                    urls = fresh
                    print(f"  {key}: refreshed {len(fresh)} live image URL(s)")
                else:
                    print(f"  {key}: live page had 0 images; using cached URLs")
            except Exception as exc:  # noqa: BLE001
                print(f"  {key}: live refresh failed ({exc}); using cached URLs")

        names: list[str] = []
        n = 0
        referer = LIVE_URLS.get(key, "https://sites.google.com/")
        for url in urls:
            n += 1
            tmp_name = f"{prefix}-{n:02d}"
            existing = list(THUMB_DIR.glob(f"{tmp_name}.*"))
            if existing and not force:
                names.append(existing[0].name)
                continue
            try:
                req = urllib.request.Request(
                    url,
                    headers={
                        "User-Agent": USER_AGENT,
                        "Referer": referer,
                        "Accept": "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
                    },
                )
                with opener.open(req, timeout=90) as resp:
                    data = resp.read()
                    ctype = (resp.headers.get("Content-Type") or "").lower()
            except Exception as exc:  # noqa: BLE001
                print(f"  WARN download failed {key} #{n}: {exc}")
                continue
            if len(data) < MIN_IMG_BYTES:
                print(f"  skip tiny bytes {key} #{n} ({len(data)} B)")
                continue
            try:
                im = Image.open(io.BytesIO(data))
                im = im.convert("RGB") if im.mode not in ("RGB", "L") else im
                w, h = im.size
                if max(w, h) < MIN_IMG_EDGE:
                    print(f"  skip tiny dims {key} #{n} ({w}x{h})")
                    continue
                max_edge = 1400
                if max(w, h) > max_edge:
                    im.thumbnail((max_edge, max_edge), Image.Resampling.LANCZOS)
                out_name = f"{tmp_name}.jpg"
                out_path = THUMB_DIR / out_name
                im.save(out_path, "JPEG", quality=88, optimize=True)
                names.append(out_name)
                print(f"  saved {out_name} ({out_path.stat().st_size} B)")
            except Exception as exc:  # noqa: BLE001
                ext = ".png" if "png" in ctype else ".jpg"
                out_name = f"{tmp_name}{ext}"
                out_path = THUMB_DIR / out_name
                out_path.write_bytes(data)
                names.append(out_name)
                print(f"  saved raw {out_name} ({exc})")
        result[key] = names
    return result


def load_existing_images() -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    for p in PAGES:
        prefix = p["img_prefix"]
        files = sorted(
            f.name
            for f in THUMB_DIR.glob(f"{prefix}-*")
            if f.suffix.lower() in {".jpg", ".jpeg", ".png", ".webp"}
        )
        result[p["key"]] = files
    return result


ANALYSIS_TITLES = {"TƏSVİRİN TƏHLİLİ", "ŞEİRİN TƏHLİLİ"}


def para_text(p: Tag) -> str:
    return normalize_ws(p.get_text("", strip=False).replace("\n", " "))


def is_credit(text: str) -> bool:
    t = text.casefold()
    return t.startswith("rus dilindən") or "tərcümə:" in t or t.startswith("rus dilindən tərcümə")


def extract_blocks(page: dict, soup: BeautifulSoup, local_images: list[str]) -> list[dict]:
    root = soup.select_one("div.UtePc.RCETm.yxgWrb")
    if not root:
        raise RuntimeError(f"Content root missing for {page['key']}")

    url_to_local: dict[str, str] = {}
    remote_urls = collect_image_urls(soup)
    for i, url in enumerate(remote_urls):
        if i < len(local_images):
            url_to_local[clean_img_url(url)] = local_images[i]
            # also map without =wNNN suffix variants
            base = re.sub(r"=w\d+$", "", clean_img_url(url))
            url_to_local[base] = local_images[i]

    def resolve_img(url: str) -> str | None:
        u = clean_img_url(url)
        if should_skip_url(u):
            return None
        if u in url_to_local:
            return url_to_local[u]
        base = re.sub(r"=w\d+$", "", u)
        return url_to_local.get(base)

    blocks: list[dict] = []
    used_imgs: set[str] = set()
    canonical = page.get("canonical_h2") or []
    is_poetry = page.get("is_poetry", False)

    sections = root.find_all("section", recursive=False)
    for sec in sections:
        # Collect ordered nodes inside this section.
        nodes: list[Tag] = []
        for el in sec.descendants:
            if not isinstance(el, Tag):
                continue
            name = el.name
            if name in ("h1", "h2", "h3"):
                nodes.append(el)
            elif name == "ul" and not el.find_parent("ul"):
                nodes.append(el)
            elif name == "p" and not el.find_parent(["li", "h1", "h2", "h3", "a"]):
                nodes.append(el)
            elif name == "img":
                nodes.append(el)
            elif name == "a" and el.get("href") and (
                "youtu" in (el.get("href") or "")
                or (el.get("href") or "").startswith("http")
            ):
                # Prefer youtube / external literary links; skip sites chrome.
                href = el.get("href") or ""
                if any(
                    x in href
                    for x in (
                        "sites.google",
                        "google.com",
                        "safelinks.protection",
                        "gstatic",
                    )
                ):
                    continue
                if el.find_parent("p") and "youtu" not in href:
                    continue
                nodes.append(el)
            elif name == "div" and el.get("style") and "googleusercontent" in el.get("style", ""):
                nodes.append(el)
            elif name == "br" and el.parent and el.parent.name in ("div", "section", "td"):
                # stanza markers between poem lines
                nodes.append(el)

        # Deduplicate while preserving order (descendants may revisit).
        seen_ids: set[int] = set()
        ordered: list[Tag] = []
        for el in nodes:
            i = id(el)
            if i in seen_ids:
                continue
            # Skip nested p inside already collected ul
            if el.name == "p" and el.find_parent("ul") and any(
                id(u) in seen_ids for u in el.find_parents("ul")
            ):
                continue
            seen_ids.add(i)
            ordered.append(el)

        poem_buf: list[str] = []
        analysis_mode: str | None = None

        def flush_poem() -> None:
            nonlocal poem_buf
            if poem_buf:
                blocks.append({"kind": "poem", "lines": poem_buf[:]})
                poem_buf = []

        for el in ordered:
            if el.name == "br":
                if is_poetry and poem_buf and analysis_mode is None:
                    poem_buf.append("")  # stanza gap
                continue

            if el.name in ("h1", "h2", "h3"):
                flush_poem()
                analysis_mode = None
                text = heading_text(el, canonical if el.name != "h1" else None)
                if not text:
                    continue
                # Demote Google Sites H1s so the DAAB hero keeps the only page H1.
                if el.name == "h1" and text.casefold() in {
                    page["nav_title"].casefold(),
                    "poeziya",
                    "bədii nəsr",
                    "esse",
                    "poetik dastanlar və əfsanələr",
                }:
                    blocks.append({"kind": "h1", "text": text})
                else:
                    blocks.append(
                        {
                            "kind": "h2",
                            "text": text,
                            "anchor": slugify_anchor(text),
                        }
                    )
                continue

            if el.name == "ul":
                flush_poem()
                items = []
                for li in el.find_all("li", recursive=False):
                    t = normalize_ws(li.get_text(" ", strip=True))
                    if t:
                        items.append(t)
                if items:
                    kind = "analysis_ul" if analysis_mode else "ul"
                    blocks.append({"kind": kind, "items": items})
                continue

            if el.name == "img":
                flush_poem()
                local = resolve_img(el.get("src") or "")
                if local and local not in used_imgs:
                    used_imgs.add(local)
                    blocks.append({"kind": "figure", "file": local})
                continue

            if el.name == "div" and "googleusercontent" in (el.get("style") or ""):
                m = re.search(
                    r"url\((?:&quot;|\"|')?(https://lh\d\.googleusercontent\.com/sitesv/[^)\"'&]+)",
                    el.get("style") or "",
                )
                if m:
                    flush_poem()
                    local = resolve_img(html.unescape(m.group(1)))
                    if local and local not in used_imgs:
                        used_imgs.add(local)
                        blocks.append({"kind": "figure", "file": local})
                continue

            if el.name == "a":
                href = el.get("href") or ""
                label = normalize_ws(el.get_text(" ", strip=True)) or href
                if "youtu" in href:
                    flush_poem()
                    blocks.append({"kind": "video", "href": href, "text": label})
                elif href.startswith("http") and "wikipedia" in href:
                    # Keep wiki link; may also appear as plain text nearby.
                    blocks.append({"kind": "ext", "href": href, "text": label})
                continue

            if el.name == "p":
                text = para_text(el)
                if not text:
                    continue
                # Skip pure anchor-only leftovers
                if text.startswith("#"):
                    continue

                upper = text.upper()
                if upper in ANALYSIS_TITLES or text in ANALYSIS_TITLES:
                    flush_poem()
                    analysis_mode = text
                    blocks.append({"kind": "analysis_title", "text": text})
                    continue

                if is_credit(text):
                    flush_poem()
                    blocks.append({"kind": "credit", "text": text})
                    continue

                # Index line of quoted titles (TOC only — not prose with dialogue quotes)
                if is_title_index_line(text):
                    flush_poem()
                    blocks.append({"kind": "index", "text": text})
                    continue

                # Stay in analysis until the next poem heading.
                if analysis_mode:
                    blocks.append({"kind": "analysis_p", "text": text})
                    continue

                # Poetry body lines: short-ish lines before analysis/credit
                if is_poetry:
                    # Heuristic: verse-like lines (no long prose paragraphs early)
                    if len(text) <= 160 and not text.endswith("."):
                        poem_buf.append(text)
                        continue
                    if poem_buf and len(text) <= 200:
                        poem_buf.append(text)
                        continue
                    flush_poem()

                flush_poem()
                blocks.append({"kind": "p", "text": text})
                continue

        flush_poem()

    # Attach any unused downloaded images at end (rare).
    for fname in local_images:
        if fname not in used_imgs:
            blocks.append({"kind": "figure", "file": fname})
            used_imgs.add(fname)

    # Drop plain-text duplicates of video link labels (keep the <a> only).
    # VƏTƏN HİSSLƏRİ: "Qarabağa səfər (video)" appears as both a caption and a link.
    drop_plain = {
        _title_key(b["text"]) for b in blocks if b.get("kind") == "video"
    }
    if drop_plain:
        blocks = [
            b
            for b in blocks
            if not (
                b.get("kind") == "p"
                and _title_key(b.get("text", "")) in drop_plain
            )
        ]

    if page.get("key") == "ozum":
        blocks = apply_ozum_bio_override(blocks, "az")
        blocks = apply_ozum_awards_override(blocks, "az")
        blocks = apply_ozum_strip_berengarten(blocks)
        blocks = apply_ozum_append_berengarten(blocks, "az")

    if page.get("key") == "poeziya":
        blocks = reorder_poetry_figures_before_poems(blocks)

    return blocks


def reorder_poetry_figures_before_poems(blocks: list[dict]) -> list[dict]:
    """Place each poem illustration right after its h2 so it aligns with the first verse."""
    out: list[dict] = []
    i = 0
    while i < len(blocks):
        b = blocks[i]
        if b.get("kind") != "h2":
            out.append(b)
            i += 1
            continue
        j = i + 1
        chunk: list[dict] = []
        while j < len(blocks) and blocks[j].get("kind") != "h2":
            chunk.append(blocks[j])
            j += 1
        has_poem = any(c.get("kind") == "poem" for c in chunk)
        fig_idx = next(
            (k for k, c in enumerate(chunk) if c.get("kind") == "figure"), None
        )
        out.append(b)
        if has_poem and fig_idx is not None:
            fig = chunk.pop(fig_idx)
            out.append(fig)
        out.extend(chunk)
        i = j
    return out


def render_literary_html(page: dict, blocks: list[dict], lang: str) -> str:
    thumb_prefix = (
        "eldar-ahadov-media-thumbnails/"
        if lang == "az"
        else "../../az/scientists/eldar-ahadov-media-thumbnails/"
    )
    parts: list[str] = ['<div class="eldar-literary">']
    open_piece = False
    first_figure_done = False
    float_mode = page.get("float_first_img")
    # poem_targets: display title (may be EN) -> AZ-stable anchor
    poem_targets: list[tuple[str, str]] = [
        (b["text"], b.get("anchor") or slugify_anchor(b["text"]))
        for b in blocks
        if b.get("kind") == "h2"
    ]
    # Also map EN canonical display titles to AZ anchors for index linking.
    canonical_az = page.get("canonical_h2") or []
    if lang == "en" and page.get("key") in EN_CANONICAL_H2 and canonical_az:
        en_titles = EN_CANONICAL_H2[page["key"]]
        az_anchor_by_key = {
            _title_key(t): slugify_anchor(t) for t in canonical_az
        }
        # Prefer anchors already present on localized h2 blocks.
        h2_anchor_by_text = {
            _title_key(t): a for t, a in poem_targets
        }
        for az_title, en_title in zip(canonical_az, en_titles):
            anchor = h2_anchor_by_text.get(_title_key(en_title)) or az_anchor_by_key.get(
                _title_key(az_title)
            )
            if anchor:
                poem_targets.append((en_title, anchor))

    def close_piece() -> None:
        nonlocal open_piece
        if open_piece:
            parts.append('<div class="eldar-clear"></div></article>')
            open_piece = False

    def open_piece_with(title: str, anchor: str) -> None:
        nonlocal open_piece
        close_piece()
        parts.append(f'<article class="eldar-piece" id="{esc(anchor)}">')
        parts.append(f"<h2>{esc(title)}</h2>")
        open_piece = True

    poem_open = False

    def close_poem() -> None:
        nonlocal poem_open
        if poem_open:
            parts.append("</div>")
            poem_open = False

    for b in blocks:
        kind = b["kind"]
        if kind == "h1":
            close_poem()
            close_piece()
            parts.append(f"<h1>{esc(b['text'])}</h1>")
            continue
        if kind == "h2":
            close_poem()
            raw_title = b["text"]
            # Anchors stay AZ-based (set at extract / before localize).
            anchor = b.get("anchor") or slugify_anchor(raw_title)
            display_title = (
                az_sentence_case(raw_title)
                if lang == "az" and page.get("key") in ("poeziya", "bedii")
                else raw_title
            )
            open_piece_with(display_title, anchor)
            first_figure_done = False
            continue
        if kind == "index":
            close_poem()
            # Prefer the page’s canonical piece titles so TOC matches every h2
            # (e.g. Bədii nəsr includes OĞLU even when the Google Sites list omitted it).
            # EN: display EN_CANONICAL_H2 labels; anchors resolve via poem_targets (AZ-based).
            if lang == "en" and page.get("key") in EN_CANONICAL_H2:
                index_titles = EN_CANONICAL_H2[page["key"]]
                sentence_case = False
            else:
                index_titles = page.get("canonical_h2") or []
                sentence_case = page.get("key") in ("poeziya", "bedii")
            if index_titles:
                index_html = render_title_index_links(
                    index_titles, poem_targets, sentence_case=sentence_case
                )
            else:
                index_html = render_poem_index_html(
                    b["text"], poem_targets, sentence_case=sentence_case
                )
            parts.append(f'<p class="eldar-index">{index_html}</p>')
            continue
        if kind in ("ul", "analysis_ul"):
            close_poem()
            cls = "eldar-analysis-list" if kind == "analysis_ul" else "eldar-awards"
            parts.append(f'<ul class="{cls}">')
            for item in b["items"]:
                parts.append(f"<li>{esc(item)}</li>")
            parts.append("</ul>")
            continue
        if kind == "figure":
            close_poem()
            src = thumb_prefix + b["file"]
            cls = "eldar-figure"
            if float_mode == "portrait" and page["key"] == "ozum" and not first_figure_done:
                cls += " eldar-portrait"
                first_figure_done = True
            elif page.get("is_poetry"):
                # Every poem illustration floats beside the verse.
                cls += " eldar-figure--float"
                first_figure_done = True
            elif float_mode == "figure" and not first_figure_done:
                cls += " eldar-figure--float"
                first_figure_done = True
            # bedii/esse: no float — keep story images a uniform centered size.
            parts.append(
                f'<figure class="{cls}"><img src="{esc(src)}" alt="" loading="lazy" decoding="async"/></figure>'
            )
            continue
        if kind == "video":
            close_poem()
            parts.append(
                f'<p><a class="eldar-video-link" href="{esc(b["href"])}" target="_blank" '
                f'rel="noopener noreferrer">{esc(b["text"])}</a></p>'
            )
            continue
        if kind == "ext":
            close_poem()
            parts.append(
                f'<p><a class="eldar-ext-link" href="{esc(b["href"])}" target="_blank" '
                f'rel="noopener noreferrer">{esc(b["text"])}</a></p>'
            )
            continue
        if kind == "credit":
            close_poem()
            credit_text = b.get("text", "")
            # EN pages: omit Əlviz Əliyev translator credits.
            if lang == "en" and (
                "əlviz əliyev" in credit_text.casefold()
                or "elviz aliyev" in credit_text.casefold()
            ):
                continue
            parts.append(f'<p class="eldar-credit">{esc(credit_text)}</p>')
            continue
        if kind == "analysis_title":
            close_poem()
            parts.append(f'<p class="eldar-analysis-title">{esc(b["text"])}</p>')
            continue
        if kind == "analysis_p":
            close_poem()
            parts.append(f'<p class="eldar-analysis-p">{esc(b["text"])}</p>')
            continue
        if kind == "poem":
            if not poem_open:
                parts.append('<div class="eldar-poem">')
                poem_open = True
            for line in b["lines"]:
                if line == "":
                    parts.append('<div class="eldar-stanza-gap" aria-hidden="true"></div>')
                else:
                    parts.append(f"<p>{esc(line)}</p>")
            continue
        if kind == "p":
            close_poem()
            # Enrich Richard Berengarten wiki mention on about page
            text = b["text"]
            if "Riçard Berengarten" in text or "Richard Berengarten" in text:
                linked = text
                linked = linked.replace(
                    "Riçard Berengarten",
                    '<a class="eldar-ext-link" href="https://en.wikipedia.org/wiki/Richard_Berengarten" '
                    'target="_blank" rel="noopener noreferrer">Riçard Berengarten</a>',
                )
                linked = linked.replace(
                    "Richard Berengarten",
                    '<a class="eldar-ext-link" href="https://en.wikipedia.org/wiki/Richard_Berengarten" '
                    'target="_blank" rel="noopener noreferrer">Richard Berengarten</a>',
                )
                parts.append(f"<p>{linked}</p>")
            else:
                parts.append(f"<p>{esc(text)}</p>")
            continue

    close_poem()
    close_piece()
    parts.append("</div>")
    return "\n".join(parts)


def section_nav_html(active_slug: str, lang: str) -> str:
    s = STRINGS[lang]
    items = []
    for slug, title_az in NAV_ITEMS:
        label = EN_NAV_TITLES.get(slug, title_az) if lang == "en" else title_az
        cur = ' aria-current="page"' if slug == active_slug else ""
        items.append(f'<li><a href="{esc(slug)}.html"{cur}>{esc(label)}</a></li>')
    return (
        f'<nav class="eldar-section-nav-wrap" aria-label="{esc(s["section_nav_aria"])}">'
        f'<ul class="eldar-section-nav">\n'
        + "\n".join(items)
        + "\n</ul></nav>"
    )


def build_page_html(page: dict, literary: str, lang: str) -> str:
    s = STRINGS[lang]
    page_id = page["page_id"]
    slug = page["slug"]
    nav_title = page["nav_title"]
    em_title, meta_desc, panel_copy = s["meta"][page_id]
    h1_em = nav_title if lang == "az" else em_title
    title = f"{s['author']} — {h1_em} | {'DAAB' if lang == 'az' else 'WAAS'}"
    crumb_current = f"{s['author']} — {h1_em}"
    canonical = f"https://daab-waas.com/{lang}/scientists/{slug}.html"
    az_url = f"https://daab-waas.com/az/scientists/{slug}.html"
    en_url = f"https://daab-waas.com/en/scientists/{slug}.html"
    en_marker = "\n<!-- daab-en-complete -->" if lang == "en" else ""

    css = STYLE_VERSIONS
    js = SCRIPT_VERSIONS

    return f"""<!DOCTYPE html>
<html lang="{s['lang']}" data-daab-lang="{s['lang']}" data-daab-asset-root="../../" data-daab-page-id="{page_id}" data-daab-nav-mount="1">
<head>{en_marker}
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(title)}</title>
<meta content="{esc(meta_desc)}" name="description"/>
<link rel="icon" href="../../images/daab-logo.png" type="image/png"/>
<link rel="canonical" href="{canonical}"/>
<link rel="alternate" hreflang="az" href="{az_url}"/>
<link rel="alternate" hreflang="en" href="{en_url}"/>
<link rel="alternate" hreflang="x-default" href="{az_url}"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="DAAB"/>
<meta property="og:title" content="{esc(title)}"/>
<meta property="og:description" content="{esc(meta_desc)}"/>
<meta property="og:url" content="{canonical}"/>
<meta property="og:image" content="https://daab-waas.com/images/daab-logo.png"/>
<meta property="og:locale" content="{s['locale']}"/>
<meta name="twitter:card" content="summary_large_image"/>
<link href="../../css/daab-fonts.css?v={v('daab-fonts.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-common.css?v={v('daab-common.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-perf.css?v={v('daab-perf.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-mobile.css?v={v('daab-mobile.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-sticky-chrome.css?v={v('daab-sticky-chrome.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-search.css?v={v('daab-search.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-back-to-top.css?v={v('daab-back-to-top.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-hero-summary.css?v={v('daab-hero-summary.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-lang.css?v={v('daab-lang.css', css)}" rel="stylesheet"/>
<link href="../../css/daab-nav-mega.css?v={v('daab-nav-mega.css', css)}" rel="stylesheet"/>
<link href="../../css/{ELDAR_CSS}?v={ELDAR_CSS_VER}" rel="stylesheet"/>
<script src="../../js/daab-mobile.js?v={v('daab-mobile.js', js)}" defer></script>
<script src="../../js/daab-perf.js?v={v('daab-perf.js', js)}" defer></script>
<script src="../../js/daab-sticky-chrome.js?v={v('daab-sticky-chrome.js', js)}" defer></script>
<script src="../../js/daab-back-to-top.js?v={v('daab-back-to-top.js', js)}" defer></script>
<script src="../../js/daab-i18n.js?v={v('daab-i18n.js', js)}" defer></script>
<script src="../../js/daab-lang-position.js?v={v('daab-lang-position.js', js)}" defer></script>
<script src="../../js/daab-design-tokens.js?v={v('daab-design-tokens.js', js)}" defer></script>
<script src="../../js/daab-nav.js?v={v('daab-nav.js', js)}" defer></script>
<script src="../../js/daab-primary-nav.js?v={v('daab-primary-nav.js', js)}" defer></script>
<script src="../../js/daab-breadcrumbs.js?v={v('daab-breadcrumbs.js', js)}" defer></script>
<script src="../../js/daab-shell.js?v={v('daab-shell.js', js)}" defer></script>
<script src="../../js/daab-page-subtitle.js?v={v('daab-page-subtitle.js', js)}" defer></script>
<script src="../../js/daab-search.js?v={v('daab-search.js', js)}" defer></script>
<script src="../../js/daab-analytics.js?v={v('daab-analytics.js', js)}" defer></script>
</head>
<body>
<a class="skip" href="#content">{esc(s['skip'])}</a>
<nav aria-label="{esc(s['brand_menu_aria'])}" class="nav-strip"><div class="nav-inner"><button class="mobile-menu-toggle" type="button" aria-label="{esc(s['menu_open'])}" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button><div class="page-logo"><a title="{esc(s['nav_home_title'])}" aria-label="{esc(s['nav_home_aria'])}" href="../index.html"><img src="../../images/daab-logo.png" class="nav-brand-logo" alt="DAAB Logo"></a></div><a aria-label="{esc(s['nav_home_aria'])}" class="nav-brand" href="../index.html"><span class="nav-brand-text">{s['brand']}</span></a><div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"><div class="nav-divider"></div></div></div></nav>
<nav class="daab-breadcrumbs" id="daab-breadcrumbs" aria-label="{esc(s['crumb_aria'])}">
<ol class="daab-breadcrumbs-list">
<li class="daab-breadcrumbs-item"><a href="../index.html">{esc(s['crumb_home'])}</a></li>
<li class="daab-breadcrumbs-item"><span class="daab-breadcrumbs-sep" aria-hidden="true">›</span><a href="list.html">{esc(s['crumb_scientists'])}</a></li>
<li class="daab-breadcrumbs-item"><span class="daab-breadcrumbs-sep" aria-hidden="true">›</span><span class="daab-breadcrumbs-current" aria-current="page">{esc(crumb_current)}</span></li>
</ol>
</nav>
<header class="page-hero">
<div class="hero-wrap shell">
<section class="hero-copy">
<h1>{esc(s['author'])}<br><em>{esc(h1_em)}</em></h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(panel_copy)}</p>
</section>
<aside aria-label="{esc(s['panel_title'])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(s['panel_title'])}</h2>
<div class="panel-copy">
<p class="panel-copy-lead">{esc(meta_desc)}</p>
</div>
</div>
</aside>
</div>
</header>
<main class="main eldar-main" id="content">
{section_nav_html(slug, lang)}
{literary}
</main>
<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>{esc(s['footer_org'])}</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">{esc(s['footer_contact'])}</h4><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a rel="noopener noreferrer" href="https://daab-waas.com" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">{esc(s['footer_addr'])}</h4><p class="footer-address">{s['footer_addr_body']}</p></div>
<div class="footer-col"><h4 class="footer-title">{esc(s['footer_lead_h'])}</h4><p class="footer-leader">{s['footer_lead_body']}</p></div>
</div>
</div>
<div class="footer-bottom">{esc(s['footer_rights'])}</div>
</footer>
</body>
</html>
"""


def ensure_source_from_temp() -> None:
    """If helpers source missing, copy from %TEMP%/eldar-site."""
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    temp = Path(__import__("os").environ.get("TEMP", "")) / "eldar-site"
    mapping = {
        "ozum.html": "page2.html",
        "poeziya.html": "page3.html",
        "poetik.html": "page4.html",
        "bedii.html": "page5.html",
        "esse.html": "page6.html",
    }
    for dest, src in mapping.items():
        dest_path = SOURCE_DIR / dest
        if dest_path.exists():
            continue
        src_path = temp / src
        if src_path.exists():
            shutil.copy2(src_path, dest_path)
            print(f"Copied {src_path} -> {dest_path}")
        else:
            raise FileNotFoundError(f"Missing source {dest_path} and temp {src_path}")


def build_all(*, download: bool, force_download: bool) -> int:
    ensure_source_from_temp()
    soups: dict[str, BeautifulSoup] = {}
    url_map: dict[str, list[str]] = {}
    for page in PAGES:
        raw = (SOURCE_DIR / page["source"]).read_text(encoding="utf-8", errors="replace")
        soup = BeautifulSoup(raw, "html.parser")
        soups[page["key"]] = soup
        url_map[page["key"]] = collect_image_urls(soup)
        print(f"{page['key']}: {len(url_map[page['key']])} content image URL(s)")

    if download or force_download or not THUMB_DIR.exists() or not any(THUMB_DIR.iterdir()):
        print("Downloading images…")
        images = download_images(url_map, force=force_download)
    else:
        images = load_existing_images()
        # If any page missing images, download those.
        missing = [k for k, v in images.items() if not v and url_map.get(k)]
        if missing:
            print(f"Downloading missing images for: {', '.join(missing)}")
            partial = download_images({k: url_map[k] for k in missing}, force=True)
            images.update(partial)

    total_imgs = sum(len(v) for v in images.values())
    print(f"Image files ready: {total_imgs}")

    for page in PAGES:
        blocks = extract_blocks(page, soups[page["key"]], images.get(page["key"], []))
        for lang in ("az", "en"):
            if lang == "en":
                lang_blocks = copy.deepcopy(blocks)
                if page["key"] == "ozum":
                    # Strip AZ Berengarten first, then apply English curated sections
                    # (do not localize ozum — structured EN overrides cover the page).
                    lang_blocks = apply_ozum_strip_berengarten(lang_blocks)
                    lang_blocks = apply_ozum_bio_override(lang_blocks, "en")
                    lang_blocks = apply_ozum_awards_override(lang_blocks, "en")
                    lang_blocks = apply_ozum_append_berengarten(lang_blocks, "en")
                else:
                    lang_blocks = localize_blocks(lang_blocks, "en")
            else:
                lang_blocks = blocks
            body = render_literary_html(page, lang_blocks, lang)
            html_out = build_page_html(page, body, lang)
            out = ROOT / lang / "scientists" / f"{page['slug']}.html"
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(html_out, encoding="utf-8", newline="\n")
            print(f"Wrote {out.relative_to(ROOT)} ({len(lang_blocks)} blocks, {lang})")

    manifest = {
        "pages": [
            {
                "key": p["key"],
                "slug": p["slug"],
                "images": images.get(p["key"], []),
            }
            for p in PAGES
        ],
        "image_count": total_imgs,
    }
    (SOURCE_DIR / "build-manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return total_imgs


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--download-images",
        action="store_true",
        help="Download/re-download content images from Googleusercontent URLs",
    )
    parser.add_argument(
        "--force-download",
        action="store_true",
        help="Overwrite existing thumbnail files",
    )
    args = parser.parse_args()
    total = build_all(download=args.download_images, force_download=args.force_download)
    print(f"Done. Images: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

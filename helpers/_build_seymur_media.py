#!/usr/bin/env python3
"""Build the "Seymur Nəsirov — Mətbuat resursları" media index pages (AZ/EN).

Source of truth for the resource cards. Edit RESOURCES / STRINGS below and
re-run to regenerate both language pages:

    python helpers/_build_seymur_media.py

Writes:
    az/scientists/seymur-nasirov-media.html
    en/scientists/seymur-nasirov-media.html
"""
from __future__ import annotations

import json

from _paths import ROOT
from _scientist_media import write_pages

THUMB_DIRNAME = "seymur-nasirov-media-thumbnails"
_MANIFEST = ROOT / "helpers" / "_seymur_thumbs.json"
THUMBS = json.loads(_MANIFEST.read_text(encoding="utf-8")) if _MANIFEST.exists() else []

# All resources are press / online news articles, in the same order as the
# source page. Thumbnails map 1:1 (by order) onto the downloaded manifest.
RESOURCES = [
    {"section": 1, "kind": "article", "source": "edebiyyatveincesenet.az", "date": "21.01.2025",
     "url": "https://edebiyyatveincesenet.az/ru/reytinq/item/19692-zhurani-kaerimdae-azaerbaydzan-soezunun-vae-bak-neftinin-yer-ald-zhh-n-elmi-aesaslarla-subut-edaen-seymur-naesirov-baraedae",
     "az": "Qurani-Kərimdə «Azərbaycan» sözünün və Bakı neftinin yer aldığını elmi əsaslarla sübut edən Seymur Nəsirov barədə",
     "en": "About Seymur Nasirov, who scientifically proved that the word «Azerbaijan» and Baku oil appear in the Holy Quran"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "16.01.2025",
     "url": "https://azertag.az/xeber/ereb_mediasinda_20_yanvar_faciesi_haqqinda_meqale_derc_olunub-3374839",
     "az": "Ərəb mediasında 20 Yanvar faciəsi haqqında məqalə dərc olunub",
     "en": "An article about the January 20 tragedy published in the Arab media"},
    {"section": 1, "kind": "article", "source": "sabaha-inamla.az", "date": "16.01.2025",
     "url": "https://sabaha-inamla.az/gundem/56133-rb-mediasnda-azrbaycanl-alimin-20-yanvar-facisi-haqqnda-mqalsi-drc-olunub.html",
     "az": "Ərəb mediasında azərbaycanlı alimin 20 Yanvar faciəsi haqqında məqaləsi dərc olunub",
     "en": "An Azerbaijani scientist's article about the January 20 tragedy published in the Arab media"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "21.10.2024",
     "url": "https://azertag.az/xeber/misir_mediasi_azerbaycanli_alimin_simpoziumda_chixisini_genis_isiqlandirib-3238596",
     "az": "Misir mediası azərbaycanlı alimin simpoziumda çıxışını geniş işıqlandırıb",
     "en": "Egyptian media widely covered the Azerbaijani scientist's speech at the symposium"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "06.11.2024",
     "url": "https://azertag.az/xeber/azerbaycan_ilahiyyat_institutunun_misirin_el_ezher_universiteti_ile_emekdasliq_etmesine_dair_fikir_mubadilesi_aparilib-3263556",
     "az": "Azərbaycan İlahiyyat İnstitutunun Misirin əl-Əzhər Universiteti ilə əməkdaşlıq etməsinə dair fikir mübadiləsi aparılıb",
     "en": "Exchange of views on cooperation between the Azerbaijan Institute of Theology and Egypt's Al-Azhar University"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "27.11.2024",
     "url": "https://azertag.az/xeber/misir_azerbaycan_dostluq_cemiyyetinde_telebelere_diplomlar_teqdim_edilib-3305040",
     "az": "Misir-Azərbaycan Dostluq Cəmiyyətində tələbələrə diplomlar təqdim edilib",
     "en": "Diplomas presented to students at the Egypt-Azerbaijan Friendship Society"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "12.12.2024",
     "url": "https://azertag.az/xeber/misirde_umummilli_lider_heyder_eliyevin_xatiresi_anilib-3329335",
     "az": "Misirdə Ümummilli Lider Heydər Əliyevin xatirəsi anılıb",
     "en": "The memory of National Leader Heydar Aliyev commemorated in Egypt"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "17.12.2024",
     "url": "https://azertag.az/xeber/misirin_benhe_universitetinde_azerbaycan_dili_bolmesinin_achilmasi_muzakire_edilib-3336559",
     "az": "Misirin Bənhə Universitetində Azərbaycan dili bölməsinin açılması müzakirə edilib",
     "en": "Opening of an Azerbaijani language department at Egypt's Benha University discussed"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "24.12.2024",
     "url": "https://azertag.az/xeber/misirde_dunya_azerbaycanlilarinin_hemreyliyi_gunu_qeyd_olunub-3345955",
     "az": "Misirdə Dünya Azərbaycanlılarının Həmrəyliyi Günü qeyd olunub",
     "en": "World Azerbaijanis' Solidarity Day celebrated in Egypt"},
    {"section": 1, "kind": "article", "source": "azertag.az", "date": "26.12.2024",
     "url": "https://azertag.az/xeber/misir_azerbaycan_dostluq_cemiyyetinde_xatire_gusesi_yaradilib-3351583",
     "az": "Misir-Azərbaycan Dostluq Cəmiyyətində xatirə guşəsi yaradılıb",
     "en": "A memorial corner created at the Egypt-Azerbaijan Friendship Society"},
    {"section": 1, "kind": "article", "source": "diaspor.gov.az", "date": "06.12.2024",
     "url": "https://diaspor.gov.az/az/news-detail/azerbaycan-diasporunun-sedri-misir-muftisi-ile-gorusub-5353",
     "az": "Azərbaycan diasporunun sədri Misir müftisi ilə görüşüb",
     "en": "The head of the Azerbaijani diaspora met with the Mufti of Egypt"},
]

STRINGS = {
    "az": {
        "lang": "az", "locale": "az_AZ",
        "skip": "Məzmuna keç",
        "nav_home_title": "Ana səhifə", "nav_home_aria": "DAAB ana səhifə",
        "brand": "<span class=\"nav-brand-line\">Dünya Azərbaycanlı</span><span class=\"nav-brand-line\">Alimlər Birliyi</span>",
        "brand_menu_aria": "Əsas naviqasiya",
        "menu_open": "Menyunu aç",
        "crumb_home": "Ana səhifə", "crumb_scientists": "Alimlərimiz",
        "crumb_current": "Seymur Nəsirov — Mətbuat resursları",
        "crumb_aria": "Səhifə yolu",
        "title": "Seymur Nəsirov — Mətbuat resursları | DAAB",
        "meta_desc": "DAAB İdarə Heyətinin həmsədri, tədqiqatçı-alim Dr. Seymur Nəsirov haqqında mətbuat və onlayn xəbər materiallarının toplusu.",
        "h1": "Seymur Nəsirov",
        "h1_em": "Mətbuat resursları",
        "subtitle": "Mətbuat və onlayn xəbər materialları",
        "panel_title": "Bu səhifə haqqında",
        "panel_copy": "DAAB İdarə Heyətinin həmsədri, tədqiqatçı-alim Dr. Seymur Nəsirov haqqında mətbuat və onlayn xəbər materiallarının toplusu.",
        "sec1": "Mətbuat və onlayn xəbər materialları",
        "tag_video": "Video", "tag_article": "Məqalə",
        "go_video": "İzlə", "go_article": "Aç",
        "count_one": "resurs",
        "footer_org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "footer_contact": "Əlaqə", "footer_addr": "Ünvan", "footer_lead_h": "Rəhbərlik",
        "footer_addr_body": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə",
        "footer_lead_body": "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Almaniya — James D. Murray mükafatlı professoru",
        "footer_rights": "© 2026 DAAB — Bütün hüquqlar qorunur",
    },
    "en": {
        "lang": "en", "locale": "en_US",
        "skip": "Skip to content",
        "nav_home_title": "Home", "nav_home_aria": "WAAS home",
        "brand": "<span class=\"nav-brand-line\">World Association of</span><span class=\"nav-brand-line\">Azerbaijani Scientists</span>",
        "brand_menu_aria": "Primary navigation",
        "menu_open": "Open menu",
        "crumb_home": "Home", "crumb_scientists": "Scientists",
        "crumb_current": "Seymur Nasirov — Press resources",
        "crumb_aria": "Breadcrumb",
        "title": "Seymur Nasirov — Press resources | WAAS",
        "meta_desc": "A collection of press and online news coverage about Dr. Seymur Nasirov — researcher and Co-Chair of the WAAS Executive Board.",
        "h1": "Seymur Nasirov",
        "h1_em": "Press resources",
        "subtitle": "Press and online news coverage",
        "panel_title": "About this page",
        "panel_copy": "A collection of press and online news coverage about Dr. Seymur Nasirov — researcher and Co-Chair of the WAAS Executive Board.",
        "sec1": "Press and online news coverage",
        "tag_video": "Video", "tag_article": "Article",
        "go_video": "Watch", "go_article": "Open",
        "count_one": "resources",
        "footer_org": "World Association of Azerbaijani Scientists",
        "footer_contact": "Contact", "footer_addr": "Address", "footer_lead_h": "Leadership",
        "footer_addr_body": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiye",
        "footer_lead_body": "<strong>Prof. Dr. Messoud Efendiev</strong><br/>Chair of the WAAS Executive Board<br/>Germany — James D. Murray Distinguished Professor",
        "footer_rights": "© 2026 WAAS — All rights reserved",
    },
}

CFG = {
    "page_id": "seymur-media",
    "slug": "seymur-nasirov-media",
    "thumb_dirname": THUMB_DIRNAME,
    "thumbs": THUMBS,
    "resources": RESOURCES,
    "strings": STRINGS,
}


def main() -> int:
    return write_pages(CFG)


if __name__ == "__main__":
    raise SystemExit(main())

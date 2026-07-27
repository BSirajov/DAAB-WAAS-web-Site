#!/usr/bin/env python3
"""Build the "Bəxtiyar Siracov — İnternet resursları" media index pages.

Source of truth for the AZ/EN media resource cards. Edit the RESOURCES list
below and re-run to regenerate both language pages:

    python helpers/_build_sirajov_media.py

Writes:
    az/scientists/bakhtiyar-sirajov-media.html
    en/scientists/bakhtiyar-sirajov-media.html
"""
from __future__ import annotations

import json

from _paths import ROOT
from _scientist_media import write_pages

# Original per-URL thumbnails downloaded from the source site (in RESOURCES
# order). Produced by helpers/_download_sirajov_thumbs.py.
THUMB_DIRNAME = "bakhtiyar-sirajov-media-thumbnails"
_MANIFEST = ROOT / "helpers" / "_sirajov_thumbs.json"
THUMBS = json.loads(_MANIFEST.read_text(encoding="utf-8")) if _MANIFEST.exists() else []

# ── Resource data ─────────────────────────────────────────────────────────
# kind: "video" (YouTube) or "article".
# For video, `yt` is the YouTube video id (thumbnail + link derived).
# For article, `url` is the direct link.
# `source` is the display label / favicon domain.
# section: 1 = interviews/events/TV, 2 = Vienna International Centre exhibitions.
RESOURCES = [
    # ── Section 1: Interviews, events, TV programmes ──
    {"section": 1, "kind": "article", "source": "azerbaijantoday.az",
     "url": "https://www.azerbaijantoday.az/2025/12/10/the-interviewee-of-azerbaijan-today-magazine-is-nobel-prize-laureate-and-azerbaijani-scientist-bakhtiyar-sirajov/",
     "date": "10.12.2025",
     "az": "The Interviewee of Azerbaijan Today Magazine is Nobel Prize Laureate and Azerbaijani Scientist Bakhtiyar Sirajov",
     "en": "The Interviewee of Azerbaijan Today Magazine is Nobel Prize Laureate and Azerbaijani Scientist Bakhtiyar Sirajov"},
    {"section": 1, "kind": "article", "source": "crossmedia.az",
     "url": "https://crossmedia.az/az/article/61595", "date": "27.12.2025",
     "az": "Azərbaycanı dünyada yalnız mədəniyyətlə yox, elmlə də tanıtmalıyıq — MÜSAHİBƏ",
     "en": "We must present Azerbaijan to the world not only through culture but also through science — INTERVIEW"},
    {"section": 1, "kind": "article", "source": "azertag.az",
     "url": "https://azertag.az/xeber/nobel_sulh_mukafatchisi_azerbaycan_alimleri_qlobal_elmi_diplomatiyada_strateji_rol_oynaya_bilerler_musahibe-3872299",
     "date": "20.11.2025",
     "az": "Azərbaycan alimləri qlobal elmi diplomatiyada strateji rol oynaya bilərlər",
     "en": "Azerbaijani scientists can play a strategic role in global science diplomacy"},
    {"section": 1, "kind": "article", "source": "azertag.az",
     "url": "https://azertag.az/xeber/nobel_sulh_mukafatchisi_azerbaycanin_cografi_movqeyi_ve_choxmedeniyyetli_muhiti_elmi_emekdasliq_uchun_ideal_platformadir-3869179",
     "date": "19.11.2025",
     "az": "Azərbaycanın coğrafi mövqeyi və çoxmədəniyyətli mühiti elmi əməkdaşlıq üçün ideal platformadır",
     "en": "Azerbaijan's geographic position and multicultural environment are an ideal platform for scientific cooperation"},
    {"section": 1, "kind": "article", "source": "azertag.az",
     "url": "https://azertag.az/xeber/nobel_sulh_mukafatchisi_elm_bu_gun_en_guclu_diplomatiya_aletlerinden_biridir-3867627",
     "date": "18.11.2025",
     "az": "Elm bu gün ən güclü diplomatiya alətlərindən biridir",
     "en": "Today science is one of the most powerful tools of diplomacy"},
    {"section": 1, "kind": "article", "source": "azertag.az",
     "url": "https://azertag.az/xeber/bextiyar_siracov_suni_intellekt_ve_texnologiyalarin_inkisafi_azerbaycanli_gencler_uchun_fursetler_yaradir-3866151",
     "date": "17.11.2025",
     "az": "Süni intellekt və texnologiyaların inkişafı azərbaycanlı gənclər üçün fürsətlər yaradır",
     "en": "The development of AI and technologies creates opportunities for young Azerbaijanis"},
    {"section": 1, "kind": "article", "source": "bsu.edu.az",
     "url": "https://bsu.edu.az/az/news/bdu_mzunu_nobel_slh_mkafats_bxtiyar_siracov_tlblrl_grb",
     "date": "20.10.2025",
     "az": "BDU — Tətbiqi Riyaziyyat və Kibernetika fakültəsində görüş",
     "en": "Baku State University — meeting at the Faculty of Applied Mathematics and Cybernetics"},
    {"section": 1, "kind": "article", "source": "media.az",
     "url": "https://media.az/society/edinstvennyj-nobelevskij-laureat-iz-azerbajdzhana-intervyu-media-az-s-bahtiyarom-siradzhevym",
     "date": "01.08.2025",
     "az": "Media.az saytına müsahibə",
     "en": "Interview for Media.az"},
    {"section": 1, "kind": "article", "source": "wikipedia.org",
     "url": "https://az.wikipedia.org/wiki/B%C9%99xtiyar_Siracov", "date": "",
     "az": "Bəxtiyar Siracov — Vikipediya",
     "en": "Bakhtiyar Sirajov — Wikipedia"},
    {"section": 1, "kind": "video", "yt": "MDouThK8Jws", "source": "youtube.com", "date": "",
     "az": "Bəxtiyar Siracov — «Belə-belə işlər»",
     "en": "Bakhtiyar Sirajov — «Belə-belə işlər» (talk show)"},
    {"section": 1, "kind": "video", "yt": "IxUzCi_GSUM", "source": "youtube.com", "date": "09.12.2022",
     "az": "Dünya azərbaycanlı elm xadimlərinin İstanbul görüşü",
     "en": "Istanbul meeting of Azerbaijani scientists from around the world"},
    {"section": 1, "kind": "video", "yt": "pVq93infVi4", "source": "youtube.com", "date": "",
     "az": "Bəxtiyar Siracov — Diasporla İş üzrə Dövlət Komitəsi",
     "en": "Bakhtiyar Sirajov — State Committee on Work with Diaspora"},
    {"section": 1, "kind": "video", "yt": "nvenMGdjBh0", "source": "youtube.com", "date": "01.05.2012",
     "az": "Bəxtiyar Siracov — «Vətənimdir Azərbaycan», Xəzər TV",
     "en": "Bakhtiyar Sirajov — «Vətənimdir Azərbaycan», Khazar TV"},
    {"section": 1, "kind": "article", "source": "1news.az",
     "url": "https://1news.az/mobile/news/sotrudnik-magate-bahtiyar-siradzhov-nashey-molodezhi-nado-smelo-integrirovat-sya-v-mirovoe-soobschestvo-ikt-professionalov",
     "date": "04.04.2014",
     "az": "Сотрудник МАГАТЭ Бахтияр Сираджов: «Нашей молодежи надо смело интегрироваться в мировое сообщество ИКТ профессионалов»",
     "en": "Сотрудник МАГАТЭ Бахтияр Сираджов: «Нашей молодежи надо смело интегрироваться в мировое сообщество ИКТ профессионалов»"},
    {"section": 1, "kind": "article", "source": "kaspi.az",
     "url": "https://kaspi.az/az/azerbaycan-pasportunu-hele-de-cibinde-saxlayan-nobel-sulh-mukafatcisi-gr-gtur",
     "date": "",
     "az": "Azərbaycan pasportunu hələ də cibində saxlayan Nobel Sülh Mükafatçısı",
     "en": "The Nobel Peace Prize laureate who still keeps his Azerbaijani passport"},
    {"section": 1, "kind": "article", "source": "science.gov.az",
     "url": "https://science.gov.az/az/news/open/25906", "date": "",
     "az": "AMEA prezidenti MAQATE-də çalışan həmvətənimizlə görüşüb",
     "en": "ANAS President met our compatriot working at the IAEA"},
    {"section": 1, "kind": "article", "source": "xalqqazeti.az",
     "url": "https://xalqqazeti.az/az/medeniyyet/157303-nobelci-azerbaycanli-bextiyar-siracov",
     "date": "",
     "az": "Nobelçi azərbaycanlı — Bəxtiyar Siracov",
     "en": "The Nobel-winning Azerbaijani — Bakhtiyar Sirajov"},
    {"section": 1, "kind": "video", "yt": "QVxntDQn73M", "source": "youtube.com", "date": "",
     "az": "Nüfuzlu beynəlxalq agentlikdə işləyən yeganə azərbaycanlı: Bəxtiyar Siracov kimdir?",
     "en": "The only Azerbaijani working at a prestigious international agency: who is Bakhtiyar Sirajov?"},
    {"section": 1, "kind": "article", "source": "science.gov.az",
     "url": "https://science.gov.az/az/news/open/26180", "date": "",
     "az": "Bəxtiyar Siracov: «Xaricdə yaşayan alimlərimiz Azərbaycan elminin problemlərinin həllində yaxından iştirak etməlidirlər»",
     "en": "Bakhtiyar Sirajov: «Our scientists abroad should actively participate in solving the problems of Azerbaijani science»"},
    {"section": 1, "kind": "article", "source": "day.az",
     "url": "https://news.day.az/azerinews/1631079.html", "date": "",
     "az": "Vyana şəhərində «BİZ — Zəfər yoluna davam» təşəbbüs qrupunun toplantısı keçirilib",
     "en": "Meeting of the «WE — Continuing the Path to Victory» initiative group held in Vienna"},
    {"section": 1, "kind": "article", "source": "diaspor.gov.az",
     "url": "https://diaspor.gov.az/az/news-detail/dunya-sohretli-alim-bextiyar-siracova-heyder-eliyevin-100-illiyi-1923-2023-yubiley-medali-ile-teqdim-edilib-4587",
     "date": "",
     "az": "Dünya şöhrətli alim Bəxtiyar Siracova «Heydər Əliyevin 100 illiyi (1923-2023)» yubiley medalı təqdim edilib",
     "en": "World-renowned scientist Bakhtiyar Sirajov awarded the «100th Anniversary of Heydar Aliyev (1923-2023)» jubilee medal"},
    {"section": 1, "kind": "article", "source": "xalqqazeti.az",
     "url": "https://xalqqazeti.az/az/sosial-heyat/176579-nobelci-soydasimiz-xalq-qezetinde",
     "date": "30.04.2024",
     "az": "Nobelçi soydaşımız «Xalq qəzeti»ndə",
     "en": "Our Nobel-winning compatriot in «Xalq qəzeti»"},
    {"section": 1, "kind": "article", "source": "azertag.az",
     "url": "https://azertag.az/xeber/bdu_nun_nobel_sulh_mukafatchisi_olan_mezunu_telebe_jurnalistlerle_gorusub-3005854",
     "date": "16.05.2024",
     "az": "BDU-nun Nobel Sülh mükafatçısı olan məzunu tələbə-jurnalistlərlə görüşüb",
     "en": "BSU's Nobel Peace Prize laureate alumnus met with student journalists"},
    {"section": 1, "kind": "article", "source": "amu.edu.az",
     "url": "https://amu.edu.az/news/4199/azerbaycan-esilli-ilk-nobel-sulh-mukafatcisi-atu-nun-qonagi-olub",
     "date": "21.05.2024",
     "az": "Azərbaycan əsilli ilk Nobel Sülh mükafatçısı ATU-nun qonağı olub",
     "en": "The first Nobel Peace Prize laureate of Azerbaijani origin was a guest of AMU"},
    {"section": 1, "kind": "article", "source": "xalqqazeti.az",
     "url": "https://xalqqazeti.az/az/musahibe/177882-azerbaycanin-adini-dunya-elm-zirvesine",
     "date": "08.05.2024",
     "az": "Azərbaycanın adını dünya elm zirvəsinə yazmış soydaşımız",
     "en": "Our compatriot who inscribed Azerbaijan's name at the summit of world science"},
    {"section": 1, "kind": "article", "source": "xalqqazeti.az",
     "url": "https://xalqqazeti.az/az/last-news/178149-sevgimin-yurduna-men-qayidiram",
     "date": "10.05.2024",
     "az": "«Sevgimin yurdu»na «Mən qayıdıram…»",
     "en": "«I am returning…» to «the homeland of my love»"},
    {"section": 1, "kind": "video", "yt": "36RZqNFnNMo", "source": "youtube.com", "date": "13.05.2024",
     "az": "Bəxtiyar Siracov, Azad Azərbaycan TV, «Xəbərlər» verilişi",
     "en": "Bakhtiyar Sirajov, Azad Azerbaijan TV, «Xəbərlər» (News) programme"},
    {"section": 1, "kind": "video", "yt": "1MKGU1Px2qE", "source": "youtube.com", "date": "14.05.2024",
     "az": "Bəxtiyar Siracov, Azad Azərbaycan TV, «Xəbəriniz Olsun» verilişi",
     "en": "Bakhtiyar Sirajov, Azad Azerbaijan TV, «Xəbəriniz Olsun» programme"},
    {"section": 1, "kind": "article", "source": "iis.nsk.su",
     "url": "http://start.iis.nsk.su/persons/briabrin/index", "date": "",
     "az": "«СПЕКТР» layihəsi",
     "en": "The «SPEKTR» project"},
    # ── Section 2: Vienna International Centre exhibitions ──
    {"section": 2, "kind": "video", "yt": "Nlc2TwbU-aA", "source": "youtube.com",
     "az_date": "07–18 Noyabr 2016", "en_date": "7–18 November 2016",
     "az": "Bəhram Bağırzadənin VBM-də sərgisi (video)",
     "en": "Behram Bagirzade's exhibition at the Vienna International Centre (video)"},
    {"section": 2, "kind": "video", "yt": "URthEQbBPN8", "source": "youtube.com",
     "az_date": "07–18 Noyabr 2016", "en_date": "7–18 November 2016",
     "az": "Bəhram Bağırzadənin VBM-də sərgisi (fotolar)",
     "en": "Behram Bagirzade's exhibition at the Vienna International Centre (photos)"},
    {"section": 2, "kind": "video", "yt": "aUyPVqL0tEU", "source": "youtube.com",
     "az_date": "21 Mart – 1 Aprel 2016", "en_date": "21 March – 1 April 2016",
     "az": "Gənc rəssamlar Nərmin Abdullayeva və Dilşad İmranovanın VBM-də sərgisi (müsahibələr)",
     "en": "Exhibition of young artists Narmin Abdullayeva and Dilshad Imranova at the VIC (interviews)"},
    {"section": 2, "kind": "video", "yt": "76xgX-zIch0", "source": "youtube.com",
     "az_date": "21 Mart – 1 Aprel 2016", "en_date": "21 March – 1 April 2016",
     "az": "Gənc rəssamlar Nərmin Abdullayeva və Dilşad İmranovanın VBM-də sərgisi (açılış)",
     "en": "Exhibition of young artists Narmin Abdullayeva and Dilshad Imranova at the VIC (opening)"},
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
        "crumb_current": "Bəxtiyar Siracov — İnternet resursları",
        "crumb_aria": "Səhifə yolu",
        "title": "Bəxtiyar Siracov — İnternet resursları | DAAB",
        "meta_desc": "Nobel Sülh Mükafatçısı, DAAB İdarə Heyətinin həmsədri Dr. Bəxtiyar Siracov haqqında müsahibələr, tədbirlər, TV proqramları və video resursların toplusu.",
        "h1": "Bəxtiyar Siracov",
        "h1_em": "İnternet resursları",
        "subtitle": "Müsahibələr, tədbirlər, TV proqramları və video materiallar",
        "panel_title": "Bu səhifə haqqında",
        "panel_copy": "Nobel Sülh Mükafatçısı, DAAB İdarə Heyətinin həmsədri Dr. Bəxtiyar Siracov haqqında mətbuat, televiziya və onlayn resursların toplusu.",
        "sec1": "Müsahibələr, tədbirlər, TV proqramları",
        "sec2": "Vyana Beynəlxalq Mərkəzində (VBM) təşkil etdiyimiz sərgilərdən videolar",
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
        "crumb_current": "Bakhtiyar Sirajov — Internet resources",
        "crumb_aria": "Breadcrumb",
        "title": "Bakhtiyar Sirajov — Internet resources | WAAS",
        "meta_desc": "A collection of interviews, events, TV programmes and video resources about Dr. Bakhtiyar Sirajov — Nobel Peace Prize laureate and Co-Chair of the WAAS Executive Board.",
        "h1": "Bakhtiyar Sirajov",
        "h1_em": "Internet resources",
        "subtitle": "Interviews, events, TV programmes and video materials",
        "panel_title": "About this page",
        "panel_copy": "A curated collection of press, television and online resources about Dr. Bakhtiyar Sirajov — Nobel Peace Prize laureate and Co-Chair of the WAAS Executive Board.",
        "sec1": "Interviews, events, TV programmes",
        "sec2": "Videos from the exhibitions we organised at the Vienna International Centre (VIC)",
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
    "page_id": "sirajov-media",
    "slug": "bakhtiyar-sirajov-media",
    "thumb_dirname": THUMB_DIRNAME,
    "thumbs": THUMBS,
    "resources": RESOURCES,
    "strings": STRINGS,
}


def main() -> int:
    return write_pages(CFG)


if __name__ == "__main__":
    raise SystemExit(main())

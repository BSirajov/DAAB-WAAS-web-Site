#!/usr/bin/env python3
"""Build the "Teymur Rzayev — Video resursları" media index pages (AZ/EN).

Source of truth for the resource cards. Edit RESOURCES / STRINGS below and
re-run to regenerate both language pages:

    python helpers/_build_teymur_media.py

Writes:
    az/scientists/teymur-rzayev-media.html
    en/scientists/teymur-rzayev-media.html
"""
from __future__ import annotations

import json

from _paths import ROOT
from _scientist_media import write_pages

THUMB_DIRNAME = "teymur-rzayev-media-thumbnails"
_MANIFEST = ROOT / "helpers" / "_teymur_thumbs.json"
THUMBS = json.loads(_MANIFEST.read_text(encoding="utf-8")) if _MANIFEST.exists() else []

# All resources are YouTube videos, in the same order as the source page.
# `yt` is the YouTube video id; the thumbnail is the original hosted image.
RESOURCES = [
    {"section": 1, "kind": "video", "yt": "UsKD1PeWbJk", "source": "youtube.com", "date": "",
     "az": "Teymur Rzayev, Hacı Nuran — «Xeyir Körpüsü»",
     "en": "Teymur Rzayev, Haji Nuran — «Bridge of Goodness»"},
    {"section": 1, "kind": "video", "yt": "DVuIxdfJPf0", "source": "youtube.com", "date": "",
     "az": "Vətəndaş Rəssam Teymur Rzayev",
     "en": "Citizen Artist Teymur Rzayev"},
    {"section": 1, "kind": "video", "yt": "dwo30CQ86Zs", "source": "youtube.com", "date": "",
     "az": "Türk Dünyasının Rəngləri (7-ci bölüm — Prof. Dr. Teymur Rzayev)",
     "en": "Colours of the Turkic World (Episode 7 — Prof. Dr. Teymur Rzayev)"},
    {"section": 1, "kind": "video", "yt": "wav9PWUTog8", "source": "youtube.com", "date": "",
     "az": "Teymur Rzayev — Mikayıl Abdullayev 100",
     "en": "Teymur Rzayev — Mikayil Abdullayev 100"},
    {"section": 1, "kind": "video", "yt": "Cfqo0RR2amc", "source": "youtube.com", "date": "",
     "az": "Teymur Rzayev — «Sanat Durağı»",
     "en": "Teymur Rzayev — «Sanat Durağı» (Art Stop)"},
    {"section": 1, "kind": "video", "yt": "B2Xvw3zk83Q", "source": "youtube.com", "date": "",
     "az": "Teymur Rzayev 60 — Bakı Muğam Mərkəzi",
     "en": "Teymur Rzayev 60 — Baku Mugham Centre"},
    {"section": 1, "kind": "video", "yt": "SAn-7iC9_xc", "source": "youtube.com", "date": "",
     "az": "Türkiyədə uğur qazanmış azərbaycanlı rəssam — Teymur Rzayev",
     "en": "The Azerbaijani artist who found success in Türkiye — Teymur Rzayev"},
    {"section": 1, "kind": "video", "yt": "fm3sagVU2fU", "source": "youtube.com", "date": "",
     "az": "Teymur Rzayev & William Turner | Bir Rəsim Bir Hekayə | 31-ci bölüm",
     "en": "Teymur Rzayev & William Turner | One Painting, One Story | Episode 31"},
    {"section": 1, "kind": "video", "yt": "DCqHTreLdcc", "source": "youtube.com", "date": "",
     "az": "Azərbaycanın Dostları — Teymur Rzayev",
     "en": "Friends of Azerbaijan — Teymur Rzayev"},
    {"section": 1, "kind": "video", "yt": "uuZ7dXUheJI", "source": "youtube.com", "date": "",
     "az": "Əli bəy Hüseynzadənin şəxsi əşyalarının Bakıya gətirilməsi",
     "en": "The arrival of Ali bey Huseynzade's personal belongings in Baku"},
    {"section": 1, "kind": "video", "yt": "BBhDeatGoS4", "source": "youtube.com", "date": "",
     "az": "Teymur Rzayev & Jan Matejko | Bir Rəsim Bir Hekayə | 4-cü bölüm",
     "en": "Teymur Rzayev & Jan Matejko | One Painting, One Story | Episode 4"},
    {"section": 1, "kind": "video", "yt": "WUAad9I6fmw", "source": "youtube.com", "date": "",
     "az": "Əli bəy Hüseynzadə, Teymur Rzayev — Azərbaycan bayrağının təqdimatı",
     "en": "Ali bey Huseynzade, Teymur Rzayev — presentation of the Azerbaijani flag"},
    {"section": 1, "kind": "video", "yt": "4iJgOsEFKjY", "source": "youtube.com", "date": "",
     "az": "Nigar İsmayılqızı — Rəssam Teymur Rzayevlə söhbət, İstanbul",
     "en": "Nigar Ismayilgizi — a conversation with artist Teymur Rzayev, Istanbul"},
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
        "crumb_current": "Teymur Rzayev — Video resursları",
        "crumb_aria": "Səhifə yolu",
        "title": "Teymur Rzayev — Video resursları | DAAB",
        "meta_desc": "DAAB İdarə Heyətinin üzvü, Azərbaycan Respublikasının Əməkdar Rəssamı Prof. Dr. Teymur Rzayev haqqında müsahibələr, sənədli filmlər və televiziya proqramlarının toplusu.",
        "h1": "Teymur Rzayev",
        "h1_em": "Video resursları",
        "subtitle": "Müsahibələr, sənədli filmlər və televiziya proqramları",
        "panel_title": "Bu səhifə haqqında",
        "panel_copy": "DAAB İdarə Heyətinin üzvü, Azərbaycan Respublikasının Əməkdar Rəssamı Prof. Dr. Teymur Rzayev haqqında müsahibələr, sənədli filmlər və televiziya proqramlarının toplusu.",
        "sec1": "Müsahibələr, sənədli filmlər və televiziya proqramları",
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
        "crumb_current": "Teymur Rzayev — Video resources",
        "crumb_aria": "Breadcrumb",
        "title": "Teymur Rzayev — Video resources | WAAS",
        "meta_desc": "A collection of interviews, documentaries and television programmes about Prof. Dr. Teymur Rzayev — Honored Artist of the Republic of Azerbaijan and member of the WAAS Executive Board.",
        "h1": "Teymur Rzayev",
        "h1_em": "Video resources",
        "subtitle": "Interviews, documentaries and television programmes",
        "panel_title": "About this page",
        "panel_copy": "A collection of interviews, documentaries and television programmes about Prof. Dr. Teymur Rzayev — Honored Artist of the Republic of Azerbaijan and member of the WAAS Executive Board.",
        "sec1": "Interviews, documentaries and television programmes",
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
    "page_id": "teymur-media",
    "slug": "teymur-rzayev-media",
    "thumb_dirname": THUMB_DIRNAME,
    "thumbs": THUMBS,
    "resources": RESOURCES,
    "strings": STRINGS,
}


def main() -> int:
    return write_pages(CFG)


if __name__ == "__main__":
    raise SystemExit(main())

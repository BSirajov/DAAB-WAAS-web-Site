#!/usr/bin/env python3
"""Build bilingual human sitemap pages (az/sitemap.html, en/sitemap.html)."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path
from urllib.parse import quote

from _footer_leader_snippets import FOOTER_AZ_HTML, FOOTER_EN_HTML
from _inject_seo_head import build_seo_block
from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

ASSET = "../"
PAGE_ID = "sitemap"
NAV_ARIA = {"az": "Əsas naviqasiya", "en": "Main navigation"}
SKIP = {"az": "Məzmuna keç", "en": "Skip to content"}

PAGE_LABEL_KEYS = {
    "home": "home",
    "foundation": "foundation",
    "mission": "mission",
    "activities-news": "activitiesNews",
    "work-done-2024-2026": "activitiesWorkDone2024",
    "forum-2024": "forum2024",
    "forum-2026": "forum2026Year",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-official": "forumOfficial",
    "forum-rector-speeches": "forumRectorSpeeches",
    "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
    "forum-program": "forumProgram",
    "forum-logistics": "forumLogistics",
    "forum-sessions-organization": "forumSessionsOrganization",
    "forum-impressions": "forumImpressions",
    "forum-roadmap": "forumRoadmap",
    "forum-bagli-hekayeler": "forumBagliHekayeler",
    "forum-cooperation": "forumCooperation",
    "forum-photos-gallery": "forumPhotosGallery",
    "forum-video-gallery": "forumVideoGallery",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    "executive-board": "executiveBoard",
    "charter": "charter",
    "legal-notice": "legalNotice",
    "privacy": "privacy",
    "cookies": "cookies",
    "terms": "terms",
    "sitemap": "sitemap",
    "membership-value": "membershipWhy",
    "membership-application": "membershipJoin",
    "membership-flyer": "membershipFlyer",
    "sponsorship-partnership": "sponsorshipPartnership",
    "donate": "donate",
    "sponsors-flyer": "sponsorsFlyer",
}

# Pages marked new / updated (shown as badges on cards)
PAGE_BADGES = {
    "forum-2026": "new",
    "sitemap": "new",
    "privacy": "updated",
    "terms": "updated",
    "cookies": "updated",
    "legal-notice": "updated",
    "work-done-2024-2026": "updated",
}

START_HERE = [
    "home",
    "mission",
    "scientists-list",
    "membership-application",
    "forum-2024",
]

SECTION_ICONS = {
    "home": "🏠",
    "about": "🏛️",
    "activities": "📰",
    "forum-2024": "🎤",
    "forum-2026": "✨",
    "scientists": "🌐",
    "membership": "✒️",
    "sponsorship": "🤝",
    "legal": "⚖️",
    "resources": "📚",
    "documents": "📁",
    "help": "🧭",
}

SECTION_TONES = {
    "home": "1",
    "about": "2",
    "activities": "3",
    "forum-2024": "4",
    "forum-2026": "5",
    "scientists": "1",
    "membership": "2",
    "sponsorship": "3",
    "legal": "4",
    "resources": "5",
    "documents": "1",
    "help": "2",
}

RESOURCE_ICONS = {
    "sirajov-media": "🌐",
    "teymur-media": "🎬",
    "seymur-media": "📰",
    "akif-media": "📚",
    "eldar-ahadov": "✍️",
    "eldar-ahadov-poeziya": "📖",
    "eldar-ahadov-poetik-dastanlar": "📜",
    "eldar-ahadov-bedii-nesr": "📘",
    "eldar-ahadov-esse": "🖊️",
}

HELP_ICONS = ("🌐", "🔍", "🍪", "⚖️")

# (section_id, label_key OR None for custom title key in COPY, page_ids)
GROUPS: list[tuple[str, str, list[str]]] = [
    ("home", "home", ["home"]),
    ("about", "about", ["foundation", "mission", "executive-board", "charter"]),
    ("activities", "activities", ["activities-news", "work-done-2024-2026"]),
    (
        "forum-2024",
        "forum2024Year",
        [
            "forum-2024",
            "forum-logistics",
            "forum-program",
            "forum-sessions-organization",
            "forum-official",
            "forum-2024-presentations",
            "forum-rector-speeches",
            "forum-anas-leadership-speeches",
            "forum-impressions",
            "forum-photos-gallery",
            "forum-video-gallery",
            "forum-roadmap",
            "forum-bagli-hekayeler",
            "forum-cooperation",
        ],
    ),
    ("forum-2026", "forum2026Year", ["forum-2026"]),
    ("scientists", "scientists", ["scientists-list", "scientists-profiles"]),
    (
        "membership",
        "membership",
        ["membership-value", "membership-application", "membership-flyer"],
    ),
    (
        "sponsorship",
        "sponsors",
        ["sponsorship-partnership", "donate", "sponsors-flyer"],
    ),
    ("legal", "legalPages", ["privacy", "terms", "cookies", "legal-notice"]),
]

RESOURCE_PAGES = [
    {
        "id": "sirajov-media",
        "az": "Bəxtiyar Siracov — internet resursları",
        "en": "Bakhtiyar Sirajov — internet resources",
        "desc_az": "İnternet və media materialları",
        "desc_en": "Internet and media materials",
    },
    {
        "id": "teymur-media",
        "az": "Teymur Rzayev — video resursları",
        "en": "Teymur Rzayev — video resources",
        "desc_az": "Video reportaj və müsahibələr",
        "desc_en": "Video reports and interviews",
    },
    {
        "id": "seymur-media",
        "az": "Seymur Nəsirov — mətbuat resursları",
        "en": "Seymur Nasirov — press resources",
        "desc_az": "Mətbuat və media materialları",
        "desc_en": "Press and media materials",
    },
    {
        "id": "akif-media",
        "az": "Akif Alaferdov — kitablar",
        "en": "Akif Alaferdov — books",
        "desc_az": "Kitab və PDF nəşrlər",
        "desc_en": "Books and PDF publications",
    },
    {
        "id": "eldar-ahadov",
        "az": "Eldar Əhədov — ədəbi hub",
        "en": "Eldar Ahadov — literary hub",
        "desc_az": "Özüm haqqında və ədəbi bölmələr",
        "desc_en": "About the author and literary sections",
    },
    {
        "id": "eldar-ahadov-poeziya",
        "az": "Eldar Əhədov — poeziya",
        "en": "Eldar Ahadov — poetry",
        "desc_az": "Şeirlər",
        "desc_en": "Poems",
    },
    {
        "id": "eldar-ahadov-poetik-dastanlar",
        "az": "Eldar Əhədov — poetik dastanlar",
        "en": "Eldar Ahadov — poetic epics",
        "desc_az": "Poetik dastanlar",
        "desc_en": "Poetic epics",
    },
    {
        "id": "eldar-ahadov-bedii-nesr",
        "az": "Eldar Əhədov — bədii nəsr",
        "en": "Eldar Ahadov — literary prose",
        "desc_az": "Bədii nəsr nümunələri",
        "desc_en": "Literary prose",
    },
    {
        "id": "eldar-ahadov-esse",
        "az": "Eldar Əhədov — esse",
        "en": "Eldar Ahadov — essays",
        "desc_az": "Esse və analitik yazılar",
        "desc_en": "Essays and analytical writing",
    },
]

DOCUMENTS = [
    {
        "kind": "pdf",
        "href": "Books/DAAB_DK/"
        + quote("Xaricdə_yaşayan_Azərbaycanlı_Alimlərin_FORUMU_(27.04.2026).pdf"),
        "az": "I Forum hesabatı (PDF)",
        "en": "I Forum report (PDF)",
        "desc_az": "Dövlət Komitəsinə təqdim olunan forum hesabatı",
        "desc_en": "Forum report submitted to the State Committee",
        "type": "PDF",
    },
    {
        "kind": "page",
        "page_id": "membership-flyer",
        "az": "Üzvlük dəvət məktubu",
        "en": "Membership invitation letter",
        "desc_az": "Paylaşıla bilən dəvət mətni",
        "desc_en": "Shareable invitation letter",
        "type": "HTML",
    },
    {
        "kind": "page",
        "page_id": "sponsors-flyer",
        "az": "Sponsor dəvət məktubu",
        "en": "Sponsor invitation letter",
        "desc_az": "Potensial tərəfdaşlar üçün dəvət",
        "desc_en": "Invitation for potential partners",
        "type": "HTML",
    },
    {
        "kind": "page",
        "page_id": "forum-2024-presentations",
        "az": "Forum məruzələri",
        "en": "Forum presentations",
        "desc_az": "Təqdimat və məruzə arxivi",
        "desc_en": "Presentation archive",
        "type": "HTML",
    },
    {
        "kind": "page",
        "page_id": "akif-media",
        "az": "Akif Alaferdov — PDF kitablar",
        "en": "Akif Alaferdov — PDF books",
        "desc_az": "Kitab və foto toplusu yükləmələri",
        "desc_en": "Book and photo-collection downloads",
        "type": "PDF",
    },
    {
        "kind": "page",
        "page_id": "charter",
        "az": "Nizamnamə",
        "en": "Charter",
        "desc_az": "Birliyin əsas sənədi",
        "desc_en": "Governing document of the association",
        "type": "HTML",
    },
]

COPY = {
    "az": {
        "title": "DAAB — Saytın xəritəsi",
        "description": "DAAB veb-saytının bütün əsas səhifələrinin, resursların və sənədlərin axtarıla bilən xəritəsi.",
        "hero_h1": "Saytın xəritəsi",
        "hero_subtitle": "Bölmələr, resurslar və sənədlər — hamısı bir yerdə",
        "panel_title": "Bu səhifə haqqında",
        "panel_copy": "Saytın xəritəsi DAAB veb-saytının bütün əsas bölmələrini, alim resurslarını və sənədləri bir yerdə toplayır. Axtarış və bölmə keçidləri ilə istədiyiniz səhifəni tez tapa, saytın strukturunu aydın görə bilərsiniz.",
        "search_label": "Səhifə axtarışı",
        "search_placeholder": "Səhifə adı və ya açar söz yazın…",
        "clear_label": "Axtarışı təmizlə",
        "count_template": "{n} / {t} nəticə",
        "section_count": "{n}",
        "empty": "Uyğun səhifə tapılmadı. Başqa açar söz yoxlayın.",
        "jump_aria": "Bölmələrə keçid",
        "start_title": "Buradan başlayın",
        "start_lead": "İlk dəfə gələnlər üçün ən faydalı səhifələr",
        "lang_title": "Dil",
        "lang_current": "Hazırkı dil: Azərbaycan",
        "lang_switch": "İngiliscə aç",
        "lang_href": "../en/sitemap.html",
        "search_full": "Tam sayt axtarışı",
        "suggest_label": "Təklif olunan açar sözlər",
        "suggest": ["Forum", "üzvlük", "sponsor", "alimlər", "məxfilik"],
        "resources_title": "Əlavə resurslar",
        "resources_blurb": "Əsas menyuda göstərilməyən alim media və ədəbi səhifələr",
        "docs_title": "Sənədlər və yükləmələr",
        "docs_blurb": "PDF hesabatlar, dəvət məktubları və digər faydalı sənədlər",
        "help_title": "Necə istifadə etməli",
        "help_blurb": "Dil, axtarış, kukilər və hüquqi məlumat — qısa bələdçi",
        "help_items": [
            ("Dil dəyişimi", "Yuxarı sağdakı AZ / EN düyməsi və ya bu səhifədəki dil keçidi ilə.", None),
            ("Sayt axtarışı", "Naviqasiyadakı axtarış və ya bu səhifədəki «Tam sayt axtarışı» ilə.", "search"),
            ("Kuki parametrləri", "Hansı kukilərin aktiv olduğunu seçə bilərsiniz.", "cookies"),
            ("Hüquqi sənədlər", "Məxfilik, şərtlər, kukilər və hüquqi rekvizitlər — aşağıdakı Hüquqi bölmədə.", "#section-legal"),
        ],
        "cta_membership_title": "DAAB-a qoşulun",
        "cta_membership_text": "Üzvlük müraciəti və ya dəvət məktubu göndərin.",
        "cta_apply": "Müraciət edin",
        "cta_flyer": "Dəvət məktubu",
        "cta_support_title": "DAAB-ı dəstəkləyin",
        "cta_support_text": "Sponsorluq və ya ianə ilə missiyamıza töhfə verin.",
        "cta_sponsor": "Sponsorluq",
        "cta_donate": "İanə edin",
        "badge_new": "Yeni",
        "badge_updated": "Yenilənib",
        "twin_label": "EN",
        "twin_meta": "İngiliscə də mövcuddur",
        "blurbs": {
            "home": "Birliyin rəsmi ana səhifəsi və girişi",
            "about": "Təsis, missiya, idarə heyəti və nizamnamə",
            "activities": "Yeniliklər və 2024–2026 fəaliyyət nəticələri",
            "forum-2024": "Proqram, nitqlər, qalereyalar və nəticələr",
            "forum-2026": "Gələcək forumun konsepsiyası və hazırlıq istiqaməti",
            "scientists": "Alimlər kataloqu və akademik profillər",
            "membership": "Üzvlüyün dəyəri, müraciət və dəvət",
            "sponsorship": "Sponsorluq, ianə və tərəfdaşlıq",
            "legal": "Məxfilik, şərtlər, kukilər və hüquqi rekvizitlər",
            "resources": "Menyudan kənar media və ədəbi səhifələr",
            "documents": "PDF və digər yüklənə bilən materiallar",
            "help": "Saytdan istifadə üçün qısa bələdçi",
        },
    },
    "en": {
        "title": "WAAS — Sitemap",
        "description": "A searchable map of every main page, resource, and document on the WAAS website.",
        "hero_h1": "Sitemap",
        "hero_subtitle": "Sections, resources, and documents — all in one place",
        "panel_title": "About this page",
        "panel_copy": "The sitemap gathers every main section, scientist resource, and document on the WAAS site in one place. Use search and section jumps to find what you need quickly and see how the site is organised.",
        "search_label": "Search pages",
        "search_placeholder": "Type a page name or keyword…",
        "clear_label": "Clear search",
        "count_template": "{n} / {t} results",
        "section_count": "{n}",
        "empty": "No matching pages. Try a different keyword.",
        "jump_aria": "Jump to sections",
        "start_title": "Start here",
        "start_lead": "The most useful pages for first-time visitors",
        "lang_title": "Language",
        "lang_current": "Current language: English",
        "lang_switch": "Open in Azerbaijani",
        "lang_href": "../az/sitemap.html",
        "search_full": "Open full site search",
        "suggest_label": "Suggested keywords",
        "suggest": ["Forum", "membership", "sponsor", "scientists", "privacy"],
        "resources_title": "Additional resources",
        "resources_blurb": "Scientist media and literary pages not listed in the main menu",
        "docs_title": "Documents & downloads",
        "docs_blurb": "PDF reports, invitation letters, and other useful files",
        "help_title": "How to use this site",
        "help_blurb": "Language, search, cookies, and legal pages — a short guide",
        "help_items": [
            ("Language switch", "Use the AZ / EN control in the top bar, or the language link on this page.", None),
            ("Site search", "Use the search control in the navigation, or “Open full site search” above.", "search"),
            ("Cookie settings", "Choose which cookies are active.", "cookies"),
            ("Legal documents", "Privacy, terms, cookies, and imprint — see the Legal section below.", "#section-legal"),
        ],
        "cta_membership_title": "Join WAAS",
        "cta_membership_text": "Submit a membership application or send an invitation letter.",
        "cta_apply": "Apply now",
        "cta_flyer": "Invitation letter",
        "cta_support_title": "Support WAAS",
        "cta_support_text": "Contribute through sponsorship or a donation.",
        "cta_sponsor": "Sponsorship",
        "cta_donate": "Donate",
        "badge_new": "New",
        "badge_updated": "Updated",
        "twin_label": "AZ",
        "twin_meta": "Also available in Azerbaijani",
        "blurbs": {
            "home": "Official home page and entry point",
            "about": "Founding, mission, board, and charter",
            "activities": "News and 2024–2026 activity outcomes",
            "forum-2024": "Programme, speeches, galleries, and outcomes",
            "forum-2026": "Concept and direction for the next forum",
            "scientists": "Scientist directory and academic profiles",
            "membership": "Membership value, application, and invitation",
            "sponsorship": "Sponsorship, donations, and partnership",
            "legal": "Privacy, terms, cookies, and legal notice",
            "resources": "Media and literary pages outside the main menu",
            "documents": "PDFs and other downloadable materials",
            "help": "Short guide to using the website",
        },
    },
}


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def extract_nav(html_text: str, nav_aria: str) -> str:
    m = re.search(
        rf'(<nav aria-label="{re.escape(nav_aria)}" class="nav-strip">.*?</nav>)',
        html_text,
        re.DOTALL,
    )
    return m.group(1) if m else ""


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def page_by_id(routes: dict, page_id: str) -> dict | None:
    for page in routes.get("pages", []):
        if page.get("id") == page_id:
            return page
    return None


def label_for(ui: dict, lang: str, page_id: str) -> str:
    nav = ui.get("nav", {}).get(lang) or ui.get("nav", {}).get("az") or {}
    key = PAGE_LABEL_KEYS.get(page_id, page_id)
    return nav.get(key) or nav.get(page_id) or page_id


def group_label(ui: dict, lang: str, label_key: str) -> str:
    nav = ui.get("nav", {}).get(lang) or ui.get("nav", {}).get("az") or {}
    return nav.get(label_key) or label_key


def subtitle_for(subs: dict, lang: str, page_id: str) -> str:
    entry = (subs.get("pages") or {}).get(page_id) or {}
    return (entry.get(lang) or "").strip()


def href_for(page: dict, lang: str) -> str:
    rel = page.get(lang) or ""
    prefix = f"{lang}/"
    if rel.startswith(prefix):
        return rel[len(prefix) :]
    return rel


def search_blob(*parts: str) -> str:
    raw = " ".join(p for p in parts if p)
    return (
        raw.lower()
        .replace("ə", "e")
        .replace("ı", "i")
        .replace("ö", "o")
        .replace("ü", "u")
        .replace("ğ", "g")
        .replace("ş", "s")
        .replace("ç", "c")
    )


def badge_html(copy: dict, page_id: str) -> str:
    kind = PAGE_BADGES.get(page_id)
    if not kind:
        return ""
    label = copy["badge_new"] if kind == "new" else copy["badge_updated"]
    return f'<span class="sitemap-badge sitemap-badge--{kind}">{esc(label)}</span>'


def page_icon(ui: dict, page_id: str, fallback: str = "📄") -> str:
    icons = ui.get("navIcons") or {}
    key = PAGE_LABEL_KEYS.get(page_id, page_id)
    return icons.get(page_id) or icons.get(key) or fallback


def render_card(
    *,
    href: str,
    title: str,
    desc: str,
    search: str,
    page_id: str = "",
    badge: str = "",
    icon: str = "",
    extra_class: str = "",
    aria_current: bool = False,
    meta: str = "",
    external: bool = False,
    extra_attrs: str = "",
) -> str:
    cur = ' aria-current="page"' if aria_current else ""
    ext = ' target="_blank" rel="noopener noreferrer"' if external else ""
    meta_html = f'<span class="sitemap-link__meta">{esc(meta)}</span>' if meta else ""
    desc_html = f'<p class="sitemap-link__desc">{esc(desc)}</p>' if desc else ""
    pid = f' data-page-id="{esc(page_id)}"' if page_id else ""
    cls = "sitemap-link" + (f" {extra_class}" if extra_class else "")
    icon_html = (
        f'<span class="sitemap-link__icon" aria-hidden="true">{icon}</span>' if icon else ""
    )
    return (
        f'<li><a class="{cls}" href="{esc(href)}" data-search="{esc(search)}"'
        f"{pid}{cur}{ext}{extra_attrs}>"
        f"{icon_html}"
        f'<span class="sitemap-link__body">'
        f'<span class="sitemap-link__title"><span class="sitemap-link__name">{esc(title)}</span>{badge}</span>'
        f"{desc_html}{meta_html}</span>"
        f"</a></li>"
    )


def render_section(
    *,
    section_id: str,
    index: str,
    title: str,
    blurb: str,
    count_tpl: str,
    items: list[str],
    cta: str = "",
    icon: str = "📑",
) -> str:
    n = len(items)
    blurb_html = f'<p class="sitemap-section__blurb">{esc(blurb)}</p>' if blurb else ""
    tone = SECTION_TONES.get(section_id, "1")
    return (
        f'<section class="sitemap-section" id="section-{esc(section_id)}" '
        f'data-section-index="{index}" data-tone="{tone}" '
        f'aria-labelledby="sitemap-h-{esc(section_id)}">'
        f'<div class="sitemap-section__ornament" aria-hidden="true"></div>'
        f'<div class="sitemap-section__head">'
        f'<div class="sitemap-section__heading">'
        f'<span class="sitemap-section__mark" aria-hidden="true">'
        f'<span class="sitemap-section__icon">{icon}</span>'
        f'<span class="sitemap-section__index">{index}</span>'
        f"</span>"
        f'<div class="sitemap-section__titles">'
        f'<h2 class="sitemap-section__title" id="sitemap-h-{esc(section_id)}">{esc(title)}</h2>'
        f"{blurb_html}"
        f"</div></div>"
        f'<span class="sitemap-section__meta" data-count-template="{esc(count_tpl)}">'
        f"{esc(count_tpl.replace('{n}', str(n)))}</span>"
        f"</div>"
        f'<ul class="sitemap-grid">{"".join(items)}</ul>'
        f"{cta}"
        f"</section>"
    )


def render_cta_block(lang: str, kind: str) -> str:
    copy = COPY[lang]
    if kind == "membership":
        return (
            f'<div class="sitemap-cta sitemap-cta--membership" '
            f'data-search="{esc(search_blob(copy["cta_membership_title"], copy["cta_apply"]))}">'
            f'<span class="sitemap-cta__icon" aria-hidden="true">✒️</span>'
            f'<div class="sitemap-cta__copy">'
            f'<strong>{esc(copy["cta_membership_title"])}</strong>'
            f'<p>{esc(copy["cta_membership_text"])}</p></div>'
            f'<div class="sitemap-cta__actions">'
            f'<a class="btn btn-primary" href="application.html">{esc(copy["cta_apply"])}</a>'
            f'<a class="btn btn-secondary" href="membership_flyer.html">{esc(copy["cta_flyer"])}</a>'
            f"</div></div>"
        )
    if kind == "sponsorship":
        return (
            f'<div class="sitemap-cta sitemap-cta--support" '
            f'data-search="{esc(search_blob(copy["cta_support_title"], copy["cta_donate"]))}">'
            f'<span class="sitemap-cta__icon" aria-hidden="true">🤝</span>'
            f'<div class="sitemap-cta__copy">'
            f'<strong>{esc(copy["cta_support_title"])}</strong>'
            f'<p>{esc(copy["cta_support_text"])}</p></div>'
            f'<div class="sitemap-cta__actions">'
            f'<a class="btn btn-primary" href="sponsorship_partnership.html">{esc(copy["cta_sponsor"])}</a>'
            f'<a class="btn btn-secondary" href="donate.html">{esc(copy["cta_donate"])}</a>'
            f"</div></div>"
        )
    return ""


def render_body(lang: str, routes: dict, ui: dict, subs: dict) -> str:
    copy = COPY[lang]
    blurbs = copy["blurbs"]
    chips: list[str] = []
    sections: list[str] = []
    section_no = 0

    def chip_html(section_id: str, label: str) -> str:
        icon = SECTION_ICONS.get(section_id, "📑")
        tone = SECTION_TONES.get(section_id, "1")
        return (
            f'<li><a class="sitemap-chip" href="#section-{esc(section_id)}" data-tone="{tone}">'
            f'<span class="sitemap-chip__icon" aria-hidden="true">{icon}</span>'
            f'<span class="sitemap-chip__label">{esc(label)}</span></a></li>'
        )

    # Start here
    start_items: list[str] = []
    for pid in START_HERE:
        page = page_by_id(routes, pid)
        if not page:
            continue
        title = label_for(ui, lang, pid)
        desc = subtitle_for(subs, lang, pid)
        href = "index.html" if pid == "home" else href_for(page, lang)
        start_items.append(
            render_card(
                href=href,
                title=title,
                desc=desc,
                search=search_blob(title, desc, pid, copy["start_title"]),
                page_id=pid,
                badge=badge_html(copy, pid),
                icon=page_icon(ui, pid),
                extra_class="sitemap-link--start",
            )
        )

    # Main groups
    for section_id, label_key, page_ids in GROUPS:
        items: list[str] = []
        for pid in page_ids:
            page = page_by_id(routes, pid)
            if not page:
                continue
            title = label_for(ui, lang, pid)
            desc = subtitle_for(subs, lang, pid)
            href = "index.html" if pid == "home" else href_for(page, lang)
            items.append(
                render_card(
                    href=href,
                    title=title,
                    desc=desc,
                    search=search_blob(title, desc, pid, blurbs.get(section_id, "")),
                    page_id=pid,
                    badge=badge_html(copy, pid),
                    icon=page_icon(ui, pid),
                    aria_current=(pid == PAGE_ID),
                )
            )
        if not items:
            continue
        section_no += 1
        gtitle = group_label(ui, lang, label_key)
        chips.append(chip_html(section_id, gtitle))
        cta = ""
        if section_id == "membership":
            cta = render_cta_block(lang, "membership")
        elif section_id == "sponsorship":
            cta = render_cta_block(lang, "sponsorship")
        sections.append(
            render_section(
                section_id=section_id,
                index=f"{section_no:02d}",
                title=gtitle,
                blurb=blurbs.get(section_id, ""),
                count_tpl=copy["section_count"],
                items=items,
                cta=cta,
                icon=SECTION_ICONS.get(section_id, "📑"),
            )
        )

    # Resources
    res_items: list[str] = []
    for res in RESOURCE_PAGES:
        page = page_by_id(routes, res["id"])
        if not page:
            continue
        title = res[lang]
        desc = res[f"desc_{lang}"]
        href = href_for(page, lang)
        res_items.append(
            render_card(
                href=href,
                title=title,
                desc=desc,
                search=search_blob(title, desc, res["id"], copy["resources_title"]),
                page_id=res["id"],
                icon=RESOURCE_ICONS.get(res["id"]) or page_icon(ui, res["id"], "📚"),
            )
        )
    if res_items:
        section_no += 1
        chips.append(chip_html("resources", copy["resources_title"]))
        sections.append(
            render_section(
                section_id="resources",
                index=f"{section_no:02d}",
                title=copy["resources_title"],
                blurb=copy["resources_blurb"],
                count_tpl=copy["section_count"],
                items=res_items,
                icon=SECTION_ICONS["resources"],
            )
        )

    # Documents
    doc_items: list[str] = []
    for doc in DOCUMENTS:
        if doc["kind"] == "pdf":
            href = "../" + doc["href"]
            external = True
        else:
            page = page_by_id(routes, doc["page_id"])
            if not page:
                continue
            href = href_for(page, lang)
            external = False
        title = doc[lang]
        desc = doc[f"desc_{lang}"]
        doc_icon = "📄" if doc.get("type") == "PDF" else "📑"
        doc_items.append(
            render_card(
                href=href,
                title=title,
                desc=desc,
                search=search_blob(title, desc, doc.get("type", ""), copy["docs_title"]),
                page_id=doc.get("page_id", ""),
                icon=doc_icon,
                meta=doc["type"],
                external=external,
                extra_class="sitemap-link--doc",
            )
        )
    if doc_items:
        section_no += 1
        chips.append(chip_html("documents", copy["docs_title"]))
        sections.append(
            render_section(
                section_id="documents",
                index=f"{section_no:02d}",
                title=copy["docs_title"],
                blurb=copy["docs_blurb"],
                count_tpl=copy["section_count"],
                items=doc_items,
                icon=SECTION_ICONS["documents"],
            )
        )

    # Help
    help_items: list[str] = []
    for idx, (title, desc, action) in enumerate(copy["help_items"]):
        if action == "search":
            href = "#"
            extra = "sitemap-link--action"
            attrs = ' data-sitemap-action="search"'
        elif action == "cookies":
            href = "#"
            extra = "sitemap-link--action"
            attrs = ' data-sitemap-action="cookies"'
        elif action and action.startswith("#"):
            href = action
            extra = ""
            attrs = ""
        else:
            href = "#section-help"
            extra = ""
            attrs = ""
        blob = search_blob(title, desc, copy["help_title"])
        icon = HELP_ICONS[idx] if idx < len(HELP_ICONS) else "💡"
        help_items.append(
            render_card(
                href=href,
                title=title,
                desc=desc,
                search=blob,
                icon=icon,
                extra_class=extra,
                extra_attrs=attrs,
            )
        )
    section_no += 1
    chips.append(chip_html("help", copy["help_title"]))
    sections.append(
        render_section(
            section_id="help",
            index=f"{section_no:02d}",
            title=copy["help_title"],
            blurb=copy["help_blurb"],
            count_tpl=copy["section_count"],
            items=help_items,
            icon=SECTION_ICONS["help"],
        )
    )

    search_icon = (
        '<svg class="sitemap-search__icon" viewBox="0 0 24 24" fill="none" '
        'stroke="currentColor" stroke-width="2" aria-hidden="true">'
        '<circle cx="11" cy="11" r="7"/><path d="M20 20l-3.5-3.5"/></svg>'
    )

    return f"""
<section class="sitemap-start" aria-labelledby="sitemap-start-title">
  <div class="sitemap-start__ornament" aria-hidden="true"></div>
  <div class="sitemap-start__head">
    <span class="sitemap-start__mark" aria-hidden="true">✨</span>
    <div>
      <h2 id="sitemap-start-title">{esc(copy["start_title"])}</h2>
      <p>{esc(copy["start_lead"])}</p>
    </div>
  </div>
  <ul class="sitemap-grid sitemap-grid--start">{"".join(start_items)}</ul>
</section>

<div class="sitemap-controls" role="search">
  <div class="sitemap-search-row">
    <div class="sitemap-search">
      <label class="visually-hidden" for="sitemap-filter">{esc(copy["search_label"])}</label>
      {search_icon}
      <input id="sitemap-filter" class="sitemap-search__input" type="search"
        autocomplete="off" spellcheck="false"
        placeholder="{esc(copy["search_placeholder"])}"
        aria-controls="sitemap-sections"/>
      <button type="button" id="sitemap-filter-clear" class="sitemap-search__clear"
        hidden aria-label="{esc(copy["clear_label"])}">✕</button>
    </div>
    <p id="sitemap-count" class="sitemap-count"
      data-label-template="{esc(copy["count_template"])}"></p>
  </div>
  <ul class="sitemap-chips" aria-label="{esc(copy["jump_aria"])}">
    {"".join(chips)}
  </ul>
</div>
<div class="sitemap-sections" id="sitemap-sections">
  {"".join(sections)}
</div>
<p id="sitemap-empty" class="sitemap-empty" role="status">{esc(copy["empty"])}</p>
""".strip()


def shell_head(cfg: dict, lang: str) -> str:
    sv = SCRIPT_VERSIONS
    st = STYLE_VERSIONS
    pair = {"az": "az/sitemap.html", "en": "en/sitemap.html"}
    seo = build_seo_block(
        rel_path=pair[lang],
        lang=lang,
        title=cfg["title"],
        description=cfg["description"],
        asset=ASSET,
        pair=pair,
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="{ASSET}" data-daab-page-id="{PAGE_ID}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(cfg["title"])}</title>
<meta name="description" content="{esc(cfg["description"])}"/>
{seo}
<link href="{ASSET}css/daab-fonts.css?v={st["daab-fonts.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-perf.css?v={st["daab-perf.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sticky-chrome.css?v={st["daab-sticky-chrome.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v={st["daab-back-to-top.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sitemap.css?v={st["daab-sitemap.css"]}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-perf.js?v={sv["daab-perf.js"]}" defer></script>
<script src="{ASSET}js/daab-sticky-chrome.js?v={sv["daab-sticky-chrome.js"]}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-design-tokens.js?v={sv["daab-design-tokens.js"]}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v={sv["daab-breadcrumbs.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v={sv["daab-page-subtitle.js"]}" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
<script src="{ASSET}js/daab-cookie-consent.js?v={sv.get("daab-cookie-consent.js", 1)}" defer></script>
<script src="{ASSET}js/daab-analytics.js?v={sv["daab-analytics.js"]}" defer></script>
<script src="{ASSET}js/daab-sitemap.js?v={sv["daab-sitemap.js"]}" defer></script>
</head>
"""


def build_page(lang: str, routes: dict, ui: dict, subs: dict) -> None:
    copy = COPY[lang]
    src = (ROOT / lang / "membership_value.html").read_text(encoding="utf-8")
    nav = extract_nav(src, NAV_ARIA[lang])
    if not nav:
        raise SystemExit(f"Could not extract nav from membership_value ({lang})")
    footer = FOOTER_AZ_HTML if lang == "az" else FOOTER_EN_HTML
    body = render_body(lang, routes, ui, subs)

    page = shell_head(copy, lang) + f"""<body class="sitemap-page">
<a class="skip" href="#content">{SKIP[lang]}</a>
{nav}
<header class="hero">
<div class="hero-wrap shell">
<section>
<h1 id="page-title" aria-describedby="page-hero-subtitle">{esc(copy["hero_h1"])}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(copy["hero_subtitle"])}</p>
</section>
<aside aria-label="{esc(copy["panel_title"])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(copy["panel_title"])}</h2>
<div class="panel-copy"><p class="panel-copy-lead">{esc(copy["panel_copy"])}</p></div>
</div>
</aside>
</div>
</header>
<main class="main sitemap-main" id="content">
{body}
</main>
{footer}
</body>
</html>
"""
    out = ROOT / lang / "sitemap.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"  wrote {out.relative_to(ROOT)}")


def main() -> int:
    routes = load_json(ROOT / "i18n" / "routes.json")
    ui = load_json(ROOT / "i18n" / "ui.json")
    subs = load_json(ROOT / "i18n" / "page-subtitles.json")
    print("Building sitemap pages…")
    for lang in ("az", "en"):
        build_page(lang, routes, ui, subs)
    print("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

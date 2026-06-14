#!/usr/bin/env python3
"""
Build and export the DAAB / WAAS Website Business Requirements Document (BRD).

Reverse-engineers current site structure, navigation, content, and functionality
into a publication-ready Word file.

Run from repo root:
  python helpers/_export_brd_docx.py
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

try:
    from _paths import ROOT
except ImportError:
    ROOT = Path(__file__).resolve().parents[1]

from daab_docx_export import export_markdown_to_docx  # noqa: E402

MD_PATH = ROOT / "documents" / "DAAB-Website-Business-Requirements.md"
OUT_PATH = ROOT / "documents" / "docx" / "DAAB-Website-Business-Requirements.docx"
ROUTES_PATH = ROOT / "i18n" / "routes.json"
UI_PATH = ROOT / "i18n" / "ui.json"
NAV_PATH = ROOT / "i18n" / "nav.json"


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _nav_label(ui: dict, lang: str, key: str) -> str:
    return ui.get("nav", {}).get(lang, {}).get(key, key)


def _page_row(page_id: str, spec: dict, routes: dict, ui: dict) -> str:
    route = next((p for p in routes["pages"] if p["id"] == page_id), None)
    az_path = route["az"].replace("az/", "") if route else "—"
    en_path = route["en"].replace("en/", "") if route else "—"
    group = route.get("navGroup") or "—" if route else "—"

    def cell(key: str) -> str:
        val = spec.get(key, "—")
        if isinstance(val, list):
            return "; ".join(val)
        return str(val)

    return (
        f"| **{spec['name_en']}** | `{az_path}` / `{en_path}` | {group} | "
        f"{cell('purpose')} | {cell('content_blocks')} | {cell('navigation')} | "
        f"{cell('interactive')} | {cell('media')} | {cell('functional')} | {cell('design')} |"
    )


PAGE_SPECS: dict[str, dict] = {
    "gateway": {
        "name_en": "Language gateway",
        "name_az": "Dil seçimi",
        "purpose": "Entry point; redirect to AZ or EN home; optional explicit language choice",
        "content_blocks": "Brand logo; association title; AZ/EN action buttons; explanatory note",
        "navigation": "No primary nav; links to az/index.html and en/index.html",
        "interactive": "Auto-redirect via localStorage; ?choose=1 forces chooser; ?lang=az|en override",
        "media": "DAAB logo SVG",
        "functional": "Must preserve query string on redirect; default language AZ",
        "design": "Centered card on site background; gateway gradient overlay",
    },
    "home": {
        "name_en": "Home",
        "name_az": "Ana səhifə",
        "purpose": "Introduce DAAB/WAAS; route visitors to major sections via hub cards",
        "content_blocks": "Hero with title, subtitle, summary panel; intro strip; section card grid; join banner",
        "navigation": "Full top nav; breadcrumbs omitted; cards link to About, Scientists, Activities, Membership, Forum",
        "interactive": "Site search; language switcher; mobile hamburger menu; back-to-top",
        "media": "Brand logo; optional partner imagery in cards; diaspora body background",
        "functional": "data-daab-page-id=home; JSON-driven nav when data-daab-nav-mount=1",
        "design": "Hub card layout (daab-hub-cards.css); hero summary panel; Playfair + Inter typography",
    },
    "foundation": {
        "name_en": "Foundation of the Association",
        "name_az": "Birliyin təsisi",
        "purpose": "Document founding history and Istanbul establishment narrative",
        "content_blocks": "Hero; page subtitle; long-form article sections; historical images",
        "navigation": "About dropdown; section nav (Foundation, Mission, Board, Charter); breadcrumbs",
        "interactive": "Language switch with scroll preservation; search",
        "media": "Historical photos (Şuşa congress, Istanbul founding, etc.)",
        "functional": "Shared content-hero pattern; justified prose",
        "design": "Content hero + foundation-page.css; white content cards on patterned background",
    },
    "mission": {
        "name_en": "Mission, vision and values",
        "name_az": "Missiya və dəyərlər",
        "purpose": "State organizational mission, vision, and core academic values",
        "content_blocks": "Hero; subtitle; mission/vision/value panels or sections",
        "navigation": "About dropdown landing; section nav; breadcrumbs",
        "interactive": "Language switch; search",
        "media": "Optional illustrative imagery in hero",
        "functional": "About section landing page in nav.json",
        "design": "daab-content-hero.css + daab-mission-page.css",
    },
    "executive-board": {
        "name_en": "Executive Board",
        "name_az": "İdarə heyəti",
        "purpose": "Present leadership and board member profiles",
        "content_blocks": "Hero; board member cards with photos, roles, affiliations; QR codes on cards",
        "navigation": "About dropdown; section nav; breadcrumbs",
        "interactive": "QR scan opens profile or contact context (where configured)",
        "media": "Portrait photos; QR code images",
        "functional": "Uses scientists-profile-qr.css patterns",
        "design": "Executive Board grid; responsive card stack on mobile",
    },
    "charter": {
        "name_en": "Charter (bylaws)",
        "name_az": "Nizamnamə",
        "purpose": "Publish official charter articles for legal/governance reference",
        "content_blocks": "Hero; table-of-contents sidebar widget; numbered articles; annexes",
        "navigation": "About dropdown; section nav; in-page TOC links; breadcrumbs",
        "interactive": "Sidebar TOC jump links; language switch preserves section where possible",
        "media": "Minimal; text-focused legal document styling",
        "functional": "Print-friendly article layout; anchor links per article",
        "design": "Legal document typography; daab-charter-page.css; sidebar widget",
    },
    "activities": {
        "name_en": "News and activities",
        "name_az": "Yeniliklər / Fəaliyyətimiz",
        "purpose": "Publish association news, events, and activity timeline",
        "content_blocks": "Hero; timeline or news cards; dated entries; sidebar timeline widget",
        "navigation": "Activities dropdown; breadcrumbs; links to Forum 2024 hub",
        "interactive": "Sidebar timeline jumps (daab-sidebar-timeline.js); search",
        "media": "News thumbnails where present",
        "functional": "Long scroll page; sticky chrome offsets",
        "design": "Activities layout CSS; card headers with blue gradient",
    },
    "scientists-list": {
        "name_en": "Scientists directory (list view)",
        "name_az": "Alimlər siyahısı",
        "purpose": "Tabular catalogue of Azerbaijani scientists abroad with sort/filter",
        "content_blocks": "Hero; toolbar (search, filters); sortable data table; row hover preview",
        "navigation": "Scientists dropdown; section nav (List, Profiles); breadcrumbs",
        "interactive": "Column sort; country/field filters; resizable columns; hover preview popover; mobile filter drawer",
        "media": "Scientist thumbnails in preview popover",
        "functional": "scientists-catalog-data.js (~83 records); AZ/EN data files; collation for AZ alphabet",
        "design": "Catalogue toolbar; table layout; scientists-list-page.css",
    },
    "scientists-profiles": {
        "name_en": "Academic profiles catalogue",
        "name_az": "CV kataloqu / Profillər",
        "purpose": "Card-based CV profiles with search, filters, TTS, and deep linking",
        "content_blocks": "Hero; sticky filter toolbar; profile cards (photo, bio, fields, QR); pagination",
        "navigation": "Scientists dropdown; section nav; breadcrumbs; #slug deep links",
        "interactive": "Multi-filter search; sort; pagination; TTS read-aloud; QR codes; URL hash opens card",
        "media": "Portrait photos; QR per profile",
        "functional": "scientists-cv-filters.js; daab-profile-tts.js; daab-profile-deep-link.js; sticky toolbar",
        "design": "Card grid; sticky toolbar on desktop; collapsible filters on mobile",
    },
    "membership-value": {
        "name_en": "Why become a member",
        "name_az": "Niyə üzv olmalı",
        "purpose": "Explain membership benefits and value proposition",
        "content_blocks": "Hero; benefit sections; CTA to application and terms",
        "navigation": "Membership dropdown landing; section nav (4 membership pages); breadcrumbs",
        "interactive": "CTA buttons; language switch",
        "media": "Iconography in benefit blocks",
        "functional": "Membership funnel entry page",
        "design": "daab-membership-value.css; hero summary panel",
    },
    "membership": {
        "name_en": "Membership terms",
        "name_az": "Üzvlük şərtləri",
        "purpose": "Define membership categories, fees, rights, and obligations",
        "content_blocks": "Hero; terms sections; fee tables; procedural text",
        "navigation": "Membership dropdown; section nav; breadcrumbs",
        "interactive": "Links to application and flyer",
        "media": "Minimal",
        "functional": "Legal/informational reference for applicants",
        "design": "daab-membership-page.css + content hero",
    },
    "membership-application": {
        "name_en": "Membership application",
        "name_az": "Üzvlük müraciəti",
        "purpose": "Collect membership applications via multi-step online form",
        "content_blocks": "Hero; 4-step wizard (personal, academic, documents, review); progress indicator",
        "navigation": "Membership dropdown; section nav; breadcrumbs",
        "interactive": "Step navigation; field validation UI; progress bar (client-side)",
        "media": "Form UI only",
        "functional": "daab-membership-application.js on az/application.html and en/application.html",
        "design": "daab-membership-application.css; accessible form controls",
    },
    "membership-flyer": {
        "name_en": "Membership invitation flyer",
        "name_az": "Dəvət flyeri",
        "purpose": "Printable/shareable invitation for potential members",
        "content_blocks": "A4 flyer sheet (brand, pillars, benefits, youth, CTA, QR); page controls toolbar",
        "navigation": "Membership dropdown; section nav; standard site chrome above flyer",
        "interactive": "Print/PDF (single-page jsPDF export); Share (Web Share API or download + mailto); controls hidden from export",
        "media": "Logos; QR code; decorative flyer layout",
        "functional": "html2canvas + jsPDF CDN; off-screen A4 clone; generatePdfBlob pipeline",
        "design": "daab-membership-flyer.css; A4 print/PDF fidelity requirements",
    },
    "forum-2024": {
        "name_en": "Forum 2024 hub",
        "name_az": "Forum 2024",
        "purpose": "Overview and entry point for all Forum 2024 materials",
        "content_blocks": "Hero; partner logos (DİDK, ETN); hub card grid to 11 subpages",
        "navigation": "Activities dropdown; forum section nav (12 pills); breadcrumbs",
        "interactive": "Card navigation; search",
        "media": "Partner logos; forum branding",
        "functional": "Forum microsite root; not in top-level bar as separate item",
        "design": "Hub cards + forum section nav icons from ui.json navIcons",
    },
    "forum-official": {
        "name_en": "Official addresses",
        "name_az": "Rəsmi müraciətlər",
        "purpose": "Publish formal opening addresses and official forum statements",
        "content_blocks": "Hero; speech/article cards; long-form justified text",
        "navigation": "Forum section nav; breadcrumbs; presentations-style TOC where used",
        "interactive": "In-page anchors; search",
        "media": "Speaker photos in speech layout",
        "functional": "Long-form reading; print-friendly",
        "design": "daab-forum-content.css; daab-presentations-toc.css",
    },
    "forum-rector-speeches": {
        "name_en": "University rectors' speeches",
        "name_az": "Rektorların çıxışları",
        "purpose": "Present rectors' forum contributions",
        "content_blocks": "Hero; speech sections with photos and attributed text",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Anchor navigation within speeches",
        "media": "Rector portrait photos (daab-speech-photos.css)",
        "functional": "Static content page",
        "design": "Speech photo + text layout",
    },
    "forum-anas-leadership-speeches": {
        "name_en": "ANAS leadership speeches",
        "name_az": "AMEA rəhbərliyinin çıxışları",
        "purpose": "Present ANAS leadership forum addresses",
        "content_blocks": "Hero; speech sections with photos",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Anchor links",
        "media": "Leadership photos",
        "functional": "Static content page",
        "design": "Speech layout CSS",
    },
    "forum-program": {
        "name_en": "Forum programme",
        "name_az": "Forum proqramı",
        "purpose": "Publish schedule and session structure of Forum 2024",
        "content_blocks": "Hero; programme tables/sections by day or track",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Search; optional sidebar",
        "media": "Minimal",
        "functional": "Reference schedule for participants and press",
        "design": "Forum content cards; tables where applicable",
    },
    "forum-2024-presentations": {
        "name_en": "Presentations and papers",
        "name_az": "Məruzələr",
        "purpose": "Table of contents for forum presentations and paper titles",
        "content_blocks": "Hero; TOC sidebar; presentation entries with authors",
        "navigation": "Forum section nav; sidebar TOC jumps; breadcrumbs",
        "interactive": "Sidebar widget navigation",
        "media": "Minimal text TOC",
        "functional": "Academic reference listing",
        "design": "daab-presentations-toc.css; sidebar widget",
    },
    "forum-impressions": {
        "name_en": "Forum impressions",
        "name_az": "Təəssüratlar",
        "purpose": "Share participant impressions and reflective essays",
        "content_blocks": "Hero; impression articles; photo-text layouts",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Search",
        "media": "Impression photos (daab-impressions-photos.css)",
        "functional": "Static editorial content",
        "design": "Photo + prose layout",
    },
    "forum-photos-gallery": {
        "name_en": "Photo gallery",
        "name_az": "Foto qalereya",
        "purpose": "Browse categorized Forum 2024 photographs with lightbox",
        "content_blocks": "Hero; category sections; thumbnail grids; lightbox overlay",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Category expand; lazy-loaded thumbnails; lightbox prev/next; keyboard navigation",
        "media": "Hundreds of JPGs in images/photos-gallery/ with _thumbs variants",
        "functional": "daab-photos-gallery.js; photos-gallery-manifest.json; thumbs manifest",
        "design": "daab-photos-gallery.css; responsive grid",
    },
    "forum-video-gallery": {
        "name_en": "Video gallery",
        "name_az": "Video qalereya",
        "purpose": "Link to Forum 2024 video recordings (YouTube)",
        "content_blocks": "Hero; video cards with titles and external links",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "External YouTube links open in new tab",
        "media": "YouTube thumbnails / embed links",
        "functional": "Static HTML; maintenance via helpers and video-gallery-data.json (build-time)",
        "design": "daab-video-gallery.css",
    },
    "forum-roadmap": {
        "name_en": "Strategic roadmap",
        "name_az": "Strateji yol xəritəsi",
        "purpose": "Present post-forum strategic priorities and roadmap",
        "content_blocks": "Hero; roadmap cards; sidebar widget",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Sidebar jumps",
        "media": "Icons in roadmap cards",
        "functional": "Policy/strategy communication",
        "design": "Forum content + sidebar widget",
    },
    "forum-bagli-hekayeler": {
        "name_en": "Forum stories",
        "name_az": "Hekayələr",
        "purpose": "Narrative stories related to Forum 2024",
        "content_blocks": "Hero; story articles; timeline sidebar",
        "navigation": "Forum section nav; daab-sidebar-timeline.js; breadcrumbs",
        "interactive": "Timeline sidebar navigation; story TTS script exists but not wired on live page",
        "media": "Story imagery inline",
        "functional": "Long-form narrative content",
        "design": "Forum content + timeline sidebar",
    },
    "forum-cooperation": {
        "name_en": "Contributions and cooperation",
        "name_az": "Töhfələr",
        "purpose": "Document institutional contributions and cooperation outcomes",
        "content_blocks": "Hero; cooperation sections; justified long-form text",
        "navigation": "Forum section nav; breadcrumbs",
        "interactive": "Search",
        "media": "Optional inline images",
        "functional": "Static content",
        "design": "Forum content cards",
    },
}


def build_markdown() -> str:
    routes = _load_json(ROUTES_PATH)
    ui = _load_json(UI_PATH)
    nav = _load_json(NAV_PATH)
    today = datetime.now().strftime("%d %B %Y")

    lines: list[str] = []
    append = lines.append

    append("# DAAB / WAAS Website — Business Requirements Document (BRD)")
    append("")
    append("Reverse-engineered from the current bilingual static website (May 2026).")
    append("")
    append(f"**Document version:** 1.0  ")
    append(f"**Date:** {today}  ")
    append("**Status:** As-built requirements baseline for stakeholders, designers, and developers")
    append("")
    append("---")
    append("")

    # 1 Purpose
    append("## 1. Purpose of the website")
    append("")
    append(
        "The **Dünya Azərbaycanlı Alimlər Birliyi (DAAB)** / **World Association of "
        "Azerbaijani Scientists (WAAS)** official website is a bilingual, static web presence "
        "that serves the global community of Azerbaijani scientists and the broader public."
    )
    append("")
    append("### 1.1 Institutional mission (as reflected on the site)")
    append("")
    append("- Present the Association's **founding story**, **mission**, **governance**, and **charter**.")
    append("- Publish **news and activities**, with a dedicated **Forum 2024** microsite.")
    append("- Maintain a **directory and profile catalogue** of Azerbaijani scientists abroad.")
    append("- Explain **membership benefits and terms**, provide an **online application**, and support **invitation/sharing** via a printable flyer.")
    append("- Offer **AZ** and **EN** parity for international and diaspora audiences.")
    append("")
    append("### 1.2 Target audience")
    append("")
    append("| Audience | Primary needs met by the site |")
    append("|----------|------------------------------|")
    append("| General public & diaspora | Learn about DAAB/WAAS, Forum 2024, and activities |")
    append("| Potential members | Understand benefits, terms, apply online, receive invitations |")
    append("| Current members | Reference charter, board, news |")
    append("| Scientists listed in catalogue | Discoverable profiles, QR/deep links |")
    append("| Partner institutions | Forum cooperation, official addresses, roadmap |")
    append("| Press & researchers | Speeches, programme, presentations, galleries |")
    append("| Site maintainers | Predictable structure, i18n JSON, helper scripts |")
    append("")
    append("### 1.3 Language and branding")
    append("")
    append("- **Default language:** Azerbaijani (`az/`).")
    append("- **English mirror:** `en/` with WAAS branding in titles.")
    append("- **Configuration:** `i18n/routes.json`, `i18n/ui.json`, `i18n/nav.json`.")
    append("")

    # 2 Scope
    append("## 2. Website scope")
    append("")
    append("### 2.1 Delivered site structure")
    append("")
    append("| Area | AZ path prefix | EN path prefix | Page count (per locale) |")
    append("|------|----------------|----------------|-------------------------|")
    append("| Language gateway | `index.html` | `index.html` | 1 (shared) |")
    append("| Site core | `az/*.html` | `en/*.html` | 10 |")
    append("| Scientists | `az/scientists/` | `en/scientists/` | 2 |")
    append("| Forum 2024 | `az/forum/2024/` | `en/forum/2024/` | 12 |")
    append("")
    append("**Total mirrored content pages:** 26 × 2 locales = **52**, plus the language gateway.")
    append("")
    append("### 2.2 Technology scope")
    append("")
    append("- Static HTML, CSS, JavaScript — no server-side application runtime in production.")
    append("- Client-side interactivity: search index, scientists filters, galleries, forms, PDF export.")
    append("- Content maintenance via HTML editing and Python helpers in `helpers/` (not deployed).")
    append("")
    append("### 2.3 Out of scope (current implementation)")
    append("")
    append("- Authenticated member portal or CMS admin UI.")
    append("- Server-side storage of membership applications (see storage strategy doc for future options).")
    append("- Automated machine translation; all copy is hand-maintained in AZ/EN pairs.")
    append("")

    # 3 Stakeholders
    append("## 3. Stakeholders and user groups")
    append("")
    append("| Stakeholder / user group | Role | Site expectations |")
    append("|--------------------------|------|-------------------|")
    append("| Visitor | Anonymous reader | Clear navigation, readable content, mobile access |")
    append("| Potential member | Prospective applicant | Benefits, terms, application, flyer share/print |")
    append("| Member scientist | Listed in catalogue | Accurate profile, QR/deep link, list + card views |")
    append("| Executive Board | Governance visibility | Board page with photos and roles |")
    append("| Partner / institution | Forum cooperation | Official texts, roadmap, galleries |")
    append("| Content editor | Staff updating HTML/JSON | Consistent templates, rebuild scripts, validation |")
    append("| Web administrator | Deploy & cache | Ship az/, en/, css/, js/, images/, i18n/ only |")
    append("| Developer | Maintenance | Central tokens, route map, version bumps, validators |")
    append("")

    # 4 Page-by-page
    append("## 4. Page-by-page requirements")
    append("")
    append(
        "Each row describes one logical page (AZ and EN mirrors share requirements). "
        "Paths are relative to the locale folder."
    )
    append("")
    append(
        "| Page | Paths (AZ / EN) | Nav group | Purpose | Main content blocks | "
        "Navigation elements | Interactive elements | Media | Functional reqs | Design reqs |"
    )
    append(
        "|------|-----------------|-----------|---------|---------------------|"
        "---------------------|----------------------|-------|-----------------|-------------|"
    )

    ordered_ids = ["gateway"] + [p["id"] for p in sorted(routes["pages"], key=lambda x: x.get("navOrder", 99))]
    seen: set[str] = set()
    for page_id in ordered_ids:
        if page_id in seen:
            continue
        seen.add(page_id)
        spec = PAGE_SPECS.get(page_id)
        if not spec:
            continue
        if page_id == "gateway":
            append(
                "| **Language gateway** | `index.html` | — | "
                f"{spec['purpose']} | {spec['content_blocks']} | {spec['navigation']} | "
                f"{spec['interactive']} | {spec['media']} | {spec['functional']} | {spec['design']} |"
            )
        else:
            append(_page_row(page_id, spec, routes, ui))

    append("")
    append("### 4.1 Language/version requirements (all pages)")
    append("")
    append("- Every public content page MUST exist in **both** AZ and EN with equivalent structure.")
    append("- `<html lang>` and `data-daab-lang` MUST match the folder (`az` or `en`).")
    append("- `data-daab-page-id` MUST match `i18n/routes.json` page id for i18n, breadcrumbs, and language pairing.")
    append("- Language switcher MUST open the alternate locale URL from `routes.json`.")
    append("- Public pages live under az/ and en/; use routes.json for language pairs.")
    append("")

    # 5 Navigation
    append("## 5. Navigation and information architecture")
    append("")
    append("### 5.1 Top-level primary navigation")
    append("")
    append("| Order | AZ label | EN label | Type | Landing / notes |")
    append("|-------|----------|----------|------|-----------------|")
    primary = nav.get("primary", [])
    for item in primary:
        lid = item.get("labelKey") or item.get("id", "")
        az_l = _nav_label(ui, "az", lid)
        en_l = _nav_label(ui, "en", lid)
        typ = item.get("type", "page")
        landing = item.get("landingId") or item.get("id", "")
        append(f"| — | {az_l} | {en_l} | {typ} | Landing: `{landing}` |")
        for child in item.get("children", []):
            cid = child.get("labelKey") or child.get("id", "")
            append(
                f"| ↳ | {_nav_label(ui, 'az', cid)} | {_nav_label(ui, 'en', cid)} | child | `{child.get('id')}` |"
            )
    append("")
    append("### 5.2 Forum 2024 section navigation")
    append("")
    append(
        "Forum subpages (12) are NOT separate top-level menu items. They appear in the "
        "**In this section** pill strip (`daab-section-nav`) and breadcrumbs when browsing `forum/2024/`."
    )
    append("")
    forum_pages = nav.get("sections", {}).get("forum", {}).get("pages", [])
    append("| Page ID | AZ label | EN label |")
    append("|---------|----------|----------|")
    key_map = {
        "forum-2024": "forum2024",
        "forum-official": "forumOfficial",
        "forum-rector-speeches": "forumRectorSpeeches",
        "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
        "forum-program": "forumProgram",
        "forum-2024-presentations": "forum2024Presentations",
        "forum-impressions": "forumImpressions",
        "forum-photos-gallery": "forumPhotosGallery",
        "forum-video-gallery": "forumVideoGallery",
        "forum-roadmap": "forumRoadmap",
        "forum-bagli-hekayeler": "forumBagliHekayeler",
        "forum-cooperation": "forumCooperation",
    }
    for pid in forum_pages:
        key = key_map.get(pid, pid)
        append(f"| `{pid}` | {_nav_label(ui, 'az', key)} | {_nav_label(ui, 'en', key)} |")
    append("")
    append("### 5.3 Other navigation mechanisms")
    append("")
    append("| Mechanism | Implementation | Requirement |")
    append("|-----------|----------------|-------------|")
    append("| Breadcrumbs | `js/daab-breadcrumbs.js` | Show path from Home to current page |")
    append("| Section nav | `js/daab-section-nav.js` | Horizontal pills for About, Scientists, Membership, Forum |")
    append("| Hub cards | `daab-hub-cards.css` | Home and Forum hub discovery grids |")
    append("| Sidebar widgets | `daab-sidebar-widget.css` | TOC/timeline on charter, presentations, stories, activities |")
    append("| Skip link | First focusable control | Keyboard users skip to `#content` |")
    append("| Back to top | `daab-back-to-top.js` | Appears after scroll on long pages |")
    append("| Sticky chrome | `daab-sticky-chrome.js` | Nav + breadcrumbs stack; height CSS variables |")
    append("| Search | `daab-search.js` | Ctrl/Cmd+K overlay; `i18n/search-index.json` |")
    append("")

    # 6 Content
    append("## 6. Content requirements")
    append("")
    append("### 6.1 Text content")
    append("")
    append("- Formal institutional tone; AZ primary, EN professional translation.")
    append("- Hero **page subtitle** from `i18n/page-subtitles.json` via `daab-page-subtitle.js`.")
    append("- Hero **summary panel** text from `i18n/page-panel-summaries.json` where configured.")
    append("- Long-form forum and charter text: justified prose, accessible heading hierarchy.")
    append("- Scientists data: names, affiliations, fields — synchronized between list and profiles.")
    append("")
    append("### 6.2 Media content")
    append("")
    append("| Content type | Location | Requirements |")
    append("|--------------|----------|--------------|")
    append("| Brand logos | `images/daab-logo.svg` | Consistent header/footer usage |")
    append("| Partner logos | Forum hub | DİDK, ETN SVG logos |")
    append("| Scientist portraits | `images/` scientist paths | Used in list preview and profile cards |")
    append("| Forum photos | `images/photos-gallery/` | Categorized; thumbnails in `_thumbs/` |")
    append("| Forum videos | YouTube URLs in HTML | Open externally; maintain titles AZ/EN |")
    append("| Site background | `images/diaspor-body-top-bg.png` | Top-faded pattern on all page bodies |")
    append("| QR codes | Profile/board cards | Link to profile deep URLs |")
    append("")
    append("### 6.3 Downloadable / shareable materials")
    append("")
    append("- Membership flyer: single-page PDF via Print/PDF and Share actions.")
    append("- Charter and long articles: browser print; print CSS hides chrome.")
    append("- No generic document library UI; PDFs linked inline where present.")
    append("")

    # 7 Functional
    append("## 7. Functional requirements")
    append("")
    append("| ID | Feature | Requirement | Primary implementation |")
    append("|----|---------|-------------|------------------------|")
    append("| FR-01 | Site search | Overlay search with debounce; AZ character normalization | `daab-search.js`, `search-index.json` |")
    append("| FR-02 | Language switch | Pair pages via routes.json; persist preference | `daab-i18n.js`, `daab-shell.js` |")
    append("| FR-03 | Scroll preservation | Maintain section on language switch | `daab-lang-position.js` |")
    append("| FR-04 | Primary nav | JSON-driven menu with dropdowns | `daab-primary-nav.js`, `nav.json` |")
    append("| FR-05 | Mobile nav | Hamburger, scroll lock, tap dropdowns | `daab-nav.js`, `daab-mobile.js` |")
    append("| FR-06 | Scientists list filters | Sort, filter, preview, resize columns | `scientists-list-preview.js`, catalog data JS |")
    append("| FR-07 | Scientists profile filters | Multi-filter, pagination, badge sync | `scientists-cv-filters.js` |")
    append("| FR-08 | Profile deep link | URL `#slug` opens matching card | `daab-profile-deep-link.js` |")
    append("| FR-09 | Profile TTS | Read profile text via Web Speech API | `daab-profile-tts.js` |")
    append("| FR-10 | Photo gallery | Categories, lazy load, lightbox | `daab-photos-gallery.js` + manifests |")
    append("| FR-11 | Video gallery | Curated YouTube links | Static HTML |")
    append("| FR-12 | Membership form | 4-step wizard, client validation UI | `daab-membership-application.js` |")
    append("| FR-13 | Flyer PDF | Single-page A4 PDF, layout preserved | `daab-membership-flyer-email.js` |")
    append("| FR-14 | Flyer share | Web Share API or download + mailto fallback | Same module |")
    append("| FR-15 | Sidebar timeline | Section jumps on activities/stories | `daab-sidebar-timeline.js` |")
    append("| FR-16 | Legacy redirects | Old root filenames → az/ paths | Hosting / routes.json map |")
    append("| FR-17 | Path validation | CI/local check for broken refs | `helpers/_validate_site.py` |")
    append("")

    # 8 UI/UX
    append("## 8. UI/UX requirements")
    append("")
    append("### 8.1 Design system")
    append("")
    append("- **Tokens:** `css/daab-tokens.css` (colors, typography, spacing, shadows, z-index).")
    append("- **Fonts:** Playfair Display (headings), Inter (body/UI) via Google Fonts.")
    append("- **Colors:** Blue palette (`--blue-700` primary), white/light blue surfaces, gold accents.")
    append("- **Background:** Diaspora pattern + soft scrim on all bodies (`daab-site-background.css`).")
    append("")
    append("### 8.2 Layout patterns")
    append("")
    append("| Pattern | Usage | Key CSS |")
    append("|---------|-------|---------|")
    append("| Standard shell | Most pages | `daab-common.css`, sticky chrome |")
    append("| Content hero | About, membership | `daab-content-hero.css` |")
    append("| Hub cards | Home, Forum hub | `daab-hub-cards.css` |")
    append("| Forum article | Forum inner pages | `daab-forum-content.css` |")
    append("| Data table | Scientists list | `daab-scientists-list-page.css` |")
    append("| Profile cards | Scientists profiles | `daab-scientists-profiles-page.css` |")
    append("| Flyer sheet | Membership flyer | `daab-membership-flyer.css` |")
    append("")
    append("### 8.3 Accessibility requirements")
    append("")
    append("- Skip-to-content link on main pages.")
    append("- `aria-current`, `aria-expanded`, and keyboard-operable nav dropdowns.")
    append("- Visible focus rings on interactive controls.")
    append("- Sufficient color contrast on body text; hero scrim preserves readability over background.")
    append("- `prefers-reduced-transparency`: simplified background gradient.")
    append("- Form labels and step indicators on membership application.")
    append("")

    # 9 Responsive
    append("## 9. Responsive and browser compatibility requirements")
    append("")
    append("- **Viewport:** `width=device-width, initial-scale=1.0, viewport-fit=cover` on all pages.")
    append("- **Breakpoints:** Nav compact ~1180px; sidebar stack ~1060px (`design-system.json`).")
    append("- **Mobile:** Hamburger menu, collapsible filters, stacked heroes, touch-friendly targets (`daab-mobile.css`).")
    append("- **Tablets:** Section nav horizontal scroll; scientists sticky toolbar behavior.")
    append("- **Browsers:** Chrome, Edge, Firefox, Safari (desktop and mobile) — static HTML/CSS/ES5+ compatible scripts.")
    append("- **PDF/print:** Flyer export tested via jsPDF; browser print as fallback with print-specific CSS.")
    append("")

    # 10 Non-functional
    append("## 10. Non-functional requirements")
    append("")
    append("| Category | Requirement |")
    append("|----------|-------------|")
    append("| Maintainability | Central i18n JSON, shared CSS modules, helper scripts for regeneration |")
    append("| Performance | Lazy-loaded gallery thumbs; cache-busting `?v=` on shared CSS/JS |")
    append("| Accessibility | WCAG-oriented patterns (skip link, ARIA, focus, reduced transparency) |")
    append("| SEO readiness | `<title>`, meta description, canonical where set, semantic headings |")
    append("| Code cleanliness | Lowercase paths; no duplicate root css/js; validators after changes |")
    append("| Naming consistency | Page IDs in routes.json; lowercase HTML filenames |")
    append("| Reusable styles | Tokens + common.css; page CSS extends rather than duplicates |")
    append("| Dead code avoidance | Audit before removal; documented unused assets (story TTS) |")
    append("")

    # 11 CMS / maintenance
    append("## 11. Content management and maintenance requirements")
    append("")
    append("### 11.1 Adding or updating content")
    append("")
    append("| Content type | Recommended workflow |")
    append("|--------------|---------------------|")
    append("| New static page | Add AZ+EN HTML; register in `routes.json` and `nav.json`; add ui labels |")
    append("| Nav label change | Edit `i18n/ui.json` only (not duplicated in HTML) |")
    append("| Scientist record | Update catalog JS + regenerate profiles via `helpers/_rebuild_cv_catalog.py` |")
    append("| Forum speech/article | Edit HTML or rebuild from docx via `helpers/_build_*` |")
    append("| Photo gallery | Add images under `images/photos-gallery/`; update manifests; run thumb helper |")
    append("| Membership form fields | Edit HTML + `daab-membership-application.js` together |")
    append("| Shared design change | Edit tokens/common CSS; bump `?v=` via `_site_wide_cleanup.py` |")
    append("")
    append("### 11.2 Quality gates before publish")
    append("")
    append("```bash")
    append("python helpers/_validate_site.py")
    append("python helpers/_validate_cv_cards.py")
    append("python helpers/_check_name_order.py")
    append("python helpers/_audit_repo_health.py")
    append("```")
    append("")

    # 12 Deployment
    append("## 12. Deployment requirements")
    append("")
    append("### 12.1 Include in production bundle")
    append("")
    append("| Path | Purpose |")
    append("|------|---------|")
    append("| `index.html` | Language gateway / redirect |")
    append("| `az/`, `en/` | All public HTML pages |")
    append("| `css/` | Stylesheets |")
    append("| `js/` | Client scripts and JSON manifests used at runtime |")
    append("| `images/` | Photos, logos, gallery assets |")
    append("| `i18n/` | routes, ui, nav, search index, subtitles |")
    append("| `cv/` | Standalone CV HTML if linked publicly |")
    append("")
    append("### 12.2 Exclude from production")
    append("")
    append("| Path | Reason |")
    append("|------|--------|")
    append("| `helpers/` | Python maintenance only |")
    append("| `documents/` | Internal documentation |")
    append("| `sources/`, `_archive/` | Prototypes and backups |")
    append("| `Deployment/`, `.deployment-staging/` | Local staging copies |")
    append("| `node_modules/`, `__pycache__/` | Dev artifacts |")
    append("")
    append("### 12.3 Hosting rules")
    append("")
    append("- Serve from site root with **case-sensitive** paths (Linux/GitHub Pages).")
    append("- Use HTTPS for production; required for embeds and modern APIs (Web Share).")
    append("- After deploy, hard-refresh or rely on bumped `?v=` to clear CSS/JS cache.")
    append("")

    # 13 Open issues
    append("## 13. Open issues and recommendations")
    append("")
    append("| # | Issue | Impact | Recommendation |")
    append("|---|-------|--------|----------------|")
    append("| 1 | ~~`daab-story-tts.js` not linked on `stories.html`~~ | Removed June 2026 | Story read-aloud feature dropped |")
    append("| 2 | `daab-forum-book.css` unused in live HTML | Dead asset | Keep for build pipeline or archive |")
    append("| 3 | Membership application has no server-side submit | Data not persisted | Implement backend or form service per storage strategy doc |")
    append("| 4 | Large scientists profiles HTML | Maintenance cost | Continue generator-based updates only |")
    append("| 5 | `Deployment/` folder may lag source versions | Stale preview | Deploy from repo root, not Deployment snapshot |")
    append("| 6 | Forum video data partly build-time | Manual sync risk | Document update steps in video gallery helper |")
    append("| 7 | Residual legacy URL bookmarks | 404 off-site | Maintain redirects; communicate new `/az/` `/en/` paths |")
    append("| 8 | Full unused CSS/JS audit deferred | Bundle size | Run `_audit_css_usage.py` per stylesheet |")
    append("| 9 | Manual QA checklist incomplete | Release risk | Complete keyboard/tablet QA from pre-release doc |")
    append("| 10 | iframe/embed constraints | X-Frame-Options | Test any third-party embed URLs after path changes |")
    append("")
    append("---")
    append("")
    append("*End of document — generated from live site structure May 2026.*")

    return "\n".join(lines) + "\n"


def main() -> int:
    if not ROUTES_PATH.is_file():
        print(f"Missing {ROUTES_PATH}", file=sys.stderr)
        return 1

    md_text = build_markdown()
    MD_PATH.parent.mkdir(parents=True, exist_ok=True)
    MD_PATH.write_text(md_text, encoding="utf-8", newline="\n")
    print(f"OK  {MD_PATH.relative_to(ROOT)}")

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    export_markdown_to_docx(MD_PATH, OUT_PATH)
    print(f"OK  {OUT_PATH.relative_to(ROOT)}")
    print("\nTip: Open in Word and press F9 to refresh the table of contents.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

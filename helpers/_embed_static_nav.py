#!/usr/bin/env python3
"""Nav HTML helpers for page builders + slim placeholder sync.

Static NAV_AZ / NAV_EN strings remain for reference and legacy tooling only.
Live pages use a minimal #primaryNavMenu placeholder; daab-primary-nav.js builds
the menu from i18n/nav.json at runtime.

To slim placeholders across az/en HTML:
    python helpers/_sync_primary_nav.py
"""
from __future__ import annotations

import re
from pathlib import Path

from _paths import ROOT
from _sync_primary_nav import MINIMAL_NAV_INNER, needs_slim_nav, patch_file, slim_nav_menu

def _top_link(href: str, nav_id: str, title: str) -> str:
    return f'<a class="nav-link" href="{href}" data-nav-id="{nav_id}">{title}</a>'


def _drop(items: list[tuple[str, str, str, str]], *, link_class: str = "nav-dropdown-link") -> str:
    parts = []
    for href, nav_id, title, desc in items:
        link = (
            f'<a class="{link_class}" role="menuitem" href="{href}" data-nav-id="{nav_id}">'
            f'<span class="nav-dropdown-link-title">{title}</span>'
        )
        if desc:
            link += f'<span class="nav-dropdown-link-desc">{desc}</span>'
        link += "</a>"
        parts.append(link)
    return "".join(parts)


def _mega_col(heading: str, items: list[tuple[str, str, str, str]], *, nested: bool = False) -> str:
    wrap_class = "nav-mega-nest" if nested else "nav-mega-links"
    return (
        '<div class="nav-mega-col">'
        f'<div class="nav-mega-heading" role="presentation">{heading}</div>'
        f'<div class="{wrap_class}">'
        + _drop(items)
        + "</div></div>"
    )


def _forum_mega_drop(lang: str) -> str:
    if lang == "en":
        sections = [
            ("Overview", False, [
                ("forum/2024/index.html", "forum-2024", "🎤 Highlights", "First Forum of Azerbaijani Scientists Living Abroad — September 2024"),
                ("forum/2024/logistics.html", "forum-logistics", "🧳 Logistics", "Transport, hotel accommodation, and catering for international participants"),
                ("forum/2024/program.html", "forum-program", "📅 Programme", "Programme of the Baku–Khankendi–Shusha forum journey"),
                ("forum/2024/sessions_organization.html", "forum-sessions-organization", "🪑 Sessions", "10 September strategic sessions — mixed and discipline-specific groups"),
            ]),
            ("Participants", True, [
                ("scientists/list.html", "scientists-list", "📋 Directory of Scientists", "Directory of all scientists"),
                ("scientists/profiles.html", "scientists-profiles", "👤 Profiles of Scientists", "Academic profiles of scientists"),
            ]),
            ("Official record", False, [
                ("forum/2024/official.html", "forum-official", "🏛️ Official addresses", "Official speeches and messages that shaped the Forum"),
                ("forum/2024/presentations.html", "forum-2024-presentations", "📊 Presentations", "Presentations on science, education, policy, and more"),
            ]),
            ("Speeches", True, [
                ("forum/2024/rector_speeches.html", "forum-rector-speeches", "🎓 Rectors", "Speeches by rectors of Azerbaijani universities at Forum 2024"),
                ("forum/2024/anas_leadership_speeches.html", "forum-anas-leadership-speeches", "🔬 Academicians", "Speeches by academicians at Forum 2024"),
            ]),
            ("Media &amp; reflections", False, [
                ("forum/2024/photos_gallery.html", "forum-photos-gallery", "📷 Photo gallery", "Photographic story of the Forum — opening to key encounters"),
                ("forum/2024/video_gallery.html", "forum-video-gallery", "📹 Video gallery", "Video reports and interviews on Forum 2024"),
                ("forum/2024/impressions.html", "forum-impressions", "💬 Impressions", "Participants' thoughts on the Forum and Karabakh visit"),
                ("forum/2024/stories.html", "forum-bagli-hekayeler", "📖 Stories", "Literary reflections from the Forum"),
            ]),
            ("Outcomes &amp; partners", False, [
                ("forum/2024/roadmap.html", "forum-roadmap", "🗺️ Strategic roadmap", "Ideas for science, education, and diaspora cooperation"),
                ("forum/2024/cooperation.html", "forum-cooperation", "🤝 Contributions", "Partners who supported the Forum"),
            ]),
        ]
        label = "🎤 I Forum"
        year_desc = "First Forum of Azerbaijani Scientists Living Abroad — September 2024"
    else:
        sections = [
            ("Ümumi baxış", False, [
                ("forum/2024/index.html", "forum-2024", "🎤\u00a0Ümumi Mənzərə", "Xaricdə yaşayan alimlərin I Forumu — sentyabr 2024"),
                ("forum/2024/logistics.html", "forum-logistics", "🧳 Logistika", "Xarici iştirakçılar üçün nəqliyyat, hotel və qidalanma"),
                ("forum/2024/program.html", "forum-program", "📅 Proqram", "Bakı–Xankəndi–Şuşa forum proqramı"),
                ("forum/2024/sessions_organization.html", "forum-sessions-organization", "🪑 Sessiyalar", "10 sentyabr strateji sessiyalar — QARIŞIQ və İXTİSAS qrupları"),
            ]),
            ("İştirakçılar", True, [
                ("scientists/list.html", "scientists-list", "📋 Alimlərin siyahısı", "Forumda iştirak edən bütün alimlərin siyahısı"),
                ("scientists/profiles.html", "scientists-profiles", "👤 Alimlərin profilləri", "Alimlərin akademik profilləri"),
            ]),
            ("Rəsmi sənədlər", False, [
                ("forum/2024/official.html", "forum-official", "🏛️ Rəsmi müraciətlər", "Forumun istiqamətini müəyyən edən rəsmi çıxış və müraciətlər"),
                ("forum/2024/presentations.html", "forum-2024-presentations", "📊 Məruzələr", "Elm, təhsil və siyasət mövzularında məruzələr"),
            ]),
            ("Nitqlər", True, [
                ("forum/2024/rector_speeches.html", "forum-rector-speeches", "🎓 Rektorlar", "Azərbaycan universitet rektorlarının Forum 2024 nitqləri"),
                ("forum/2024/anas_leadership_speeches.html", "forum-anas-leadership-speeches", "🔬 Akademiklər", "Akademiklərin Forumla bağlı görüş və nitqləri"),
            ]),
            ("Media və təəssüratlar", False, [
                ("forum/2024/photos_gallery.html", "forum-photos-gallery", "📷 Foto qalereya", "Forumun foto-hekayəsi — açılışdan əsas görüşlərə"),
                ("forum/2024/video_gallery.html", "forum-video-gallery", "📹 Video qalereya", "Forum 2024 haqqında video reportajlar və müsahibələr"),
                ("forum/2024/impressions.html", "forum-impressions", "💬 Təəssüratlar", "İştirakçıların Forum və Qarabağ təəssüratları"),
                ("forum/2024/stories.html", "forum-bagli-hekayeler", "📖 Hekayələr", "Forumun ab-havasını əks etdirən ədəbi yazılar"),
            ]),
            ("Nəticələr və tərəfdaşlar", False, [
                ("forum/2024/roadmap.html", "forum-roadmap", "🗺️ Strateji yol xəritəsi", "Elm, təhsil və diaspora əməkdaşlığına dair təkliflər"),
                ("forum/2024/cooperation.html", "forum-cooperation", "🤝 Töhfələr", "Forumun təşkilinə dəstək verən tərəfdaşlar"),
            ]),
        ]
        label = "🎤 I Forum"
        year_desc = "Xaricdə yaşayan alimlərin I Forumu — sentyabr 2024"
    cols = "".join(_mega_col(heading, items, nested=nested) for heading, nested, items in sections)
    return (
        '<div class="nav-dropdown nav-dropdown--mega nav-dropdown--forum nav-dropdown--nested nav-dropdown--has-mega" data-nav-dropdown data-nav-group="forum" data-has-nested-mega="1">'
        + '<button type="button" class="nav-link nav-dropdown-toggle nav-dropdown-toggle--forum-year" aria-expanded="false" aria-haspopup="true">'
        + f'<span class="nav-dropdown-link-title">{label}</span>'
        + f'<span class="nav-dropdown-link-desc">{year_desc}</span>'
        + ' <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
        + '<div class="nav-dropdown-panel nav-dropdown-panel--mega" role="menu">'
        + '<div class="nav-mega-grid">'
        + cols
        + "</div></div></div>"
    )


def _forum_2026_link(lang: str) -> str:
    href = "forum/2026/index.html"
    if lang == "en":
        title = "🎤 II Forum"
        desc = "Second Forum of Azerbaijani Scientists Living Abroad — December 2026, draft concept"
    else:
        title = "🎤 II Forum"
        desc = "Xaricdə yaşayan alimlərin II Forumu — dekabr 2026, konsepsiya layihəsi"
    return _drop(
        [(href, "forum-2026", title, desc)],
        link_class="nav-dropdown-link nav-dropdown-link--forum-year",
    )


def _forums_drop(lang: str) -> str:
    label = "🎤\u00a0Forumlar" if lang == "az" else "🎤\u00a0Forums"
    return (
        '<div class="nav-dropdown nav-dropdown--forums" data-nav-dropdown data-nav-group="forums">'
        + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
        + label
        + ' <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
        + '<div class="nav-dropdown-panel" role="menu">'
        + _forum_mega_drop(lang)
        + _forum_2026_link(lang)
        + "</div></div>"
    )


def _simple_nav_dropdown(label: str, items: list[tuple[str, str, str, str]]) -> str:
    return (
        '<div class="nav-dropdown" data-nav-dropdown>'
        + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
        + label
        + ' <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
        + '<div class="nav-dropdown-panel" role="menu">'
        + _drop(items)
        + "</div></div>"
    )


SPONSORSHIP_AZ = (
    '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + '🤝\u00a0Bizi dəstəkləyin <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("sponsorship_partnership.html", "sponsorship-partnership", "🤝\u00a0Niyə DAAB-a dəstək verilməli", "DAAB üçün sponsorluq paketləri və tərəfdaşlıq təklifi"),
        ("donate.html", "donate", "💝\u00a0İanə Edin", "Fərdi, fond və xatirə ianələri"),
        ("sponsors_flyer.html", "sponsors-flyer", "📤\u00a0Dəvət məktubu", "Potensial tərəfdaşlar üçün paylaşıla bilən dəvət məktubu"),
    ])
    + "</div></div>"
)

SPONSORSHIP_EN = (
    '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + '🤝\u00a0Support us <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("sponsorship_partnership.html", "sponsorship-partnership", "🤝\u00a0Why Sponsor WAAS?", "WAAS sponsorship packages and partnership proposal"),
        ("donate.html", "donate", "💝\u00a0Donate", "Individual, foundation, and memorial gifts"),
        ("sponsors_flyer.html", "sponsors-flyer", "📤\u00a0Invitation Letter", "Printable invitation letter for potential partners"),
    ])
    + "</div></div>"
)


def _activities_drop(lang: str) -> str:
    if lang == "en":
        label = "📰\u00a0Activities"
        items = [
            ("activities.html", "activities-news", "📰\u00a0News", "News and updates"),
            (
                "work_done_2024_2026.html",
                "work-done-2024-2026",
                "📋\u00a0Work Done 2024-2026",
                "Association work and outcomes, 2024–2026",
            ),
        ]
    else:
        label = "📰\u00a0Fəaliyyətimiz"
        items = [
            ("activities.html", "activities-news", "📰\u00a0Yeniliklər", "Əsas fəaliyyət və yeniliklər"),
            (
                "work_done_2024_2026.html",
                "work-done-2024-2026",
                "📋\u00a0Görülən işlər, 2024-2026",
                "2024-2026-cu illərdə Birliyin fəaliyyəti və nəticələri",
            ),
        ]
    return _simple_nav_dropdown(label, items)


NAV_AZ = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">🏠\u00a0Ana səhifə</a>'
    + _activities_drop("az")
    + _forums_drop("az")
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + '🏛️\u00a0Haqqımızda <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "🏛️\u00a0Birliyin təsisi", "Yaradılma tarixi və təsis prosesi"),
        ("mission.html", "mission", "💎\u00a0Missiya və dəyərlər", "Missiya, vizyon və akademik dəyərlər"),
        ("executive-board.html", "executive-board", "🎓\u00a0İdarə heyəti", "İdarə heyəti və rəhbərlik"),
        ("charter.html", "charter", "📜\u00a0Nizamnamə", "Nizamnamə və idarəetmə qaydaları"),
    ])
    + "</div></div>"
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + '✒️\u00a0Üzvlük <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("membership_value.html", "membership-value", "💡\u00a0Niyə DAAB-a üzv olmalı", "Üzvlüyün dəyəri və əsas faydalar"),
        ("application.html", "membership-application", "📝\u00a0Bizə qoşulun", "Onlayn üzvlük müraciət forması"),
        ("membership_flyer.html", "membership-flyer", "📤\u00a0Dəvət məktubu", "Potensial üzvlər üçün çap oluna bilən flyer"),
    ])
    + "</div></div>"
    + SPONSORSHIP_AZ
)

NAV_EN = (
    '<div class="nav-divider"></div>'
    '<a class="nav-link" href="index.html" data-nav-id="home">🏠\u00a0Home</a>'
    + _activities_drop("en")
    + _forums_drop("en")
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + '🏛️\u00a0About us <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("foundation.html", "foundation", "🏛️\u00a0Foundation", "History and founding process"),
        ("mission.html", "mission", "💎\u00a0Mission &amp; values", "Mission, vision and academic values"),
        ("executive-board.html", "executive-board", "🎓\u00a0Executive Board", "Leadership and governance structure"),
        ("charter.html", "charter", "📜\u00a0Charter", "Charter and governance rules"),
    ])
    + "</div></div>"
    + '<div class="nav-dropdown" data-nav-dropdown>'
    + '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" aria-haspopup="true">'
    + '✒️\u00a0Membership <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
    + '<div class="nav-dropdown-panel" role="menu">'
    + _drop([
        ("membership_value.html", "membership-value", "💡\u00a0Why join WAAS", "Membership value, benefits, and opportunities"),
        ("application.html", "membership-application", "📝\u00a0Join us", "Online membership application form"),
        ("membership_flyer.html", "membership-flyer", "📤\u00a0Invitation Letter", "Printable invitation letter for potential members"),
    ])
    + "</div></div>"
    + SPONSORSHIP_EN
)

NAV_SCI_AZ = NAV_AZ.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace('href="work_done_2024_2026.html"', 'href="../work_done_2024_2026.html"'
).replace('href="forum/2024/', 'href="../forum/2024/').replace('href="forum/2026/', 'href="../forum/2026/').replace('href="membership.html"', 'href="../membership.html"').replace(
    'href="membership_value.html"', 'href="../membership_value.html"'
).replace('href="application.html"', 'href="../application.html"').replace(
    'href="membership_flyer.html"', 'href="../membership_flyer.html"'
).replace(
    'href="sponsorship_partnership.html"', 'href="../sponsorship_partnership.html"'
).replace('href="donate.html"', 'href="../donate.html"').replace(
    'href="sponsors_flyer.html"', 'href="../sponsors_flyer.html"'
)

FORUM_PREFIX_REPLACES = [
    ('href="index.html"', 'href="../../index.html"'),
    ('href="activities.html"', 'href="../../activities.html"'),
    ('href="work_done_2024_2026.html"', 'href="../../work_done_2024_2026.html"'),
    ('href="forum/2024/', 'href="'),
    ('href="forum/2026/', 'href="../2026/'),
    ('href="scientists/', 'href="../../scientists/'),
    ('href="foundation.html"', 'href="../../foundation.html"'),
    ('href="mission.html"', 'href="../../mission.html"'),
    ('href="executive-board.html"', 'href="../../executive-board.html"'),
    ('href="charter.html"', 'href="../../charter.html"'),
    ('href="membership.html"', 'href="../../membership.html"'),
    ('href="membership_value.html"', 'href="../../membership_value.html"'),
    ('href="application.html"', 'href="../../application.html"'),
    ('href="membership_flyer.html"', 'href="../../membership_flyer.html"'),
    ('href="sponsorship_partnership.html"', 'href="../../sponsorship_partnership.html"'),
    ('href="donate.html"', 'href="../../donate.html"'),
    ('href="sponsors_flyer.html"', 'href="../../sponsors_flyer.html"'),
]


FORUM_2026_PREFIX_REPLACES = [
    ('href="index.html"', 'href="../../index.html"'),
    ('href="activities.html"', 'href="../../activities.html"'),
    ('href="work_done_2024_2026.html"', 'href="../../work_done_2024_2026.html"'),
    ('href="forum/2024/', 'href="../2024/'),
    ('href="forum/2026/', 'href="'),
    ('href="scientists/', 'href="../../scientists/'),
    ('href="foundation.html"', 'href="../../foundation.html"'),
    ('href="mission.html"', 'href="../../mission.html"'),
    ('href="executive-board.html"', 'href="../../executive-board.html"'),
    ('href="charter.html"', 'href="../../charter.html"'),
    ('href="membership.html"', 'href="../../membership.html"'),
    ('href="membership_value.html"', 'href="../../membership_value.html"'),
    ('href="application.html"', 'href="../../application.html"'),
    ('href="membership_flyer.html"', 'href="../../membership_flyer.html"'),
    ('href="sponsorship_partnership.html"', 'href="../../sponsorship_partnership.html"'),
    ('href="donate.html"', 'href="../../donate.html"'),
    ('href="sponsors_flyer.html"', 'href="../../sponsors_flyer.html"'),
]


def forum_2026_nav(nav: str) -> str:
    for old, new in FORUM_2026_PREFIX_REPLACES:
        nav = nav.replace(old, new)
    return nav


def forum_nav(nav: str) -> str:
    for old, new in FORUM_PREFIX_REPLACES:
        nav = nav.replace(old, new)
    return nav


def mark_active_nav(menu: str, active_nav_id: str) -> str:
    """Add active class and aria-current to the nav link for active_nav_id."""
    pattern = re.compile(
        rf'(<a\b[^>]*\bdata-nav-id="{re.escape(active_nav_id)}"[^>]*>)',
        re.I,
    )

    def merge_active(match: re.Match[str]) -> str:
        tag = match.group(1)
        if re.search(r'\bclass="', tag, re.I):

            def add_active(m: re.Match[str]) -> str:
                classes = m.group(1).split()
                if "active" not in classes:
                    classes.append("active")
                return f'class="{" ".join(classes)}"'

            tag = re.sub(r'\bclass="([^"]*)"', add_active, tag, count=1, flags=re.I)
        else:
            tag = tag[:-1] + ' class="active"'
        if "aria-current=" not in tag:
            tag = tag[:-1] + ' aria-current="page"'
        return tag

    new_menu, count = pattern.subn(merge_active, menu, count=1)
    return new_menu if count else menu


def forum_nav_strip(lang: str = "az", *, active_nav_id: str | None = None) -> str:
    """Full nav-strip HTML for pages under az|en/forum/2024/ (three levels below locale root)."""
    asset = "../../../"
    menu = MINIMAL_NAV_INNER
    _ = active_nav_id  # active state is applied by daab-primary-nav.js from nav.json
    if lang == "en":
        return (
            f'<nav aria-label="Main navigation" class="nav-strip"><div class="nav-inner">'
            f'<button class="mobile-menu-toggle" type="button" aria-label="Open menu" '
            f'aria-expanded="false" aria-controls="primaryNavMenu">'
            f"<span></span><span></span><span></span></button>"
            f'<div class="page-logo"><a aria-label="WAAS home" title="Home page" href="../../index.html">'
            f'<img src="{asset}images/daab-logo.png" class="nav-brand-logo" alt="WAAS Logo"></a></div>'
            f'<a aria-label="WAAS home" class="nav-brand" href="../../index.html">'
            f'<span class="nav-brand-text">World Association of<br class="mobile-hidden-break">'
            f"Azerbaijani Scientists</span></a>"
            f'<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">{menu}</div>'
            f'<div class="nav-actions" role="group"></div>'
            f"</div></nav>"
        )
    return (
        f'<nav aria-label="Əsas naviqasiya" class="nav-strip"><div class="nav-inner">'
        f'<button class="mobile-menu-toggle" type="button" aria-label="Menyunu aç" '
        f'aria-expanded="false" aria-controls="primaryNavMenu">'
        f"<span></span><span></span><span></span></button>"
        f'<div class="page-logo"><a aria-label="DAAB ana səhifə" title="Ana səhifə" href="../../index.html">'
        f'<img src="{asset}images/daab-logo.png" class="nav-brand-logo" alt="DAAB Logo"></a></div>'
        f'<a aria-label="DAAB ana səhifə" class="nav-brand" href="../../index.html">'
        f'<span class="nav-brand-text">Dünya Azərbaycanlı<br class="mobile-hidden-break">'
        f"Alimlər Birliyi</span></a>"
        f'<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1">{menu}</div>'
        f'<div class="nav-actions" role="group"></div>'
        f"</div></nav>"
    )


NAV_SCI_EN = NAV_EN.replace('href="scientists/list.html"', 'href="list.html"').replace(
    'href="scientists/profiles.html"', 'href="profiles.html"'
).replace('href="index.html"', 'href="../index.html"').replace(
    'href="foundation.html"', 'href="../foundation.html"'
).replace('href="mission.html"', 'href="../mission.html"').replace(
    'href="executive-board.html"', 'href="../executive-board.html"'
).replace('href="charter.html"', 'href="../charter.html"').replace(
    'href="activities.html"', 'href="../activities.html"'
).replace('href="work_done_2024_2026.html"', 'href="../work_done_2024_2026.html"'
).replace('href="forum/2024/', 'href="../forum/2024/').replace('href="forum/2026/', 'href="../forum/2026/').replace('href="membership.html"', 'href="../membership.html"').replace(
    'href="membership_value.html"', 'href="../membership_value.html"'
).replace('href="application.html"', 'href="../application.html"').replace(
    'href="membership_flyer.html"', 'href="../membership_flyer.html"'
).replace(
    'href="sponsorship_partnership.html"', 'href="../sponsorship_partnership.html"'
).replace('href="donate.html"', 'href="../donate.html"').replace(
    'href="sponsors_flyer.html"', 'href="../sponsors_flyer.html"'
)

PLACEHOLDER_RE = re.compile(
    r'(<div[^>]*class="nav-menu"[^>]*id="primaryNavMenu"[^>]*>)(.*?)(</div>\s*(?:<div class="nav-actions"|</div>\s*</nav>))',
    re.DOTALL | re.IGNORECASE,
)


def is_live_page(path: Path) -> bool:
    """Only pages under /az and /en are live site pages."""
    rel = path.relative_to(ROOT).as_posix()
    return rel.startswith("az/") or rel.startswith("en/")


def nav_html(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.startswith("en/scientists/"):
        return NAV_SCI_EN
    if rel.startswith("az/scientists/"):
        return NAV_SCI_AZ
    if "forum/2024/" in rel:
        if rel.startswith("en/"):
            return forum_nav(NAV_EN)
        return forum_nav(NAV_AZ)
    if "forum/2026/" in rel:
        if rel.startswith("en/"):
            return forum_2026_nav(NAV_EN)
        return forum_2026_nav(NAV_AZ)
    if rel.startswith("en/"):
        return NAV_EN
    return NAV_AZ


def patch(path: Path) -> bool:
    if not is_live_page(path):
        return False
    text = path.read_text(encoding="utf-8")
    if "primaryNavMenu" not in text:
        return False
    if needs_slim_nav(text):
        return patch_file(path)
    return False


def main() -> None:
    from _sync_primary_nav import main as sync_main

    raise SystemExit(sync_main())


if __name__ == "__main__":
    main()

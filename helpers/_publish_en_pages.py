#!/usr/bin/env python3
"""Publish completed English pages from /az/ sources (preserved on rebuild).

Usage:
    python helpers/_publish_en_pages.py mission
    python helpers/_publish_en_pages.py --all
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from _paths import ROOT

try:
    from i18n_foundation_en import FOUNDATION_REPLACEMENTS
    from i18n_membership_en import MEMBERSHIP_REPLACEMENTS
    from i18n_executive_board_en import EXECUTIVE_BOARD_REPLACEMENTS
    from i18n_activities_en import ACTIVITIES_REPLACEMENTS
    from i18n_charter_en import CHARTER_REPLACEMENTS
    from i18n_scientists_en import SCIENTISTS_LIST_REPLACEMENTS, SCIENTISTS_PROFILES_REPLACEMENTS
except ImportError:
    from helpers.i18n_foundation_en import FOUNDATION_REPLACEMENTS  # type: ignore
    from helpers.i18n_membership_en import MEMBERSHIP_REPLACEMENTS  # type: ignore
    from helpers.i18n_executive_board_en import EXECUTIVE_BOARD_REPLACEMENTS  # type: ignore
    from helpers.i18n_activities_en import ACTIVITIES_REPLACEMENTS  # type: ignore
    from helpers.i18n_charter_en import CHARTER_REPLACEMENTS  # type: ignore
    from helpers.i18n_scientists_en import (  # type: ignore
        SCIENTISTS_LIST_REPLACEMENTS,
        SCIENTISTS_PROFILES_REPLACEMENTS,
    )

EN_COMPLETE_MARKER = "<!-- daab-en-complete -->"

LEGACY_REDIRECT_RE = re.compile(
    r'<meta\s+http-equiv=["\']refresh["\'][^>]*>\s*',
    re.IGNORECASE,
)


def strip_legacy_redirect_meta(html: str) -> str:
    html = LEGACY_REDIRECT_RE.sub("", html)
    html = re.sub(r"<!-- data-daab-legacy-redirect -->\s*", "", html)
    html = re.sub(
        r'<link\s+rel=["\']canonical["\']\s+href=["\']az/[^"\']*["\']\s*/>\s*',
        "",
        html,
        count=1,
        flags=re.IGNORECASE,
    )
    return html

EN_NAV_ITEMS = [
    ("home", "index.html", "🏠 Home"),
    ("foundation", "foundation.html", "🏛️ Foundation"),
    ("mission", "mission.html", "💎 Mission"),
    ("activities", "activities.html", "📰 Activities"),
    ("scientists-list", "scientists/list.html", "📋 Directory"),
    ("scientists-profiles", "scientists/profiles.html", "👤 Profiles"),
    ("executive-board", "executive-board.html", "🎓 Executive Board"),
    ("charter", "charter.html", "📜 Charter"),
    ("membership", "membership.html", "✒️ Membership"),
]


def _nav_href(nav_id: str, href: str, nav_depth: int) -> str:
    if nav_depth == 0:
        return href
    if nav_id in ("scientists-list", "scientists-profiles"):
        return href.split("/", 1)[-1]
    return f"../{href}"


def en_nav_html(active_id: str, nav_depth: int = 0) -> str:
    home_href = "../index.html" if nav_depth else "index.html"
    img_src = "../../images/daab-logo.svg" if nav_depth else "../images/daab-logo.svg"
    lines = [
        '<nav aria-label="Main navigation" class="nav-strip">',
        '<div class="nav-inner">',
        '<button class="mobile-menu-toggle" type="button" aria-label="Open menu" '
        'aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>',
        f'<div class="page-logo"><a aria-label="DAAB home" href="{home_href}">',
        f'<img src="{img_src}" class="nav-brand-logo" alt="DAAB Logo"></a></div>',
        f'<a aria-label="DAAB home" class="nav-brand" href="{home_href}">',
        '<span class="nav-brand-text">World Association of<br class="mobile-hidden-break">'
        "Azerbaijani Scientists</span></a>",
        '<div class="nav-menu" id="primaryNavMenu"><div class="nav-divider"></div>',
    ]
    for nav_id, href, label in EN_NAV_ITEMS[:4]:
        cls = "nav-link active" if nav_id == active_id else "nav-link"
        ac = ' aria-current="page"' if nav_id == active_id else ""
        lines.append(
            f'<a class="{cls}" data-nav-id="{nav_id}" href="{_nav_href(nav_id, href, nav_depth)}"{ac}>{label}</a>'
        )
    lines.append(
        '<div class="nav-dropdown" data-nav-dropdown>'
        '<button type="button" class="nav-link nav-dropdown-toggle" aria-expanded="false" '
        'aria-haspopup="true">🌐 Scientists <span class="nav-dropdown-caret" aria-hidden="true"></span></button>'
        '<div class="nav-dropdown-panel" role="menu">'
    )
    for nav_id, href, label in EN_NAV_ITEMS[4:6]:
        cls = "nav-dropdown-link active" if nav_id == active_id else "nav-dropdown-link"
        ac = ' aria-current="page"' if nav_id == active_id else ""
        lines.append(
            f'<a class="{cls}" data-nav-id="{nav_id}" role="menuitem" href="{_nav_href(nav_id, href, nav_depth)}"{ac}>{label}</a>'
        )
    lines.append("</div></div>")
    for nav_id, href, label in EN_NAV_ITEMS[6:]:
        cls = "nav-link active" if nav_id == active_id else "nav-link"
        ac = ' aria-current="page"' if nav_id == active_id else ""
        lines.append(
            f'<a class="{cls}" data-nav-id="{nav_id}" href="{_nav_href(nav_id, href, nav_depth)}"{ac}>{label}</a>'
        )
    lines.append("</div></div></nav>")
    return "\n".join(lines)


def en_footer_html() -> str:
    return """<footer class="footer-pro">
  <div class="footer-inner">
    <div class="footer-brand">
      <h3>World Association of Azerbaijani Scientists</h3>
    </div>
    <div class="footer-grid">
      <div class="footer-col">
        <h4 class="footer-title">Contact</h4>
        <div class="footer-item">✉ <a href="mailto:daad.waas2024@gmail.com">daad.waas2024@gmail.com</a></div>
        <div class="footer-item">☎ <span>+90 555 147 46 74</span></div>
        <div class="footer-item">🌐 <a href="https://daab-waas.org" rel="noopener noreferrer" target="_blank">daab-waas.org</a></div>
      </div>
      <div class="footer-col">
        <h4 class="footer-title">Address</h4>
        <p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p>
      </div>
      <div class="footer-col">
        <h4 class="footer-title">Leadership</h4>
        <p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>
        Chair of the DAAB Executive Board<br/>Germany — James D. Murray Distinguished Professor</p>
      </div>
    </div>
  </div>
  <div class="footer-bottom">© 2026 DAAB / WAAS — All Rights Reserved</div>
</footer>"""


MISSION_REPLACEMENTS: list[tuple[str, str]] = [
    ('<title>\n      DAAB — Missiya, Vizyon və Dəyərlər\n    </title>',
     "<title>DAAB — Mission, Vision and Values</title>"),
    ('content="Dünya Azərbaycanlı Alimlər Birliyinin missiyası, vizyonu və akademik dəyərləri."',
     'content="Mission, vision and academic values of the World Association of Azerbaijani Scientists."'),
    ("Məzmuna keç", "Skip to content"),
    ("Missiya, Vizyon və\n        <span>\n          Dəyərlər\n        </span>",
     "Mission, Vision and\n        <span>\n          Values\n        </span>"),
    ('aria-label="DAAB missiya və vizyon qısa məlumat"', 'aria-label="DAAB mission and vision summary"'),
    ("Elm, etika və gələcəyə baxış", "Science, ethics and outlook"),
    (
        "DAAB-ın məqsədi, gələcəyə baxışı və akademik fəaliyyət istiqamətləri akademik azadlıq, "
        "şəffaflıq, keyfiyyət və məsuliyyət prinsiplərinə əsaslanır və Azərbaycan elminin beynəlxalq "
        "inteqrasiyasına töhfə verməyə yönəlir.",
        "DAAB's purpose, outlook and academic priorities are grounded in academic freedom, transparency, "
        "quality and responsibility, and aim to strengthen the international integration of Azerbaijani science.",
    ),
    ("DAAB-ın institusional əsasları", "DAAB institutional foundations"),
    (
        "Bu səhifədə birliyin missiyası, vizyonu və akademik dəyərləri vahid konseptual çərçivədə təqdim olunur.",
        "This page presents the Association's mission, vision and academic values within a single conceptual framework.",
    ),
    ('aria-label="Səhifədaxili keçidlər"', 'aria-label="On-page sections"'),
    ("Missiya", "Mission"),
    ("Vizyon", "Vision"),
    ("Dəyərlər", "Values"),
    ('aria-label="Missiya, vizyon və dəyərlər"', 'aria-label="Mission, vision and values"'),
    ("Missiyamız", "Our mission"),
    (
        "Dünya Azərbaycanlı Alimlər Birliyi dünyanın müxtəlif ölkələrində yaşayan Azərbaycanlı "
        "ziyalıların birliyi kimi fəaliyyət göstərən qeyri-hökumət təşkilatı olaraq elm və texnologiya, "
        "energetika, təhsil, səhiyyə, sosial elmlər və mədəniyyət sahələri ilə bağlı strateji planların "
        "hazırlanması və icra olunmasında Azərbaycana dəstək verir.",
        "As a non-governmental organisation uniting Azerbaijani scholars living in countries around the world, "
        "the World Association of Azerbaijani Scientists supports Azerbaijan in developing and implementing "
        "strategic plans related to science and technology, energy, education, health, social sciences and culture.",
    ),
    ("Vizyonumuz", "Our vision"),
    (
        "Dünya Azərbaycanlı Alimlər Birliyi elmi biliklərin inkişaf etdirilməsi, innovasiyaların təşviqi, "
        "Azərbaycanda və dünya çapında fərq yarada biləcək alimlərin, mühəndislərin, incəsənət xadimlərinin, "
        "səhiyyə işçilərinin yetişdirilməsinə yönəlmiş fəaliyyətində mükəmməlliyi ilə tanınan beynəlxalq bir "
        "qurum olmaq niyyətindədir. Biz Azərbaycanın dünya miqyasında zəngin və dərin tarixə malik, bəşəriyyət "
        "üçün firavan və dinc gələcək yaratmaq uğrunda böyük sərmayə yatırmış sülhsevər bir dövlət kimi tanınması "
        "və qəbul edilməsini istəyirik. Dünya Azərbaycanın qlobal arenada iştirakından faydalanacaq və öz növbəsində "
        "Azərbaycan da beynəlxalq təcrübədən yararlanaraq gələcək nəsillər üçün daha güclü dövlət qurmağa davam edəcək.",
        "The World Association of Azerbaijani Scientists aspires to be recognised internationally for excellence in "
        "advancing scientific knowledge, promoting innovation, and nurturing scientists, engineers, artists and health "
        "professionals who can make a difference in Azerbaijan and worldwide. We want Azerbaijan to be known and accepted "
        "as a peace-loving state with a rich and deep history that has invested greatly in a prosperous and peaceful future "
        "for humanity. The world will benefit from Azerbaijan's participation on the global stage, and Azerbaijan will "
        "continue to draw on international experience to build a stronger state for future generations.",
    ),
    ("Dəyərlərimiz", "Our values"),
    ("Akademik Azadlıq", "Academic freedom"),
    ("Akademik Etika", "Academic ethics"),
    ("Dürüstlük", "Integrity"),
    ("Fərqliliklərə Hörmət", "Respect for diversity"),
    ("Keyfiyyət", "Quality"),
    ("Məsuliyyət", "Responsibility"),
    ("Mükəmməllik", "Excellence"),
    ("Ləyaqət", "Dignity"),
    ("Şəffaflıq", "Transparency"),
    ("Dəyərlərin izahı", "Explaining our values"),
    (
        "Dəyərlər DAAB-ın akademik mədəniyyətini, əməkdaşlıq modelini və beynəlxalq elmi mühitdə etibarlılığını "
        "formalaşdıran əsas prinsiplərdir.",
        "These values are the core principles that shape DAAB's academic culture, model of cooperation and "
        "credibility in the international scientific community.",
    ),
    ("Akademik azadlıq", "Academic freedom"),
    (
        "Elmi tədqiqatların sərbəst şəkildə aparılması və hər hansı ideoloji, siyasi və ya kommersiya təsirindən uzaq olması.",
        "Scientific research is conducted freely, without ideological, political or commercial pressure.",
    ),
    (
        "Alimlərin öz elmi görüşlərini maneəsiz şəkildə ifadə edə bilməsi.",
        "Scholars can express their scientific views without obstruction.",
    ),
    ("Akademik etika", "Academic ethics"),
    (
        "Elmi fəaliyyət zamanı etik qaydalara əməl olunması, plagiat və saxta nəticələrdən uzaq durulması.",
        "Adherence to ethical standards in scientific work; avoidance of plagiarism and falsified results.",
    ),
    (
        "Tədqiqatlarda obyektivliyin qorunması və elmi işlərin dürüst aparılması.",
        "Objectivity in research and honest conduct of scholarly work.",
    ),
    (
        "Alimlərin öz tədqiqatlarında və elmi müzakirələrində həqiqətə sadiq qalması.",
        "Scholars remain truthful in their research and academic discourse.",
    ),
    (
        "Mövcud biliklər əsasında səhvlərin qəbul edilməsi və düzəldilməsi.",
        "Errors are acknowledged and corrected on the basis of evidence.",
    ),
    ("Fərqliliklərə hörmət", "Respect for diversity"),
    (
        "Fərqli elmi yanaşmalara və alternativ baxışlara açıq olmaq.",
        "Openness to different scientific approaches and alternative perspectives.",
    ),
    (
        "Cins, irq, din, dil, sosial status və digər fərqliliklərə qarşı dözümlülük və inklüzivlik.",
        "Tolerance and inclusion with regard to gender, ethnicity, religion, language, social status and other differences.",
    ),
    (
        "Tədqiqatların yüksək akademik standartlara uyğun aparılması.",
        "Research is carried out to high academic standards.",
    ),
    (
        "Beynəlxalq səviyyədə qəbul edilən metodologiyalardan və araşdırma prinsiplərindən istifadə edilməsi.",
        "Use of methodologies and research principles accepted internationally.",
    ),
    (
        "Alimlərin cəmiyyətə, tələbələrə və gələcək nəsillərə qarşı məsuliyyət daşıması.",
        "Scholars take responsibility towards society, students and future generations.",
    ),
    (
        "Elmin yalnız nəzəri deyil, praktik və sosial fayda verməsi üçün çalışmaq.",
        "Commitment to science that delivers practical and social benefit, not theory alone.",
    ),
    (
        "Davamlı öyrənmək, inkişaf etmək və daha yüksək elmi nailiyyətlər əldə etməyə çalışmaq.",
        "Continuous learning, development and pursuit of higher scientific achievement.",
    ),
    (
        "Elmi araşdırmalarda və tədrisdə daim ən yaxşı nəticələri əldə etməyə yönəlmək.",
        "Aiming for the best outcomes in research and teaching.",
    ),
    (
        "Alimlərin öz peşə fəaliyyətlərini yüksək əxlaqi dəyərlərlə aparması.",
        "Scholars conduct their professional work with high ethical standards.",
    ),
    (
        "Bir-birinə hörmət və kollektiv akademik mühitin yaradılması.",
        "Mutual respect and a supportive collective academic environment.",
    ),
    (
        "Elmi araşdırmaların açıq və aydın şəkildə aparılması.",
        "Scientific work is conducted openly and clearly.",
    ),
    (
        "Qərarvermə prosesində obyektivlik və hesabatlılığın təmin olunması.",
        "Objectivity and accountability in decision-making processes.",
    ),
    (
        "Bu dəyərlər alimlər arasında həmrəyliyi gücləndirir, beynəlxalq elmi mühitdə etibarı artırır "
        "və gənc tədqiqatçılar üçün sağlam akademik ənənələr yaradır.",
        "These values strengthen solidarity among scholars, build trust in the international scientific community "
        "and establish sound academic traditions for young researchers.",
    ),
    ("Dünya Azərbaycanlı Alimlər Birliyi", "World Association of Azerbaijani Scientists"),
    ("Əlaqə", "Contact"),
    ("Ünvan", "Address"),
    ("Türkiyə", "Türkiye"),
    ("Rəhbərlik", "Leadership"),
    ("DAAB İdarə Heyətinin Sədri", "Chair of the DAAB Executive Board"),
]


def postprocess_membership_en(html: str) -> str:
    html = re.sub(
        r'<div class="lang-card">\s*<div class="lang-label">(?:Dünya Azərbaycanlı|World Association of Azerbaijani Scientists \(DAAB\)).*?</div>\s*'
        r'<p><strong>DAAB</strong>.*?</p>\s*<p>DAAB elm.*?</p>\s*</div>\s*',
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r'<p><strong>DAAB</strong>.*?</p>\s*<p>DAAB elm.*?</p>\s*</div>\s*',
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = re.sub(
        r"<article class=\"card\">\s*<div class=\"card-header\">✒️ Üzvlük Şərtləri</div>.*?</article>\s*",
        "",
        html,
        count=1,
        flags=re.DOTALL,
    )
    html = html.replace("✒️ Terms of Membership", "✒️ Membership Terms")
    html = re.sub(
        r"\.cards\{display:grid;grid-template-columns:1fr 1fr",
        ".cards{display:grid;grid-template-columns:1fr",
        html,
        count=1,
    )
    html = re.sub(
        r"\.intro-card\{display:grid;grid-template-columns:1fr 1fr",
        ".intro-card{display:grid;grid-template-columns:1fr",
        html,
        count=1,
    )
    return html


def postprocess_activities_en(html: str) -> str:
    html = html.replace('src="/images/', 'src="../images/')
    for old, new in (
        ("Executive Boardnin həmsədri", "Executive Board Co-Chair"),
        ("Executive Boardnin sədri", "Executive Board Chair"),
        ("Executive Boardnin Sədri", "Executive Board Chair"),
        ("Executive Boardnin üzvü", "Executive Board member"),
        ("Executive Boardnin üzvləri", "Executive Board members"),
        ("Executive Boardnin", "of the Executive Board"),
        ("Search üçün yazmağa başlayın…", "Start typing to search…"),
    ):
        html = html.replace(old, new)
    return html


def postprocess_charter_en(html: str) -> str:
    html = re.sub(r"<h2>Maddə (\d+)\.</h2>", r"<h2>Article \1.</h2>", html)
    return html


def postprocess_scientists_list_en(html: str) -> str:
    html = html.replace(" nəticə", " results")
    html = html.replace(" ümumi)", " total)")
    html = html.replace('href="/cv/', 'href="../../cv/')
    return html


def postprocess_scientists_profiles_en(html: str) -> str:
    return postprocess_scientists_list_en(html)


def publish_from_az(
    az_rel: str,
    en_rel: str,
    active_nav: str,
    replacements: list[tuple[str, str]],
    postprocess: callable[[str], str] | None = None,
) -> None:
    az_path = ROOT / az_rel
    en_path = ROOT / en_rel
    en_parts = Path(en_rel).parts
    nav_depth = max(0, len(en_parts) - 2)
    asset_root = "../" * (nav_depth + 1)
    html = az_path.read_text(encoding="utf-8")
    html = strip_legacy_redirect_meta(html)
    html = html.replace('data-daab-lang="az"', 'data-daab-lang="en"')
    html = re.sub(r'\s*lang="az"\s*', " ", html, count=1)
    html = re.sub(
        r'data-daab-asset-root="[^"]*"',
        f'data-daab-asset-root="{asset_root}"',
        html,
        count=1,
    )
    html = re.sub(r"<html([^>]*)lang=\"az\"", r'<html\1lang="en"', html, count=1, flags=re.I)
    if EN_COMPLETE_MARKER not in html:
        html = html.replace("<head>", f"<head>\n{EN_COMPLETE_MARKER}", 1)

    html = re.sub(
        r"<nav[^>]*class=\"nav-strip\".*?</nav>",
        en_nav_html(active_nav, nav_depth),
        html,
        count=1,
        flags=re.DOTALL | re.IGNORECASE,
    )
    html = re.sub(r'<div id="daab-locale-hint".*?</div>\s*', "", html, flags=re.DOTALL)
    for old, new in sorted(replacements, key=lambda pair: len(pair[0]), reverse=True):
        if new:
            html = html.replace(old, new)
    if postprocess:
        html = postprocess(html)
    html = re.sub(r'\s*lang="az"\s*', " ", html)
    html = re.sub(r"<html([^>\n]*)>", r'<html lang="en"\1>', html, count=1, flags=re.I)
    html = re.sub(
        r"<html([^>]*)\s+lang=\"en\"\s+lang=\"en\"",
        r'<html lang="en"\1',
        html,
        count=1,
        flags=re.I,
    )
    html = re.sub(r"<html([^>\n]*)\n", r"<html\1>\n", html, count=1, flags=re.I)
    html = re.sub(r"<footer class=\"footer-pro\">.*?</footer>", en_footer_html(), html, flags=re.DOTALL)
    en_path.parent.mkdir(parents=True, exist_ok=True)
    en_path.write_text(html, encoding="utf-8", newline="\n")
    print(f"Published {en_path.relative_to(ROOT)}")


def publish_mission() -> None:
    publish_from_az("az/mission.html", "en/mission.html", "mission", MISSION_REPLACEMENTS)


def publish_foundation() -> None:
    publish_from_az(
        "az/foundation.html",
        "en/foundation.html",
        "foundation",
        FOUNDATION_REPLACEMENTS,
    )


def publish_membership() -> None:
    publish_from_az(
        "az/membership.html",
        "en/membership.html",
        "membership",
        MEMBERSHIP_REPLACEMENTS,
        postprocess_membership_en,
    )


def publish_executive_board() -> None:
    publish_from_az(
        "az/executive-board.html",
        "en/executive-board.html",
        "executive-board",
        EXECUTIVE_BOARD_REPLACEMENTS,
    )


def publish_activities() -> None:
    publish_from_az(
        "az/activities.html",
        "en/activities.html",
        "activities",
        ACTIVITIES_REPLACEMENTS,
        postprocess_activities_en,
    )


def publish_charter() -> None:
    publish_from_az(
        "az/charter.html",
        "en/charter.html",
        "charter",
        CHARTER_REPLACEMENTS,
        postprocess_charter_en,
    )


def publish_scientists_list() -> None:
    publish_from_az(
        "az/scientists/list.html",
        "en/scientists/list.html",
        "scientists-list",
        SCIENTISTS_LIST_REPLACEMENTS,
        postprocess_scientists_list_en,
    )


def publish_scientists_profiles() -> None:
    publish_from_az(
        "az/scientists/profiles.html",
        "en/scientists/profiles.html",
        "scientists-profiles",
        SCIENTISTS_PROFILES_REPLACEMENTS,
        postprocess_scientists_profiles_en,
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "page",
        nargs="?",
        choices=[
            "mission",
            "foundation",
            "membership",
            "executive-board",
            "activities",
            "charter",
            "scientists-list",
            "scientists-profiles",
            "scientists",
            "all",
        ],
        default="all",
    )
    args = parser.parse_args()
    pages = {
        "mission": publish_mission,
        "foundation": publish_foundation,
        "membership": publish_membership,
        "executive-board": publish_executive_board,
        "activities": publish_activities,
        "charter": publish_charter,
        "scientists-list": publish_scientists_list,
        "scientists-profiles": publish_scientists_profiles,
    }
    if args.page == "scientists":
        publish_scientists_list()
        publish_scientists_profiles()
        return 0
    if args.page == "all":
        for fn in pages.values():
            fn()
    else:
        pages[args.page]()
    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Build az|en membership_flyer.html — print-ready one-page membership promo."""
from __future__ import annotations

import html
import json
import re
import urllib.parse

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

ASSET = "../"
FLYER_CSS_V = STYLE_VERSIONS["daab-membership-flyer.css"]
FONT_LINK = '<link href="{ASSET}css/daab-fonts.css?v=1" rel="stylesheet"/>'
DESIGN_TOKENS_V = SCRIPT_VERSIONS["daab-design-tokens.js"]
MEMBERSHIP_HTML = {
    "az": ROOT / "az" / "membership_value.html",
    "en": ROOT / "en" / "membership_value.html",
}
NAV_ARIA = {"az": "Əsas naviqasiya", "en": "Main navigation"}
SKIP = {"az": "Məzmuna keç", "en": "Skip to content"}

APPLY_URL = {
    "az": "https://daab-waas.com/az/application.html",
    "en": "https://daab-waas.com/en/application.html",
}
MEMBERSHIP_URL = {
    "az": "https://daab-waas.com/az/membership_value.html",
    "en": "https://daab-waas.com/en/membership_value.html",
}

AZ_FLAG_SVG = (
    '<svg class="daab-az-flag" viewBox="0 0 60 30" xmlns="http://www.w3.org/2000/svg" '
    'aria-hidden="true" focusable="false">'
    '<rect width="60" height="30" fill="#00b9e4"/>'
    '<rect y="10" width="60" height="10" fill="#ef3340"/>'
    '<rect y="20" width="60" height="10" fill="#509e2f"/>'
    '<circle cx="27" cy="15" r="4" fill="#fff"/>'
    '<circle cx="28.4" cy="15" r="3.4" fill="#ef3340"/>'
    '<path d="M33.4 11.5l1 2.2 2.4.1-1.9 1.5.7 2.3-2.2-1.3-2.2 1.3.7-2.3-1.9-1.5 2.4-.1z" fill="#fff"/>'
    "</svg>"
)

LOCALES = {
    "az": {
        "lang": "az",
        "title": "DAAB — Üzvlük flyer",
        "description": "DAAB üzvlüyünün dəyəri — potensial üzvlər üçün çap flyer.",
        "hero_h1": "Üzvlüyə <span>Dəvət Məktubu</span>",
        "hero_subtitle": "Potensial üzvlərə dəvət məktubu göndərin",
        "panel_title": "Həmkarlarınızı məktub vasitəsilə dəvət edin",
        "panel_copy": (
            "Bu səhifədə DAAB üzvlüyünün dəyərini qısa şəkildə təqdim edən və paylaşmağa hazır "
            "dəvət məktubu yerləşdirilib. Məktubun yuxarı sağ küncündəki Çap/PDF düyməsindən "
            "istifadə edərək onu PDF formatında yaradın, çap edin və ya e-poçt vasitəsilə paylaşın"
        ),
        "toolbar_hint": "Brauzerdə «Çap» → «PDF kimi yadda saxla» seçin.",
        "controls_aria": "Flyer idarəetməsi",
        "print_btn": "Çap / PDF",
        "print_tooltip": "Brauzerin çap pəncərəsini açın və «PDF kimi yadda saxla» seçin.",
        "email_btn": "Paylaş",
        "share_tooltip": "PDF yaradın və cihazın sistem paylaşma menyusunda tətbiq seçərək paylaşın.",
        "email_subject": "Dünya Azərbaycanlı Alimlər Birliyinə üzv olun",
        "email_pdf_filename": "DAAB-uzvluk-flyeri.pdf",
        "email_busy": "PDF hazırlanır…",
        "email_attach_note": (
            "Bu e-poçta yüklənmiş PDF flyer faylını əlavə edin."
        ),
        "email_error": "PDF yaradıla bilmədi. Yenidən cəhd edin.",
        "print_fallback_alert": (
            "PDF yükləndi. Faylı açın və «Çap» → «PDF kimi yadda saxla» seçin."
        ),
        "print_error_alert": "Flyer PDF-i çap üçün hazırlanmadı.",
        "share_fallback_alert": (
            "PDF yükləndi. Faylı «Fayllar» və ya «Endirmələr» qovluğundan WhatsApp, e-poçt və "
            "digər tətbiqlərlə paylaşa bilərsiniz."
        ),
        "share_ready_confirm": "PDF hazırdır. Sistem paylaşma menyusunu açmaq istəyirsiniz?",
        "share_secure_context_alert": (
            "Paylaşma təhlükəsiz bağlantı (HTTPS) tələb edir. PDF endirildi."
        ),
        "org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "brand_short": "DAAB",
        "headline": "Niyə <span>DAAB üzvü</span> olmalısınız?",
        "lead": (
            "DAAB üzvlüyü sadəcə bir təşkilata qoşulmaq deyil — peşəkar nüfuzunuzu artıran, "
            "beynəlxalq əlaqələrinizi genişləndirən və Azərbaycanın elmi-intellektual gələcəyinə "
            "töhfə verməyə imkan verən qlobal Azərbaycan elmi ekosisteminin bir hissəsidir."
        ),
        "stats": [("🌍", "Tanınma"), ("🤝", "Əlaqələr"), ("🚀", "İnkişaf")],
        "pillars_title": "Üzvlüyün əsas dəyəri",
        "pillars": [
            ("Peşəkar tanınma", "Elmi fəaliyyətiniz daha geniş auditoriyaya çatır."),
            ("Əməkdaşlıq şəbəkəsi", "Alimlər, universitetlər və mərkəzlərlə əlaqə."),
            ("Karyera dəstəyi", "Layihə, mentorluq və təqdimat imkanları."),
            ("Milli töhfə", "Azərbaycan elminə real xidmət kanalı."),
        ],
        "benefits_title": "Əsas üstünlüklər",
        "benefits": [
            ("🌐", "Qlobal elmi tanınma", "Profiliniz və elmi fəaliyyətiniz platformada görünür.", ["Alimlər kataloqu", "Beynəlxalq auditoriya"]),
            ("🤝", "Güclü əlaqələr şəbəkəsi", "Dünyanın müxtəlif ölkələrindəki azərbaycanlı alimlərlə əlaqə.", ["Birgə layihələr", "Universitet əməkdaşlığı"]),
            ("🚀", "Karyera və inkişaf", "Akademik və peşəkar nüfuzun güclənməsi.", ["Forum və seminarlar", "Mentorluq mühiti"]),
            ("🇦🇿", "Azərbaycana töhfə", "Biliklərinizi universitet və gənclərlə bölüşün.", ["Gənc alimlərə dəstək", "Elmi diplomatiya"]),
            ("🧠", "İdeyalar platforması", "Fərdi ideyalar kollektiv təşəbbüslərə çevrilir.", ["Məruzə və nəşrlər", "Forum ideyaları"]),
            ("🎓", "Gənc alimlər üçün", "Təcrübə, istiqamət və beynəlxalq mühit.", ["Mentor dəstəyi", "Elmi inkişaf"]),
        ],
        "youth_title": "Gənc tədqiqatçılar",
        "youth_lead": "DAAB gənc alimlər üçün beynəlxalq akademik mühitə çıxış imkanıdır.",
        "youth_items": [
            ("Mentor dəstəyi", "Təcrübəli alimlərlə ünsiyyət"),
            ("Elmi inkişaf", "Məqalə, layihə, təqdimat"),
            ("Beynəlxalq mühit", "Diaspora alimlərinin təcrübəsi"),
        ],
        "cta_title": "Qlobal Azərbaycan elmi ekosisteminin bir hissəsi olun",
        "cta_copy": (
            "Üzvlük yalnız adınızın siyahıda olması deyil — bilik, təcrübə, əlaqə və vətənə xidmət "
            "enerjisinin ortaq məqsəd ətrafında birləşməsidir."
        ),
        "cta_btn": "Bizə qoşulun",
        "cta_href": "application.html",
        "fees": "Üzvlük haqqı: 5 USD/ay və ya 60 USD/il",
        "contact_email": "info@daab-waas.com",
        "contact_site": "daab-waas.com",
        "qr_caption": "Onlayn müraciət",
        "tagline": "© 2026 DAAB / WAAS — Dünya Azərbaycanlı Alimlər Birliyi",
    },
    "en": {
        "lang": "en",
        "title": "WAAS — Membership flyer",
        "description": "Value of WAAS membership — printable flyer for potential members.",
        "hero_h1": "Membership <span>Invitation Letter</span>",
        "hero_subtitle": "Share invitation letter with potential members",
        "panel_title": "Invite colleagues with the letter",
        "panel_copy": (
            "This page provides a ready-to-share letter summarizing WAAS membership value. Use "
            "the Print.PDF button at the top right of the letter to create a PDF, print, or share by email."
        ),
        "toolbar_hint": "Use Print → Save as PDF in your browser.",
        "controls_aria": "Flyer actions",
        "print_btn": "Print / PDF",
        "print_tooltip": "Open the browser print dialog and choose Save as PDF.",
        "email_btn": "Share",
        "share_tooltip": "Generate PDF and share via your device's native sharing apps.",
        "email_subject": "Join the World Association of Azerbaijani Scientists (WAAS)",
        "email_pdf_filename": "WAAS-membership-flyer.pdf",
        "email_busy": "Preparing PDF…",
        "email_attach_note": (
            "Please attach the membership flyer PDF that was just downloaded to this email."
        ),
        "email_error": "Could not create the PDF. Please try again.",
        "print_fallback_alert": (
            "The PDF was downloaded. Open it and choose Print, or Save as PDF in the print dialog."
        ),
        "print_error_alert": "Could not prepare the flyer PDF for printing.",
        "share_fallback_alert": (
            "The PDF was downloaded. Share it from your Files or Downloads folder via WhatsApp, "
            "email, or another app."
        ),
        "share_ready_confirm": "PDF ready. Open the system sharing menu?",
        "share_secure_context_alert": (
            "Sharing requires a secure connection (HTTPS). The PDF was downloaded instead."
        ),
        "org": "World Association of Azerbaijani Scientists",
        "brand_short": "WAAS",
        "headline": "Why <span>become a WAAS</span> member?",
        "lead": (
            "WAAS membership is not simply joining an association — it means becoming part of a "
            "global Azerbaijani scientific ecosystem that enhances your visibility, expands "
            "international connections, and enables meaningful contribution to Azerbaijan's "
            "scientific and intellectual future."
        ),
        "stats": [("🌍", "Visibility"), ("🤝", "Connections"), ("🚀", "Growth")],
        "pillars_title": "Core value of membership",
        "pillars": [
            ("Professional visibility", "Your scientific work reaches a wider audience."),
            ("Collaboration network", "Links with scientists, universities, and centres."),
            ("Career support", "Projects, mentoring, and presentation opportunities."),
            ("National contribution", "A real channel for serving Azerbaijani science."),
        ],
        "benefits_title": "Key benefits",
        "benefits": [
            ("🌐", "Global scientific visibility", "Your profile and activity are showcased on the platform.", ["Scientists' directory", "International audience"]),
            ("🤝", "Strong network", "Connect with Azerbaijani scientists worldwide.", ["Joint projects", "University cooperation"]),
            ("🚀", "Career & growth", "Strengthen your academic and professional reputation.", ["Forums & seminars", "Mentoring environment"]),
            ("🇦🇿", "Contributing to Azerbaijan", "Share knowledge with universities and young researchers.", ["Youth support", "Scientific diplomacy"]),
            ("🧠", "Platform for ideas", "Turn individual ideas into collective initiatives.", ["Talks & publications", "Forum proposals"]),
            ("🎓", "For young scientists", "Experience, direction, and international exposure.", ["Mentor support", "Research development"]),
        ],
        "youth_title": "Young researchers",
        "youth_lead": "WAAS offers young scientists access to an international academic environment.",
        "youth_items": [
            ("Mentor support", "Guidance from experienced scientists"),
            ("Research growth", "Articles, projects, presentations"),
            ("Global context", "Diaspora scientists' experience"),
        ],
        "cta_title": "Join the global Azerbaijani scientific ecosystem",
        "cta_copy": (
            "Membership is not just having your name on a list — it is uniting knowledge, "
            "experience, connections, and service to the homeland around a shared purpose."
        ),
        "cta_btn": "Join us",
        "cta_href": "application.html",
        "fees": "Membership fee: 5 USD/month or 60 USD/year",
        "contact_email": "info@daab-waas.com",
        "contact_site": "daab-waas.com",
        "qr_caption": "Apply online",
        "tagline": "© 2026 WAAS — World Association of Azerbaijani Scientists",
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


def shell_head(cfg: dict) -> str:
    sv = SCRIPT_VERSIONS
    st = STYLE_VERSIONS
    return f"""<!DOCTYPE html>
<html lang="{cfg["lang"]}" data-daab-lang="{cfg["lang"]}" data-daab-asset-root="{ASSET}" data-daab-page-id="membership-flyer" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(cfg["title"])}</title>
<meta name="description" content="{esc(cfg["description"])}"/>
<meta name="robots" content="noindex"/>
{FONT_LINK.format(ASSET=ASSET)}
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-content-hero.css?v={st["daab-content-hero.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-tokens.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-membership-flyer.css?v={FLYER_CSS_V}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-design-tokens.js?v={DESIGN_TOKENS_V}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v={sv["daab-breadcrumbs.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v=2" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
</head>
"""


def hero_block(cfg: dict) -> str:
    return f"""<header class="hero">
<div class="hero-wrap shell">
<section>
<h1 aria-describedby="page-hero-subtitle">{cfg["hero_h1"]}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(cfg["hero_subtitle"])}</p>
</section>
<aside aria-label="{esc(cfg["panel_title"])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(cfg["panel_title"])}</h2>
<p class="panel-copy">{esc(cfg["panel_copy"])}</p>
</div>
</aside>
</div>
</header>
"""


def benefit_icon_markup(icon: str) -> str:
    if icon == "🇦🇿":
        return (
            f'<div class="flyer-benefit-icon flyer-benefit-icon--flag" aria-hidden="true">'
            f"{AZ_FLAG_SVG}</div>"
        )
    return f'<div class="flyer-benefit-icon" aria-hidden="true">{icon}</div>'


def qr_img_url(target: str) -> str:
    return (
        "https://api.qrserver.com/v1/create-qr-code/?size=144x144&margin=0&data="
        + urllib.parse.quote(target, safe="")
    )


def build_email_body(cfg: dict, lang: str) -> str:
    membership_url = MEMBERSHIP_URL[lang]
    apply_url = APPLY_URL[lang]

    if lang == "az":
        return "\n".join(
            [
                "Hörmətli həmkar,",
                "",
                "Sizi Dünya Azərbaycanlı Alimlər Birliyinə (DAAB) qoşulmağa dəvət etmək istəyirəm.",
                "",
                "Ətraflı məlumat: " + membership_url,
                "Onlayn müraciət: " + apply_url,
                "",
                cfg["email_attach_note"],
                "",
                "Hörmətlə,",
                "[Adınız]",
            ]
        )

    return "\n".join(
        [
            "Dear colleague,",
            "",
            "I would like to invite you to join the World Association of "
            "Azerbaijani Scientists (WAAS).",
            "",
            "Learn more: " + membership_url,
            "Apply online: " + apply_url,
            "",
            cfg["email_attach_note"],
            "",
            "Best regards,",
            "[Your name]",
        ]
    )


def email_page_scripts(cfg: dict, lang: str) -> str:
    payload = {
        "subject": cfg["email_subject"],
        "body": build_email_body(cfg, lang),
        "pdfFilename": cfg["email_pdf_filename"],
        "busyLabel": cfg["email_busy"],
        "errorAlert": cfg["email_error"],
        "printFallbackAlert": cfg["print_fallback_alert"],
        "printErrorAlert": cfg["print_error_alert"],
        "shareReadyConfirm": cfg["share_ready_confirm"],
        "shareSecureContextAlert": cfg["share_secure_context_alert"],
        "shareFallbackAlert": cfg["share_fallback_alert"],
    }
    data = json.dumps(payload, ensure_ascii=False)
    js_v = SCRIPT_VERSIONS["daab-membership-flyer-email.js"]
    vendor = f'{ASSET}js/vendor'
    return f"""<script>window.DAAB_FLYER_EMAIL = {data};</script>
<script src="{ASSET}js/daab-membership-flyer-email.js?v={js_v}" defer></script>"""


def build_locale(key: str) -> None:
    cfg = LOCALES[key]
    membership_path = MEMBERSHIP_HTML[key]
    membership_html = membership_path.read_text(encoding="utf-8")
    nav = extract_nav(membership_html, NAV_ARIA[key])
    if not nav:
        raise SystemExit(f"Could not extract nav from {membership_path}")
    apply_abs = APPLY_URL[key]
    qr_url = qr_img_url(apply_abs)

    stats_html = "".join(
        f'<span class="flyer-stat"><strong>{esc(icon)}</strong>{esc(label)}</span>'
        for icon, label in cfg["stats"]
    )
    pillars_html = "".join(
        f'<div class="flyer-pillar"><strong>{esc(t)}</strong><span>{esc(d)}</span></div>'
        for t, d in cfg["pillars"]
    )
    benefits_html = ""
    for icon, title, desc, bullets in cfg["benefits"]:
        bullets_html = "".join(f"<li>{esc(b)}</li>" for b in bullets)
        benefits_html += (
            f'<article class="flyer-benefit">'
            f"{benefit_icon_markup(icon)}"
            f"<h3>{esc(title)}</h3><p>{esc(desc)}</p>"
            f"<ul>{bullets_html}</ul></article>"
        )
    youth_html = "".join(
        f'<div class="flyer-youth-item"><strong>{esc(t)}</strong>{esc(d)}</div>'
        for t, d in cfg["youth_items"]
    )

    page = shell_head(cfg) + f"""<body class="membership-flyer-page membership-page">
<a class="skip" href="#content">{SKIP[key]}</a>
{nav}
{hero_block(cfg)}
<main class="main membership-flyer-main" id="content">
<div class="flyer-wrap">
<div class="flyer-page-controls" role="toolbar" aria-label="{esc(cfg["controls_aria"])}" data-flyer-export-exclude="1">
<button type="button" class="flyer-btn flyer-btn-primary" id="flyerPrintPdfBtn" title="{esc(cfg["print_tooltip"])}" aria-label="{esc(cfg["print_tooltip"])}">{esc(cfg["print_btn"])}</button>
</div>
<article class="flyer-sheet" aria-label="{esc(cfg["title"])}">
<header class="flyer-header">
<img class="flyer-logo" src="{ASSET}images/daab-logo.png" alt="{esc(cfg["brand_short"])}" width="72" height="72"/>
<div class="flyer-brand-block">
<p class="flyer-org">{esc(cfg["org"])}</p>
<h1>{esc(cfg["brand_short"])}</h1>
</div>
</header>
<section class="flyer-hero">
<h2>{cfg["headline"]}</h2>
<p>{esc(cfg["lead"])}</p>
<div class="flyer-stats">{stats_html}</div>
</section>
<section aria-labelledby="flyer-pillars-title">
<h2 class="flyer-section-title" id="flyer-pillars-title">{esc(cfg["pillars_title"])}</h2>
<div class="flyer-pillars">{pillars_html}</div>
</section>
<section aria-labelledby="flyer-benefits-title">
<h2 class="flyer-section-title" id="flyer-benefits-title">{esc(cfg["benefits_title"])}</h2>
<div class="flyer-benefits">{benefits_html}</div>
</section>
<section class="flyer-youth" aria-labelledby="flyer-youth-title">
<div class="flyer-youth-lead">
<strong id="flyer-youth-title">{esc(cfg["youth_title"])}</strong>
{esc(cfg["youth_lead"])}
</div>
{youth_html}
</section>
<footer class="flyer-footer">
<div class="flyer-cta">
<h3>{esc(cfg["cta_title"])}</h3>
<p>{esc(cfg["cta_copy"])}</p>
<a class="flyer-cta-link" href="{esc(cfg["cta_href"])}">{esc(cfg["cta_btn"])}</a>
<div class="flyer-meta">
<p><strong>{esc(cfg["fees"])}</strong></p>
<p>✉ <a href="mailto:{esc(cfg["contact_email"])}">{esc(cfg["contact_email"])}</a><br/>
🌐 <a href="https://{esc(cfg["contact_site"])}">{esc(cfg["contact_site"])}</a><br/>
🔗 {esc(apply_abs)}</p>
</div>
</div>
<div class="flyer-qr">
<img src="{qr_url}" width="72" height="72" alt="{esc(cfg["qr_caption"])}" decoding="async" crossorigin="anonymous"/>
<span>{esc(cfg["qr_caption"])}</span>
</div>
</footer>
<p class="flyer-tagline">{esc(cfg["tagline"])}</p>
</article>
</div>
</main>
{email_page_scripts(cfg, key)}
</body>
</html>
"""
    out = ROOT / key / "membership_flyer.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(ROOT)}")


def main() -> None:
    for key in LOCALES:
        build_locale(key)


if __name__ == "__main__":
    main()

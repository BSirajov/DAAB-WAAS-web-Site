#!/usr/bin/env python3
"""Build az|en sponsors_flyer.html — print-ready one-page sponsorship promo."""
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
SPONSORS_HTML = {
    "az": ROOT / "az" / "sponsorship_partnership.html",
    "en": ROOT / "en" / "sponsorship_partnership.html",
}
NAV_ARIA = {"az": "Əsas naviqasiya", "en": "Main navigation"}
SKIP = {"az": "Məzmuna keç", "en": "Skip to content"}

SPONSORS_URL = {
    "az": "https://daab-waas.com/az/sponsorship_partnership.html",
    "en": "https://daab-waas.com/en/sponsorship_partnership.html",
}
CONTACT_URL = {
    "az": "https://daab-waas.com/az/sponsorship_partnership.html#contact",
    "en": "https://daab-waas.com/en/sponsorship_partnership.html#contact",
}
FLYER_PAGE_URL = {
    "az": "https://daab-waas.com/az/sponsors_flyer.html",
    "en": "https://daab-waas.com/en/sponsors_flyer.html",
}

LOCALES = {
    "az": {
        "lang": "az",
        "title": "DAAB — Sponsorluq dəvət məktubu",
        "description": "DAAB sponsorluğu və strateji tərəfdaşlıq — potensial tərəfdaşlar üçün çap olunan dəvət məktubu.",
        "hero_h1": "Sponsorluq <span>Dəvət Məktubu</span>",
        "hero_subtitle": "Potensial tərəfdaşlar üçün paylaşıla bilən dəvət məktubu",
        "panel_title": "Tərəfdaşlara dəvət məktubu göndərin",
        "panel_copy": (
            "Bu səhifədə DAAB sponsorluğu və tərəfdaşlıq təklifini qısa şəkildə təqdim edən "
            "paylaşmağa hazır dəvət məktubu yerləşdirilib. Sağ alt küncdəki «Çap et / PDF» düyməsindən "
            "istifadə edərək brauzerin çap pəncərəsini açın və «PDF kimi yadda saxla» seçin."
        ),
        "controls_aria": "Dəvət məktubu idarəetməsi",
        "print_btn": "Çap et / PDF",
        "print_tooltip": "Brauzerin çap pəncərəsini açın və «PDF kimi yadda saxla» seçin.",
        "email_btn": "Paylaş",
        "share_tooltip": "PDF yaradın və paylaşma menyusundan tətbiq seçin.",
        "email_subject": "DAAB sponsorluğuna dəstək verin",
        "email_pdf_filename": "DAAB-sponsorluq-devet-mektubu.pdf",
        "email_busy": "PDF hazırlanır…",
        "email_attach_note": "Bu e-poçta yüklənmiş PDF dəvət məktubu faylını əlavə edin.",
        "email_error": "PDF yaradıla bilmədi. Yenidən cəhd edin.",
        "print_fallback_alert": (
            "PDF yükləndi. Faylı açın və «Çap» → «PDF kimi yadda saxla» seçin."
        ),
        "print_error_alert": "Dəvət məktubu PDF-i çap üçün hazırlanmadı.",
        "share_fallback_alert": (
            "PDF yükləndi. Faylı «Fayllar» və ya «Endirmələr» qovluğundan WhatsApp, e-poçt və "
            "digər tətbiqlərlə paylaşa bilərsiniz."
        ),
        "share_ready_confirm": "PDF hazırdır. Sistem paylaşma menyusunu açmaq istəyirsiniz?",
        "share_secure_context_alert": (
            "Paylaşma təhlükəsiz bağlantı (HTTPS) tələb edir. PDF endirildi."
        ),
        "share_document_title": "Sponsorluq Dəvət Məktubu",
        "share_dialog_title": "«{title}» paylaşın",
        "share_invite_placeholder": "Dəvət üçün ad və ya e-poçt daxil edin",
        "share_whatsapp": "WhatsApp",
        "share_outlook": "Microsoft Outlook",
        "share_teams": "Microsoft Teams",
        "share_gmail": "Gmail",
        "share_get_link": "Keçidi əldə et",
        "share_email": "E-poçt",
        "share_pdf_file": "PDF faylı ilə paylaş",
        "share_note": "Paylaşarkən dəvət məktubunun PDF surəti cihazınızda hazırlanır.",
        "share_link_copied": "Keçid mübadilə buferinə kopyalandı.",
        "share_close": "Bağla",
        "share_download_first": "PDF endirildi — mesajınıza əlavə edin.",
        "org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "brand_short": "DAAB",
        "headline": "Sponsorluq və <span>tərəfdaşlıq</span>",
        "lead": (
            "DAAB strateji tərəfdaşları elm, təhsil, innovasiya və insan kapitalına sərmayə qoymağa dəvət edir — "
            "təşkilatınız üçün brend tanınması, beynəlxalq alim şəbəkəsinə çıxış və ölçülə bilən sosial təsir."
        ),
        "stats": [("🌐", "Brend tanınması"), ("🤝", "Şəbəkə əlaqəsi"), ("🏅", "Ölçülə bilən təsir")],
        "pillars_title": "Sponsorluq paketləri",
        "pillars": [
            ("💎 Platin / Baş", "€50 000+ — açılış çıxışı, prioritet loqo, media"),
            ("🥇 Qızıl", "€25 000–49 999 — panel sponsorluğu, loqo, şəbəkələşmə"),
            ("🥈 Gümüş", "€10 000–24 999 — sponsor siyahısı, loqo, veb-sayt"),
            ("🥉 Bürünc", "€5 000–9 999 — veb-sayt və DAAB materiallarında qeyd"),
        ],
        "benefits_title": "Sponsor üçün üstünlüklər",
        "benefits": [
            ("🌐", "Brendinizin tanınması", "DAAB materiallarında, veb-sayt, media və rəsmi tədbirlərdə tanınma.", ["Loqo yerləşdirməsi", "Beynəlxalq platforma"]),
            ("🏅", "Nüfuz və hesabatlılıq", "Elm, təhsil və innovasiyaya sərmayə qoyan etibarlı tərəfdaş imici.", ["Sosial təsir", "İllik hesabat"]),
            ("🤝", "Diaspora şəbəkəsi", "20-dən çox ölkədən alim və ekspertlərlə birbaşa əlaqə.", ["Mentorluq", "VIP dialoq"]),
            ("🔬", "Elmi əməkdaşlıq", "Universitetlər və AMEA ilə körpü; ortaq tədqiqat imkanları.", ["Ortaq nəşrlər", "Bilik transferi"]),
            ("📚", "İnnovasiya və nəşrlər", "Prioritet sahələrdə birgə layihələr və açıq elmi mühit.", ["Ekspert hesabatları", "Açıq giriş"]),
            ("🎓", "İnsan kapitalı", "Gənc tədqiqatçılar, təqaüdlər və Qarabağ Universiteti dəstəyi.", ["Doktorantura", "Region universitetləri"]),
        ],
        "cta_title": "Əməkdaşlıq üçün növbəti addım",
        "cta_copy": (
            "DAAB rəhbərlik etdiyiniz şirkətlə təqdimat görüşü keçirməyə və mümkün əməkdaşlıq formatlarını "
            "müzakirə etməyə hazırdır."
        ),
        "cta_btn": "info@daab-waas.com",
        "cta_href": "sponsorship_partnership.html#contact",
        "fees": "Bütün paketlər: rəsmi təşəkkür, hesabatlılıq və DAAB platformasında tanınma",
        "contact_email": "info@daab-waas.com",
        "contact_site": "daab-waas.com",
        "qr_caption": "Sponsorluq əlaqəsi",
        "tagline": "© 2026 DAAB — Dünya Azərbaycanlı Alimlər Birliyi",
    },
    "en": {
        "lang": "en",
        "title": "WAAS — Sponsorship Invitation Letter",
        "description": "WAAS sponsorship and strategic partnership — printable invitation letter for potential partners.",
        "hero_h1": "Sponsorship <span>Invitation Letter</span>",
        "hero_subtitle": "Shareable invitation letter for potential partners",
        "panel_title": "Share the invitation letter with partners",
        "panel_copy": (
            "This page provides a ready-to-share invitation letter summarizing WAAS sponsorship and "
            "partnership opportunities. Use the Print / PDF button at the bottom right to open "
            "the browser print dialog and choose Save as PDF."
        ),
        "controls_aria": "Flyer actions",
        "print_btn": "Print / PDF",
        "print_tooltip": "Open the browser print dialog and choose Save as PDF.",
        "email_btn": "Share",
        "share_tooltip": "Generate a PDF and share via your device's apps.",
        "email_subject": "Support WAAS through sponsorship",
        "email_pdf_filename": "WAAS-sponsorship-invitation-letter.pdf",
        "email_busy": "Preparing PDF…",
        "email_attach_note": "Please attach the sponsorship flyer PDF that was just downloaded to this email.",
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
        "share_document_title": "Sponsorship Invitation Letter",
        "share_dialog_title": 'Share "{title}"',
        "share_invite_placeholder": "Add name or email to invite",
        "share_whatsapp": "WhatsApp",
        "share_outlook": "Microsoft Outlook",
        "share_teams": "Microsoft Teams",
        "share_gmail": "Gmail",
        "share_get_link": "Get a link",
        "share_email": "Email",
        "share_pdf_file": "Share PDF file",
        "share_note": "A PDF copy of the invitation letter is prepared on your device when you share.",
        "share_link_copied": "Link copied to clipboard.",
        "share_close": "Close",
        "share_download_first": "The PDF was downloaded — attach it to your message.",
        "org": "World Association of Azerbaijani Scientists",
        "brand_short": "WAAS",
        "headline": "Sponsorship &amp; <span>partnership</span>",
        "lead": (
            "WAAS invites strategic partners to invest in science, education, innovation, and human capital — "
            "with brand visibility, access to an international scientist network, and measurable social impact."
        ),
        "stats": [("🌐", "Brand visibility"), ("🤝", "Network access"), ("🏅", "Measurable impact")],
        "pillars_title": "Sponsorship packages",
        "pillars": [
            ("💎 Title / Platinum", "€50,000+ — opening address, priority logo, media"),
            ("🥇 Gold", "€25,000–49,999 — panel sponsorship, logo, networking"),
            ("🥈 Silver", "€10,000–24,999 — sponsor listing, logo, website"),
            ("🥉 Bronze", "€5,000–9,999 — website and WAAS materials listing"),
        ],
        "benefits_title": "Benefits for sponsors",
        "benefits": [
            ("🌐", "Brand visibility", "Recognition across WAAS materials, the website, media, and official events.", ["Logo placement", "International platform"]),
            ("🏅", "Reputation & accountability", "Trusted partner investing in science, education, and innovation.", ["Social impact", "Annual report"]),
            ("🤝", "Diaspora network", "Direct links to scientists and experts from 20+ countries.", ["Mentoring", "VIP dialogue"]),
            ("🔬", "Research collaboration", "Bridges with universities and ANAS; joint research pathways.", ["Co-publications", "Knowledge transfer"]),
            ("📚", "Innovation & publications", "Joint initiatives and open science in priority fields.", ["Expert reports", "Open access"]),
            ("🎓", "Human capital", "Young researchers, scholarships, and Karabakh University support.", ["Doctoral pathways", "Regional universities"]),
        ],
        "cta_title": "Next step toward partnership",
        "cta_copy": (
            "WAAS is ready to hold a presentation meeting with your company and discuss possible "
            "formats of cooperation."
        ),
        "cta_btn": "info@daab-waas.com",
        "cta_href": "sponsorship_partnership.html#contact",
        "fees": "All packages: formal acknowledgment, impact reporting, and visibility across WAAS channels",
        "contact_email": "info@daab-waas.com",
        "contact_site": "daab-waas.com",
        "qr_caption": "Sponsorship contact",
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
<html lang="{cfg["lang"]}" data-daab-lang="{cfg["lang"]}" data-daab-asset-root="{ASSET}" data-daab-page-id="sponsors-flyer" data-daab-nav-mount="1">
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
    return f'<div class="flyer-benefit-icon" aria-hidden="true">{icon}</div>'


def qr_img_url(target: str) -> str:
    return (
        "https://api.qrserver.com/v1/create-qr-code/?size=144x144&margin=0&data="
        + urllib.parse.quote(target, safe="")
    )


def build_email_body(cfg: dict, lang: str) -> str:
    sponsors_url = SPONSORS_URL[lang]
    contact_url = CONTACT_URL[lang]

    if lang == "az":
        return "\n".join(
            [
                "Hörmətli tərəfdaş,",
                "",
                "Sizi DAAB ilə sponsorluq və strateji tərəfdaşlıq çərçivəsində əməkdaşlığa dəvət etmək istəyirəm.",
                "",
                "Ətraflı məlumat: " + sponsors_url,
                "Əlaqə: " + contact_url,
                "",
                cfg["email_attach_note"],
                "",
                "Hörmətlə,",
                "[Adınız]",
            ]
        )

    return "\n".join(
        [
            "Dear partner,",
            "",
            "I would like to invite you to support WAAS through sponsorship and strategic partnership.",
            "",
            "Learn more: " + sponsors_url,
            "Contact: " + contact_url,
            "",
            cfg["email_attach_note"],
            "",
            "Best regards,",
            "[Your name]",
        ]
    )


def flyer_print_button(cfg: dict) -> str:
    return (
        f'<button type="button" class="report-print-btn" id="flyerPrintPdfBtn" '
        f'title="{esc(cfg["print_tooltip"])}" aria-label="{esc(cfg["print_tooltip"])}">'
        f'{esc(cfg["print_btn"])}</button>'
    )


def email_page_scripts(cfg: dict, lang: str) -> str:
    js_v = SCRIPT_VERSIONS["daab-membership-flyer-email.js"]
    return f'<script src="{ASSET}js/daab-membership-flyer-email.js?v={js_v}" defer></script>'


def build_locale(key: str) -> None:
    cfg = LOCALES[key]
    sponsors_path = SPONSORS_HTML[key]
    sponsors_html = sponsors_path.read_text(encoding="utf-8")
    nav = extract_nav(sponsors_html, NAV_ARIA[key])
    if not nav:
        raise SystemExit(f"Could not extract nav from {sponsors_path}")
    if key == "az":
        nav = nav.replace("çap oluna bilən flyer", "çap oluna bilən dəvət məktubu")
    contact_abs = CONTACT_URL[key]
    qr_url = qr_img_url(contact_abs)

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

    page = shell_head(cfg) + f"""<body class="membership-flyer-page sponsors-flyer-page membership-page">
<a class="skip" href="#content">{SKIP[key]}</a>
{nav}
{hero_block(cfg)}
<main class="main membership-flyer-main" id="content">
<div class="flyer-wrap">
<article class="flyer-sheet" aria-label="{esc(cfg["title"])}">
<header class="flyer-header">
<img class="flyer-logo" src="{ASSET}images/daab-logo.png" alt="{esc(cfg["brand_short"])}" width="72" height="72"/>
<div class="flyer-brand-block">
<p class="flyer-org">{esc(cfg["org"])}</p>
<h2 class="flyer-brand-mark">{esc(cfg["brand_short"])}</h2>
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
<footer class="flyer-footer">
<div class="flyer-cta">
<h3>{esc(cfg["cta_title"])}</h3>
<p>{esc(cfg["cta_copy"])}</p>
<a class="flyer-cta-link" href="{esc(cfg["cta_href"])}">{esc(cfg["cta_btn"])}</a>
<div class="flyer-meta">
<p><strong>{esc(cfg["fees"])}</strong></p>
<p>✉ <a href="mailto:{esc(cfg["contact_email"])}">{esc(cfg["contact_email"])}</a><br/>
🌐 <a href="https://{esc(cfg["contact_site"])}">{esc(cfg["contact_site"])}</a><br/>
🔗 {esc(contact_abs)}</p>
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
{flyer_print_button(cfg)}
</main>
{email_page_scripts(cfg, key)}
</body>
</html>
"""
    out = ROOT / key / "sponsors_flyer.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(ROOT)}")


def main() -> None:
    for key in LOCALES:
        build_locale(key)


if __name__ == "__main__":
    main()

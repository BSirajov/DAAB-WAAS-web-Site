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
SPONSORS_HTML = {
    "az": ROOT / "az" / "sponsors.html",
    "en": ROOT / "en" / "sponsors.html",
}
NAV_ARIA = {"az": "Əsas naviqasiya", "en": "Main navigation"}
SKIP = {"az": "Məzmuna keç", "en": "Skip to content"}

SPONSORS_URL = {
    "az": "https://daab-waas.com/az/sponsors.html",
    "en": "https://daab-waas.com/en/sponsors.html",
}
CONTACT_URL = {
    "az": "https://daab-waas.com/az/sponsors.html#contact",
    "en": "https://daab-waas.com/en/sponsors.html#contact",
}

LOCALES = {
    "az": {
        "lang": "az",
        "title": "DAAB — Sponsorluq dəvət məktubu",
        "description": "DAAB sponsorluğu — potensial tərəfdaşlar üçün çap olunan dəvət məktubu.",
        "hero_h1": "Sponsorluğa <span>dəvət</span>",
        "hero_subtitle": "Potensial tərəfdaşlar üçün paylaşıla bilən dəvət məktubu",
        "panel_title": "Tərəfdaşlara dəvət məktubu göndərin",
        "panel_copy": (
            "Bu səhifədə DAAB sponsorluğunun dəyərini və səviyyələrini qısa şəkildə təqdim edən "
            "paylaşmağa hazır dəvət məktubu yerləşdirilib. Məktubun yuxarı sağ küncündəki Çap/PDF düyməsindən "
            "istifadə edərək onu PDF formatında yaradın, çap edin və ya e-poçt vasitəsilə paylaşın"
        ),
        "controls_aria": "Dəvət məktubu idarəetməsi",
        "print_btn": "Çap / PDF",
        "print_tooltip": "Brauzerin çap pəncərəsini açın və «PDF kimi yadda saxla» seçin.",
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
        "org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "brand_short": "DAAB",
        "headline": "Azərbaycan elminə <span>sərmayə yatırın</span>",
        "lead": (
            "DAAB bütün dünyada fəaliyyət göstərən azərbaycanlı alimləri birləşdirir. Sizin dəstəyiniz "
            "təqaüd proqramlarına, elmi əməkdaşlıqlara və ölkəmizin bilik iqtisadiyyatının gələcəyinə töhfə verir."
        ),
        "stats": [("🎓", "Təqaüdlər"), ("🔬", "Əməkdaşlıq"), ("🌐", "Forumlar")],
        "pillars_title": "Sponsorluq səviyyələri",
        "pillars": [
            ("🥉 Bürünc", "€1 000 / il — hesabatda ad, sertifikat"),
            ("🥈 Gümüş", "€5 000 / il — loqo, Forum dəvətləri"),
            ("🥇 Qızıl", "€15 000 / il — VIP, media, birgə layihə"),
            ("💎 Platin", "€30 000+ / il — strategiya, keynote, MoU"),
        ],
        "benefits_title": "Niyə DAAB-a dəstək verməli?",
        "benefits": [
            ("🎓", "Təqaüdlər və proqramlar", "Gənc tədqiqatçıların aparıcı müəssisələrdə iştirakı.", ["Doktorantura", "Postdoktorantura"]),
            ("🔬", "Elmi əməkdaşlıqlar", "Alimlərimizlə universitetlər və AMEA arasında körpü.", ["Ortaq nəşrlər", "Bilik transferi"]),
            ("🌐", "Beynəlxalq forumlar", "Xaricdə yaşayan alimlərin illik Forumu.", ["Milli R&D gündəliyi", "Əməkdaşlıq platforması"]),
            ("🏗️", "Qarabağın bərpası", "Azad edilmiş ərazilərin elmi-texniki bərpasına dəstək.", ["Ekspert potensialı", "Mobilizasiya"]),
            ("📚", "Nəşrlər və açıq çıxış", "Azərbaycan və ingilis dillərində bilik mübadiləsi.", ["Jurnallar", "Açıq giriş"]),
            ("🤝", "Diaspora şəbəkəsi", "Alimlər bazası, mentorluq və mobillik.", ["Karyera imkanları", "Canlı reyestr"]),
        ],
        "cta_title": "Gəlin dəyərli iş birliyi quraq",
        "cta_copy": (
            "Sponsorluğunuz gənc tədqiqatçılar üçün təqaüd proqramlarını, beynəlxalq elmi əməkdaşlıqları "
            "və diaspora alimləri ilə yerli qurumlar arasında bilik mübadiləsini birbaşa dəstəkləyə bilər."
        ),
        "cta_btn": "Əlaqə saxlayın",
        "cta_href": "sponsors.html#contact",
        "fees": "Bütün səviyyələr: rəsmi təşəkkür, hesabatlılıq, İdarə Heyəti ilə birbaşa əlaqə",
        "contact_email": "info@daab-waas.com",
        "contact_site": "daab-waas.com",
        "qr_caption": "Sponsorluq əlaqəsi",
        "tagline": "© 2026 DAAB / WAAS — Dünya Azərbaycanlı Alimlər Birliyi",
    },
    "en": {
        "lang": "en",
        "title": "WAAS — Sponsorship flyer",
        "description": "WAAS sponsorship — printable flyer for potential partners.",
        "hero_h1": "Sponsorship <span>Flyer</span>",
        "hero_subtitle": "Shareable flyer for potential partners",
        "panel_title": "Share the flyer with partners",
        "panel_copy": (
            "This page provides a ready-to-share flyer summarizing WAAS sponsorship levels and impact. "
            "Use the Print/PDF button at the top right of the flyer to create a PDF, print, or share by email."
        ),
        "controls_aria": "Flyer actions",
        "print_btn": "Print / PDF",
        "print_tooltip": "Open the browser print dialog and choose Save as PDF.",
        "email_subject": "Support WAAS through sponsorship",
        "email_pdf_filename": "WAAS-sponsorship-flyer.pdf",
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
        "org": "World Association of Azerbaijani Scientists",
        "brand_short": "WAAS",
        "headline": "Invest in <span>Azerbaijani science</span>",
        "lead": (
            "WAAS unites Azerbaijani scientists around the world. Your support helps fund scholarships, "
            "research collaborations, and the future of Azerbaijan's knowledge economy."
        ),
        "stats": [("🎓", "Scholarships"), ("🔬", "Collaboration"), ("🌐", "Forums")],
        "pillars_title": "Sponsorship tiers",
        "pillars": [
            ("🥉 Bronze", "€1,000 / year — report listing, certificate"),
            ("🥈 Silver", "€5,000 / year — logo, Forum passes"),
            ("🥇 Gold", "€15,000 / year — VIP, media, co-branded research"),
            ("💎 Platinum", "€30,000+ / year — strategy seat, keynote, MoU"),
        ],
        "benefits_title": "Why support WAAS?",
        "benefits": [
            ("🎓", "Scholarships & fellowships", "Early-career researchers at leading institutions.", ["Doctoral study", "Postdoctoral programmes"]),
            ("🔬", "Research collaborations", "Bridging diaspora experts with universities and ANAS.", ["Co-publications", "Know-how transfer"]),
            ("🌐", "International forums", "The regular Forum of Azerbaijani Scientists Abroad.", ["National R&D agenda", "Collaboration platform"]),
            ("🏗️", "Karabakh reconstruction", "Scientific support for liberated territories.", ["Expert mobilisation", "Technical contribution"]),
            ("📚", "Publications & open access", "Knowledge sharing in Azerbaijani and English.", ["Journals", "Open-access materials"]),
            ("🤝", "Diaspora network", "Living registry, mentorship, and mobility.", ["Career pathways", "Global connections"]),
        ],
        "cta_title": "Let's build a meaningful partnership",
        "cta_copy": (
            "Your sponsorship can directly support scholarships for young researchers, international "
            "scientific cooperation, and knowledge exchange between diaspora scientists and local institutions."
        ),
        "cta_btn": "Get in touch",
        "cta_href": "sponsors.html#contact",
        "fees": "All tiers: formal acknowledgment, reporting, direct Board relationship",
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
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..800&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
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
<script src="{ASSET}js/daab-design-tokens.js?v=1" defer></script>
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
                "Sizi Dünya Azərbaycanlı Alimlər Birliyinə (DAAB) sponsorluq ilə dəstəkləməyə dəvət etmək istəyirəm.",
                "",
                "Ətraflı məlumat: " + sponsors_url,
                "Əlaqə forması: " + contact_url,
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
            "I would like to invite you to support the World Association of "
            "Azerbaijani Scientists (WAAS) through sponsorship.",
            "",
            "Learn more: " + sponsors_url,
            "Contact form: " + contact_url,
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
    vendor = f"{ASSET}js/vendor"
    return f"""<script src="{vendor}/html2canvas.min.js"></script>
<script src="{vendor}/jspdf.umd.min.js"></script>
<script>window.DAAB_FLYER_EMAIL = {data};</script>
<script src="{ASSET}js/daab-membership-flyer-email.js?v={js_v}" defer></script>"""


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
<div class="flyer-page-controls" role="toolbar" aria-label="{esc(cfg["controls_aria"])}" data-flyer-export-exclude="1">
<button type="button" class="flyer-btn flyer-btn-primary" id="flyerPrintPdfBtn" title="{esc(cfg["print_tooltip"])}" aria-label="{esc(cfg["print_tooltip"])}">{esc(cfg["print_btn"])}</button>
</div>
<article class="flyer-sheet" aria-label="{esc(cfg["title"])}">
<header class="flyer-header">
<img class="flyer-logo" src="{ASSET}images/daab-logo.svg" alt="" width="72" height="72"/>
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
<img src="{qr_url}" width="72" height="72" alt="" decoding="async" crossorigin="anonymous"/>
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
    out = ROOT / key / "sponsors_flyer.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(ROOT)}")


def main() -> None:
    for key in LOCALES:
        build_locale(key)


if __name__ == "__main__":
    main()

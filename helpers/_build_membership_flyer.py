#!/usr/bin/env python3
"""Build az|en membership_flyer.html — print-ready one-page membership promo."""
from __future__ import annotations

import html
import json
import sys
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "helpers") not in sys.path:
    sys.path.insert(0, str(ROOT / "helpers"))

ASSET = "../"
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
        "toolbar_hint": "Brauzerdə «Çap» → «PDF kimi yadda saxla» seçin.",
        "print_btn": "Çap / PDF",
        "email_btn": "Paylaş",
        "email_subject": "Dünya Azərbaycanlı Alimlər Birliyinə üzv olun",
        "email_pdf_filename": "DAAB-uzvluk-flyeri.pdf",
        "email_busy": "PDF hazırlanır…",
        "email_attach_note": (
            "Bu e-poçta yüklənmiş PDF flyer faylını əlavə edin."
        ),
        "email_error": (
            "PDF yaradıla bilmədi. E-poçt açılır; flyerı «Çap / PDF» ilə saxlayıb əlavə edə bilərsiniz."
        ),
        "web_btn": "Tam səhifə",
        "web_href": "membership_value.html",
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
        "toolbar_hint": "Use Print → Save as PDF in your browser.",
        "print_btn": "Print / PDF",
        "email_btn": "Share",
        "email_subject": "Join the World Association of Azerbaijani Scientists (WAAS)",
        "email_pdf_filename": "WAAS-membership-flyer.pdf",
        "email_busy": "Preparing PDF…",
        "email_attach_note": (
            "Please attach the membership flyer PDF that was just downloaded to this email."
        ),
        "email_error": (
            "Could not create the PDF. Opening email — you can save the flyer via Print / PDF and attach it."
        ),
        "web_btn": "Full page",
        "web_href": "membership_value.html",
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
    }
    data = json.dumps(payload, ensure_ascii=False)
    return f"""<script>window.DAAB_FLYER_EMAIL = {data};</script>
<script src="{ASSET}js/daab-membership-flyer-email.js?v=1" defer></script>"""


def build_locale(key: str) -> None:
    cfg = LOCALES[key]
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

    page = f"""<!DOCTYPE html>
<html lang="{cfg["lang"]}">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0"/>
<title>{esc(cfg["title"])}</title>
<meta name="description" content="{esc(cfg["description"])}"/>
<meta name="robots" content="noindex"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:opsz,wght@14..32,400..800&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-tokens.css?v=1" rel="stylesheet"/>
<link href="{ASSET}css/daab-membership-flyer.css?v=3" rel="stylesheet"/>
</head>
<body class="membership-flyer-page">
<div class="flyer-toolbar">
<p>{esc(cfg["toolbar_hint"])}</p>
<div class="flyer-toolbar-actions">
<button type="button" class="flyer-btn flyer-btn-primary" onclick="window.print()">{esc(cfg["print_btn"])}</button>
<button type="button" class="flyer-btn" id="flyerSendEmailBtn">{esc(cfg["email_btn"])}</button>
<a class="flyer-btn" href="{esc(cfg["web_href"])}">{esc(cfg["web_btn"])}</a>
</div>
</div>
<div class="flyer-wrap">
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
<img src="{qr_url}" width="72" height="72" alt="" decoding="async" crossorigin="anonymous"/>
<span>{esc(cfg["qr_caption"])}</span>
</div>
</footer>
<p class="flyer-tagline">{esc(cfg["tagline"])}</p>
</article>
</div>
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

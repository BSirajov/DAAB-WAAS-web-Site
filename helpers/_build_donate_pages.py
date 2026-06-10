#!/usr/bin/env python3
"""Build az|en donate.html — Phase 1 individual donation (bank transfer)."""
from __future__ import annotations

import html
import re

from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

ASSET = "../"
DONATE_CSS_V = STYLE_VERSIONS.get("daab-donate-page.css", 1)
NAV_ARIA = {"az": "Əsas naviqasiya", "en": "Main navigation"}
SKIP = {"az": "Məzmuna keç", "en": "Skip to content"}

LOCALES = {
    "az": {
        "lang": "az",
        "title": "DAAB — İanə",
        "description": "DAAB-a fərdi ianə — bank köçürməsi ilə Azərbaycan elminə dəstək.",
        "hero_h1": "İanə",
        "hero_subtitle": "Hər bir töhfə təqaüdlər, forumlar və elmi əməkdaşlıqlara dəstək verir",
        "panel_title": "Fərdi ianəçilər üçün",
        "panel_copy": (
            "Məbləğindən asılı olmayaraq hər bir ianə — təqaüd, mentorluq və bilik mübadiləsi "
            "proqramlarına birbaşa təsir göstərir. Korporativ tərəfdaşlıq üçün "
            "<a href=\"sponsors.html\">sponsorluq səhifəsinə</a> baxın."
        ),
        "impact_title": "İanəniz nəyə dəstək verir?",
        "impact_lead": "DAAB hər bir töhfəni Azərbaycanın elmi tərəqqisinə və uzunmüddətli inkişaf potensialına çevirir.",
        "impacts": [
            ("🎓", "Təqaüdlər", "Gənc tədqiqatçıların aparıcı müəssisələrdə iştirakı."),
            ("🔬", "Əməkdaşlıq", "Alimlərimizlə universitetlər və AMEA arasında körpü."),
            ("🌐", "Forumlar", "Xaricdə yaşayan alimlərin Forumları."),
        ],
        "amounts_title": "Tövsiyə olunan məbləğlər",
        "amounts_lead": "İstənilən məbləğ qəbul edilir. İllik fərdi dəstəyinizi aşağıdakı nümunələrə uyğun seçə bilərsiniz.",
        "amounts": ["€25", "€50", "€100", "€250", "İstəyə görə"],
        "bank_title": "Bank köçürməsi",
        "bank_lead": "Ödənişi aşağıdakı hesaba edin və ödəniş təyinatında göstərilən istinadı qeyd edin.",
        "bank_name": "Bankın adı",
        "bank_value": "VAKIFBANK",
        "beneficiary": "Benefisiar",
        "beneficiary_value": "Dunya Azerbaycanli Alimler Dernegi",
        "swift": "SWIFT",
        "swift_value": "TVBATR2A",
        "iban": "IBAN",
        "ibans": [
            ("TR07 0001 5001 5804 8024 7796 47", "AVRO ilə ödəniş üçün"),
            ("TR66 0001 5001 5804 8024 7796 52", "USD ilə ödəniş üçün"),
            ("TR83 0001 5001 5800 7346 6459 46", "TL ilə ödəniş üçün"),
        ],
        "ref_title": "Ödəniş təyinatı (vacibdir)",
        "ref_text": (
            "Köçürmə zamanı təyinat sahəsində bunu yazın: "
            "<span class=\"dn-code\">DAAB-IANE-[Ad Soyad]</span>. "
            "Bu, ianənizin düzgün qeydə alınmasına kömək edir."
        ),
        "charter_btn": "Birliyin gəlir mənbələri",
        "charter_title": (
            "Gəlir mənbələri ilə tanış olmaq üçün nizamnaməmizin 12-ci maddəsini oxuyun"
        ),
        "cta_title": "Sualınız var?",
        "cta_lead": "İanə, fond və ya xatirə ianəsi barədə komandamızla əlaqə saxlayın.",
        "cta_email": "E-poçt göndərin",
        "cta_email_title": "DAAB komandasına ianə barədə e-poçt yazın",
        "cta_form": "Sponsorluq forması",
        "cta_form_title": "Korporativ sponsorluq üçün əlaqə formasına keçin",
        "cta_sponsors": "Korporativ sponsorluq",
        "cta_sponsors_title": "Sponsorluq və tərəfdaşlıq səviyyələrinə baxın",
    },
    "en": {
        "lang": "en",
        "title": "WAAS — Donation",
        "description": "Support WAAS with an individual donation via bank transfer.",
        "hero_h1": "Donation",
        "hero_subtitle": "Every gift helps fund scholarships, forums, and research collaboration",
        "panel_title": "For individual donors",
        "panel_copy": (
            "Every contribution — of any size — directly supports scholarships, mentoring, "
            "and knowledge exchange. For corporate partnership, see our "
            "<a href=\"sponsors.html\">sponsorship page</a>."
        ),
        "impact_title": "What your gift supports",
        "impact_lead": "WAAS turns every contribution into scientific progress and long-term capacity for Azerbaijan.",
        "impacts": [
            ("🎓", "Scholarships", "Early-career researchers at leading institutions worldwide."),
            ("🔬", "Collaboration", "Bridging diaspora experts with universities and ANAS."),
            ("🌐", "Forums", "Forums of Azerbaijani scientists abroad."),
        ],
        "amounts_title": "Suggested amounts",
        "amounts_lead": "Any amount is welcome. You can choose your annual individual support to match the examples below.",
        "amounts": ["€25", "€50", "€100", "€250", "Your choice"],
        "bank_title": "Bank transfer",
        "bank_lead": "Please transfer to the account below and include the payment reference shown.",
        "bank_name": "Bank",
        "bank_value": "VAKIFBANK",
        "beneficiary": "Beneficiary",
        "beneficiary_value": "Dunya Azerbaycanli Alimler Dernegi",
        "swift": "SWIFT",
        "swift_value": "TVBATR2A",
        "iban": "IBAN",
        "ibans": [
            ("TR07 0001 5001 5804 8024 7796 47", "For payments in EUR"),
            ("TR66 0001 5001 5804 8024 7796 52", "For payments in USD"),
            ("TR83 0001 5001 5800 7346 6459 46", "For payments in TRY"),
        ],
        "ref_title": "Payment reference (required)",
        "ref_text": (
            "In the transfer description field, please write: "
            "<span class=\"dn-code\">DAAB-DONATION-[Your Name]</span>. "
            "This helps us record your gift correctly."
        ),
        "charter_btn": "Sources of Income of the Association",
        "charter_title": (
            "Read Article 12 of our charter to learn about the Association's sources of income"
        ),
        "cta_title": "Questions?",
        "cta_lead": "Contact our team about one-time, recurring, memorial, or foundation gifts.",
        "cta_email": "Send email",
        "cta_email_title": "Email the WAAS team about your donation",
        "cta_form": "Sponsorship form",
        "cta_form_title": "Open the corporate sponsorship contact form",
        "cta_sponsors": "Corporate sponsorship",
        "cta_sponsors_title": "View sponsorship tiers and partnership options",
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
    donate_v = st.get("daab-donate-page.css", DONATE_CSS_V)
    return f"""<!DOCTYPE html>
<html lang="{cfg["lang"]}" data-daab-lang="{cfg["lang"]}" data-daab-asset-root="{ASSET}" data-daab-page-id="donate" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(cfg["title"])}</title>
<meta name="description" content="{esc(cfg["description"])}"/>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&amp;family=Playfair+Display:wght@700;800&amp;display=swap" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sticky-chrome.css?v={st.get("daab-sticky-chrome.css", 1)}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v=2" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-donate-page.css?v={donate_v}" rel="stylesheet"/>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-sticky-chrome.js?v={sv.get("daab-sticky-chrome.js", 1)}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v={sv["daab-breadcrumbs.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v=2" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
</head>
"""


def footer_block(lang: str) -> str:
    if lang == "az":
        return """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Əlaqə</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Ünvan</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><div class="footer-title">Rəhbərlik</div><p class="footer-leader"><strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Almaniya — James D. Murray mükafatlı professoru</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 DAAB — Bütün hüquqlar qorunur</div>
</footer>"""
    return """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>World Association of Azerbaijani Scientists</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Contact</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Address</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p></div>
<div class="footer-col"><div class="footer-title">Leadership</div><p class="footer-leader"><strong>Prof. Dr. Masud Afandiyev</strong><br/>Chair of the WAAS Executive Board<br/>Germany — James D. Murray Prize laureate</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 WAAS — All rights reserved</div>
</footer>"""


def build_locale(key: str) -> None:
    cfg = LOCALES[key]
    src = (ROOT / key / "membership_value.html").read_text(encoding="utf-8")
    nav = extract_nav(src, NAV_ARIA[key])
    if not nav:
        raise SystemExit(f"Could not extract nav from membership_value ({key})")

    impacts_html = "".join(
        f'<article class="dn-impact-card"><div class="dn-icon" aria-hidden="true">{icon}</div>'
        f"<h3>{esc(title)}</h3><p>{esc(desc)}</p></article>"
        for icon, title, desc in cfg["impacts"]
    )
    amounts_html = "".join(
        f'<span class="dn-amount{" dn-amount--custom" if i == len(cfg["amounts"]) - 1 else ""}">'
        f"{esc(label)}</span>"
        for i, label in enumerate(cfg["amounts"])
    )
    ibans_html = "".join(
        f'<li><span class="dn-code">{esc(iban)}</span> — {esc(note)}</li>'
        for iban, note in cfg["ibans"]
    )

    page = shell_head(cfg) + f"""<body class="donate-page">
<a class="skip" href="#content">{SKIP[key]}</a>
{nav}
<header class="hero">
<div class="hero-wrap shell">
<section>
<h1 aria-describedby="page-hero-subtitle">{cfg["hero_h1"]}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(cfg["hero_subtitle"])}</p>
</section>
<aside aria-label="{esc(cfg["panel_title"])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(cfg["panel_title"])}</h2>
<div class="panel-copy"><p>{cfg["panel_copy"]}</p></div>
</div>
</aside>
</div>
</header>
<main class="donate-main" id="content">
<section class="dn-section" id="impact">
<div class="dn-section-head"><h2>{esc(cfg["impact_title"])}</h2><p>{esc(cfg["impact_lead"])}</p></div>
<div class="dn-impact-grid">{impacts_html}</div>
</section>
<section class="dn-section" id="amounts">
<div class="dn-section-head"><h2>{esc(cfg["amounts_title"])}</h2><p>{esc(cfg["amounts_lead"])}</p></div>
<div class="dn-amounts">{amounts_html}</div>
</section>
<section class="dn-section" id="bank">
<div class="dn-section-head"><h2>{esc(cfg["bank_title"])}</h2><p>{esc(cfg["bank_lead"])}</p></div>
<div class="dn-bank-card">
<table class="dn-bank-table">
<tr><th>{esc(cfg["bank_name"])}</th><td>{esc(cfg["bank_value"])}</td></tr>
<tr><th>{esc(cfg["beneficiary"])}</th><td>{esc(cfg["beneficiary_value"])}</td></tr>
<tr><th>{esc(cfg["swift"])}</th><td><span class="dn-code">{esc(cfg["swift_value"])}</span></td></tr>
<tr><th>{esc(cfg["iban"])}</th><td><ul class="dn-bank-list">{ibans_html}</ul></td></tr>
</table>
<div class="dn-ref-box"><strong>{esc(cfg["ref_title"])}</strong><p>{cfg["ref_text"]}</p></div>
<a class="dn-charter-btn" href="charter.html#section-12" title="{esc(cfg["charter_title"])}">{esc(cfg["charter_btn"])}</a>
</div>
</section>
<section class="dn-section dn-cta" id="contact">
<h2>{esc(cfg["cta_title"])}</h2>
<p>{esc(cfg["cta_lead"])}</p>
<div class="dn-cta-actions">
<a class="btn btn-primary" href="mailto:info@daab-waas.com?subject={esc("DAAB ianə" if key == "az" else "WAAS donation")}" title="{esc(cfg["cta_email_title"])}">{esc(cfg["cta_email"])}</a>
<a class="btn btn-secondary" href="sponsors.html#contact" title="{esc(cfg["cta_form_title"])}">{esc(cfg["cta_form"])}</a>
<a class="btn btn-secondary" href="sponsors.html" title="{esc(cfg["cta_sponsors_title"])}">{esc(cfg["cta_sponsors"])}</a>
</div>
</section>
</main>
{footer_block(key)}
</body>
</html>
"""
    out = ROOT / key / "donate.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(ROOT)}")


def main() -> None:
    for key in LOCALES:
        build_locale(key)


if __name__ == "__main__":
    main()

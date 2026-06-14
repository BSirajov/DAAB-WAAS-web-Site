"""Shared English shell strings for Forum 2024 pages."""
from __future__ import annotations

FORUM_FOOTER_EN = """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>World Association of Azerbaijani Scientists</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">Contact</h4><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">Address</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Pasa Sokak No:44<br/>Kadikoy, Istanbul, Turkiye</p></div>
<div class="footer-col"><h4 class="footer-title">Leadership</h4><p class="footer-leader"><strong>Prof. Dr. Mesud Afandiyev</strong><br/>Chair of the WAAS Executive Board<br/>Germany — James D. Murray Distinguished Professor</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 WAAS — All Rights Reserved</div>
</footer>"""

SHELL_REPLACEMENTS: list[tuple[str, str]] = [
    ('lang="az"', 'lang="en"'),
    ('data-daab-lang="az"', 'data-daab-lang="en"'),
    ("Məzmuna keç", "Skip to content"),
    ('aria-label="Əsas naviqasiya"', 'aria-label="Main navigation"'),
    ('aria-label="Menyunu aç"', 'aria-label="Open menu"'),
    ('aria-label="DAAB ana səhifə"', 'aria-label="WAAS home"'),
    ("alt=\"DAAB Logo\"", "alt=\"WAAS Logo\""),
    (
        "Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi",
        "World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists",
    ),
    ("Ana səhifə", "Home"),
    ("Fəaliyyətimiz", "Activities"),
    ("Yeniliklər", "News"),
    ("Əsas fəaliyyət və yeniliklər", "News and updates"),
    ("Forum 2024 kitabı və bölmələr", "Forum 2024 book and sections"),
    ("Alimlərimiz", "Scientists"),
    ("Siyahı", "Directory"),
    ("Bütün alimlərin siyahısı", "Directory of all scientists"),
    ("Profillər", "Profiles"),
    ("Alimlərin akademik profilləri", "Academic profiles of scientists"),
    ("Haqqımızda", "About us"),
    ("Birliyin təsisi", "Foundation"),
    ("Yaradılama tarixi və təsis prosesi", "History and founding process"),
    ("Yaradılma tarixi və təsis prosesi", "History and founding process"),
    ("Missiya və dəyərlər", "Mission &amp; values"),
    ("Missiya, vizyon və akademik dəyərlər", "Mission, vision and academic values"),
    ("İdarə heyəti", "Executive Board"),
    ("İdarə heyəti və rəhbərlik", "Leadership and governance structure"),
    ("Board of Directors və rəhbərlik", "Leadership and governance structure"),
    ("Charter və idarəetmə qaydaları", "Charter and governance rules"),
    ("Nizamnamə", "Charter"),
    ("Nizamnamə və idarəetmə qaydaları", "Charter and governance rules"),
    ("Üzvlük", "Membership"),
    ('aria-label="Səhifə yolu"', 'aria-label="Breadcrumb"'),
    ("— DAAB", "— WAAS"),
    ("Dünya Azərbaycanlı Alimlər Birliyi", "World Association of Azerbaijani Scientists"),
    ("DAAB İdarə Heyətinin Sədri", "Chair of the WAAS Executive Board"),
    ("Prof. Dr. Məsud Əfəndiyev", "Prof. Dr. Mesud Afandiyev"),
    ("Gazi Muhtar Paşa Sokak No:44", "Gazi Muhtar Pasa Sokak No:44"),
    ("Kadıköy, İstanbul, Türkiyə", "Kadikoy, Istanbul, Türkiye"),
    ("Əlaqə", "Contact"),
    ("Ünvan", "Address"),
    ("Rəhbərlik", "Leadership"),
]


def apply_shell(text: str) -> str:
    for old, new in SHELL_REPLACEMENTS:
        if isinstance(new, str) and old in text:
            text = text.replace(old, new)
    return text

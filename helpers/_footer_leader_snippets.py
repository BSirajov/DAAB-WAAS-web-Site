"""Canonical footer leadership lines for AZ/EN page shells."""

try:
    from _paths import FOOTER_COPYRIGHT_AZ, FOOTER_COPYRIGHT_EN
except ImportError:
    from helpers._paths import FOOTER_COPYRIGHT_AZ, FOOTER_COPYRIGHT_EN  # type: ignore

FOOTER_AZ_CREDENTIAL = "Almaniya — James D. Murray mükafatlı professoru"
FOOTER_EN_CREDENTIAL = "Germany — James D. Murray Distinguished Professor"

FOOTER_AZ_LEADER_HTML = (
    "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>"
    "DAAB İdarə Heyətinin Sədri<br/>"
    f"{FOOTER_AZ_CREDENTIAL}"
)

FOOTER_EN_LEADER_HTML = (
    "<strong>Prof. Dr. Messoud Efendiyev</strong><br/>"
    "Chair of the WAAS Executive Board<br/>"
    f"{FOOTER_EN_CREDENTIAL}"
)

FOOTER_AZ_LEGAL_LINKS = (
    '<nav class="footer-legal-links" aria-label="Hüquqi sənədlər və saytın xəritəsi">'
    '<a href="/az/privacy.html#page-title">Məxfilik bildirişi</a>'
    '<a href="/az/terms.html#page-title">İstifadə şərtləri</a>'
    '<a href="/az/cookies.html#page-title">Kuki siyasəti</a>'
    '<a href="/az/legal-notice.html#page-title">Hüquqi rekvizitlər</a>'
    '<a href="/az/sitemap.html#page-title">Saytın xəritəsi</a>'
    "</nav>"
)

FOOTER_EN_LEGAL_LINKS = (
    '<nav class="footer-legal-links" aria-label="Legal documents and sitemap">'
    '<a href="/en/privacy.html#page-title">Privacy notice</a>'
    '<a href="/en/terms.html#page-title">Terms of use</a>'
    '<a href="/en/cookies.html#page-title">Cookie policy</a>'
    '<a href="/en/legal-notice.html#page-title">Legal notice (Imprint)</a>'
    '<a href="/en/sitemap.html#page-title">Sitemap</a>'
    "</nav>"
)

FOOTER_AZ_BOTTOM = (
    f'<div class="footer-bottom">{FOOTER_AZ_LEGAL_LINKS}'
    f'<div class="footer-copy">{FOOTER_COPYRIGHT_AZ}</div></div>'
)

FOOTER_EN_BOTTOM = (
    f'<div class="footer-bottom">{FOOTER_EN_LEGAL_LINKS}'
    f'<div class="footer-copy">{FOOTER_COPYRIGHT_EN}</div></div>'
)

FOOTER_AZ_HTML = f"""<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">Əlaqə</h4><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">Ünvan</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">Rəhbərlik</h4><p class="footer-leader">{FOOTER_AZ_LEADER_HTML}</p></div>
</div>
</div>
{FOOTER_AZ_BOTTOM}
</footer>"""

FOOTER_EN_HTML = f"""<footer class="footer-pro">
  <div class="footer-inner">
    <div class="footer-brand">
      <h3>World Association of Azerbaijani Scientists</h3>
    </div>
    <div class="footer-grid">
      <div class="footer-col">
        <h4 class="footer-title">Contact</h4>
        <div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div>
        <div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div>
        <div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div>
      </div>
      <div class="footer-col">
        <h4 class="footer-title">Address</h4>
        <p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p>
      </div>
      <div class="footer-col">
        <h4 class="footer-title">Leadership</h4>
        <p class="footer-leader">{FOOTER_EN_LEADER_HTML}</p>
      </div>
    </div>
  </div>
  {FOOTER_EN_BOTTOM}
</footer>"""

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

FOOTER_AZ_HTML = f"""<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>Dünya Azərbaycanlı Alimlər Birliyi</h3></div>
<div class="footer-grid">
<div class="footer-col"><h4 class="footer-title">Əlaqə</h4><div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div><div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">daab-waas.com</a></div></div>
<div class="footer-col"><h4 class="footer-title">Ünvan</h4><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə</p></div>
<div class="footer-col"><h4 class="footer-title">Rəhbərlik</h4><p class="footer-leader">{FOOTER_AZ_LEADER_HTML}</p></div>
</div>
</div>
<div class="footer-bottom">{FOOTER_COPYRIGHT_AZ}</div>
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
  <div class="footer-bottom">{FOOTER_COPYRIGHT_EN}</div>
</footer>"""

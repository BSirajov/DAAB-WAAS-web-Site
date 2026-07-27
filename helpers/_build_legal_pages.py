#!/usr/bin/env python3
"""Build AZ/EN legal pages: künye, privacy (KVKK), cookies, terms of use."""
from __future__ import annotations

import html
import re

from _footer_leader_snippets import FOOTER_AZ_HTML, FOOTER_EN_HTML
from _inject_seo_head import build_seo_block
from _paths import ROOT
from _site_wide_cleanup import SCRIPT_VERSIONS, STYLE_VERSIONS

ASSET = "../"
NAV_ARIA = {"az": "Əsas naviqasiya", "en": "Main navigation"}
SKIP = {"az": "Məzmuna keç", "en": "Skip to content"}
UPDATED = "2026-07-27"

PAGES = (
    "legal-notice",
    "privacy",
    "cookies",
    "terms",
)

TOC_LABEL = {"az": "Bölmələr", "en": "Sections"}
TOC_TOGGLE = {"az": "Bölmələr menyusunu aç", "en": "Open sections menu"}
PLAIN_LABEL = {"az": "Sadə dillə", "en": "In plain language"}
TAKEAWAYS_TOC = {
    "az": ("★", "Əsas məqamlar"),
    "en": ("★", "Key takeaways"),
}

H2_RE = re.compile(r"<h2(\s[^>]*)?>(.*?)</h2>", re.IGNORECASE | re.DOTALL)
TAG_RE = re.compile(r"<[^>]+>")


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def extract_nav(html_text: str, nav_aria: str) -> str:
    m = re.search(
        rf'(<nav aria-label="{re.escape(nav_aria)}" class="nav-strip">.*?</nav>)',
        html_text,
        re.DOTALL,
    )
    return m.group(1) if m else ""


def _plain_text(fragment: str) -> str:
    return re.sub(r"\s+", " ", TAG_RE.sub("", fragment)).strip()


def prepare_body_and_toc(body: str, lang: str) -> tuple[str, list[tuple[str, str, str]]]:
    """Assign stable section ids and build News-style sidebar TOC entries."""
    toc: list[tuple[str, str, str]] = []
    out = body

    # Takeaways box → first TOC item (matches visible content topic)
    takeaways_re = re.compile(
        r'(<section\s+class="legal-takeaways")([^>]*)(>)(.*?)(</section>)',
        re.IGNORECASE | re.DOTALL,
    )

    def takeaways_repl(m: re.Match[str]) -> str:
        attrs = m.group(2)
        inner = m.group(4)
        attrs = re.sub(r'\s*id="[^"]*"', "", attrs)
        attrs = re.sub(r'\s*aria-labelledby="[^"]*"', "", attrs)
        attrs = f'{attrs} id="section-takeaways" aria-labelledby="legal-takeaways-title"'
        # Prefer a non-h2 title so it is not double-counted as a section heading
        inner2 = re.sub(
            r"<h2(?:\s[^>]*)?>(.*?)</h2>",
            lambda mm: (
                f'<p class="legal-takeaways__title" id="legal-takeaways-title">'
                f"{mm.group(1)}</p>"
            ),
            inner,
            count=1,
            flags=re.IGNORECASE | re.DOTALL,
        )
        date_lbl, title = TAKEAWAYS_TOC[lang]
        toc.append((date_lbl, "section-takeaways", title))
        return f"{m.group(1)}{attrs}{m.group(3)}{inner2}{m.group(5)}"

    out, n_take = takeaways_re.subn(takeaways_repl, out, count=1)
    if n_take == 0:
        pass

    used_ids = {"section-takeaways"} if toc else set()

    def h2_repl(m: re.Match[str]) -> str:
        attrs = m.group(1) or ""
        inner = m.group(2)
        text = _plain_text(inner)
        if not text:
            return m.group(0)
        # Skip titles that belong to takeaways (already handled)
        if text in {"Əsas məqamlar", "Key takeaways"}:
            return m.group(0)

        num_m = re.match(r"^(\d+)\.\s*(.+)$", text)
        if num_m:
            num = f"{int(num_m.group(1)):02d}"
            title = num_m.group(2).strip()
        else:
            num = f"{len([t for t in toc if t[0] != TAKEAWAYS_TOC[lang][0]]) + 1:02d}"
            title = text

        sid = f"section-{num}"
        n = 2
        while sid in used_ids:
            sid = f"section-{num}-{n}"
            n += 1
        used_ids.add(sid)
        toc.append((num, sid, title))

        # Replace/remove existing id in attrs
        attrs2 = re.sub(r'\s*id="[^"]*"', "", attrs)
        return f'<h2{attrs2} id="{sid}">{inner}</h2>'

    out = H2_RE.sub(h2_repl, out)
    return out, toc


def render_sidebar(lang: str, toc: list[tuple[str, str, str]]) -> str:
    items = []
    for date_lbl, sid, title in toc:
        items.append(
            f'<li><span class="tl-date">{esc(date_lbl)}</span>'
            f'<a href="#{esc(sid)}">{esc(title)}</a></li>'
        )
    menu = "\n".join(items)
    return f"""<aside class="sidebar" aria-label="{esc(TOC_LABEL[lang])}">
<div class="sidebar-widget">
<div class="widget-head"><span><span aria-hidden="true">📑</span> {esc(TOC_LABEL[lang])}</span><button aria-controls="legalTocMenu" aria-expanded="false" aria-label="{esc(TOC_TOGGLE[lang])}" class="events-menu-toggle" type="button"><span></span><span></span><span></span></button></div>
<div class="widget-body">
<ul class="timeline-list" id="legalTocMenu">
{menu}
</ul>
</div>
</div>
</aside>"""


CONTENT: dict[str, dict[str, dict[str, str]]] = {
    "legal-notice": {
        "az": {
            "title": "DAAB — Hüquqi rekvizitlər",
            "description": "Dünya Azərbaycanlı Alimlər Birliyinin (DAAB) hüquqi kimliyi, ünvanı və əlaqə məlumatları.",
            "hero_h1": "Hüquqi rekvizitlər",
            "hero_subtitle": "Saytın sahibi və birliyin hüquqi kimliyi haqqında",
            "panel_title": "Saytı kim idarə edir?",
            "panel_copy": (
                "Bu veb-saytı Türkiyədə qeydiyyatdan keçmiş birlik idarə edir "
                "(rəsmi türkcə adı: dernek). Rəsmi müraciət üçün aşağıdakı ünvandan və e-poçtdan istifadə edin."
            ),
            "meta": f"Son yenilənmə: {UPDATED}",
            "body": f"""
<p class="legal-meta">Son yenilənmə: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Əsas məqamlar</h2>
<ul>
<li><mark class="legal-mark">Bu saytı Türkiyədə qeydiyyatdan keçmiş birlik (dernek) idarə edir</mark> — rəsmi ad: Dünya Azerbaycanlı Alimler Derneği.</li>
<li>Rəsmi müraciət üçün poçt ünvanı, e-poçt və telefon bu səhifədədir.</li>
<li>Sayt məzmunu ümumi məlumat üçündür; <mark class="legal-mark">hüquqi məsləhət hesab edilmir</mark>.</li>
<li>Alimlərin foto və bioqrafiyası onların icazəsi ilə dərc olunur; müəllif hüququ onlarda qalır.</li>
</ul>
</section>
<div class="legal-callout">
<p>Bu səhifədə Türkiyə praktikasına uyğun olaraq veb-saytlar üçün tövsiyə olunan <strong>hüquqi rekvizitlər</strong> (kim idarə edir, harada yerləşir, necə əlaqə saxlamaq) yer alır. Qeydiyyat nömrəsi və digər rəsmi məlumatlar dəyişərsə, mətn yenilənəcək.</p>
</div>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>«Hüquqi rekvizitlər» və ya «künye» deməkdir: saytı kimə yazmaq, şikayət və ya rəsmi sorğu göndərmək istəyirsinizsə, buradakı ad və ünvanı istifadə edin. Bu, məxfilik və ya istifadə şərtlərinin əvəzi deyil — onlar ayrıca səhifələrdədir.</p>
</div>
<h2>1. Saytın sahibi</h2>
<p><strong>Rəsmi ad (TR):</strong> Dünya Azerbaycanlı Alimler Derneği</p>
<p><strong>Qısa ad / brend:</strong> DAAB — Dünya Azərbaycanlı Alimlər Birliyi<br/>
<strong>İngiliscə:</strong> WAAS — World Association of Azerbaijani Scientists</p>
<p><strong>Hüquqi forma:</strong> Türkiyə Respublikasının qanunvericiliyinə əsasən yaradılmış birlik (türkcə: dernek)</p>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>«Dernek» Türkiyədə qeyri-kommersiya birlik deməkdir. Şirkət (ticari şirket) deyil; elmi və ictimai fəaliyyət üçün yaradılmış təşkilat formasıdır.</p>
</div>
<p><strong>Mərkəz ünvanı:</strong><br/>
Feneryolu Mahallesi<br/>
Gazi Muhtar Paşa Sokak No:44<br/>
Kadıköy, İstanbul, Türkiyə</p>
<div class="legal-contact-card">
<p><strong>E-poçt:</strong> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a><br/>
<strong>Telefon:</strong> <a href="tel:+905551474674">+90 555 147 46 74</a><br/>
<strong>Veb:</strong> <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">https://daab-waas.com</a></p>
</div>

<h2>2. Rəhbərlik</h2>
<p>İdarə Heyətinin sədri: Prof. Dr. Məsud Əfəndiyev<br/>
Ümumi suallar üçün: <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></p>

<h2>3. Məzmun və məsuliyyət</h2>
<p>Saytdakı məlumatlar elmi, təşkilati və ictimai maarifləndirmə məqsədi ilə verilir. Dəqiqliyə çalışsaq da, xəta və ya yenilənmədə gecikmə ola bilər. <mark class="legal-mark">Bu məlumatlar hüquqi məsləhət və ya rəsmi dövlət bəyanatı hesab edilməməlidir.</mark></p>
<div class="legal-note">
<p>Fərdi hüquqi vəziyyətiniz üçün müstəqil hüquqşünas və ya səlahiyyətli orqanla məsləhətləşin. Sayt ümumi məlumat verir.</p>
</div>

<h2>4. Müəllif hüququ və istinad</h2>
<p>Əksinə qeyd olunmayıbsa, saytın dizaynı, tərtibatı, qrafikası və orijinal yazılı məzmunu © 2026 DAAB / WAAS-ə məxsusdur. Bütün hüquqlar qorunur. Bu, DAAB/WAAS adı və loqosunu da əhatə edir.</p>
<p><mark class="legal-mark">Hər töhfənin müəllif hüququ müəllifdə və ya hüquq sahibində qalır; dərc olunmaq mülkiyyəti DAAB / WAAS-ə keçirmir.</mark></p>
<p>Saytda azərbaycanlı alim və ziyalıların bioqrafiya, foto, kitab və digər əsərləri onların (və ya hüquq sahibinin) icazəsi ilə dərc olunur.</p>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Keçidi paylaşmaq adətən olar. Amma foto, bioqrafiya və ya kitabı öz saytınıza köçürmək, satmaq və ya «mənimdir» demək olmaz — əvvəlcə icazə alın. Hüquq sahibisinizsə və materialın səhvən dərc olunduğunu düşünürsünüzsə, e-poçtla yazın; əsaslı müraciətlərə tez baxırıq.</p>
</div>
<p>Nümunələr: alim profil səhifələri, idarə heyəti fotoları, forum materialları, kitab və media topluları. İkon, şrift və digər lisenziyalı materiallar öz lisenziyasına uyğun istifadə olunur.</p>
<p>Şəxsi, qeyri-kommersiya və akademik məqsədlə səhifə keçidlərini paylaşmaq olar. İcazəsiz məzmunu (o cümlədən üzv fotoları, bioqrafiya və ya tam mətnli kitabları) çoxaltmaq, kommersiya məqsədilə istifadə etmək və ya müəlliflik iddia etmək olmaz.</p>
<p>Hüquq sahibisinizsə və materialın icazəsiz dərc olunduğunu düşünürsünüzsə, və ya silinmə/düzəliş istəyirsinizsə, materialın təsviri və URL-i, hüquqlarınız və əlaqə məlumatlarınızla <a href="mailto:info@daab-waas.com">info@daab-waas.com</a> ünvanına yazın. Əsaslı müraciətlərə operativ baxılacaq.</p>

<h2>5. Əlaqəli sənədlər</h2>
<ul>
<li><a href="/az/privacy.html#page-title">Məxfilik bildirişi</a></li>
<li><a href="/az/terms.html#page-title">İstifadə şərtləri</a></li>
<li><a href="/az/cookies.html#page-title">Kuki siyasəti</a></li>
<li><a href="/az/charter.html">Nizamnamə</a></li>
</ul>
""",
        },
        "en": {
            "title": "WAAS — Legal notice (Imprint)",
            "description": "Legal identity, address and contact details of the World Association of Azerbaijani Scientists (WAAS).",
            "hero_h1": "Legal notice (Imprint)",
            "hero_subtitle": "Website operator and association identity",
            "panel_title": "Who operates this site?",
            "panel_copy": (
                "This website is operated by an association (dernek) established under the laws of Türkiye. "
                "Please use the address and email below for official contact."
            ),
            "meta": f"Last updated: {UPDATED}",
            "body": f"""
<p class="legal-meta">Last updated: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Key takeaways</h2>
<ul>
<li><mark class="legal-mark">This website is operated by a Turkish association (dernek)</mark> — official name: Dünya Azerbaycanlı Alimler Derneği.</li>
<li>Use the postal address, email and phone on this page for official contact.</li>
<li>Site content is for general information; <mark class="legal-mark">it is not legal advice</mark>.</li>
<li>Scientist photos and biographies are published with permission; copyright stays with the rights holder.</li>
</ul>
</section>
<div class="legal-callout">
<p>This page provides the <strong>legal notice / imprint</strong> information recommended for websites under Turkish practice (who runs the site, where they are based, how to contact them). Official registration details will be updated if they change.</p>
</div>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>An “imprint” (künye) tells you who is legally responsible for the website. If you need to send a formal request or complaint, use the name and address here. This page does not replace the privacy notice or terms of use — those are separate.</p>
</div>
<h2>1. Website operator</h2>
<p><strong>Official name (TR):</strong> Dünya Azerbaycanlı Alimler Derneği</p>
<p><strong>Short name / brand:</strong> WAAS — World Association of Azerbaijani Scientists<br/>
<strong>Azerbaijani:</strong> DAAB — Dünya Azərbaycanlı Alimlər Birliyi</p>
<p><strong>Legal form:</strong> Association (dernek) established under the laws of the Republic of Türkiye</p>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>A <em>dernek</em> is a non-profit association under Turkish law — not a commercial company. It is a common legal form for scientific and civic organisations.</p>
</div>
<p><strong>Registered / headquarters address:</strong><br/>
Feneryolu Mahallesi<br/>
Gazi Muhtar Paşa Sokak No:44<br/>
Kadıköy, Istanbul, Türkiye</p>
<div class="legal-contact-card">
<p><strong>Email:</strong> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a><br/>
<strong>Phone:</strong> <a href="tel:+905551474674">+90 555 147 46 74</a><br/>
<strong>Web:</strong> <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">https://daab-waas.com</a></p>
</div>

<h2>2. Leadership (for contact)</h2>
<p>Chair of the Executive Board: Prof. Dr. Messoud Efendiyev<br/>
General enquiries: <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></p>

<h2>3. Content and responsibility</h2>
<p>Information on this site is provided for scientific, organisational and public-information purposes. While we aim for accuracy, errors or delays in updates may occur. <mark class="legal-mark">Content is not legal advice or an official government statement.</mark></p>
<div class="legal-note">
<p>For your personal legal situation, consult an independent lawyer or the competent authority. This site provides general information only.</p>
</div>

<h2>4. Copyright and attribution</h2>
<p>Unless otherwise noted, the design, layout, graphics and original written content of this Site are © 2026 DAAB / WAAS. All Rights Reserved. This includes the DAAB/WAAS name and logo.</p>
<p><mark class="legal-mark">Copyright in each contributed work remains with its original author or rights holder; publication does not transfer ownership to DAAB / WAAS.</mark></p>
<p>This Site features biographies, photographs, books, articles and other works contributed by or about Azerbaijani scientists, scholars and public figures. Such content is published with the knowledge and permission of the Featured Individual or Contributor (or, for published books, with the author’s or rights holder’s consent).</p>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>Sharing a page link is usually fine. Copying photos, biographies or books onto your own site, selling them, or claiming authorship is not — ask for permission first. If you are a rights holder and believe something was published in error, email us; we review legitimate requests promptly.</p>
</div>
<p>Examples include scientist profile pages, board member photographs, forum materials, and book/media collections. Where the Site uses icons, fonts or other licensed assets not created by WAAS or its members, such material is used under its applicable licence.</p>
<p>You may view and share links to pages for personal, non-commercial and academic purposes. You may not reproduce or redistribute site content (including member photos, biographies or full-text books) without permission, use a Featured Individual’s name, photo or biography for commercial purposes, or claim authorship of any work published on this Site.</p>
<p>If you are a rights holder and believe your work has been published without proper authorisation, or you would like content removed or corrected, contact <a href="mailto:info@daab-waas.com">info@daab-waas.com</a> with a description of the material and its URL, a description of your rights, and your contact information. We will review legitimate requests promptly.</p>

<h2>5. Related documents</h2>
<ul>
<li><a href="/en/privacy.html#page-title">Privacy notice</a></li>
<li><a href="/en/terms.html#page-title">Terms of use</a></li>
<li><a href="/en/cookies.html#page-title">Cookie policy</a></li>
<li><a href="/en/charter.html">Charter</a></li>
</ul>
""",
        },
    },
    "privacy": {
        "az": {
            "title": "DAAB — Məxfilik bildirişi",
            "description": "DAAB veb-saytı və üzvlük forması üzrə KVKK məlumatlandırma mətni və məxfilik bildirişi.",
            "hero_h1": "Məxfilik bildirişi",
            "hero_subtitle": "Şəxsi məlumatlarınız necə istifadə olunur",
            "panel_title": "Məlumat nəzarətçisi",
            "panel_copy": (
                "Türkiyənin 6698 saylı «Şəxsi Məlumatların Qorunması Qanunu» "
                "(Kişisel Verilerin Korunması Kanunu — KVKK) üzrə məlumatlarınızın "
                "hansı məqsədlə, hansı hüquqi əsasla işləndiyi və hansı hüquqlarınız olduğu burada izah olunur."
            ),
            "meta": f"Son yenilənmə: {UPDATED}",
            "body": f"""
<p class="legal-meta">Son yenilənmə: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Əsas məqamlar</h2>
<ul>
<li><mark class="legal-mark">Şəxsi məlumatlarınızı satmırıq.</mark></li>
<li>Məlumat nəzarətçisi: Dünya Azerbaycanlı Alimler Derneği (DAAB / WAAS), İstanbul.</li>
<li>Analitika kukiləri <mark class="legal-mark">yalnız sizin razılığınızla</mark> işə düşür.</li>
<li>Hüquqlarınız üçün (düzəliş, silinmə, məlumat alma) <a href="mailto:info@daab-waas.com">info@daab-waas.com</a> ünvanına yazın.</li>
<li>Üzvlük formasını göndərməzdən əvvəl bu bildirişi oxuduğunuzu təsdiqləməlisiniz.</li>
</ul>
</section>
<div class="legal-callout">
<p>Bu mətn <strong>KVKK-nin 10-cu maddəsinə</strong> uyğun məlumatlandırma (izahedici bildiriş) məqsədi ilə hazırlanıb. Hüquqi məsləhət deyil; lazım gələrsə, vəkillə razılaşdırılmalıdır.</p>
</div>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p><strong>KVKK</strong> — Türkiyənin «Şəxsi Məlumatların Qorunması Qanunu»dur. «Məlumat nəzarətçisi» sizin məlumatlarınızın necə istifadə olunduğuna cavabdeh təşkilatdır. Bu səhifə: nə topladığımızı, niyə, kimə verə biləcəyimizi və sizin hansı hüquqlarınız olduğunu izah edir.</p>
</div>

<h2>1. Məlumat nəzarətçisi</h2>
<p><strong>Dünya Azerbaycanlı Alimler Derneği</strong> (DAAB / WAAS)<br/>
Ünvan: Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, İstanbul, Türkiyə<br/>
E-poçt: <a href="mailto:info@daab-waas.com">info@daab-waas.com</a><br/>
Telefon: <a href="tel:+905551474674">+90 555 147 46 74</a></p>

<h2>2. Hansı şəxsi məlumatları işləyirik?</h2>
<p>Fəaliyyətimizə görə, məsələn aşağıdakı məlumatlar işlənə bilər:</p>
<ul>
<li><strong>Şəxsiyyət:</strong> ad, soyad, akademik dərəcə və ya titul</li>
<li><strong>Əlaqə:</strong> e-poçt, telefon, ölkə və şəhər</li>
<li><strong>Peşəkar:</strong> universitet, iş yeri, elmi sahə, töhfə haqqında qeydlər</li>
<li><strong>Müraciət / CV:</strong> forma sahələri; ayrıca e-poçtla göndərilən CV və foto</li>
<li><strong>Alim / idarə heyəti profil məzmunu:</strong> bioqrafiya, foto, nəşrlər və icazə ilə dərc olunan digər materiallar</li>
<li><strong>Texniki:</strong> IP ünvanı, brauzer növü, səhifə ziyarətləri (analitika üçün razılıq verdikdə)</li>
<li><strong>Kukilər və lokal yaddaş:</strong> zəruri kukilər/yaddaş və (razılıq verdikdə) analitika — ətraflı: <a href="/az/cookies.html#page-title">Kuki siyasəti</a></li>
</ul>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Sadəcə saytı oxusanız, əsasən texniki və (razılıq verdikdə) statistika məlumatları toplanır. Üzvlük forması və ya e-poçt göndərsəniz, ad, əlaqə və peşəkar məlumatlarınız da işlənə bilər. Profil dərc olunursa, bunu əvvəlcədən razılaşdırırıq.</p>
</div>

<h2>3. Məlumatları nə üçün işləyirik?</h2>
<ul>
<li>veb-saytı işlək və təhlükəsiz saxlamaq</li>
<li>üzvlük müraciətlərini qəbul etmək, qiymətləndirmək və sizinlə əlaqə saxlamaq</li>
<li>ianə və ya sponsorluq sorğularına cavab vermək</li>
<li>elmi fəaliyyət, forumlar və təşkilati məlumatlandırma aparmaq</li>
<li>üzv/alim profillərini və töhfə əsərlərini icazə ilə dərc etmək</li>
<li>statistika toplamaq və saytı təkmilləşdirmək (yalnız analitika razılığı ilə)</li>
<li>hüquqi öhdəlikləri yerinə yetirmək və hüquqlarımızı qorumaq</li>
</ul>

<h2>4. Hüquqi əsaslar (KVKK m. 5)</h2>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>«Hüquqi əsas» — qanunun bizə məlumatı işləməyə icazə verdiyi səbəbdir. Məsələn: razılığınız; üzvlük müraciətini nəzərdən keçirmək; saytı təhlükəsiz saxlamaq. Aşağıdakı cədvəl ən çox rast gəlinən halları ümumiləşdirir.</p>
</div>
<p>Məlumatlar vəziyyətdən asılı olaraq aşağıdakı əsaslardan biri və ya bir neçəsi ilə işlənir:</p>
<ul>
<li>açıq razılığınız (məsələn, analitika kukiləri və razılıq tələb olunan digər hallar)</li>
<li>müqavilənin bağlanması və ya icrası üçün zəruri olması (üzvlük müraciəti prosesi)</li>
<li>məlumat nəzarətçisinin qanuni öhdəliyini yerinə yetirməsi</li>
<li>məlumat nəzarətçisinin qanuni maraqları (saytın təhlükəsizliyi, fəaliyyətin davamı), bu maraqlar sizin əsas hüquq və azadlıqlarınıza zərər verməmək şərtilə</li>
</ul>
<table class="legal-table">
<thead><tr><th>Məqsəd</th><th>Tipik hüquqi əsas</th></tr></thead>
<tbody>
<tr><td>Üzv/alim profili, foto və bioqrafiyanın dərcı</td><td>Dərc üçün verilmiş razılıq / icazə</td></tr>
<tr><td>Kitab, məqalə və ya foto toplularının dərcı</td><td>Müəllifin və ya hüquq sahibinin razılığı</td></tr>
<tr><td>Üzvlük müraciətinin işlənməsi</td><td>Müqavilə zərurəti / müraciətlərin qiymətləndirilməsinə qanuni maraq</td></tr>
<tr><td>Əlaqə, ianə və ya sponsorluq sorğularına cavab</td><td>Qanuni maraq (sizin başlatdığınız müraciətə cavab)</td></tr>
<tr><td>Saytın işlədilməsi və təhlükəsizliyi</td><td>Qanuni maraq (təhlükəsizlik və funksionallıq)</td></tr>
<tr><td>Google Analytics 4</td><td>Kuki pəncərəsi vasitəsilə açıq razılıq</td></tr>
</tbody>
</table>

<h2>5. Kimə ötürülə bilər?</h2>
<p><mark class="legal-mark">Şəxsi məlumatları satmırıq.</mark> Məlumatlarınız yalnız məqsədə uyğun həcmdə aşağıdakılara ötürülə bilər:</p>
<ul>
<li>DAAB-ın üzvlük və ya idarə heyəti komissiyasına və səlahiyyətli könüllü komanda üzvlərinə</li>
<li>hostinq, e-poçt və İT xidməti göstərənlərə (məlumatları işləyən tərəf kimi)</li>
<li>Google LLC-yə — Google Analytics 4 (yalnız analitika üçün razılıq verdikdə; məlumatlar xaricə də ötürülə bilər)</li>
<li>qanun tələb etdikdə səlahiyyətli dövlət orqanlarına</li>
<li>dərcinə razı olduğunuz məlumatlar üçün saytın ictimai ziyarətçilərinə (məsələn, profil, foto, töhfə əsərləri)</li>
</ul>
<p>Məlumatlar xaricə ötürülərsə, KVKK və əlaqəli qaydalara uyğun tədbirlər nəzərdə tutulur.</p>

<h2>6. Nə qədər müddətə saxlanılır?</h2>
<p>Məlumatlar yalnız məqsəd üçün lazım olan müddət ərzində və qanunda nəzərdə tutulan saxlama müddətlərinə uyğun saxlanılır. Üzvlük müraciətləri qiymətləndirmə və əlaqə üçün ağlabatan müddət saxlanılır. Profil və dərc olunmuş əsərlər dərc icazəsi qüvvədə olduqca və ya silinmə tələb olunana qədər saxlanılır; analitika məlumatları isə razılığa və alətin parametrlərinə uyğun silinir və ya anonimləşdirilir.</p>

<h2>7. Sizin hüquqlarınız (KVKK m. 11)</h2>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Qısaca: məlumatlarınız haqqında soruşa, səhv varsa düzəliş, müəyyən hallarda silinmə istəyə, razılığı geri götürə bilərsiniz. Müraciəti e-poçtla göndərin; kim olduğunuzu təsdiqləmək üçün kifayət qədər məlumat yazın (məsələn, ad və əlaqə e-poçtu).</p>
</div>
<p>Şəxsi məlumat sahibi kimi, digər hüquqlarla yanaşı, aşağıdakıları tələb edə bilərsiniz:</p>
<ul>
<li>məlumatlarınızın işlənib-işlənmədiyini öyrənmək</li>
<li>işlənirsə, bu barədə məlumat almaq</li>
<li>işlənmənin məqsədini və məqsədə uyğun olub-olmadığını öyrənmək</li>
<li>natamam və ya yanlış məlumatların düzəldilməsini istəmək</li>
<li>KVKK-da göstərilən hallarda silinmə və ya məhv etmə tələb etmək</li>
<li>məlumat ötürülmüş üçüncü şəxslərə düzəliş və ya silinmə barədə xəbər verilməsini istəmək</li>
<li>yalnız avtomatik sistemlərlə aparılan təhlilin nəticəsinə etiraz etmək</li>
<li>qanunsuz işlənmə nəticəsində dəymiş zərərin ödənilməsini tələb etmək</li>
<li><mark class="legal-mark">gələcək dərc və ya analitika üçün razılığı geri götürmək</mark> (əvvəlki qanuni işlənməyə təsir etmədən)</li>
</ul>
<p>Müraciət üçün <a href="mailto:info@daab-waas.com">info@daab-waas.com</a> ünvanına yazın və ya yuxarıdakı poçt ünvanına müraciət edin. Şəxsiyyətinizi təsdiqləmək üçün kifayət qədər məlumat göstərin. Cavab müddəti KVKK və tətbiq olunan qaydalara uyğun müəyyən edilir.</p>

<h2>8. Üzvlük forması</h2>
<p>Onlayn üzvlük müraciəti forması (<a href="/az/application.html">application.html</a>) ilə göndərdiyiniz məlumatlar yalnız üzvlük prosesi üçün istifadə olunur. <mark class="legal-mark">Formanı göndərməzdən əvvəl bu bildirişi oxuduğunuzu və onunla razı olduğunuzu təsdiqləməlisiniz.</mark> CV və foto ayrıca e-poçtla göndərilir.</p>

<h2>9. Uşaqlar</h2>
<p>Sayt və üzvlük xidmətləri əsasən yetkin akademik auditoriya üçündür. <mark class="legal-mark">18 yaşdan kiçik şəxslərdən qəsdən şəxsi məlumat toplamırıq.</mark></p>

<h2>10. Təhlükəsizlik</h2>
<p>Şəxsi məlumatları icazəsiz giriş, itki və ya sui-istifadəyə qarşı qorumaq üçün ağlabatan texniki və təşkilati tədbirlər görürük. Heç bir ötürmə və ya saxlama üsulu 100% təhlükəsiz deyil.</p>

<h2>11. Dəyişikliklər</h2>
<p>Bu bildiriş yenilənə bilər. Əhəmiyyətli dəyişikliklər saytda dərc olunacaq və “Son yenilənmə” tarixi dəyişdiriləcək.</p>

<h2>12. Əlaqə</h2>
<div class="legal-contact-card">
<p><strong>Dünya Azerbaycanlı Alimler Derneği</strong> — Dünya Azərbaycanlı Alimlər Birliyi (DAAB / WAAS)<br/>
Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, İstanbul, Türkiyə<br/>
<a href="mailto:info@daab-waas.com">info@daab-waas.com</a> · <a href="tel:+905551474674">+90 555 147 46 74</a> · <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">daab-waas.com</a></p>
</div>
""",
        },
        "en": {
            "title": "WAAS — Privacy notice",
            "description": "PDPL privacy notice for the WAAS website and membership application.",
            "hero_h1": "Privacy notice",
            "hero_subtitle": "How we process your personal data",
            "panel_title": "Data controller",
            "panel_copy": (
                "This notice explains purposes, legal bases and your rights under Türkiye’s "
                "Personal Data Protection Law No. 6698 (PDPL)."
            ),
            "meta": f"Last updated: {UPDATED}",
            "body": f"""
<p class="legal-meta">Last updated: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Key takeaways</h2>
<ul>
<li><mark class="legal-mark">We do not sell personal data.</mark></li>
<li>Data controller: Dünya Azerbaycanlı Alimler Derneği (DAAB / WAAS), Istanbul.</li>
<li>Analytics cookies run <mark class="legal-mark">only with your consent</mark>.</li>
<li>To exercise your rights (access, correction, erasure), email <a href="mailto:info@daab-waas.com">info@daab-waas.com</a>.</li>
<li>Before sending a membership application, you must confirm you have read this notice.</li>
</ul>
</section>
<div class="legal-callout">
<p>This text is prepared to serve as a <strong>PDPL Art. 10 information notice</strong> under Türkiye’s Personal Data Protection Law No. 6698. It is not legal advice and should be reviewed by counsel when needed.</p>
</div>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p><strong>PDPL</strong> (Personal Data Protection Law; Turkish: KVKK) is Türkiye’s data-protection statute. The “data controller” is the organisation responsible for how your data is used. This page explains what we collect, why, who may receive it, and what rights you have.</p>
</div>

<h2>1. Data controller</h2>
<p>The data controller is <strong>Dünya Azerbaycanlı Alimler Derneği</strong>, a Turkish association (dernek), operating publicly as <strong>World Association of Azerbaijani Scientists</strong> (DAAB / WAAS).</p>
<p>Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, Istanbul, Türkiye<br/>
Email: <a href="mailto:info@daab-waas.com">info@daab-waas.com</a><br/>
Phone: <a href="tel:+905551474674">+90 555 147 46 74</a><br/>
Web: <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">https://daab-waas.com</a><br/>
Leadership contact: Prof. Dr. Messoud Efendiyev, Chair of the WAAS Executive Board</p>

<h2>2. Personal data we process</h2>
<p>Depending on your interaction with the Site, we may process:</p>
<ul>
<li><strong>Identity:</strong> name, surname, academic degree or title</li>
<li><strong>Contact:</strong> email, phone, country and city</li>
<li><strong>Professional:</strong> university, workplace, scientific field, contribution notes</li>
<li><strong>Membership application / CV:</strong> online form fields; CV and photo sent separately by email</li>
<li><strong>Scientist / board profile content:</strong> biography, photograph, publications and related materials published with permission</li>
<li><strong>Technical:</strong> IP address, browser type, page visits (if analytics consent is given)</li>
<li><strong>Cookies and local storage:</strong> essential cookies/storage and, with consent, analytics — see the <a href="/en/cookies.html#page-title">Cookie policy</a></li>
</ul>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>If you only browse, we mainly process technical data and (if you agree) analytics. If you apply for membership or email us, we also process identity, contact and professional details. Profiles are published only after permission is arranged.</p>
</div>

<h2>3. Purposes of processing</h2>
<ul>
<li>Operate and secure the website</li>
<li>Receive, assess and respond to membership applications</li>
<li>Respond to donation and sponsorship enquiries</li>
<li>Scientific activity, forums and organisational communication</li>
<li>Publish member/scientist profiles and contributed works with permission</li>
<li>Statistics and site improvement (only with analytics consent)</li>
<li>Comply with legal obligations and protect legal rights</li>
</ul>

<h2>4. Legal bases (PDPL Art. 5)</h2>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>A “legal basis” is the lawful reason that allows us to process data — for example your consent, handling a membership application, or keeping the site secure. The table below summarises the most common cases.</p>
</div>
<p>Processing relies on one or more of the following, as applicable:</p>
<ul>
<li>Your explicit consent (e.g. analytics cookies; other cases where consent is required)</li>
<li>Necessity for establishing or performing a contract (membership application process)</li>
<li>Necessity for the controller’s legal obligation</li>
<li>Legitimate interests of the controller (site security and continuity of operations), provided this does not harm your fundamental rights and freedoms</li>
</ul>
<table class="legal-table">
<thead><tr><th>Purpose</th><th>Typical legal basis</th></tr></thead>
<tbody>
<tr><td>Publishing member/scientist profiles, photos and biographies</td><td>Consent / permission given for publication</td></tr>
<tr><td>Publishing submitted books, articles or photo collections</td><td>Consent / permission of the author or rights holder</td></tr>
<tr><td>Membership application processing</td><td>Contractual necessity / legitimate interest in assessing applications</td></tr>
<tr><td>Responding to contact, donation or sponsorship enquiries</td><td>Legitimate interest (responding to a request you initiated)</td></tr>
<tr><td>Operating and securing the Site</td><td>Legitimate interest (security and functionality)</td></tr>
<tr><td>Google Analytics 4</td><td>Explicit consent via the cookie banner</td></tr>
</tbody>
</table>

<h2>5. Recipients and transfers</h2>
<p><mark class="legal-mark">We do not sell personal data.</mark> Data may be shared, limited to purpose, with:</p>
<ul>
<li>WAAS membership / board commission and authorised volunteer team members</li>
<li>Hosting, email and IT service providers acting as processors</li>
<li>Google LLC — Google Analytics 4 (only if you consent; may involve transfers abroad)</li>
<li>Competent public authorities where required by law</li>
<li>Public visitors to the Site, for information you have agreed to publish (e.g. profile, photo, submitted works)</li>
</ul>
<p>Where data is transferred abroad, measures aligned with PDPL and related rules are intended.</p>

<h2>6. Retention</h2>
<p>Data is kept only as long as necessary for the purpose and applicable legal retention periods. Membership applications are retained for a reasonable assessment and follow-up period. Profile and published works remain while publication is authorised or until removal is requested. Analytics data is deleted or anonymised according to consent and tool settings.</p>

<h2>7. Your rights (PDPL Art. 11)</h2>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>In short: you can ask what we hold about you, request corrections, ask for erasure in the cases the law allows, and withdraw consent for future analytics or publication. Email us and include enough details to confirm your identity (for example your name and the email you used).</p>
</div>
<p>As a data subject you may, among other rights:</p>
<ul>
<li>learn whether your data is processed and request information</li>
<li>learn the purpose and whether use is consistent with that purpose</li>
<li>request correction of incomplete or inaccurate data</li>
<li>request erasure/destruction under the conditions in PDPL</li>
<li>request that corrections/erasures be notified to recipients</li>
<li>object to results of exclusively automated analysis</li>
<li>claim compensation for damage arising from unlawful processing</li>
<li><mark class="legal-mark">withdraw consent for future publication or analytics</mark> (without affecting prior lawful processing)</li>
</ul>
<p>Contact: <a href="mailto:info@daab-waas.com">info@daab-waas.com</a> or the postal address above. Please include enough information to verify your identity. Response times follow PDPL and applicable procedures.</p>

<h2>8. Membership form</h2>
<p>Data submitted via the online membership form (<a href="/en/application.html">application.html</a>) is used only for the membership process. <mark class="legal-mark">Before sending, applicants must confirm that they have read and agree to this notice.</mark> CV and photo are sent separately by email.</p>

<h2>9. Children</h2>
<p>The Site and membership services are generally intended for an adult academic audience. <mark class="legal-mark">We do not knowingly collect personal data from persons under 18.</mark></p>

<h2>10. Security</h2>
<p>We take reasonable technical and organisational measures to protect personal data against unauthorised access, loss or misuse. No method of transmission or storage is 100% secure.</p>

<h2>11. Changes</h2>
<p>This notice may be updated. Material changes will be published on the Site; the “Last updated” date will change.</p>

<h2>12. Contact</h2>
<div class="legal-contact-card">
<p><strong>Dünya Azerbaycanlı Alimler Derneği</strong> — World Association of Azerbaijani Scientists (DAAB / WAAS)<br/>
Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, Istanbul, Türkiye<br/>
<a href="mailto:info@daab-waas.com">info@daab-waas.com</a> · <a href="tel:+905551474674">+90 555 147 46 74</a> · <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">daab-waas.com</a></p>
</div>
""",
        },
    },
    "cookies": {
        "az": {
            "title": "DAAB — Kuki siyasəti",
            "description": "DAAB saytında istifadə olunan zəruri və analitika kukiləri haqqında məlumat.",
            "hero_h1": "Kuki siyasəti",
            "hero_subtitle": "Hansı kukilərdən istifadə edirik və onları necə idarə edə bilərsiniz",
            "panel_title": "Seçim sizin əlinizdədir",
            "panel_copy": (
                "Zəruri kukilər saytın işləməsi üçün lazımdır. Analitika kukiləri isə "
                "yalnız sizin razılığınızla işə düşür. İstədiyiniz vaxt seçimlərinizi dəyişə bilərsiniz."
            ),
            "meta": f"Son yenilənmə: {UPDATED}",
            "body": f"""
<p class="legal-meta">Son yenilənmə: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Əsas məqamlar</h2>
<ul>
<li>Zəruri kukilər saytın işləməsi üçün lazımdır — <mark class="legal-mark">həmişə aktivdir</mark>.</li>
<li>Google Analytics <mark class="legal-mark">yalnız razılığınızdan sonra</mark> yüklənir.</li>
<li>İstədiyiniz vaxt aşağıdakı düymə ilə seçimlərinizi dəyişə bilərsiniz.</li>
<li>«Yalnız zəruri» seçsəniz, analitika işləmir.</li>
</ul>
</section>
<div class="legal-callout">
<p>Bu siyasəti <a href="/az/privacy.html#page-title">Məxfilik bildirişi</a> ilə birlikdə oxuyun. Analitika üçün razılıq xüsusi pəncərə vasitəsilə alınır.</p>
</div>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Kuki — brauzerin cihazınızda saxladığı kiçik qeyddir (məsələn, dil seçiminiz). «Lokal yaddaş» da oxşardır, amma brauzerin öz yaddaş sahəsidir. Biz reklama yönəlmiş sosial kuki kateqoriyalarından istifadə etmirik.</p>
</div>

<h2>1. Kuki nədir?</h2>
<p>Kukilər brauzerin cihazınızda saxladığı kiçik mətn fayllarıdır. Saytın işləməsi, dil seçimi və (razılıq verdikdə) ziyarət statistikası üçün istifadə oluna bilər. Sayt bəzi seçimləri brauzerin lokal yaddaşında da saxlayır.</p>

<h2>2. Hansı kukilərdən və yaddaşdan istifadə edirik?</h2>
<table class="legal-table">
<thead><tr><th>Növ</th><th>Nə üçün lazımdır</th><th>Nümunə / açarlar</th><th>Razılıq lazımdır?</th></tr></thead>
<tbody>
<tr><td>Zəruri</td><td>Saytın əsas funksiyaları, təhlükəsizlik, dil və kuki seçiminin yadda saxlanması</td><td><code>daab-cookie-consent</code> (localStorage); <code>daab-lang</code> (dil seçimi)</td><td>Xeyr — həmişə aktiv</td></tr>
<tr><td>Analitika (istəyə bağlı)</td><td>Google Analytics 4 — səhifə ziyarətləri və ümumi statistika</td><td>GA4 kukiləri / teqləri (yalnız razılıqdan sonra)</td><td>Bəli — kuki pəncərəsi ilə</td></tr>
</tbody>
</table>
<p>Hazırda zəruri və istəyə bağlı analitika kateqoriyalarından kənar ayrıca “funksional” və ya sosial paylaşım kuki kateqoriyalarından istifadə olunmur. Sonradan kuki qoyan üçüncü tərəf məzmunu əlavə olunarsa, bu siyasət yenilənəcək.</p>

<h2>3. Google Analytics</h2>
<p>Razılıq verdikdə Google Analytics 4 işə salına bilər. Bu xidməti Google LLC təqdim edir və məlumatlar xaricə ötürülə bilər. <mark class="legal-mark">Razılıq verməsəniz (və ya “Yalnız zəruri” seçsəniz), analitika skripti yüklənmir.</mark></p>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Analitika saytın hansı səhifələrinin daha çox oxunduğunu ümumi şəkildə görməyə kömək edir. Sizi reklam üçün hədəfləmək məqsədi ilə istifadə etmirik. Razılıq verməsəniz, sayt normal işləyir — sadəcə statistika toplanmır.</p>
</div>

<h2>4. Lokal yaddaş</h2>
<p>Kuki seçiminiz brauzerin <code>localStorage</code> yaddaşında <code>daab-cookie-consent</code> açarı ilə saxlanılır. Beləliklə, razılıq pəncərəsi hər dəfə yenidən çıxmır. Dil seçimi <code>daab-lang</code> açarı ilə saxlana bilər.</p>

<h2>5. Seçimlərinizi necə idarə edə bilərsiniz?</h2>
<p>Razılıq pəncərəsində “Hamısını qəbul et”, “Yalnız zəruri”, “Seçimlər” və “Seçimləri saxla” düymələri ilə analitikanı aça və ya bağlaya bilərsiniz.</p>
<p><button type="button" class="legal-cookie-settings" id="daab-open-cookie-settings">Kuki seçimlərini aç</button></p>
<div class="legal-note">
<p>Kukiləri brauzerin öz parametrlərindən də silə və ya bloklaya bilərsiniz; bu zaman dil seçimi təsirlənə və razılıq pəncərəsi yenidən çıxa bilər.</p>
</div>

<h2>6. Əlaqəli sənədlər</h2>
<ul>
<li><a href="/az/privacy.html#page-title">Məxfilik bildirişi</a></li>
<li><a href="/az/terms.html#page-title">İstifadə şərtləri</a></li>
<li><a href="/az/legal-notice.html#page-title">Hüquqi rekvizitlər</a></li>
</ul>

<h2>7. Dəyişikliklər</h2>
<p>Saytdakı kuki istifadəsi dəyişdikcə bu siyasət yenilənə bilər. “Son yenilənmə” tarixi ən son düzəlişi göstərir.</p>

<h2>8. Əlaqə</h2>
<p><a href="mailto:info@daab-waas.com">info@daab-waas.com</a><br/>
Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, İstanbul, Türkiyə</p>
""",
        },
        "en": {
            "title": "WAAS — Cookie policy",
            "description": "Essential and analytics cookies used on the WAAS website.",
            "hero_h1": "Cookie policy",
            "hero_subtitle": "Which cookies we use and how you can control them",
            "panel_title": "Your choice",
            "panel_copy": (
                "Essential cookies are needed for the site to work. Analytics cookies run "
                "only with your consent. You can change your choices at any time."
            ),
            "meta": f"Last updated: {UPDATED}",
            "body": f"""
<p class="legal-meta">Last updated: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Key takeaways</h2>
<ul>
<li>Essential cookies are needed for the site to work — <mark class="legal-mark">always active</mark>.</li>
<li>Google Analytics loads <mark class="legal-mark">only after you consent</mark>.</li>
<li>You can change your choices any time with the button below.</li>
<li>If you choose “Essential only”, analytics does not run.</li>
</ul>
</section>
<div class="legal-callout">
<p>Please read this policy together with the <a href="/en/privacy.html#page-title">Privacy notice</a>. Consent for analytics is obtained via the cookie banner.</p>
</div>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>A cookie is a small note your browser stores on your device (for example, your language choice). “Local storage” is similar but uses a browser storage area. We do not use advertising-oriented social cookie categories.</p>
</div>

<h2>1. What are cookies?</h2>
<p>Cookies are small text files stored on your device by your browser. They may support site functions, language preference and (with consent) visit statistics. The Site also uses browser local storage for certain preferences.</p>

<h2>2. Cookies and storage we use</h2>
<table class="legal-table">
<thead><tr><th>Category</th><th>Purpose</th><th>Examples / keys</th><th>Consent required?</th></tr></thead>
<tbody>
<tr><td>Essential</td><td>Core site functions, security, remembering language and cookie choice</td><td><code>daab-cookie-consent</code> (localStorage); <code>daab-lang</code> (language preference)</td><td>No — always active</td></tr>
<tr><td>Analytics (optional)</td><td>Google Analytics 4 — page views and aggregate statistics</td><td>GA4 cookies / tags (only after consent)</td><td>Yes — via cookie banner</td></tr>
</tbody>
</table>
<p>The Site does not currently rely on separate “functional” or social-share cookie categories beyond essential and optional analytics. If additional third-party embeds that set cookies are introduced later, this policy and the banner categories will be updated.</p>

<h2>3. Google Analytics</h2>
<p>If you consent, Google Analytics 4 may be enabled. This is a service provided by Google LLC and may involve transfers of data abroad. <mark class="legal-mark">If you do not consent (or choose “Essential only”), the analytics script is not loaded.</mark></p>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>Analytics helps us see which pages are read most, in aggregate. We do not use it to target you with ads. If you decline, the site still works — we simply do not collect visit statistics.</p>
</div>

<h2>4. Local storage</h2>
<p>Your cookie consent choice is stored in the browser’s <code>localStorage</code> under the key <code>daab-cookie-consent</code> so the banner is not shown on every visit. Language preference may be stored under <code>daab-lang</code>.</p>

<h2>5. How we obtain and manage consent</h2>
<p>On your first visit, a cookie banner offers: Accept all, Essential only, Preferences, and Save choices. Essential cookies do not require consent. Analytics cookies run only with your consent.</p>
<p><button type="button" class="legal-cookie-settings" id="daab-open-cookie-settings">Open cookie settings</button></p>
<div class="legal-note">
<p>In addition to the Site’s consent tool, you can control or delete cookies through your browser settings. Blocking all cookies or clearing local storage may affect language preference and may cause the consent banner to reappear.</p>
</div>

<h2>6. Related documents</h2>
<ul>
<li><a href="/en/privacy.html#page-title">Privacy notice</a></li>
<li><a href="/en/terms.html#page-title">Terms of use</a></li>
<li><a href="/en/legal-notice.html#page-title">Legal notice (Imprint)</a></li>
</ul>

<h2>7. Changes</h2>
<p>We may update this Cookie Policy as the Site’s use of cookies changes. The “Last updated” date reflects the most recent revision.</p>

<h2>8. Contact</h2>
<p><a href="mailto:info@daab-waas.com">info@daab-waas.com</a><br/>
Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, Istanbul, Türkiye</p>
""",
        },
    },
    "terms": {
        "az": {
            "title": "DAAB — İstifadə şərtləri",
            "description": "DAAB veb-saytından istifadənin ümumi şərtləri.",
            "hero_h1": "İstifadə şərtləri",
            "hero_subtitle": "Bu saytdan istifadə edərkən nəyi bilməlisiniz",
            "panel_title": "Qısaca",
            "panel_copy": (
                "Saytdan qanuna uyğun və hörmətlə istifadə edin. Məzmun əqli mülkiyyətlə qorunur. "
                "Mübahisələrə Türkiyə hüququ tətbiq olunur."
            ),
            "meta": f"Son yenilənmə: {UPDATED}",
            "body": f"""
<p class="legal-meta">Son yenilənmə: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Əsas məqamlar</h2>
<ul>
<li><mark class="legal-mark">Saytdan istifadə etməklə bu şərtlərlə razılaşırsınız</mark> — razı deyilsinizsə, istifadə etməyin.</li>
<li>Məzmunu hörmətlə oxuyun; kataloqu və ya fotoları icazəsiz kommersiya məqsədilə köçürməyin.</li>
<li>Üzv materiallarının müəllif hüququ müəllifdə qalır; silinmə üçün e-poçt yazmaq olar.</li>
<li><mark class="legal-mark">Mübahisələrə Türkiyə hüququ və İstanbul məhkəmələri</mark> tətbiq olunur (məcburi hüquqlar qorunur).</li>
</ul>
</section>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Bu səhifə saytdan istifadənin «oyun qaydaları»dır: nə etmək olar, nə olmaz, məzmun kimə məxsusdur və mübahisə olarsa hansı ölkənin qanunu tətbiq olunur. Şəxsi məlumatlar üçün ayrıca <a href="/az/privacy.html#page-title">Məxfilik bildirişi</a> oxuyun.</p>
</div>

<h2>1. Tərəflər və razılaşma</h2>
<p><a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">https://daab-waas.com</a> saytından (“Sayt”) istifadə etməklə bu İstifadə şərtləri ilə razılaşırsınız. Razı deyilsinizsə, saytdan istifadə etməyin.</p>
<p>Saytı <strong>Dünya Azerbaycanlı Alimler Derneği</strong> (Dünya Azərbaycanlı Alimlər Birliyi, DAAB / WAAS) — Türkiyədə qeydiyyatdan keçmiş birlik (dernek) idarə edir; mərkəz: Kadıköy, İstanbul, Türkiyə.</p>

<h2>2. Sayt haqqında</h2>
<p>Sayt azərbaycanlı alim və tədqiqatçıları birləşdirmək, tanıtmaq və dəstəkləmək üçündür. Burada birlik haqqında məlumat, alimlər kataloqu və profilləri, forumlar və fəaliyyətlər, üzvlük, sponsorluq və ianə səhifələri (AZ və EN) yer alır.</p>

<h2>3. Əqli mülkiyyət</h2>
<p>DAAB / WAAS tərəfindən yaradılmış dizayn, mətn və digər orijinal məzmun (o cümlədən loqo) DAAB / WAAS-ə məxsusdur və müəllif hüququ ilə qorunur. İcazəsiz çoxaltmaq və ya yaymaq olmaz.</p>
<p><mark class="legal-mark">Üzvlərin təqdim etdiyi bioqrafiya, foto, kitab və digər əsərlər müəllifin və ya hüquq sahibinin mülkiyyətində qalır.</mark> Dərc yalnız töhfəçinin icazəsi ilə aparılır. Ətraflı: <a href="/az/legal-notice.html#page-title">Hüquqi rekvizitlər</a>.</p>

<h2>4. Məqbul istifadə qaydaları</h2>
<p>Saytdan istifadə edərkən razılaşırsınız ki:</p>
<ul>
<li>üzvlər kataloqunu və ya profil məlumatlarını icazəsiz kommersiya məqsədilə sistematik surətdə köçürməyəcəksiniz</li>
<li>saytdakı məzmundan kimisə təhqir, böhtan və ya yanlış təqdim etmək üçün istifadə etməyəcəksiniz</li>
<li>sayta və ya sistemlərinə icazəsiz daxil olmağa cəhd etməyəcəksiniz</li>
<li>qanunsuz, hüquq pozan və ya yanıltıcı məzmun göndərməyəcəksiniz</li>
<li>üzvlük, sponsorluq və ya əlaqə formalarından sui-istifadə etməyəcəksiniz</li>
</ul>

<h2>5. Üzv və töhfəçi materialları</h2>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["az"]}</p>
<p>Material göndərdikdə: (1) dərc hüququnuz olduğunu təsdiq edirsiniz; (2) bizə saytda göstərmək üçün qeyri-eksklüziv icazə verirsiniz; (3) mülkiyyət sizdə qalır; (4) istənilən vaxt silinmə istəyə bilərsiniz.</p>
</div>
<p>Bioqrafiya, foto, məqalə, kitab və ya digər əsər təqdim etdikdə:</p>
<ul>
<li>dərc üçün hüquqa malik olduğunuzu və ya lazımi icazəni aldığınızı təsdiq edirsiniz</li>
<li>WAAS-ə materialı saytda və əlaqəli materiallarda göstərmək, çoxaltmaq və (lazım gələrsə) AZ/EN dilinə çevirmək üçün qeyri-eksklüziv, royaltisiz lisenziya verirsiniz — silinmə tələb edənə qədər</li>
<li>istənilən vaxt <a href="mailto:info@daab-waas.com">info@daab-waas.com</a> ünvanına yazaraq silinmə və ya düzəliş tələb edə bilərsiniz</li>
</ul>

<h2>6. Məsuliyyətdən imtina</h2>
<p>Sayt “olduğu kimi” təqdim olunur. Dəqiqliyə çalışsaq da, məzmunun (xüsusən üzvlərin təqdim etdiyi məlumatların) tamlığına zəmanət verilmir. <mark class="legal-mark">Məzmun elmi, təşkilati və ictimai məlumat üçündür; hüquqi məsləhət və ya rəsmi dövlət bəyanatı deyil.</mark></p>
<p>Xarici keçidlər rahatlıq üçündür; üçüncü saytların məzmununa görə məsuliyyət daşımırıq.</p>

<h2>7. Məsuliyyətin məhdudlaşdırılması</h2>
<p>Qanunun yol verdiyi maksimum həddə WAAS saytdan istifadə və oradakı məlumata əsaslanma nəticəsində dolayı, təsadüfi və ya nəticə zərərlərinə görə məsuliyyət daşımır. Bu, məcburi qanun müddəalarını ləğv etmir.</p>
<div class="legal-note">
<p>Bəzi ölkələrdə qanun müəyyən məsuliyyəti tam istisna etməyə imkan vermir. Belə hallarda məcburi hüquqlar qüvvədə qalır.</p>
</div>

<h2>8. Məxfilik və kukilər</h2>
<p>Şəxsi məlumatların işlənməsi <a href="/az/privacy.html#page-title">Məxfilik bildirişi</a> və <a href="/az/cookies.html#page-title">Kuki siyasəti</a> ilə tənzimlənir.</p>

<h2>9. Tətbiq olunan hüquq</h2>
<p>Bu şərtlərə <strong>Türkiyə Respublikası</strong> qanunları tətbiq olunur. Mübahisələrə İstanbul məhkəmələri baxır (məcburi istehlakçı və digər hüquq müddəaları qorunur).</p>

<h2>10. Dəyişikliklər</h2>
<p>Şərtlər vaxtaşırı yenilənə bilər. Yenilənmiş mətn dərc olunduqdan sonra saytdan istifadə davam etdirilməsi qəbul sayılır.</p>

<h2>11. Əlaqə</h2>
<div class="legal-contact-card">
<p><strong>Dünya Azerbaycanlı Alimler Derneği</strong> — Dünya Azərbaycanlı Alimlər Birliyi (DAAB / WAAS)<br/>
Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, İstanbul, Türkiyə<br/>
<a href="mailto:info@daab-waas.com">info@daab-waas.com</a> · <a href="tel:+905551474674">+90 555 147 46 74</a></p>
</div>
""",
        },
        "en": {
            "title": "WAAS — Terms of use",
            "description": "General terms for using the WAAS website.",
            "hero_h1": "Terms of use",
            "hero_subtitle": "Rules for using this website",
            "panel_title": "In brief",
            "panel_copy": (
                "Use the site lawfully and respectfully. Content is protected by intellectual property law. "
                "The laws of Türkiye apply."
            ),
            "meta": f"Last updated: {UPDATED}",
            "body": f"""
<p class="legal-meta">Last updated: {UPDATED}</p>
<section class="legal-takeaways" aria-labelledby="legal-takeaways-title">
<h2 id="legal-takeaways-title">Key takeaways</h2>
<ul>
<li><mark class="legal-mark">By using the Site you agree to these Terms</mark> — if you do not agree, please do not use it.</li>
<li>Read content respectfully; do not scrape the directory or reuse photos for unauthorised commercial purposes.</li>
<li>Copyright in member materials stays with the author; you can request removal by email.</li>
<li><mark class="legal-mark">Turkish law and Istanbul courts</mark> apply (mandatory rights are preserved).</li>
</ul>
</section>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>These are the ground rules for using the website: what you may and may not do, who owns the content, and which country’s law applies if there is a dispute. For personal data, also read the <a href="/en/privacy.html#page-title">Privacy notice</a>.</p>
</div>

<h2>1. Parties and acceptance</h2>
<p>By accessing or using <a href="https://daab-waas.com" target="_blank" rel="noopener noreferrer">https://daab-waas.com</a> (the “Site”), you agree to these Terms of Use. If you do not agree, please do not use the Site.</p>
<p>The Site is operated by <strong>Dünya Azerbaycanlı Alimler Derneği</strong> (World Association of Azerbaijani Scientists, DAAB / WAAS), a Turkish association (dernek) based in Kadıköy, Istanbul, Türkiye.</p>

<h2>2. About the Site</h2>
<p>The Site connects, showcases and supports Azerbaijani scientists and scholars. It includes, among other things, association information, scientist directory and profiles, forums and activities, membership information, and sponsorship or donation pages, in Azerbaijani and English.</p>

<h2>3. Intellectual property</h2>
<p>Site design, text and original content created by DAAB / WAAS (layout, graphics, original articles, the DAAB/WAAS logo) are owned by DAAB / WAAS and protected by copyright. You may not copy, reproduce or redistribute this content without prior written permission.</p>
<p><mark class="legal-mark">Member-submitted content remains the intellectual property of the respective author or rights holder.</mark> WAAS publishes such content only with the contributor’s permission. See also the copyright notes on the <a href="/en/legal-notice.html#page-title">Legal notice (Imprint)</a> page.</p>
<p>Third-party trademarks or logos (e.g. partner institutions, universities) remain the property of their respective owners.</p>

<h2>4. Acceptable use</h2>
<p>When using the Site, you agree not to:</p>
<ul>
<li>Scrape, systematically copy or republish the member directory or profile data for unauthorised commercial use</li>
<li>Use any content from the Site to harass, defame or misrepresent any individual featured on it</li>
<li>Attempt to gain unauthorised access to any part of the Site or its underlying systems</li>
<li>Upload or submit content that is unlawful, infringing or misleading</li>
<li>Misuse membership, sponsorship or contact forms</li>
</ul>

<h2>5. Member and contributor submissions</h2>
<div class="legal-plain">
<p class="legal-plain__label">{PLAIN_LABEL["en"]}</p>
<p>If you submit material: (1) you confirm you have the right to publish it; (2) you give us a non-exclusive licence to display it on the Site; (3) ownership stays with you; (4) you can request removal at any time.</p>
</div>
<p>If you submit a biography, photograph, article, book or other work for publication:</p>
<ul>
<li>You confirm that you own the rights, or have obtained the necessary permission, for WAAS to publish the material</li>
<li>You grant WAAS a non-exclusive, royalty-free licence to display, reproduce and translate (into English/Azerbaijani as applicable) the material on the Site and in related WAAS materials until you request removal</li>
<li>You may request removal or correction at any time by contacting <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></li>
</ul>

<h2>6. Disclaimers</h2>
<p>The Site is provided “as is.” While we make reasonable efforts to keep information accurate and current, WAAS does not guarantee completeness or accuracy of all content, much of which is supplied by members. <mark class="legal-mark">Content is for scientific, organisational and public-information purposes and is not legal advice or an official government statement.</mark></p>
<p>Links to external sites are provided for convenience. WAAS is not responsible for the content or practices of external sites.</p>

<h2>7. Limitation of liability</h2>
<p>To the fullest extent permitted by applicable law, WAAS shall not be liable for any indirect, incidental or consequential damages arising from your use of the Site, including reliance on any information published on it. This does not override mandatory provisions of applicable law.</p>
<div class="legal-note">
<p>Some jurisdictions do not allow certain liability limitations. Where that is the case, mandatory rights remain in force.</p>
</div>

<h2>8. Privacy and cookies</h2>
<p>Processing of personal data is governed by the <a href="/en/privacy.html#page-title">Privacy notice</a> and <a href="/en/cookies.html#page-title">Cookie policy</a>.</p>

<h2>9. Governing law</h2>
<p>These Terms are governed by the laws of the Republic of Türkiye. Any disputes shall be subject to the jurisdiction of the courts of Istanbul, Türkiye, unless otherwise required by applicable mandatory law in your jurisdiction.</p>

<h2>10. Changes</h2>
<p>We may revise these Terms from time to time. Continued use of the Site after changes are posted constitutes acceptance of the revised Terms.</p>

<h2>11. Contact</h2>
<div class="legal-contact-card">
<p><strong>Dünya Azerbaycanlı Alimler Derneği</strong> — World Association of Azerbaijani Scientists (DAAB / WAAS)<br/>
Feneryolu Mahallesi, Gazi Muhtar Paşa Sokak No:44, Kadıköy, Istanbul, Türkiye<br/>
<a href="mailto:info@daab-waas.com">info@daab-waas.com</a> · <a href="tel:+905551474674">+90 555 147 46 74</a></p>
</div>
""",
        },
    },
}


def shell_head(cfg: dict, lang: str, page_id: str) -> str:
    sv = SCRIPT_VERSIONS
    st = STYLE_VERSIONS
    pair = {"az": f"az/{page_id}.html", "en": f"en/{page_id}.html"}
    seo = build_seo_block(
        rel_path=pair[lang],
        lang=lang,
        title=cfg["title"],
        description=cfg["description"],
        asset=ASSET,
        pair=pair,
    )
    return f"""<!DOCTYPE html>
<html lang="{lang}" data-daab-lang="{lang}" data-daab-asset-root="{ASSET}" data-daab-page-id="{page_id}" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{esc(cfg["title"])}</title>
<meta name="description" content="{esc(cfg["description"])}"/>
{seo}
<link href="{ASSET}css/daab-fonts.css?v={st["daab-fonts.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-common.css?v={st["daab-common.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-perf.css?v={st["daab-perf.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-mobile.css?v={st["daab-mobile.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sticky-chrome.css?v={st["daab-sticky-chrome.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-search.css?v={st["daab-search.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-back-to-top.css?v={st["daab-back-to-top.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-lang.css?v={st["daab-lang.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-nav-mega.css?v={st["daab-nav-mega.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-hero-summary.css?v={st["daab-hero-summary.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-sidebar-widget.css?v={st["daab-sidebar-widget.css"]}" rel="stylesheet"/>
<link href="{ASSET}css/daab-legal-page.css?v={st.get("daab-legal-page.css", 1)}" rel="stylesheet"/>
<script>
(function () {{
  if ("scrollRestoration" in history) history.scrollRestoration = "manual";
  try {{
    sessionStorage.removeItem("daab-lang-position");
    sessionStorage.removeItem("daab-force-page-top");
  }} catch (e) {{}}
  function toTop() {{
    document.documentElement.scrollTop = 0;
    if (document.body) document.body.scrollTop = 0;
    if (window.scrollTo) window.scrollTo(0, 0);
  }}
  toTop();
  document.addEventListener("DOMContentLoaded", toTop);
  window.addEventListener("pageshow", toTop);
}})();
</script>
<script src="{ASSET}js/daab-mobile.js?v={sv["daab-mobile.js"]}" defer></script>
<script src="{ASSET}js/daab-perf.js?v={sv["daab-perf.js"]}" defer></script>
<script src="{ASSET}js/daab-sticky-chrome.js?v={sv["daab-sticky-chrome.js"]}" defer></script>
<script src="{ASSET}js/daab-back-to-top.js?v={sv["daab-back-to-top.js"]}" defer></script>
<script src="{ASSET}js/daab-i18n.js?v={sv["daab-i18n.js"]}" defer></script>
<script src="{ASSET}js/daab-lang-position.js?v={sv["daab-lang-position.js"]}" defer></script>
<script src="{ASSET}js/daab-design-tokens.js?v={sv["daab-design-tokens.js"]}" defer></script>
<script src="{ASSET}js/daab-nav.js?v={sv["daab-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-primary-nav.js?v={sv["daab-primary-nav.js"]}" defer></script>
<script src="{ASSET}js/daab-breadcrumbs.js?v={sv["daab-breadcrumbs.js"]}" defer></script>
<script src="{ASSET}js/daab-shell.js?v={sv["daab-shell.js"]}" defer></script>
<script src="{ASSET}js/daab-page-subtitle.js?v={sv["daab-page-subtitle.js"]}" defer></script>
<script src="{ASSET}js/daab-search.js?v={sv["daab-search.js"]}" defer></script>
<script src="{ASSET}js/daab-cookie-consent.js?v={sv.get("daab-cookie-consent.js", 1)}" defer></script>
<script src="{ASSET}js/daab-analytics.js?v={sv["daab-analytics.js"]}" defer></script>
<script src="{ASSET}js/daab-sidebar-spy.js?v={sv["daab-sidebar-spy.js"]}" defer></script>
<script src="{ASSET}js/daab-sidebar-timeline.js?v={sv["daab-sidebar-timeline.js"]}" defer></script>
<script src="{ASSET}js/daab-legal-page.js?v={sv.get("daab-legal-page.js", 1)}" defer></script>
</head>
"""


def build_page(page_id: str, lang: str) -> None:
    cfg = CONTENT[page_id][lang]
    src = (ROOT / lang / "membership_value.html").read_text(encoding="utf-8")
    nav = extract_nav(src, NAV_ARIA[lang])
    if not nav:
        raise SystemExit(f"Could not extract nav from membership_value ({lang})")

    body, toc = prepare_body_and_toc(cfg["body"].strip(), lang)
    if not toc:
        raise SystemExit(f"No TOC sections found for {lang}/{page_id}")
    sidebar = render_sidebar(lang, toc)

    footer = FOOTER_AZ_HTML if lang == "az" else FOOTER_EN_HTML
    cookie_boot = ""
    if page_id == "cookies":
        cookie_boot = """
<script>
document.addEventListener("DOMContentLoaded", function () {
  var btn = document.getElementById("daab-open-cookie-settings");
  if (!btn) return;
  btn.addEventListener("click", function () {
    if (window.DAAB_COOKIE && typeof window.DAAB_COOKIE.openSettings === "function") {
      window.DAAB_COOKIE.openSettings();
    }
  });
});
</script>
"""

    page = shell_head(cfg, lang, page_id) + f"""<body class="legal-page">
<a class="skip" href="#content">{SKIP[lang]}</a>
{nav}
<header class="hero">
<div class="hero-wrap shell">
<section>
<h1 id="page-title" aria-describedby="page-hero-subtitle">{esc(cfg["hero_h1"])}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{esc(cfg["hero_subtitle"])}</p>
{f'<p class="legal-hero-note" id="page-hero-law-note">{esc(cfg["hero_note"])}</p>' if cfg.get("hero_note") else ""}
</section>
<aside aria-label="{esc(cfg["panel_title"])}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{esc(cfg["panel_title"])}</h2>
<div class="panel-copy"><p>{cfg["panel_copy"]}</p></div>
</div>
</aside>
</div>
</header>

<div class="content-wrap">
{sidebar}
<main class="legal-main main" id="content">
<article class="legal-doc">
{body}
</article>
</main>
</div>
{footer}
{cookie_boot}
</body>
</html>
"""
    out = ROOT / lang / f"{page_id}.html"
    out.write_text(page, encoding="utf-8", newline="\n")
    print(f"Wrote {out.relative_to(ROOT)}")


def main() -> None:
    for page_id in PAGES:
        for lang in ("az", "en"):
            build_page(page_id, lang)


if __name__ == "__main__":
    main()

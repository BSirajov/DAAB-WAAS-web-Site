"""English UI strings and label maps for prominent-figure profiles."""
from __future__ import annotations

GROUP_LABEL_EN = {
    "azturk": "Azerbaijani & Turkic heritage",
    "world": "World scientists",
}

PERIOD_EN = {
    "Qədim dövr": "Ancient era",
    "Orta əsrlər": "Middle Ages",
    "Yeni dövr": "Modern era",
    "Müasir dövr": "Contemporary era",
    "Antik dövr": "Antiquity",
}

FIELD_EN = {
    "Anatomiya": "Anatomy",
    "Arxeologiya": "Archaeology",
    "Ədəbiyyat": "Literature",
    "Fəlsəfə": "Philosophy",
    "Fizika": "Physics",
    "Riyaziyyat": "Mathematics",
    "Kimya": "Chemistry",
    "Biologiya": "Biology",
    "Botanika": "Botany",
    "Tarix": "History",
    "Coğrafiya": "Geography",
    "Tibb": "Medicine",
    "Cərrahiyyə": "Surgery",
    "Astronomiya": "Astronomy",
    "Memarlıq": "Architecture",
    "Musiqi": "Music",
    "Bəstəkarlıq": "Composition",
    "Dövlətçilik": "Statecraft",
    "dövlətçilik": "Statecraft",
    "Dövlət idarəçiliyi": "Governance",
    "Hərbi": "Military affairs",
    "Hərbi iş": "Military affairs",
    "Pedaqogika": "Education",
    "Hüquq": "Law",
    "İqtisadiyyat": "Economics",
    "Din": "Religion",
    "Mədəniyyət": "Culture",
    "Elm": "Science",
    "Aşıq sənəti": "Ashig art",
    "Dilçilik": "Linguistics",
    "Dramaturgiya": "Drama",
    "Dənizçilik": "Seafaring",
    "Ensiklopedist": "Encyclopedic scholarship",
    "Epos": "Epic tradition",
    "Fikir": "Intellectual thought",
    "Genetika": "Genetics",
    "Geologiya": "Geology",
    "Jurnalistika": "Journalism",
    "Kosmologiya": "Cosmology",
    "Kristalloqrafiya": "Crystallography",
    "Maarifçilik": "Enlightenment thought",
    "Maqnetizm": "Magnetism",
    "Mexanika": "Mechanics",
    "Mikrobiologiya": "Microbiology",
    "Mühəndislik": "Engineering",
    "Neft elmi": "Petroleum science",
    "Nobel": "Nobel Prize",
    "Nəsr": "Prose",
    "Opera": "Opera",
    "Muğam": "Mugham",
    "Optika": "Optics",
    "Paleontologiya": "Paleontology",
    "Polimat": "Polymathy",
    "Roman": "Novel",
    "Rəssamlıq": "Painting",
    "Satirik şeir": "Satirical poetry",
    "Sosiologiya": "Sociology",
    "Sufizm": "Sufism",
    "Türkologiya": "Turkology",
    "Təbiətşünaslıq": "Natural history",
    "Təsəvvüf": "Sufism",
    "İctimai fikir": "Public thought",
    "Şeir": "Poetry",
    "Qəzəl": "Ghazal",
    "Atomizm": "Atomism",
    "Fiziologiya": "Physiology",
    "Hesablama": "Computing",
    "Poeziya": "Poetry",
    "Teatr": "Theatre",
    "Robototexnika": "Robotics",
    "Hərb": "Military affairs",
    "hərb": "Military affairs",
    "ədəbiyyat": "Literature",
    "fəlsəfə": "Philosophy",
    "neft elmi": "Petroleum science",
    "aşıq sənəti": "Ashig art",
    "poeziya": "Poetry",
    "roman": "Novel",
    "tarixi roman": "Historical novel",
    "xalq şeiri": "Folk poetry",
    "Xalq şeiri": "Folk poetry",
    "mexanika": "Mechanics",
    "dövlətçilik": "Statecraft",
}

_FIELD_LOOKUP = {k.lower(): v for k, v in FIELD_EN.items()}

REGION_EN = {
    "Dünya elmi": "World science",
}

# Longest-first phrase replacements for leftover Azerbaijani in migrated pages.
PHRASE_REPLACEMENTS: list[tuple[str, str]] = [
    ("Azərbaycan və türk dünyası", "Azerbaijani & Turkic heritage"),
    ("Dünya alimləri", "World scientists"),
    ("Dünya elmi", "World science"),
    ("Görkəmli Şəxsiyyətlər", "Prominent Figures"),
    ("Görkəmli şəxsiyyətlər", "Prominent figures"),
    ("Ensiklopediya", "Encyclopedia"),
    ("Türkiyə", "Türkiye"),
]

FOOTER_EN = """<footer class="footer-pro">
<div class="footer-inner">
<div class="footer-brand"><h3>World Association of Azerbaijani Scientists</h3></div>
<div class="footer-grid">
<div class="footer-col"><div class="footer-title">Contact</div><div class="footer-item">✉ <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div><div class="footer-item">☎ <span>+90 555 147 46 74</span></div><div class="footer-item">🌐 <a href="https://daab-waas.com" target="_blank" rel="noopener">daab-waas.com</a></div></div>
<div class="footer-col"><div class="footer-title">Address</div><p class="footer-address">Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye</p></div>
<div class="footer-col"><div class="footer-title">Leadership</div><p class="footer-leader"><strong>Prof. Dr. Masud Afandiyev</strong><br/>Chair of the WAAS Executive Board</p></div>
</div>
</div>
<div class="footer-bottom">© 2026 WAAS — All rights reserved</div>
</footer>"""


def translate_field(raw: str) -> str:
    if not raw:
        return ""
    normalized = raw.replace("&", "·")
    parts = [p.strip() for p in normalized.split("·")]
    out = []
    for p in parts:
        out.append(_FIELD_LOOKUP.get(p.lower(), FIELD_EN.get(p, p)))
    return " · ".join(out) if len(out) > 1 else (out[0] if out else "")


def translate_period(period: str) -> str:
    return PERIOD_EN.get(period, period)


def translate_region(region: str) -> str:
    return REGION_EN.get(region, region)


def translate_group_tag(tag: str) -> str:
    if tag == "Azərbaycan və türk dünyası":
        return GROUP_LABEL_EN["azturk"]
    if tag == "Dünya alimləri":
        return GROUP_LABEL_EN["world"]
    return tag


COUNTRY_PARTS: list[tuple[str, str]] = [
    ("Almaniya / ABŞ", "Germany / USA"),
    ("Almaniya / İngiltərə", "Germany / England"),
    ("Qədim Yunanıstan / Sirakuza", "Ancient Greece / Syracuse"),
    ("Qədim Yunanıstan / İsgəndəriyyə", "Ancient Greece / Alexandria"),
    ("Yeni Zelandiya / İngiltərə", "New Zealand / England"),
    ("İrlandiya / İngiltərə", "Ireland / England"),
    ("İrlandiya / Şotlandiya", "Ireland / Scotland"),
    ("İtaliya / Fransa", "Italy / France"),
    ("Polşa / Fransa", "Poland / France"),
    ("Suriya / Misir", "Syria / Egypt"),
    ("Əndəlüs / Misir", "Al-Andalus / Egypt"),
    ("Anadolu / Cəzirə", "Anatolia / the Maghreb"),
    ("Xarəzm / Abbasilər", "Khwarazm / Abbasid realms"),
    ("İslam dünyası", "Islamic world"),
    ("Səlcuq/Türk", "Seljuk / Turkic"),
    ("Anadolu/Türk", "Anatolian / Turkic"),
    ("Anadolu türkü", "Anatolian Turk"),
    ("Azərbaycan/Türk", "Azerbaijani / Turkic"),
    ("Başqırd/Türk", "Bashkir / Turkic"),
    ("Osmanlı/Türk", "Ottoman / Turkic"),
    ("Oğuz/Türk", "Oghuz / Turkic"),
    ("Qaraxanlı/Uyğur", "Karakhanid / Uyghur"),
    ("Qəznəvi/Türk", "Ghaznavid / Turkic"),
    ("Tatar/Krım", "Tatar / Crimean"),
    ("Tatar/Türk", "Tatar / Turkic"),
    ("Teymuri/Türk", "Timurid / Turkic"),
    ("Türk/Qazax", "Turkic / Kazakh"),
    ("Türk/Xorasanlı", "Turkic / Khorasani"),
    ("Türk/Özbək-Osmanlı", "Turkic / Uzbek-Ottoman"),
    ("Türk/Özbək-Teymuri", "Turkic / Uzbek-Timurid"),
    ("Türk/Özbək", "Turkic / Uzbek"),
    ("Özbək/Teymurid", "Uzbek / Timurid"),
    ("Krım tatarı", "Crimean Tatar"),
    ("Qədim Hindistan", "Ancient India"),
    ("Qədim Yunanıstan", "Ancient Greece"),
    ("Avstriya imperiyası", "Austrian Empire"),
    ("Roma İmperiyası", "Roman Empire"),
    ("Şərqşünaslıq", "Oriental studies"),
    ("Almaniya", "Germany"),
    ("Azərbaycan", "Azerbaijan"),
    ("İngiltərə", "England"),
    ("Avstriya", "Austria"),
    ("Danimarka", "Denmark"),
    ("Fransa", "France"),
    ("İsveç", "Sweden"),
    ("İsveçrə", "Switzerland"),
    ("Niderland", "Netherlands"),
    ("Hindistan", "India"),
    ("Polşa", "Poland"),
    ("Qazaxıstan", "Kazakhstan"),
    ("Qırğızıstan", "Kyrgyzstan"),
    ("Rusiya", "Russia"),
    ("Çin", "China"),
    ("İtaliya", "Italy"),
    ("Şotlandiya", "Scotland"),
    ("Türkiyə", "Türkiye"),
    ("Özbək", "Uzbek"),
    ("Uyğur", "Uyghur"),
    ("Qazax", "Kazakh"),
    ("Qırğız", "Kyrgyz"),
    ("Türkmən", "Turkmen"),
    ("Tatar", "Tatar"),
    ("Qaraqalpaq", "Karakalpak"),
    ("Göytürk", "Gokturk"),
    ("Qaraxanlı", "Karakhanid"),
    ("Osmanlı", "Ottoman"),
    ("İsgəndəriyyə", "Alexandria"),
    ("Türk", "Turkic"),
    ("Əndəlüs", "Al-Andalus"),
    ("Flandriya", "Flanders"),
    ("ABŞ", "USA"),
]


def translate_country(country: str) -> str:
    if not country:
        return country
    out = country.replace("Türkiyə", "Türkiye")
    for az, en in sorted(COUNTRY_PARTS, key=lambda p: -len(p[0])):
        if az == "Türkiyə":
            continue
        out = out.replace(az, en)
    return out.replace("Turkiciye", "Türkiye")

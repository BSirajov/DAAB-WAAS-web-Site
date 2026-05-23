# -*- coding: utf-8 -*-
from pathlib import Path
import importlib.util

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")
spec = importlib.util.spec_from_file_location("batch", ROOT / "helpers" / "_build_batch_cvs.py")
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

CV_DIR = ROOT / "cv"


def write_cv(slug, title, body, footer_en, footer_az):
    html = b.page(title, body).replace("FOOTER_PLACEHOLDER", b.bi(footer_en, footer_az))
    out = CV_DIR / slug
    out.write_text(html, encoding="utf-8")
    print(f"Wrote {out.name} ({out.stat().st_size} bytes)")


def std_sections(h, prof_en, prof_az, stats, comps, exp_items, edu_items, extra="", pubs_ul=""):
    prof = b.section("Academic Profile", "Akademik profil",
        '<div class="callout">' + b.bib(prof_en, prof_az) + '</div>' + stats)
    comp = b.section("Core Competencies", "Əsas kompetensiyalar", comps)
    exp = b.section("Professional Experience", "Peşəkar fəaliyyət",
        '<div class="timeline">' + "".join(exp_items) + "</div>")
    edu = b.section("Education", "Təhsil",
        '<div class="education-grid">' + "".join(edu_items) + "</div>")
    pubs = ""
    if pubs_ul:
        pubs = b.section("Selected Publications", "Seçilmiş nəşrlər",
            '<div class="pub-block"><div class="pub-category"><ul>' + pubs_ul + "</ul></div></div>")
    return h + prof + comp + exp + edu + extra + pubs


# 1 Mehdi Genceli
h = b.hero(
    "Mehdi Genceli, Prof. Dr.", "Mehdi Gəncəli (İsmayilov), prof. dr.",
    "Associate professor at Marmara University Institute of Turcology. Scholar of Azerbaijani and Turkish literature, press history, and Karabakh studies; author of monographs on Mehemmed Hadi and Abdullah Sur.",
    "Marmara Universiteti Türkiyat Araştırmaları Enstitüsündə dosent. Azərbaycan və türk ədəbiyyatı, mətbuat tarixi və Qarabağ tədqiqatları üzrə alim; Mehemmed Hadi və Abdullah Sur monoqrafiyalarının müəllifi.",
    "mehdi-genceli-ismayilov.png", "Mehdi Genceli",
    b.rank_item("Academic Rank", "Akademik rütbə", "Prof. Dr.", "Prof. dr.")
    + b.rank_item("Affiliation", "Əlaqə", "Marmara University", "Marmara Universiteti")
    + b.rank_item("E-mail", "E-poçt", "mehdi.genceli@marmara.edu.tr", "mehdi.genceli@marmara.edu.tr")
    + b.rank_item("Location", "Yer", "Istanbul, Turkey", "İstanbul, Türkiyə"))
write_cv("mehdi_genceli.html", "Curriculum Vitae — Mehdi Genceli",
    std_sections(h,
        "Dr. Mehdi Genceli (born 21 September 1973, Azerbaijan) holds BA (1999), MA (2002), and PhD (2008) from Marmara University on poet Mehemmed Hadi. Associate professor at Marmara University Turcology Institute since 2012; deputy director (2018–). Author of three books including <em>Mehemmed Hadi: Life, Art, Works</em> (2011) and <em>Turk-minded Turk Abdullah Sur</em> (2021); co-editor of <em>Karabakh Region of Azerbaijan</em> (2021). Mevlana Exchange Program coordinator (2013–2016). Supervisor of 11 master students; eight articles in peer-reviewed journals.",
        "Dr. Mehdi Gəncəli (1973, Azərbaycanda anadan olub) Marmara Universitetində bakalavr (1999), magistr (2002) və PhD (2008) — Mehemmed Hadi mövzusu. 2012-dən Marmara Türkiyat Enstitüsündə dosent; müdir müavini (2018–). Üç kitabın müəllifi; Mevlana mübadilə koordinatoru (2013–2016). 11 magistrant rəhbərliyi; səkkiz jurnal məqaləsi.",
        '<div class="stats">' + b.stat("3", "Books", "Kitab") + b.stat("11", "Master Supervised", "Magistr rəhbərliyi") + b.stat("2012", "Assoc. Prof.", "Dosent") + b.stat("8", "Articles", "Məqalə") + "</div>",
        '<div class="competency-grid">' + b.comp("Research", "Tədqiqat", [
            ("Azerbaijani & Turkish literature", "Azərbaycan və türk ədəbiyyatı"),
            ("Press history & Karabakh studies", "Mətbuat tarixi və Qarabağ"),
            ("Turkic identity and ideology", "Türklük ideologiyası")]) + b.comp("Publications", "Nəşrlər", [
            ("Monographs on Mehemmed Hadi & Abdullah Sur", "Mehemmed Hadi və Abdullah Sur monoqrafiyaları"),
            ("Book chapters in Turkish studies", "Türkoloji kitab fəsilləri")]) + b.comp("Administration", "İdarəetmə", [
            ("Mevlana Program coordinator", "Mevlana koordinatoru"),
            ("Institute deputy director", "Enstitü müdir müavini")]) + b.comp("Languages", "Dillər", [
            ("Russian (KPDS-74)", "Rus dili (KPDS-74)"),
            ("Azerbaijani, Turkish", "Azərbaycan, türk")]) + "</div>",
        [b.item("2012–", "Marmara University, Turcology Institute", "Associate Professor", "Dosent"),
         b.item("2018–", "Marmara University", "Deputy Director", "Müdür müavini"),
         b.item("2013–2016", "Marmara University", "Mevlana Exchange Coordinator", "Mevlana koordinatoru")],
        [b.edu("2008", "Ph.D., New Turkish Literature", "PhD, Yeni türk ədəbiyyatı", "Marmara University. Mehemmed Hadi.", "Marmara Universiteti."),
         b.edu("2002", "M.A.", "Magistr", "Marmara University.", "Marmara Universiteti."),
         b.edu("1999", "B.A., Turkish Language & Literature", "Bakalavr", "Marmara University.", "Marmara Universiteti.")],
        pubs_ul="<li><em>Azerbaijanli Poet Mehemmed Hadi: Life, Art, Works</em>, Ötüken, 2011.</li><li><em>Turk-minded Turk Abdullah Sur</em>, Ötüken, 2021.</li>"),
    "Mehdi Genceli, Prof. Dr. · Curriculum Vitae · Istanbul", "Mehdi Gəncəli, prof. dr. · Tərcümeyi-hal · İstanbul")

# 2 Mehmet Riza Heyet
h = b.hero(
    "Mehmet Riza Heyet, Ph.D.", "Mehmet Rıza Heyət, Ph.D.",
    "Turkologist at Ankara University; editor-in-chief of <em>Varliq</em> journal; director of Tabriz Research Institute (TEBAREN). PhD (2021) on contemporary Turkic dialects and literatures.",
    "Ankara Universitetində türkoloq; <em>Varlıq</em> jurnalının baş redaktoru; TEBAREN rəhbəri. Çağdaş türk ləhcələri üzrə PhD (2021).",
    "mehmet-riza-heyet.png", "Mehmet Riza Heyet",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D.", "Ph.D.")
    + b.rank_item("Affiliation", "Əlaqə", "Ankara University", "Ankara Universiteti")
    + b.rank_item("E-mail", "E-poçt", "mrheyet@gmail.com", "mrheyet@gmail.com")
    + b.rank_item("Location", "Yer", "Ankara, Turkey", "Ankara, Türkiyə"))
write_cv("mehmet_riza_heyet.html", "Curriculum Vitae — Mehmet Riza Heyet",
    std_sections(h,
        "Dr. Mehmet Riza Heyet (born 28 June 1972, Tabriz) holds citizenship of Turkey and Iran. BA in Azerbaijani language and literature (Baku State University, 1998); MA (2005) and PhD (2021) from Ankara University. Editor of <em>Varliq</em> journal since 1995; owner and editor-in-chief since 2015. Lecturer at Ankara University Faculty of Languages, History and Geography since 2013. Director of Tabriz Research Institute (TEBAREN) since 2016. Former TRT Persian and South Azerbaijan broadcaster; translator at Azerbaijan Embassy in Tehran. Organizer of annual Turkology Day symposia (2010–2018+).",
        "Dr. Mehmet Rıza Heyət (1972, Təbriz) Türkiyə və İran vətəndaşı. BSU bakalavr (1998); Ankara magistr (2005) və PhD (2021). 1995-dən <em>Varlıq</em> redaktoru; 2015-dən baş redaktor. 2013-dən Ankara Universitetində müəllim; 2016-dan TEBAREN rəhbəri. Keçmiş TRT mütərcim-spikeri; Türkologiya Günü simpoziumlarının təşkilatçısı.",
        '<div class="stats">' + b.stat("PhD", "2021", "2021") + b.stat("2015", "Editor-in-Chief", "Baş redaktor") + b.stat("2013", "Ankara Univ.", "Ankara Univ.") + b.stat("TEBAREN", "Director", "Direktor") + "</div>",
        '<div class="competency-grid">' + b.comp("Turkology", "Türkologiya", [
            ("Contemporary Turkic dialects & literature", "Çağdaş türk ləhcələri və ədəbiyyatı"),
            ("Iranian Turkology", "İran türkologiyası")]) + b.comp("Journalism & Media", "Jurnalistika", [
            ("<em>Varliq</em> journal leadership", "<em>Varlıq</em> jurnal rəhbərliyi"),
            ("TRT international broadcasting", "TRT beynəlxalq yayımları")]) + b.comp("Academic Events", "Akademik tədbirlər", [
            ("Turkology Day symposia organizer", "Türkologiya Günü simpoziumları"),
            ("International Armenian studies symposium (2018)", "Beynəlxalq ermənşünaslıq simpoziumu")]) + b.comp("Languages", "Dillər", [
            ("Azerbaijani, Turkish, Persian", "Azərbaycan, türk, fars")]) + "</div>",
        [b.item("2013–", "Ankara University", "Lecturer, Turkic Dialects & Literatures", "Müəllim"),
         b.item("2015–", "Varliq Journal", "Owner & Editor-in-Chief", "Sahib və baş redaktor"),
         b.item("2016–", "TEBAREN (Tabriz Research Institute)", "Director", "Rəhbər"),
         b.item("2008–2013", "TRT External Broadcasts", "Translator-Announcer", "Mütərcim-spiker"),
         b.item("1995–2014", "Varliq Journal", "Editor", "Redaktor")],
        [b.edu("2021", "Ph.D.", "PhD", "Ankara University, Contemporary Turkic Dialects.", "Ankara Universiteti."),
         b.edu("2005", "M.A.", "Magistr", "Ankara University.", "Ankara Universiteti."),
         b.edu("1998", "B.A., Azerbaijani Language & Literature", "Bakalavr", "Baku State University.", "Bakı Dövlət Universiteti.")]),
    "Mehmet Riza Heyet, Ph.D. · Curriculum Vitae · Ankara", "Mehmet Rıza Heyət, Ph.D. · Tərcümeyi-hal · Ankara")

print("batch2 part 1 done")

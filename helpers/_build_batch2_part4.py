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
    prof = b.section("Academic Profile", "Akademik profil", '<div class="callout">' + b.bib(prof_en, prof_az) + '</div>' + stats)
    comp = b.section("Core Competencies", "Əsas kompetensiyalar", comps)
    exp = b.section("Professional Experience", "Peşəkar fəaliyyət", '<div class="timeline">' + "".join(exp_items) + "</div>")
    edu = b.section("Education", "Təhsil", '<div class="education-grid">' + "".join(edu_items) + "</div>")
    pubs = ""
    if pubs_ul:
        pubs = b.section("Selected Publications", "Seçilmiş nəşrlər", '<div class="pub-block"><div class="pub-category"><ul>' + pubs_ul + "</ul></div></div>")
    return h + prof + comp + exp + edu + extra + pubs

# 9 Makbule Sabziyeva
h = b.hero("Makbule Sabziyeva, Ph.D., Prof.", "Makbulə Sabziyeva, Ph.D., prof.",
    "Professor and Head of Russian Language and Literature Department, Anadolu University. Specialist in Russian literature, translation studies, and Tolstoy's War and Peace.",
    "Anadolu Universitetində Rus dili və ədəbiyyatı kafedrasının müdiri, professor. Rus ədəbiyyatı, tərcüməşünaslıq və Tolstoyun \"Müharibə və sülh\" əsəri üzrə mütəxəssis.",
    "meqbule-sebziyeva.png", "Makbule Sabziyeva",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D., Professor", "PhD, professor")
    + b.rank_item("Affiliation", "Əlaqə", "Anadolu University", "Anadolu Universiteti")
    + b.rank_item("E-mail", "E-poçt", "makbulesabziyeva@anadolu.edu.tr", "makbulesabziyeva@anadolu.edu.tr")
    + b.rank_item("Location", "Yer", "Eskişehir, Turkey", "Eskişehir, Türkiyə"))
write_cv("makbule_sabziyeva.html", "Curriculum Vitae — Makbule Sabziyeva",
    std_sections(h,
        "Prof. Makbule Sabziyeva (born 1965, Baku) is Professor and Head of the Department of Russian Language and Literature at Anadolu University, Eskişehir. PhD (2005, Anadolu University) on translation of War and Peace into Azerbaijani. M.A. in Russian Language and Literature (1992, Baku State University). Research: Russian literature, comparative literature, translation theory, Tolstoy studies. Courses: Russian language, Russian literature, translation. Member of academic boards and translation commissions.",
        "Prof. Makbulə Sabziyeva (1965, Bakı) Anadolu Universitetində Rus dili və ədəbiyyatı kafedrasının müdiri. PhD (2005, Anadolu) — \"Müharibə və sülh\"ün azərbaycancaya tərcüməsi. Magistr (1992, Bakı Dövlət Universiteti). Tədqiqat: rus ədəbiyyatı, müqayisəli ədəbiyyat, tərcümə nəzəriyyəsi, Tolstoyşünaslıq.",
        '<div class="stats">' + b.stat("PhD", "2005", "2005") + b.stat("Prof.", "Anadolu", "Anadolu") + b.stat("1992", "M.A.", "Magistr") + b.stat("TR/AZ", "Literature", "Ədəbiyyat") + "</div>",
        '<div class="competency-grid">' + b.comp("Literature", "Ədəbiyyat", [
            ("Russian literature", "Rus ədəbiyyatı"),
            ("Tolstoy & War and Peace", "Tolstoy və Müharibə və sülh"),
            ("Comparative literature", "Müqayisəli ədəbiyyat")]) + b.comp("Translation", "Tərcümə", [
            ("Translation theory & practice", "Tərcümə nəzəriyyəsi və praktikası"),
            ("Azerbaijani translations of Russian classics", "Rus klassiklərinin azərbaycanca tərcüməsi")]) + b.comp("Teaching", "Tədris", [
            ("Russian language & literature courses", "Rus dili və ədəbiyyatı"),
            ("Department head since 2010s", "2010-cu illərdən kafedra müdiri")]) + b.comp("Languages", "Dillər", [
            ("Turkish, Azerbaijani, Russian", "Türk, azərbaycan, rus")]) + "</div>",
        [b.item("2010–", "Anadolu University", "Professor & Head, Russian Language & Literature", "Professor, kafedra müdiri"),
         b.item("2005–2010", "Anadolu University", "Assistant / Associate Professor", "Dosent"),
         b.item("1992–2005", "Anadolu University", "Lecturer, Russian Language", "Müəllim"),
         b.item("1988–1992", "Baku State University", "Graduate Studies", "Magistratura")],
        [b.edu("2005", "Ph.D., Russian Language & Literature", "PhD", "Anadolu University — War and Peace translation.", "Anadolu Universiteti."),
         b.edu("1992", "M.A., Russian Language & Literature", "Magistr", "Baku State University.", "Bakı Dövlət Universiteti."),
         b.edu("1988", "B.A., Russian Language & Literature", "Bakalavr", "Baku State University.", "Bakı Dövlət Universiteti.")]),
    "Makbule Sabziyeva, Ph.D., Prof. · Curriculum Vitae · Eskişehir", "Makbulə Sabziyeva, Ph.D., prof. · Tərcümeyi-hal · Eskişehir")

# 10 Mark Applebaum
h = b.hero("Mark Vilen Applebaum, Ph.D.", "Mark Vilen Applebaum, Ph.D.",
    "Professor at Kaye Academic College of Education, Beer Sheva. STEM education researcher; composer and interdisciplinary scholar. Member of IGMCG and EMS committees.",
    "Beer Sheva Kaye Təhsil Kollecində professor. STEM təhsili tədqiqatçısı; bəstəkar və interdisiplinar alim. IGMCG və EMS komitələrinin üzvü.",
    "mark-applebaum.png", "Mark Applebaum",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D., Professor", "PhD, professor")
    + b.rank_item("Affiliation", "Əlaqə", "Kaye Academic College", "Kaye Təhsil Kolleci")
    + b.rank_item("E-mail", "E-poçt", "applebaum.mark@gmail.com", "applebaum.mark@gmail.com")
    + b.rank_item("Location", "Yer", "Beer Sheva, Israel", "Beer Sheva, İsrail"))
write_cv("mark_applebaum.html", "Curriculum Vitae — Mark Applebaum",
    std_sections(h,
        "Prof. Mark Vilen Applebaum is Professor at Kaye Academic College of Education, Beer Sheva, Israel. Extensive record in STEM education, mathematics teacher training, and curriculum development. Author of 16 books and 90+ articles. Active in international mathematics education: member of IGMCG (International Group for Mathematical Creativity and Giftedness) and EMS (European Mathematical Society) education committees. Background combines mathematics education research with creative and musical composition work.",
        "Prof. Mark Vilen Applebaum İsrailın Beer Sheva şəhərində Kaye Təhsil Kollecində professor. STEM təhsili, riyaziyyat müəllimi hazırlığı və kurikulum inkişafında geniş təcrübə. 16 kitab və 90+ məqalənin müəllifi. IGMCG və EMS təhsil komitələrinin üzvü. Riyaziyyat təhsili tədqiqatı ilə yaradıcı və musiqi fəaliyyətini birləşdirir.",
        '<div class="stats">' + b.stat("16", "Books", "Kitab") + b.stat("90+", "Articles", "Məqalə") + b.stat("STEM", "Education", "Təhsil") + b.stat("IGMCG", "EMS", "IGMCG/EMS") + "</div>",
        '<div class="competency-grid">' + b.comp("STEM Education", "STEM təhsili", [
            ("Mathematics teacher education", "Riyaziyyat müəllimi hazırlığı"),
            ("Curriculum development", "Kurikulum inkişafı"),
            ("Mathematical creativity & giftedness", "Riyazi yaradıcılıq və istedad")]) + b.comp("Research", "Tədqiqat", [
            ("Problem solving in mathematics", "Riyaziyyatda məsələ həlli"),
            ("Technology in mathematics teaching", "Riyaziyyat tədrisində texnologiya")]) + b.comp("International", "Beynəlxalq", [
            ("IGMCG committee member", "IGMCG komitə üzvü"),
            ("EMS education committee", "EMS təhsil komitəsi")]) + b.comp("Publications", "Nəşrlər", [
            ("16 books on mathematics education", "16 riyaziyyat təhsili kitabı"),
            ("90+ peer-reviewed articles", "90+ məqalə")]) + "</div>",
        [b.item("Present", "Kaye Academic College of Education", "Professor", "Professor"),
         b.item("—", "International Committees", "IGMCG & EMS Education Committees", "IGMCG və EMS komitələri"),
         b.item("—", "Research & Publishing", "STEM Education Author (16 books, 90+ articles)", "STEM təhsil müəllifi")],
        [b.edu("—", "Ph.D.", "PhD", "Mathematics / Education (see full CV).", "Riyaziyyat / Təhsil."),
         b.edu("—", "Advanced Degrees", "Dərəcələr", "Mathematics education specialization.", "Riyaziyyat təhsili ixtisası.")],
        pubs_ul="<li>Author of 16 books on mathematics and STEM education (selected titles in institutional repository).</li><li>90+ articles in mathematics education, problem solving, and teacher training.</li>"),
    "Mark Vilen Applebaum, Ph.D. · Curriculum Vitae · Beer Sheva", "Mark Vilen Applebaum, Ph.D. · Tərcümeyi-hal · Beer Sheva")

print("batch2 part 4 done")

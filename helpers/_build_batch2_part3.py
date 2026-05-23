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

# 6 Natiq Atakishiyev
h = b.hero("Natig M. Atakishiyev, Ph.D.", "Natiq Atakişiyev, Ph.D.",
    "Emeritus National Researcher (Investigador Nacional Emérito), UNAM Mexico. Theoretical physicist in quantum groups, q-polynomials, and deformed quantum systems.",
    "Meksika UNAM-da Emeritus Milli Tədqiqatçı. Kvant qrupları, q-polinomlar və deformasiya olunmuş kvant sistemləri üzrə nəzəri fizik.",
    "natiq-agakisiyev.png", "Natig Atakishiyev",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D., Dr.Sc.", "PhD, elmlər doktoru")
    + b.rank_item("Affiliation", "Əlaqə", "UNAM, Cuernavaca", "UNAM, Kuernavaka")
    + b.rank_item("E-mail", "E-poçt", "natig_atakishiyev@hotmail.com", "natig_atakishiyev@hotmail.com")
    + b.rank_item("Location", "Yer", "Cuernavaca, Mexico", "Kuernavaka, Meksika"))
write_cv("natiq_atakishiyev.html", "Curriculum Vitae — Natig Atakishiyev",
    std_sections(h,
        "Dr. Natig M. Atakishiyev (born 15 February 1939, Baku) is Investigador Nacional Emérito at Instituto de Matemáticas, UNAM, Cuernavaca (since 1996). M.Sc. equivalent (1961, Azerbaijan State University); PhD (1971, Serpukhov); Dr.Sc. (1987, Kiev Institute of Theoretical Physics). Head of Laboratory for Theory of Elementary Particles, Azerbaijan AS Institute of Physics (1983–1994). Five PhD students supervised. Extensive visiting positions at Columbia, Berlin, Ottawa, Tampa, Montreal, Istanbul, Sevilla, São Paulo, and others.",
        "Dr. Natiq Atakişiyev (1939, Bakı) 1996-dan UNAM Instituto de Matemáticas, Kuernavaka — Investigador Nacional Emérito. Bakı DU (1961); PhD (1971, Serpukhov); elmlər doktoru (1987, Kiyev). 1983–1994 AEA Fizika İnstitutunda laboratoriya müdiri. Beş doktorant rəhbərliyi.",
        '<div class="stats">' + b.stat("1961", "M.Sc.", "Magistr") + b.stat("5", "PhD Students", "PhD tələbəsi") + b.stat("1996", "UNAM", "UNAM") + b.stat("1939", "Born", "Anadan olub") + "</div>",
        '<div class="competency-grid">' + b.comp("Physics", "Fizika", [
            ("Quantum groups & q-polynomials", "Kvant qrupları və q-polinomlar"),
            ("Deformed quantum systems", "Deformasiya olunmuş kvant sistemlər"),
            ("Elementary particle theory", "Elementar hissəcik nəzəriyyəsi")]) + b.comp("Career", "Karyera", [
            ("AEA Institute of Physics (1961–1994)", "AEA Fizika İnstitutu"),
            ("UNAM Mexico (1996–present)", "UNAM Meksika (1996–)")]) + b.comp("Supervision", "Rəhbərlik", [
            ("PhD students in Baku and Mexico", "Bakı və Meksikada doktorantlar")]) + b.comp("International", "Beynəlxalq", [
            ("Visiting professor at 15+ institutions", "15+ qurumda visiting professor")]) + "</div>",
        [b.item("1996–", "UNAM, Instituto de Matemáticas", "Investigador Nacional Emérito", "Emeritus tədqiqatçı"),
         b.item("1983–1994", "Azerbaijan AS, Institute of Physics", "Head, Elementary Particles Lab", "Laboratoriya müdiri"),
         b.item("1972–1983", "Azerbaijan AS, Institute of Physics", "Senior Researcher", "Baş elmi işçi"),
         b.item("1961–1972", "Azerbaijan AS, Institute of Physics", "Researcher / Graduate Study", "Tədqiqatçı")],
        [b.edu("1987", "Doctor of Physical-Mathematical Sciences", "Fizika-riyaziyyat elmləri doktoru", "Kiev Institute of Theoretical Physics.", "Kiyev Nəzəri Fizika İnstitutu."),
         b.edu("1971", "Ph.D. (Candidate)", "PhD", "Institute of High Energy Physics, Serpukhov.", "Serpukhov."),
         b.edu("1961", "Diploma (M.Sc. equiv.)", "Diplom", "Azerbaijan State University, Physics.", "Azərbaycan Dövlət Universiteti.")]),
    "Natig M. Atakishiyev, Ph.D. · Curriculum Vitae · Mexico", "Natiq Atakişiyev, Ph.D. · Tərcümeyi-hal · Meksika")

# 7 Nigar Masumova
h = b.hero("Nigar Masumova, Ph.D.", "Nigar Məsumova, Ph.D.",
    "Associate Professor at MGIMO; Head of Advertising and Public Relations Department; Deputy Dean of School of International Journalism. Expert on economies of Turkey, Iran, and CIS; branding.",
    "MGIMO-da dosent; Reklam və İctimaiyyətlə Əlaqələr kafedrasının müdiri; Beynəlxalq Jurnalistika fakültəsi dekan müavini. Türkiyə, İran və MDB iqtisadiyyatı; brendinq.",
    "nigar-masimova.png", "Nigar Masumova",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D., Associate Professor", "PhD, dosent")
    + b.rank_item("Affiliation", "Əlaqə", "MGIMO University", "MGIMO Universiteti")
    + b.rank_item("E-mail", "E-poçt", "masumova@mail.ru", "masumova@mail.ru")
    + b.rank_item("Location", "Yer", "Moscow, Russia", "Moskva, Rusiya"))
write_cv("nigar_masumova.html", "Curriculum Vitae — Nigar Masumova",
    std_sections(h,
        "Dr. Nigar Masumova (Nigar Mamedova) is Associate Professor and Head of the Department of Advertising and Public Relations at MGIMO University; Deputy Dean of the School of International Journalism (since 2015). PhD in Economics (2012, MGIMO). Specialist in foreign economic ties (2007). Research: social and economic development of Turkey and Iran; branding. Courses: Economy of Russia, Turkey, Iran, CIS; social-economic geography; branding. Languages: English, Spanish, Azerbaijani, Turkish, Persian.",
        "Dr. Nigar Məsumova MGIMO-da reklam və PR kafedrasının müdiri, beynəlxalq jurnalistika fakültəsi dekan müavini (2015-dən). İqtisad üzrə PhD (2012, MGIMO). Tədqiqat: Türkiyə və İranın sosial-iqtisadi inkişafı; brendinq. Dillər: ingilis, ispan, azərbaycan, türk, fars.",
        '<div class="stats">' + b.stat("PhD", "2012", "2012") + b.stat("2023", "Dept. Head", "Kafedra müdiri") + b.stat("5", "Languages", "Dil") + b.stat("2015", "Deputy Dean", "Dekan müavini") + "</div>",
        '<div class="competency-grid">' + b.comp("Economics", "İqtisadiyyat", [
            ("Turkey & Iran economies", "Türkiyə və İran iqtisadiyyatı"),
            ("CIS economic geography", "MDB iqtisadi coğrafiyası"),
            ("Branding", "Brendinq")]) + b.comp("Academic Roles", "Akademik rollar", [
            ("Head, Advertising & PR Department", "Reklam və PR kafedra müdiri"),
            ("Deputy Dean, International Journalism", "Beynəlxalq jurnalistika dekan müavini")]) + b.comp("Publications", "Nəşrlər", [
            ("Monograph on Turkey (2015)", "Türkiyə monoqrafiyası (2015)"),
            ("Springer volume co-editor (2023)", "Springer cild həmmüəllifi (2023)")]) + b.comp("Languages", "Dillər", [
            ("EN, ES, AZ, TR, FA", "EN, ES, AZ, TR, FA")]) + "</div>",
        [b.item("2023–", "MGIMO", "Head, Advertising & Public Relations", "Reklam və PR müdiri"),
         b.item("2015–", "MGIMO", "Deputy Dean, School of International Journalism", "Dekan müavini"),
         b.item("2012–", "MGIMO", "Associate Professor, World Economy", "Dünya iqtisadiyyatı dosenti"),
         b.item("2002–2012", "MGIMO", "Multimedia Center Specialist", "Multimedia mərkəzi")],
        [b.edu("2012", "Ph.D., Economics", "PhD, İqtisadiyyat", "MGIMO.", "MGIMO."),
         b.edu("2007", "Specialist, Foreign Economic Ties", "İxtisas", "MGIMO.", "MGIMO."),
         b.edu("2002", "College Diploma", "Kollec", "MFA College, Russia.", "Rusiya XİN kolleci.")],
        pubs_ul="<li><em>Features of social and economic development of Turkey</em>, Moscow, 2015.</li><li>Mamedova N., Masumova N. <em>The Economy of Turkey</em>, 2018.</li><li><em>World Economy and International Business</em>, Springer, 2023.</li>"),
    "Nigar Masumova, Ph.D. · Curriculum Vitae · Moscow", "Nigar Məsumova, Ph.D. · Tərcümeyi-hal · Moskva")

# 8 Lev Eppelbaum
h = b.hero("Lev Eppelbaum, Ph.D., Prof.", "Lev Eppelbaum, Ph.D., prof.",
    "Professor of Geophysics, Tel Aviv University. Christian Huygens Medal (EGU, 2018–2019). Expert in potential field interpretation, archaeological geophysics, and environmental geophysics.",
    "Tel-Aviv Universitetində geofizika professoru. Christian Huygens medalı (EGU, 2018–2019). Potensial sahələrin interpretasiyası, arxeoloji və ekoloji geofizika.",
    "lev-v-eppelbaum.png", "Lev Eppelbaum",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D., Professor", "PhD, professor")
    + b.rank_item("Affiliation", "Əlaqə", "Tel Aviv University", "Tel-Aviv Universiteti")
    + b.rank_item("E-mail", "E-poçt", "levap@tauex.tau.ac.il", "levap@tauex.tau.ac.il")
    + b.rank_item("Location", "Yer", "Tel Aviv, Israel", "Tel-Aviv, İsrail"))
write_cv("lev_eppelbaum.html", "Curriculum Vitae — Lev Eppelbaum",
    std_sections(h,
        "Prof. Lev Eppelbaum (born 1959, Tbilisi) is Professor in the Department of Geosciences, Tel Aviv University. MSc (1982, Azerbaijan Oil & Industry University); PhD (1989, All-Union Geophysical Institute); postdoctoral studies at TAU (1991–1993). Christian Huygens Medal of the European Geosciences Union (2018–2019). Google Scholar: 7,192+ citations, h-index 46. Honorary Professor, Azerbaijan State Oil and Industry University (since 2020). Research: interpretation of potential geophysical fields, magnetic and gravity methods, archaeological and environmental geophysics, geodynamic models.",
        "Prof. Lev Eppelbaum (1959, Tbilisi) Tel-Aviv Universitetində geofizika professoru. Magistr (1982, ADNİ); PhD (1989); TAU postdoktorantura (1991–1993). Avropa Geosciences Union Christian Huygens medalı (2018–2019). Google Scholar: 7192+ sitat, h-indeks 46. ADNİ fəxri professoru (2020-dən).",
        '<div class="stats">' + b.stat("h-46", "Google Scholar", "Google Scholar") + b.stat("7192+", "Citations", "Sitat") + b.stat("2018", "Huygens Medal", "Huygens medalı") + b.stat("1989", "Ph.D.", "PhD") + "</div>",
        '<div class="competency-grid">' + b.comp("Geophysics", "Geofizika", [
            ("Potential field interpretation", "Potensial sahə interpretasiyası"),
            ("Magnetic & gravity methods", "Maqnit və cazibə metodları"),
            ("Archaeological geophysics", "Arxeoloji geofizika")]) + b.comp("Applications", "Tətbiqlər", [
            ("Oil & gas exploration", "Neft-qaz axtarışı"),
            ("Environmental monitoring", "Ekoloji monitorinq"),
            ("Geodynamic modeling", "Geodinamik modelləşdirmə")]) + b.comp("Recognition", "Tanınma", [
            ("EGU Christian Huygens Medal", "EGU Huygens medalı"),
            ("Honorary Professor, ASOIU", "ADNİ fəxri professoru")]) + b.comp("Publications", "Nəşrlər", [
            ("250,900+ ResearchGate reads", "250900+ ResearchGate oxunuş"),
            ("Extensive international conference participation", "Geniş konfrans iştirakı")]) + "</div>",
        [b.item("2005–", "Tel Aviv University", "Research Professor", "Tədqiqat professoru"),
         b.item("1998–2005", "Tel Aviv University", "Senior Lecturer / Researcher", "Baş müəllim / tədqiqatçı"),
         b.item("1991–1995", "Tel Aviv University", "Postdoctoral Researcher", "Postdoktorant"),
         b.item("1983–1990", "All-Union Geophysical Institute, Baku", "Researcher", "Tədqiqatçı")],
        [b.edu("1993", "Postdoctoral Studies", "Postdoktorantura", "Tel Aviv University, Dead Sea Rift geophysics.", "Tel-Aviv Universiteti."),
         b.edu("1989", "Ph.D., Geophysics", "PhD, Geofizika", "All-Union Geophysical Institute.", "AEA Geofizika İnstitutu."),
         b.edu("1982", "M.Sc., Geophysics", "Magistr", "Azerbaijan Oil & Industry University.", "ADNİ.")]),
    "Lev Eppelbaum, Ph.D., Prof. · Curriculum Vitae · Tel Aviv", "Lev Eppelbaum, Ph.D., prof. · Tərcümeyi-hal · Tel-Aviv")

print("batch2 part 3 done")

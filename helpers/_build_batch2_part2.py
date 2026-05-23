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
    comp = b.section("Core Competencies", "Esas kompetensiyalar", comps).replace("Esas", "Əsas")
    exp = b.section("Professional Experience", "Peşəkar fəaliyyət", '<div class="timeline">' + "".join(exp_items) + "</div>")
    edu = b.section("Education", "Təhsil", '<div class="education-grid">' + "".join(edu_items) + "</div>")
    pubs = ""
    if pubs_ul:
        pubs = b.section("Selected Publications", "Seçilmiş nəşrlər", '<div class="pub-block"><div class="pub-category"><ul>' + pubs_ul + "</ul></div></div>")
    return h + prof + comp + exp + edu + extra + pubs

# 3 Mesud Efendiyev
h = b.hero("Messoud A. Efendiyev, Prof. Dr.", "Məsud Əfəndiyev, prof. dr.",
    "Mathematician specializing in infinite-dimensional dynamical systems and mathematical biology. DAAB board chair; Rector's Distinguished Visiting Professor at Marmara University; leading professor at Helmholtz Center Munich / TUM.",
    "Sonsuz ölçülü dinamik sistemlər və riyazi biologiya üzrə riyaziyyatçı. DAAB idarə heyəti sədri; Marmara Universitetində fəxri professor; Helmholtz Münhen / TUM aparıcı professor.",
    "messoud-efendiyev.png", "Messoud Efendiyev",
    b.rank_item("Academic Rank", "Akademik rütbə", "Prof. Dr., Dr. habil.", "Prof. dr., Dr. habil.")
    + b.rank_item("Affiliation", "Əlaqə", "Helmholtz Munich / Marmara Univ.", "Helmholtz Münhen / Marmara Univ.")
    + b.rank_item("E-mail", "E-poçt", "messoud.efendiyev@gmail.com", "messoud.efendiyev@gmail.com")
    + b.rank_item("Location", "Yer", "Affalterbach, Germany", "Affalterbach, Almaniya"))
write_cv("mesud_efendiyev.html", "Curriculum Vitae — Messoud Efendiyev",
    std_sections(h,
        "Prof. Messoud A. Efendiyev (born 21 October 1953, Zaqatala) holds distinguished diploma (1975) and PhD (1980) from Lomonosov Moscow State University; Dr. habil. (1998, FU Berlin). Author of 8 books and 186 journal/conference papers. Leading professor at Helmholtz Center Munich / TUM since 2008; Rector's Distinguished Visiting Professor at Marmara University (2020–). Fields Institute Fellow (2023). James D. Murray Distinguished Professor, Waterloo (2019–2020). Research: dynamical systems, mathematical biology, nonlinear PDEs, homogenization, topological methods.",
        "Prof. Məsud Əfəndiyev (1953, Zaqatala) Lomonosov MSU fərqlənmə diplomu (1975) və PhD (1980); Dr. habil. (1998, FU Berlin). 8 kitab və 186 məqalənin müəllifi. 2008-dən Helmholtz Münhen / TUM; 2020-dən Marmara fəxri professor. Fields Institute Fellow (2023). Tədqiqat: dinamik sistemlər, riyazi biologiya, qeyrixətti PDE.",
        '<div class="stats">' + b.stat("8", "Books", "Kitab") + b.stat("186", "Papers", "Məqalə") + b.stat("2023", "Fields Fellow", "Fields Fellow") + b.stat("2008", "Helmholtz/TUM", "Helmholtz/TUM") + "</div>",
        '<div class="competency-grid">' + b.comp("Research", "Tədqiqat", [
            ("Infinite-dimensional dynamical systems", "Sonsuz ölçülü dinamik sistemlər"),
            ("Mathematical biology & medicine", "Riyazi biologiya və tibb"),
            ("Homogenization & attractors", "Homogenizasiya və atraktorlar")]) + b.comp("Books", "Kitablar", [
            ("Multifield Problems (Springer, 2003)", "Multifield Problems (Springer, 2003)"),
            ("Evolution Equations in Life Sciences (2013)", "Evolution Equations (2013)")]) + b.comp("Editorial", "Redaksiya", [
            ("Editor-in-Chief, IJ Biomathematics & Biostatistics", "IJ Biomathematics baş redaktoru"),
            ("Editor, Math. Methods in Applied Sciences", "Math. Methods redaktoru")]) + b.comp("Awards", "Mükafatlar", [
            ("Fields Institute Fellow 2023", "Fields Fellow 2023"),
            ("Alexander von Humboldt Fellowship 1991", "Humboldt stipendiyası 1991")]) + "</div>",
        [b.item("2020–", "Marmara University", "Rector's Distinguished Visiting Professor", "Fəxri professor"),
         b.item("2008–", "Helmholtz Center Munich / TUM", "Leading Professor", "Aparıcı professor"),
         b.item("2005–2008", "TUM Munich", "Professor", "Professor"),
         b.item("2000–2005", "University of Stuttgart", "Professor, SFB-404 Manager", "Professor"),
         b.item("1991–1993", "University of Stuttgart", "Humboldt Fellow", "Humboldt fellow")],
        [b.edu("1998", "Dr. habil.", "Dr. habil.", "Freie Universität Berlin.", "FU Berlin."),
         b.edu("1980", "Ph.D.", "PhD", "Lomonosov Moscow State University.", "Lomonosov MSU."),
         b.edu("1975", "Diploma (with distinction)", "Fərqlənmə diplomu", "Lomonosov MSU / Baku.", "Lomonosov MSU / Bakı.")],
        pubs_ul="<li><em>Analysis and Simulation of Multifield Problems</em> (with W.L. Wendland), Springer, 2003.</li><li><em>Mathematical Modelling of Mitochondrial Swelling</em>, Springer, 2018.</li>"),
    "Messoud A. Efendiyev, Prof. Dr. · Curriculum Vitae", "Məsud Əfəndiyev, prof. dr. · Tərcümeyi-hal")

# 4 Murad Abuzerli
h = b.hero("Murad Abuzerli, Ph.D.", "Murad Abuzərli, Ph.D.",
    "Quantum optics researcher; MSCA postdoctoral fellow at University of Vienna (NEOVITA project). PhD from Kastler Brossel Lab, Paris (2022) on out-of-equilibrium paraxial fluid of light.",
    "Kvant optika tədqiqatçısı; Vyana Universitetində MSCA postdoktorant (NEOVITA). Paris Kastler Brossel Lab PhD (2022) — paraksial işıq mayesi.",
    "murad-abuzerli.png", "Murad Abuzerli",
    b.rank_item("Academic Rank", "Akademik rütbə", "Ph.D.", "Ph.D.")
    + b.rank_item("Affiliation", "Əlaqə", "University of Vienna", "Vyana Universiteti")
    + b.rank_item("E-mail", "E-poçt", "murad.abuzarli@univie.ac.at", "murad.abuzarli@univie.ac.at")
    + b.rank_item("Location", "Yer", "Vienna, Austria", "Vyana, Avstriya"))
write_cv("murad_abuzerli.html", "Curriculum Vitae — Murad Abuzerli",
    std_sections(h,
        "Dr. Murad Abuzerli (born 12 December 1994, Baku) is a Marie Skłodowska-Curie postdoctoral fellow at the University of Vienna (2023–2026), NEOVITA project with Prof. Markus Aspelmeyer and Dr. Uroš Delić. PhD (2018–2022, Paris): out-of-equilibrium dynamics in a paraxial fluid of light (Kastler Brossel Lab). M2 Laser, Optique, Matière at Paris-Saclay / ESPCI–IOGS (2017–2018). Engineering cycle at ESPCI Paris. Expertise: nonlinear and quantum optics, quantum fluids of light, complex wave propagation. Languages: Azerbaijani, English, German, French, Russian, Turkish.",
        "Dr. Murad Abuzərli (1994, Bakı) Vyana Universitetində MSCA postdoktorant (2023–2026), NEOVITA layihəsi. PhD (2018–2022, Paris): paraksial işıq mayesinin tarazlıqdankənar dinamikası. Paris-Saclay magistr. Ekspertiza: qeyrixətti və kvant optikası, mürəkkəb dalğa ötürməsi.",
        '<div class="stats">' + b.stat("MSCA", "2023–26", "2023–26") + b.stat("PhD", "2022", "2022") + b.stat("6", "Languages", "Dil") + b.stat("Paris", "ESPCI/IOGS", "ESPCI/IOGS") + "</div>",
        '<div class="competency-grid">' + b.comp("Quantum Optics", "Kvant optikası", [
            ("Paraxial fluid of light", "Paraksial işıq mayesi"),
            ("Field/intensity correlations", "Sahə/intensivlik korrelyasiyaları")]) + b.comp("Technical Skills", "Texniki bacarıqlar", [
            ("Matlab/Python, Mathematica", "Matlab/Python, Mathematica"),
            ("SLM light control, diode lasers", "SLM, diod lazerlər")]) + b.comp("Teaching", "Tədris", [
            ("Lab works at Sorbonne Université (128 h)", "Sorbonne laboratoriya (128 saat)")]) + b.comp("Languages", "Dillər", [
            ("EN/DE/FR fluent; AZ/RU native", "EN/DE/FR səlis; AZ/RU ana dili")]) + "</div>",
        [b.item("2023–2026", "University of Vienna", "MSCA Postdoctoral Fellow, NEOVITA", "MSCA postdoktorant"),
         b.item("2018–2022", "Kastler Brossel Lab, Paris", "PhD Researcher", "PhD tədqiqatçısı"),
         b.item("2020–2021", "Sorbonne Université", "Teaching Assistant", "Tədris assistenti"),
         b.item("2017–2018", "Paris-Saclay / ESPCI–IOGS", "M2 Laser, Optique, Matière", "M2 magistr")],
        [b.edu("2022", "Ph.D., Quantum Optics", "PhD, Kvant optika", "Kastler Brossel Lab, Paris.", "Paris Kastler Brossel Lab."),
         b.edu("2018", "M2, Laser Optics & Matter", "M2", "Paris-Saclay / ESPCI–IOGS.", "Paris-Saclay."),
         b.edu("2017", "Engineering, ESPCI Paris", "Mühəndislik", "ESPCI Paris.", "ESPCI Paris.")]),
    "Murad Abuzerli, Ph.D. · Curriculum Vitae · Vienna", "Murad Abuzərli, Ph.D. · Tərcümeyi-hal · Vyana")

# 5 Murad Omarov
h = b.hero("Murad Omarov, Ph.D., Prof.", "Murad Ömərov, Ph.D., prof.",
    "Vice-Rector for International Cooperation, Kharkiv National University of Radio Electronics. Doctor of Technical Sciences; Academician of Ukrainian Academy of Applied Radioelectronic Sciences; Honored Scientist of Azerbaijan.",
    "Xarkov Milli Radioelektronika Universitetində beynəlxalq əməkdaşlıq üzrə prorektor. Texnika elmləri doktoru; Ukrayna Tətbiqi Radioelektronika Akademiyasının akademiki; Azərbaycanın fəxri elm xadimi.",
    "murad-omerov.png", "Murad Omarov",
    b.rank_item("Academic Rank", "Akademik rütbə", "Dr.Sc., Professor", "Elmlər doktoru, professor")
    + b.rank_item("Affiliation", "Əlaqə", "Kharkiv NURE", "Xarkov MREU")
    + b.rank_item("E-mail", "E-poçt", "murad.omarov@nure.ua", "murad.omarov@nure.ua")
    + b.rank_item("Location", "Yer", "Kharkiv, Ukraine", "Xarkov, Ukrayna"))
write_cv("murad_omarov.html", "Curriculum Vitae — Murad Omarov",
    std_sections(h,
        "Prof. Murad Anver oglu Omarov (born 28 March 1963, Kurdamir region) is Vice-Rector for International Cooperation at Kharkiv National University of Radio Electronics (since 2015). Dr.Sc. (2002) on electrodynamic devices with distributed nonlinear elements; PhD (1991) on fiber-optic information transmission systems. Co-author of 150+ works (17 in Scopus), 3 monographs, 11 textbooks, 12 Ukrainian patents. Supervised 5+ PhD theses. Dean, head of departments, director of foreign students center. Academician of Ukrainian Academy of Applied Radioelectronic Sciences (2004). Honored Scientist of Azerbaijan (2016).",
        "Prof. Murad Ömərov (1963, Kürdəmir) 2015-dən Xarkov MREU beynəlxalq əməkdaşlıq prorektoru. Elmlər doktoru (2002); namizədlik (1991). 150+ əsərin həmmüəllifi (17 Scopus), 3 monoqrafiya, 11 dərsliyi, 12 patent. 5+ PhD rəhbərliyi. Ukrayna Tətbiqi Radioelektronika akademiki (2004). Azərbaycan fəxri elm xadimi (2016).",
        '<div class="stats">' + b.stat("150+", "Works", "Əsər") + b.stat("40+", "Years", "İl təcrübə") + b.stat("5+", "PhD Guided", "PhD rəhbərliyi") + b.stat("2016", "Honored Scientist", "Fəxri elm xadimi") + "</div>",
        '<div class="competency-grid">' + b.comp("Engineering", "Mühəndislik", [
            ("Fiber-optic communication systems", "Lifli-optik rabitə"),
            ("Electrodynamic device design", "Elektrodinamik qurğu layihəsi"),
            ("Robotics & automation", "Robototexnika və avtomatlaşdırma")]) + b.comp("Administration", "İdarəetmə", [
            ("Vice-Rector, International Cooperation", "Beynəlxalq əməkdaşlıq prorektoru"),
            ("Dean; foreign students center director", "Dekan; xarici tələbələr mərkəzi")]) + b.comp("Teaching", "Tədris", [
            ("Computerized communication systems", "Kompüterləşdirilmiş rabitə"),
            ("Higher mathematics; robotics", "Ali riyaziyyat; robototexnika")]) + b.comp("Recognition", "Tanınma", [
            ("ICONAT conference series chair since 2019", "ICONAT sədri (2019-dan)"),
            ("12 Ukrainian invention patents", "12 ukrayna patenti")]) + "</div>",
        [b.item("2015–", "Kharkiv NURE", "Vice-Rector, International Cooperation", "Prorektor"),
         b.item("2003–2009", "Kharkiv NURE", "Professor", "Professor"),
         b.item("2009–2015", "Kharkiv NURE", "Dean; Director, Foreign Students Center", "Dekan; mərkəz direktoru"),
         b.item("1999–2002", "Kharkiv NURE", "Doctoral Studies; Senior Researcher", "Doktorantura"),
         b.item("1980–1985", "Kharkiv Institute of Radio Electronics", "Student / Engineer", "Tələbə / mühəndis")],
        [b.edu("2002", "Dr.Sc., Technical Sciences", "Elmlər doktoru", "Electrodynamic devices with nonlinear elements.", "Qeyri-xətti elementli elektrodinamik qurğular."),
         b.edu("1991", "PhD (Candidate)", "Namizədlik", "Fiber-optic information transmission systems.", "Lifli-optik informasiya ötürmə."),
         b.edu("1985", "Electronic Engineering Engineer", "Mühəndis", "Kharkiv Institute of Radio Electronics.", "Xarkov Radioelektronika İnstitutu.")]),
    "Murad Omarov, Ph.D., Prof. · Curriculum Vitae · Kharkiv", "Murad Ömərov, Ph.D., prof. · Tərcümeyi-hal · Xarkov")

print("batch2 part 2 done")

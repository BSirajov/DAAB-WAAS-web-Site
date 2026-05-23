"""Generate bilingual CV HTML pages for batch of scientists."""
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")
CV_DIR = ROOT / "cv"
TEMPLATE = (CV_DIR / "gunel_seferova.html").read_text(encoding="utf-8")
CSS = re.search(r"<style>(.*?)</style>", TEMPLATE, re.S).group(1)
SCRIPT = re.search(r"<script>.*?</script>", TEMPLATE, re.S).group(0)


def bi(en: str, az: str) -> str:
    return f'<span class="lang en">{en}</span><span class="lang az">{az}</span>'


def bib(en: str, az: str) -> str:
    return f'<span class="lang en block">{en}</span><span class="lang az block">{az}</span>'


def rank_item(label_en: str, label_az: str, dd_en: str, dd_az: str) -> str:
    return (
        f'<div class="rank-item"><dt>{bi(label_en, label_az)}</dt>'
        f"<dd>{bi(dd_en, dd_az) if dd_en != dd_az else dd_en}</dd></div>"
    )


def stat(num: str, label_en: str, label_az: str) -> str:
    return (
        f'<div class="stat-item"><span class="stat-num">{num}</span>'
        f'<span class="stat-label">{bi(label_en, label_az)}</span></div>'
    )


def comp(title_en: str, title_az: str, items: list[tuple[str, str]]) -> str:
    lis = "".join(f"<li>{bi(e, a)}</li>" for e, a in items)
    return f'<div class="comp-group"><h3>{bi(title_en, title_az)}</h3><ul>{lis}</ul></div>'


def item(period: str, org: str, role_en: str, role_az: str, desc_en: str = "", desc_az: str = "") -> str:
    p = ""
    if desc_en:
        p = f"<p>{bib(desc_en, desc_az)}</p>"
    return (
        f'<article class="item"><div class="period">{period}</div><div>'
        f"<h3>{org}</h3>"
        f'<span class="role">{bi(role_en, role_az)}</span>{p}</div></article>'
    )


def edu(period: str, title_en: str, title_az: str, desc_en: str, desc_az: str) -> str:
    return (
        f'<article class="edu-card"><div class="period">{period}</div>'
        f"<h3>{bi(title_en, title_az)}</h3>"
        f"<p>{bib(desc_en, desc_az)}</p></article>"
    )


def page(title: str, body: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{title}</title>
  <style>{CSS}</style>
</head>
<body>
<main class="page">
{body}
  <footer>
    FOOTER_PLACEHOLDER
  </footer>
</main>
{SCRIPT}
</body>
</html>"""


def hero(name_en, name_az, subtitle_en, subtitle_az, photo, alt, ranks: str) -> str:
    return f"""
  <div class="lang-switch">
    <button id="btn-en" type="button" onclick="setLang('en')">English</button>
    <button id="btn-az" type="button" onclick="setLang('az')">Azərbaycan</button>
  </div>
  <header class="hero">
    <div class="hero-top">
      <div class="hero-text">
        <span class="cv-label">{bi("Curriculum Vitae", "Tərcümeyi-hal")}</span>
        <h1>{bi(name_en, name_az)}</h1>
        <p class="subtitle">{bib(subtitle_en, subtitle_az)}</p>
      </div>
      <figure class="hero-photo">
        <img src="../images/scientists-photos/{photo}" alt="{alt}" width="160" height="200" loading="eager" />
      </figure>
    </div>
    <dl class="rank-bar">{ranks}</dl>
  </header>"""


def section(title_en: str, title_az: str, inner: str) -> str:
    return f'<section class="section"><h2 class="section-title">{bi(title_en, title_az)}</h2>{inner}</section>'


def build_xelil_kelenter() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Ph.D. (Dual Doctorate)", "PhD (iki doktorluq)")
        + rank_item("Affiliation", "Əlaqə", "Global Optical Solutions & Kepler", "Global Optical Solutions & Kepler")
        + rank_item("E-mail", "E-poçt", "gosx2020@gmail.com", "gosx2020@gmail.com")
        + rank_item("Location", "Yer", "Japan", "Yaponiya")
    )
    h = hero(
        "Khalil Kelenter, Ph.D.",
        "Xəlil Kələntər, Ph.D.",
        "Senior researcher and developer in optical engineering and display technologies. SID Fellow, IEC expert, and pioneer of LCD backlight (BLU) optics with nearly 100 patents and 96+ publications.",
        "Optik mühəndisliyi və displey texnologiyaları üzrə baş tədqiqatçı. SID Fellow, IEC eksperti; LCD arxa işıqlandırma (BLU) optikası sahəsinin yaradıcısı; təxminən 100 patent və 96+ nəşr.",
        "xelil-kelenter.png",
        "Khalil Kelenter",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class="callout">' + bib("Dr. Khalil Kelenter (K. Käläntär) was born in Azerbaijan in 1953. He earned B.E. (1980) from the Polytechnic University, M.E. (1984) from Toyohashi University of Technology, and doctorates from Nagoya University (1987) and Tohoku University (2003). His research spans 2D/3D optical transmission, optoelectronic sensors, LCD/BLU optics, and smectic liquid-crystal vortex arrays. Since 1995 he has developed optical devices for LCD units, pioneering microstructure light-guide plates. He holds nearly 100 patents (Japan, USA, Canada, Europe, South Korea, Taiwan), authored three Japanese books on LCD backlighting, and supervised doctoral candidates internationally. SID Special Recognition Award (2007), SID Fellow (2013), IEC1906 Award (2018), and Progress medal of Azerbaijan (2026).", "Dr. Xəlil Kələntər (K. Käläntär) 1953-cü ildə Azərbaycanda anadan olub. Politeknik Universitet (B.E., 1980), Toyohashi Texnologiya Universiteti (M.E., 1984), Naqoya (1987) və Tohoku (2003) universitetlərində doktorluq alıb. Tədqiqatları 2D/3D optik ötürmə, optoelektron sensorlar, LCD/BLU optikası və smektik maye kristal vorteks massivlərini əhatə edir. 1995-dən LCD modulları üçün optik cihazlar hazırlayır; mikrostrukturlu işıq bələdçi plitələrinin kütləvi istehsalında öncül olub. Təxminən 100 patent, LCD arxa işıqlandırması üzrə 3 yapon kitabı, beynəlxalq doktorantlara rəhbərlik. SID xüsusi mükafatı (2007), SID Fellow (2013), IEC1906 (2018), Azərbaycan Tərəqqi medalı (2026).") + '</div>'
        + '<div class="stats">'
        + stat("96+", "Articles", "Məqalə")
        + stat("~100", "Patents", "Patent")
        + stat("SID", "Fellow 2013", "Fellow 2013")
        + stat("7", "IEC Documents", "IEC sənədi")
        + "</div>",
    )
    comp_sec = section(
        "Core Competencies",
        "Əsas kompetensiyalar",
        '<div class="competency-grid">'
        + comp("Optical Engineering", "Optik mühəndislik", [
            ("Graded-index and step-index fiber optics", "Qradiyentli və addımlı lif optikası"),
            ("LCD backlight unit (BLU) design", "LCD BLU layihələndirilməsi"),
            ("Micro-reflector light-guide plates", "Mikroreflektor işıq bələdçi plitələri"),
        ])
        + comp("Display Technologies", "Displey texnologiyaları", [
            ("LCD and LED backlight systems", "LCD və LED arxa işıq sistemləri"),
            ("Optical vortex arrays (smectic LC)", "Optik vorteks massivləri"),
            ("Electronic displays and sensors", "Elektron displey və sensorlar"),
        ])
        + comp("Standards & Leadership", "Standartlar və liderlik", [
            ("IEC expert; 7 standard documents", "IEC eksperti; 7 standart sənədi"),
            ("SID DSY Subcommittee Chair (since 2020)", "SID DSY alt komitə sədri (2020-dən)"),
            ("IDW FMC/DES workshop founder", "IDW FMC/DES seminar təsisçisi"),
        ])
        + comp("Languages", "Dillər", [
            ("English, Japanese, Chinese publications", "İngilis, yapon, çin dilində nəşrlər"),
            ("Azerbaijani (native)", "Azərbaycan dili (ana dili)"),
        ])
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("Since 1995", "Global Optical Solutions & Kepler", "Senior Researcher & Developer", "Baş tədqiqatçı və developer", "Development of optical devices and modules for LCD units; mass production of functional light-guide plates.", "LCD modulları üçün optik cihaz və modulların inkişafı; funksional işıq bələdçi plitələrinin kütləvi istehsalı.")
        + item("3 years", "Samsung-Cheil Mojik, South Korea", "Display Technology Expert", "Displey texnologiyası eksperti", "Expanded expertise in electronic display manufacturing.", "Elektron displey istehsalında ekspertiza.")
        + item("Advisor", "Aomori Prefecture, Japan", "OCB LCD Technology Advisor", "OCB LCD texnologiyası məsləhətçisi", "Advanced optically compensated bend LCD technology.", "Optik kompensasiyalı əyilmə LCD texnologiyasının inkişafı.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("2003", "Ph.D., Tohoku University", "PhD, Tohoku Universiteti", "Doctor of Engineering.", "Mühəndislik elmləri doktoru.")
        + edu("1987", "Ph.D., Nagoya University", "PhD, Naqoya Universiteti", "Doctor of Engineering.", "Mühəndislik elmləri doktoru.")
        + edu("1984", "M.E., Toyohashi Univ. of Technology", "M.E., Toyohashi Texnologiya Universiteti", "Master of Engineering in Electronics.", "Elektronika mühəndisliyi üzrə magistr.")
        + edu("1980", "B.E., Polytechnic University", "B.E., Politeknik Universitet", "Bachelor of Electronics Engineering.", "Elektronika mühəndisliyi bakalavr.")
        + "</div>",
    )
    awards = section(
        "Awards & Honors",
        "Mükafatlar",
        '<div class="callout">' + bib("SID Special Recognition Award (2007); Distinguished Paper Awards SID2011 & SID2018; SID Fellow (2013); JLCS R&amp;D Award (2016); KUM Award IDW Japan (2023); IEC1906 Award (2018); Progress medal, Azerbaijan (2026).", "SID xüsusi tanınma mükafatı (2007); SID2011 və SID2018 fərqlənən məqalə mükafatları; SID Fellow (2013); JLCS T&amp;D mükafatı (2016); KUM mükafatı IDW Yaponiya (2023); IEC1906 (2018); Tərəqqi medalı, Azərbaycan (2026).") + '</div>',
    )
    body = h + profile + comp_sec + exp + edu_sec + awards
    html = page("Curriculum Vitae — Khalil Kelenter", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Khalil Kelenter, Ph.D. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Japan", "Xəlil Kələntər, Ph.D. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Yaponiya"),
    )


def build_kamal_akbarov() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "DMSc, PhD — Radiation Oncology", "T.E.N., PhD — Radiasiya onkologiyası")
        + rank_item("Affiliation", "Əlaqə", "WHO Regional Europe-Ukraine", "ÜST Avropa-Ukrayna regional ofisi")
        + rank_item("E-mail", "E-poçt", "kamal.akbarov@gmail.com", "kamal.akbarov@gmail.com")
        + rank_item("Location", "Yer", "Vienna, Austria", "Vyana, Avstriya")
    )
    h = hero(
        "Kamal Akbarov, DMSc, PhD",
        "Kamal Əkbərov, T.E.N., PhD",
        "Radiation oncologist and healthcare project manager. Technical Officer (CBRN) at WHO; former IAEA radiation oncology officer. Expert in cancer control, radiotherapy development, and international cooperation.",
        "Radiasiya onkoloqu və səhiyyə layihə meneceri. ÜST-də CBRN üzrə texniki məsul; IAEA-nın keçmiş radiasiya onkologiyası məsul şəxsi. Onkoloji xəstəliklərin nəzarəti, radioterapiya inkişafı və beynəlxalq əməkdaşlıq üzrə ekspert.",
        "kamal-ekberov.png",
        "Kamal Akbarov",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Dr. Kamal Akbarov is a highly accomplished radiation oncologist with DMSc and PhD degrees from the National Center of Oncology of Azerbaijan. He currently serves as Technical Officer (CBRN, P4/S5) at WHO Regional Europe-Ukraine office. Previously Technical Officer – Radiation Oncologist at IAEA Vienna (2018–2023), where he supported 61 technical cooperation projects (2021 budget USD 331M), led the UN Global Joint Program on Cervical Cancer, and spearheaded the ELAISA AI-contouring research project. At Azerbaijan National Oncology Center (2005–2018) he implemented 3D CRT, IMRT, VMAT, SBRT, SRS, and brachytherapy. MBA in International Healthcare Management (University of Cumbria/RKC). Fluent in German, English, Russian, Turkish, and Azerbaijani.", "Dr. Kamal Əkbərov Azərbaycan Milli Onkologiya Mərkəzindən T.E.N. və PhD dərəcələrinə malik radiasiya onkoloqudur. Hazırda ÜST Avropa-Ukrayna regional ofisində CBRN üzrə texniki məsul (P4/S5) vəzifəsindədir. Əvvəl IAEA Vyana (2018–2023) radiasiya onkoloqu; 61 texniki əməkdaşlıq layihəsini (2021, 331 mln USD) dəstəkləmiş, BMT-nin Serviks xərçəngi qlobal birgə proqramına rəhbərlik etmiş, ELAISA AI konturlama layihəsinə başçılıq etmişdir. 2005–2018 Azərbaycan Milli Onkologiya Mərkəzində 3D CRT, IMRT, VMAT, SBRT, SRS və brahiterapiya tətbiq etmişdir. Beynəlxalq səhiyyə menecmenti MBA (Kumbriya/RKC).") + '</div>'
        + '<div class="stats">'
        + stat("WHO", "Since 2024", "2024-dən")
        + stat("IAEA", "2018–2023", "2018–2023")
        + stat("61", "TC Projects 2021", "TC layihə 2021")
        + stat("5", "Languages", "Dil")
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2024–", "World Health Organization", "Technical Officer – CBRN (P4/S5)", "Texniki məsul – CBRN (P4/S5)", "Scientific and technical support for chemical, biological, radiation and nuclear threats under WHO Health Emergencies.", "Kimyəvi, bioloji, radiasiya və nüvə təhlükələrinə qarşı elmi-texniki dəstək (ÜST Fövqəladə Hallar).")
        + item("2018–2023", "International Atomic Energy Agency, Vienna", "Technical Officer – Radiation Oncologist", "Texniki məsul – Radiasiya onkoloqu", "Supported national cancer control programs; coordinated with WHO, ESTRO, ASTRO; led ELAISA and ICARO3 activities.", "Milli onkoloji nəzarət proqramları; ÜST, ESTRO, ASTRO ilə koordinasiya; ELAISA və ICARO3.")
        + item("2005–2018", "National Center of Oncology, Baku", "Radiation Oncologist, DMSc, PhD", "Radiasiya onkoloqu, T.E.N., PhD", "Modern radiotherapy techniques; concurrent chemoradiotherapy research; EMBRACEII multicenter studies.", "Müasir radioterapiya; kombinə kemoradioterapiya tədqiqatları; EMBRACEII.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("—", "DMSc & PhD, Radiation Oncology", "T.E.N. və PhD, Radiasiya onkologiyası", "National Center of Oncology of Azerbaijan Republic.", "Azərbaycan Respublikası Milli Onkologiya Mərkəzi.")
        + edu("—", "MBA, International Healthcare Management", "MBA, Beynəlxalq səhiyyə menecmenti", "University of Cumbria (UK) / Robert Kennedy College, Switzerland.", "Kumbriya Universiteti (Böyük Britaniya) / Robert Kennedy Kollec, İsveçrə.")
        + edu("—", "Medical Residencies", "Tibb rezidentura proqramları", "Oncology and radiation oncology specialties; Azerbaijan Medical University.", "Onkologiya və radiasiya onkologiyası; Azərbaycan Tibb Universiteti.")
        + "</div>",
    )
    body = h + profile + exp + edu_sec
    html = page("Curriculum Vitae — Kamal Akbarov", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Kamal Akbarov, DMSc, PhD &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Vienna", "Kamal Əkbərov, T.E.N., PhD &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Vyana"),
    )


def build_kamran_rustemov() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Dr.Sc., Professor", "Elmlər doktoru, professor")
        + rank_item("Affiliation", "Əlaqə", "Center for Modeling Political Communications, Moscow", "Siyasi Kommunikasiyaların Modelləşdirilməsi Mərkəzi, Moskva")
        + rank_item("E-mail", "E-poçt", "aliev.05@mail.ru", "aliev.05@mail.ru")
        + rank_item("Location", "Yer", "Moscow, Russia", "Moskva, Rusiya")
    )
    h = hero(
        "Kamran Rustemov, Dr.Sc., Prof.",
        "Kamran Rüstəmov, elmlər doktoru, prof.",
        "Azerbaijani scientist, educator, publicist and public figure. Honored Scientist of Azerbaijan; foreign member of RAASN. Pioneer in oil/gas hydraulics, building climatology, and non-Newtonian mechanics.",
        "Azərbaycanlı alim, pedaqoq, publisist və ictimai xadim. Azərbaycan Respublikasının əməkdar elm xadimi; RAASN xarici üzvü. Neft-qaz hidravlikası, bina iqlimologiyası və qeyri-nyuton mexanikası üzrə öncül.",
        "kamran-rustemov.png",
        "Kamran Rustemov",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Prof. Kamran Rustemov (born 23 June 1948, Baku) holds a doctorate in technical sciences and the title of professor. He is Honored Scientist of the Republic of Azerbaijan and a foreign member of the Russian Academy of Architecture and Construction Sciences (1998). His fundamental work covers oil and gas field development, drilling hydraulics, and non-Newtonian system mechanics. He first developed gas-dynamic theory of pipeline operation under abnormal conditions and classification models for two-phase flows. He created mathematical foundations of building climatology and generalized heat/mass transfer theory in building structures. Author of 300+ scientific works. Presidential adviser to Azerbaijan (1991–1992). Scientific director of the Center for Modeling Political Communications, Moscow. Awarded Order of Friendship of Peoples (1986) and Azerbaijan diaspora service medal (2020).", "Prof. Kamran Rüstəmov (1948-ci il 23 iyun, Bakı) texnika elmləri doktoru, professordur. Azərbaycan Respublikasının əməkdar elm xadimi, Rusiya Memarlıq və İnşaat Elmləri Akademiyasının xarici üzvü (1998). Neft-qaz yataqlarının istismarı, qazma hidravlikası və qeyri-nyuton sistemlərinin mexanikası üzrə fundamental işlər. Boru kəmərlərinin anormal rejimlərinin qaz-dinamik nəzəriyyəsi, ikifazalı axınların təsnifat modelləri, bina iqlimologiyasının riyazi əsasları. 300-dən çox elmi əsərin müəllifi. 1991–1992 Azərbaycan prezidentinin dövlət müşaviri. Moskva, Siyasi Kommunikasiyaların Modelləşdirilməsi Mərkəzinin elmi rəhbəri. Xalqlar Dostluğu ordeni (1986), diaspora medalı (2020).") + '</div>'
        + '<div class="stats">'
        + stat("300+", "Publications", "Nəşr")
        + stat("1998", "RAASN Member", "RAASN üzvü")
        + stat("1991–92", "Presidential Adviser", "Prezident müşaviri")
        + stat("2020", "Diaspora Medal", "Diaspora medalı")
        + "</div>",
    )
    comp_sec = section(
        "Core Competencies",
        "Əsas kompetensiyalar",
        '<div class="competency-grid">'
        + comp("Engineering Science", "Mühəndislik elmi", [
            ("Oil & gas drilling hydraulics", "Neft-qaz qazma hidravlikası"),
            ("Two-phase flow modeling", "İkifazalı axın modelləşdirməsi"),
            ("Non-Newtonian mechanics", "Qeyri-nyuton mexanikası"),
        ])
        + comp("Building & Energy", "Bina və enerji", [
            ("Building climatology", "Bina iqlimologiyası"),
            ("Heat and mass transfer in structures", "Strukturlarda istilik və kütlə ötürmə"),
            ("Heating system economic models", "İstilik sistemlərinin iqtisadi modelləri"),
        ])
        + comp("Education & Industry", "Təhsil və sənaye", [
            ("University production technologies for engineer training", "Mühəndis hazırlığı üçün universitet istehsal texnologiyaları"),
            ("Leadership at Sibur, MIR, Iskra-Energetika", "Sibur, MIR, İskra-Energetika rəhbərliyi"),
        ])
        + comp("Public Activity", "İctimai fəaliyyət", [
            ("Journalist unions of Azerbaijan and Russia", "Azərbaycan və Rusiya jurnalistlər birlikləri"),
            ("Diaspora and publicist work in Russian media", "Diaspora və rusdilli publisistika"),
        ])
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("Present", "Center for Modeling Political Communications, Moscow", "Scientific Director", "Elmi rəhbər", "Research leadership in political communications modeling.", "Siyasi kommunikasiyaların modelləşdirilməsi üzrə elmi rəhbərlik.")
        + item("2000s", "Russia — Sibur, MIR, Iskra-Energetika", "Executive Leadership", "İcra rəhbərliyi", "Turkey and Iraq representative for Sibur; CEO MIR; board chair Iskra-Energetika.", "Sibur Türkiyə/İraq nümayəndəsi; MIR baş direktoru; İskra-Energetika sədri.")
        + item("1991–1992", "Republic of Azerbaijan", "Presidential State Adviser", "Prezidentin dövlət müşaviri", "Advised on state policy during early independence period.", "Müstəqillik dövründə dövlət siyasəti üzrə məsləhət.")
        + item("1977–1978", "United Kingdom", "Scientific Training", "Elmi təcrübə", "Research fellowship in Great Britain.", "Böyük Britaniyada elmi təcrübə.")
        + "</div>",
    )
    body = h + profile + comp_sec + exp
    html = page("Curriculum Vitae — Kamran Rustemov", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Kamran Rustemov, Dr.Sc., Prof. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Moscow", "Kamran Rüstəmov, elmlər doktoru, prof. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Moskva"),
    )


def build_ismayil_aliyev() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Dr.Sc., Professor", "İqtisad elmləri doktoru, professor")
        + rank_item("Affiliation", "Əlaqə", "St. Petersburg State University of Economics", "Sankt-Peterburq Dövlət İqtisad Universiteti")
        + rank_item("E-mail", "E-poçt", "aliev.05@mail.ru", "aliev.05@mail.ru")
        + rank_item("Location", "Yer", "St. Petersburg, Russia", "Sankt-Peterburq, Rusiya")
    )
    h = hero(
        "Ismayil Aliyev, Dr.Sc., Prof.",
        "İsmayıl Əliyev, iqtisad elmləri doktoru, prof.",
        "Professor of labor economics and human resource management at St. Petersburg State University of Economics. Head of the Labor Economics scientific school; author of 150+ publications including major textbooks.",
        "Sankt-Peterburq Dövlət İqtisad Universitetində əməyin iqtisadiyyatı və insan resurslarının idarə edilməsi professoru. 'Əməyin iqtisadiyyatı' elmi məktəbinin rəhbəri; 150-dən artıq nəşrin, o cümlədən dərsliklərin müəllifi.",
        "ismayil-eliyev.png",
        "Ismayil Aliyev",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Prof. Ismayil Aliyev (born 6 May 1966, Ordubad, Nakhchivan) graduated from St. Petersburg State University of Economics and Finance in 1992 (Labor Economics). He defended candidate (1990s) and doctoral (2007) dissertations; associate professor since 2002, professor since 2009. Research areas: labor economics, social policy, living standards, wage management, state regulation, and HR management. Deputy head of the Labor Economics department (2002–2019); department head (2020–2023); professor at Enterprise and Industrial Complex Economics department since 2023. Academic director of HR management master program; head of Labor Economics master program; chair of dissertation council (since 2022). Supervised 10 candidates and 2 doctors of sciences. Author of textbooks <em>Labor Economics</em> (5th ed.), <em>Human Resource Management</em> (4th ed.), and <em>Income and Wage Policy</em>. Honored by Russian Ministry of Education (2018) and St. Petersburg Legislative Assembly.", "Prof. İsmayıl Əliyev (1966-cı il 6 may, Ordubad) 1992-ci ildə Sankt-Peterburq Dövlət İqtisadiyyat və Maliyyə Universitetini 'Əməyin iqtisadiyyatı' ixtisası üzrə bitirib. Namizədlik və doktorluq dissertasiyalarını müdafiə etmiş; 2002-dən dosent, 2009-cu ildən professor. Tədqiqat: əməyin iqtisadiyyatı, sosial siyasət, həyat səviyyəsi, əməkhaqqı, dövlət tənzimlənməsi, HR idarəetməsi. 2002–2019 kafedra müdir müavini; 2020–2023 kafedra müdiri; 2023-dən 'Müəssisələrin və Sənaye Komplekslərinin İqtisadiyyatı' kafedrasında professor. Magistr proqramlarının elmi rəhbəri və akademik direktoru; 2022-dən dissertasiya şurasının sədri. 10 namizəd və 2 elmlər doktoru hazırlayıb. 'Əməyin iqtisadiyyatı' (V nəşr), 'İnsan resurslarının idarə edilməsi' (IV nəşr), 'Gəlir və əmək haqqı siyasəti' dərsliklərinin müəllifi. RF Təhsil Nazirliyinin fəxri fərmanı (2018), SPb Qanunvericilik Məclisinin fəxri fərmanı.") + '</div>'
        + '<div class="stats">'
        + stat("150+", "Publications", "Nəşr")
        + stat("12", "Textbooks", "Dərslik")
        + stat("12", "Graduates Supervised", "Məzun rəhbərlik")
        + stat("2009", "Professor", "Professor")
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2023–", "St. Petersburg State University of Economics", "Professor; Head, Labor Economics School", "Professor; 'Əməyin iqtisadiyyatı' elmi məktəbinin rəhbəri", "Professor at Enterprise and Industrial Complex Economics department; chairs dissertation council.", "Müəssisələrin və Sənaye Komplekslərinin İqtisadiyyatı kafedrasında professor; dissertasiya şurasına sədrlik.")
        + item("2020–2023", "St. Petersburg State University of Economics", "Department Head", "Kafedra müdiri", "Led Labor Economics department.", "'Əməyin iqtisadiyyatı' kafedrasına rəhbərlik.")
        + item("2002–2019", "St. Petersburg State University of Economics", "Deputy Department Head", "Kafedra müdir müavini", "Teaching, research, and graduate supervision.", "Tədris, tədqiqat və magistr/aspirant rəhbərliyi.")
        + item("1990s–", "St. Petersburg State University of Economics", "Assistant to Associate Professor", "Assistentdən dosentə", "Progression through assistant, senior lecturer, associate professor.", "Assistent, baş müəllim, dosent vəzifələrində irəliləyiş.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("2007", "Doctor of Economic Sciences", "İqtisad elmləri doktoru", "Thesis on income and living standards in the context of Russia's social policy (federal and regional aspects).", "RF sosial siyasəti kontekstində gəlir və həyat səviyyəsi (federal və regional aspektlər).")
        + edu("1990s", "Candidate of Economic Sciences", "İqtisad elmləri namizədi", "Thesis on remuneration and incentives for industrial managers and specialists.", "Sənaye rəhbər və mütəxəssislərinin əməyinin ödənilməsi və həvəsləndirilməsi.")
        + edu("1992", "Specialist, Labor Economics", "İxtisas, Əməyin iqtisadiyyatı", "St. Petersburg State University of Economics and Finance.", "Sankt-Peterburq Dövlət İqtisadiyyat və Maliyyə Universiteti.")
        + "</div>",
    )
    pubs = section(
        "Selected Publications",
        "Seçilmiş nəşrlər",
        '<div class="pub-block"><div class="pub-category"><ul>'
        + "<li>Human capital adaptation to external volatility (Scopus, 2017)</li>"
        + "<li>Social investments as a factor of sustainable regional development (2020)</li>"
        + "<li>DevOps methodology and IT staffing analysis (Scopus, 2020)</li>"
        + "<li>Labor potential as strategic resource (2021)</li>"
        + "<li>Virtualization technologies: comparative review (Scopus, 2022)</li>"
        + "<li>Employment forms transformation in digital economy context (Scopus, 2023)</li>"
        + "<li><em>Population income and state social policy</em> (monograph)</li>"
        + "</ul></div></div>",
    )
    body = h + profile + exp + edu_sec + pubs
    html = page("Curriculum Vitae — Ismayil Aliyev", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Ismayil Aliyev, Dr.Sc., Prof. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; St. Petersburg", "İsmayıl Əliyev, iqtisad elmləri doktoru, prof. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Sankt-Peterburq"),
    )


def build_sevda_kerimova() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "PhD(c) — Law & Bioethics", "PhD(m) — Hüquq və bioetika")
        + rank_item("Affiliation", "Əlaqə", "Vice Versa Consulting; TABİB (former)", "Vice Versa Consulting; TABİB (keçmiş)")
        + rank_item("E-mail", "E-poçt", "sevda.aydin.k@gmail.com", "sevda.aydin.k@gmail.com")
        + rank_item("Location", "Yer", "Bochum, Germany / Baku", "Bochum, Almaniya / Bakı")
    )
    h = hero(
        "Sevda Karimova, PhD(c)",
        "Sevda Kərimova, PhD(m)",
        "Legal scholar specializing in bioethics, medical law, and criminal law. Former ethics consultant at TABİB; visiting fellow at Ruhr University Bochum; lecturer on bioethics and medical law.",
        "Bioetika, tibb hüququ və cinayət hüququ üzrə ixtisaslaşmış hüquqşünas. TABİB-də keçmiş etika məsləhətçisi; Ruhr Universitetində visiting fellow; bioetika və tibb hüququ müəllimi.",
        "sevda-kerimova.png",
        "Sevda Karimova",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Sevda Karimova (born 28 February 1993) holds a bachelor&#8217;s degree in law from Nakhchivan State University (honors), a master&#8217;s in transnational criminal law from Baku State University (English section, state scholarship), and is PhD candidate in bioethics and criminal law (Institute of Law and Human Rights, ANAS; transferred to BSU). Yale Interdisciplinary Center for Bioethics summer institute (2020). Visiting fellow at Ruhr University Bochum Institute for Medical Ethics (2023). Former senior specialist and ethics consultant at TABİB; law lecturer at Sabah Center and BSU UNESCO Chair. General manager of Azerbaijan Science Association NGO. Medical law consultant at Vice Versa Consulting. Thesis: <em>Bioethical aspects of the right to life and health in criminal law</em>.", "Sevda Kərimova (1993-cü il 28 fevral) Naxçıvan Dövlət Universitetində bakalavr (fərqlənmə), Bakı Dövlət Universitetində magistr (transmilli cinayət hüququ, dövlət təqaüdü), bioetika və cinayət hüququ üzrə PhD(m) (AEİ Hüquq və İnsan Hüquqları İnstitutu; BSU-ya transfer). Yale Bioetika Mərkəzi yay institutu (2020). Ruhr Universiteti Tibb Etikası İnstitutunda visiting fellow (2023). TABİB-də etika məsləhətçisi; Sabah Mərkəzi və BSU UNESCO kafedrasında müəllim. 'Azərbaycan Elm Assosiasiyası' QHT-nin baş direktoru. Vice Versa Consulting-də tibb hüququ məsləhətçisi. Dissertasiya: 'Cinayət hüququnda həyat və sağlamlıq hüququnun bioetik aspektləri'.") + '</div>'
        + '<div class="stats">'
        + stat("PhD(c)", "Bioethics", "Bioetika")
        + stat("TABİB", "2020–2022", "2020–2022")
        + stat("Yale", "2020", "2020")
        + stat("C1", "English", "İngilis dili")
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2023–", "Vice Versa Consulting LTD", "Medical Law Consultant", "Tibb hüququ məsləhətçisi", "Legal consulting in medical law.", "Tibb hüququ üzrə hüquqi məsləhət.")
        + item("2023", "Ruhr University Bochum", "International Visiting Fellow", "Beynəlxalq visiting fellow", "Institute for Medical Ethics and History of Medicine.", "Tibb Etikası və Tarixi İnstitutu.")
        + item("2020–2022", "TABİB", "Ethics Consultant / Senior Legal Specialist", "Etika məsləhətçisi / Baş hüquqşünas", "Established research ethics commissions; COVID-19 and Karabakh war medical service staff.", "Elmi etika komissiyalarının yaradılması; COVID-19 və Karabakh müharibəsi tibbi xidməti.")
        + item("2018–2019", "Hacettepe University Bioethics Center", "International Researcher", "Beynəlxalq tədqiqatçı", "Doctoral courses in law, medicine, and philosophy.", "Hüquq, tibb və fəlsəfə doktorantura kursları.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("2017–2020", "PhD(c), Bioethics & Criminal Law", "PhD(m), Bioetika və cinayət hüququ", "Institute of Law and Human Rights, ANAS / Baku State University.", "AEİ Hüquq və İnsan Hüquqları İnstitutu / BSU.")
        + edu("2014–2016", "Master, Transnational Criminal Law", "Magistr, Transmilli cinayət hüququ", "Baku State University, English section (state scholarship).", "Bakı Dövlət Universiteti, ingilis bölməsi (dövlət təqaüdü).")
        + edu("2009–2014", "Bachelor, Law", "Bakalavr, Hüquq", "Nakhchivan State University (honors diploma).", "Naxçıvan Dövlət Universiteti (fərqlənmə diplomu).")
        + edu("2020", "Yale Bioethics Summer Institute", "Yale Bioetika Yay İnstitutu", "Sherwin B. Nuland Summer Institute (virtual).", "Sherwin B. Nuland Yay İnstitutu (virtual).")
        + "</div>",
    )
    body = h + profile + exp + edu_sec
    html = page("Curriculum Vitae — Sevda Karimova", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Sevda Karimova, PhD(c) &ensp;·&ensp; Curriculum Vitae", "Sevda Kərimova, PhD(m) &ensp;·&ensp; Tərcümeyi-hal"),
    )


def build_ilham_akhundov() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Ph.D. in Mathematics", "Riyaziyyat üzrə PhD")
        + rank_item("Affiliation", "Əlaqə", "University of Waterloo", "Vaterloo Universiteti")
        + rank_item("E-mail", "E-poçt", "iakhundo@uwaterloo.ca", "iakhundo@uwaterloo.ca")
        + rank_item("Location", "Yer", "Waterloo, Ontario, Canada", "Vaterloo, Ontario, Kanada")
    )
    h = hero(
        "Ilham Akhundov, Ph.D.",
        "İlham Axundov, Ph.D.",
        "Director of Undergraduate Mathematics Business and Accounting Programs, University of Waterloo. Probability theorist and statistician; former Fulbright professor at Texas A&amp;M and faculty at McMaster University.",
        "Vaterloo Universitetində riyaziyyat, biznes və mühasibat proqramları direktoru. Ehtimal nəzəriyyəçisi və statistik; Texas A&amp;M Fulbright professoru; McMaster Universitetində keçmiş fakültə üzvü.",
        "ilham-axundov.png",
        "Ilham Akhundov",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Dr. Ilham Akhundov holds a Ph.D. in Mathematics (Probability Theory and Mathematical Statistics, St. Petersburg University, 1988) and B.Sc. in Mathematics (1981). Since 2013 Director of Undergraduate Mathematics Business and Accounting Programs at University of Waterloo (3000+ students): hiring, budgeting, strategic planning, and program development. Former Deputy Director Academic at UW UAE Campus (2009–2013). Research in asymptotic probability, order statistics, records, extreme value theory, and distribution characterizations. Author of 24 scientific articles and 3 textbooks; referee for three journals. Progress medal of Azerbaijan (2016); UW highest performance award (2017).", "Dr. İlham Axundov riyaziyyat üzrə PhD (ehtimal nəzəriyyəsi və riyazi statistika, Sankt-Peterburq Universiteti, 1988) və bakalavr (1981) dərəcələrinə malikdir. 2013-dən Vaterloo Universitetində riyaziyyat, biznes və mühasibat proqramları direktoru (3000+ tələbə). 2009–2013 UW BƏƏ kampusunda akademik direktor müavini. Asimptotik ehtimal, sıra statistikası, rekordlar, ekstremal dəyər nəzəriyyəsi tədqiqatları. 24 elmi məqalə və 3 dərs vəsaiti; 3 jurnal üçün rəyçi. 'Tərəqqi' medalı (2016); Vaterloo ən yüksək performans mükafatı (2017).") + '</div>'
        + '<div class="stats">'
        + stat("24", "Articles", "Məqalə")
        + stat("3000+", "Students", "Tələbə")
        + stat("1988", "Ph.D.", "PhD")
        + stat("2013", "Director", "Direktor")
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2013–", "University of Waterloo", "Director, Math Business & Accounting Programs", "Riyaziyyat, biznes və mühasibat proqramları direktoru", "Unit planning, hiring, budget, strategic plans, space management.", "Vahid planlaşdırma, işə qəbul, büdcə, strategiya, məkan idarəetməsi.")
        + item("2009–2013", "University of Waterloo UAE Campus", "Deputy Director Academic", "Akademik direktor müavini", "Executive support, student recruitment, undergraduate committee.", "İcra dəstəyi, tələbə qəbulu, bakalavr komitəsi.")
        + item("2007–2009", "University of Waterloo", "Lecturer, Statistics & Actuarial Science", "Müəllim, Statistika və aktuar elmi", "STAT 231, MATH 116/137/118, ME 202 and related courses.", "STAT 231, MATH 116/137/118, ME 202 və digər kurslar.")
        + item("2000–2007", "McMaster University", "Assistant Professor", "Assistents professor", "Mathematical statistics, linear models, probability courses.", "Riyazi statistika, xətti modellər, ehtimal kursları.")
        + item("1999–2000", "Texas A&M University", "Fulbright Research Professor", "Fulbright tədqiqat professoru", "Research in probability and statistics.", "Ehtimal və statistika tədqiqatları.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("1988", "Ph.D., Mathematics", "PhD, Riyaziyyat", "St. Petersburg University — Probability Theory and Mathematical Statistics.", "Sankt-Peterburq Universiteti — Ehtimal nəzəriyyəsi və riyazi statistika.")
        + edu("1981", "B.Sc., Mathematics", "B.Sc., Riyaziyyat", "St. Petersburg (Leningrad) University.", "Sankt-Peterburq (Leninqrad) Universiteti.")
        + "</div>",
    )
    body = h + profile + exp + edu_sec
    html = page("Curriculum Vitae — Ilham Akhundov", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Ilham Akhundov, Ph.D. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Waterloo, Canada", "İlham Axundov, Ph.D. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Vaterloo, Kanada"),
    )


def build_ilkin_qulusoy() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Associate Professor", "Dosent")
        + rank_item("Affiliation", "Əlaqə", "Kafkas University", "Qafqaz Universiteti")
        + rank_item("E-mail", "E-poçt", "ilkingulusoy@gmail.com", "ilkingulusoy@gmail.com")
        + rank_item("Location", "Yer", "Kars, Turkey", "Qars, Türkiyə")
    )
    h = hero(
        "Ilkin Gulusoy, Assoc. Prof.",
        "İlkin Gulusoy, dosent",
        "Associate Professor and head of Contemporary Turkic Dialects and Literatures (Azerbaijani Turkish and Literature) at Kafkas University. Turkologist, author of 12 books and organizer of major international conferences.",
        "Qafqaz Universitetində Çağdaş Türk Ləhcələri və Ədəbiyyatları (Azərbaycan türkcəsi və ədəbiyyatı) bölməsinin dosenti və rəhbəri. Türkoloq; 12 kitabın müəllifi; beynəlxalq konfransların təşkilatçısı.",
        "ilkin-qulusoy.png",
        "Ilkin Gulusoy",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Assoc. Prof. Ilkin Gulusoy earned his Ph.D. (2008) from Baku Slavic University on the syntax of Kadı Burhaneddin&#8217;s language; master&#8217;s (2003) and bachelor&#8217;s (2001) from Baku State University. Since 2019 Associate Professor at Kafkas University, Faculty of Arts and Sciences, Contemporary Turkic Dialects and Literatures department — the only 4-year program in Turkey training Azerbaijani language specialists. Founded master&#8217;s program (2014); ~60 graduates. Author of 12 books; 27 articles in indexed journals; scientific editor of 60+ books; 70+ conference presentations. Supervised 10 master theses. Organized 10+ international conferences including events for Heydar Aliyev centenary and Nakhchivan 100th anniversary.", "Dos. İlkin Gulusoy Bakı Slavyan Universitetində PhD (2008, Kadı Burhaneddin dilinin sintaksisi); BSU magistr (2003) və bakalavr (2001). 2019-dan Qafqaz Universitetində Çağdaş Türk Ləhcələri və Ədəbiyyatları bölməsində dosent — Türkiyədə Azərbaycan dili mütəxəssisi yetişdirən yeganə 4 illik bölüm. 2014-dən magistratura şöbəsi; ~60 məzun. 12 kitab; indekslənən jurnallarda 27 məqalə; 60+ kitabın elmi redaktoru; 70+ konfrans məruzəsi. 10 magistr dissertasiyasına rəhbərlik. Heydər Əliyev centenari və Naxçıvan 100 illiyi çərçivəsində 10+ beynəlxalq konfrans.") + '</div>'
        + '<div class="stats">'
        + stat("12", "Books", "Kitab")
        + stat("27", "Articles", "Məqalə")
        + stat("~60", "Master Graduates", "Magistr məzunu")
        + stat("70+", "Conferences", "Konfrans")
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2019–", "Kafkas University", "Associate Professor; Department Head", "Dosent; Bölmə rəhbəri", "Contemporary Turkic Dialects and Literatures — Azerbaijani Turkish and Literature.", "Çağdaş Türk Ləhcələri və Ədəbiyyatları — Azərbaycan türkcəsi və ədəbiyyatı.")
        + item("2012–2019", "Kafkas University / Baku Slavic Univ.", "Assistant Professor / Visiting Faculty", "Doktor öğretim üyesi / Qonaq müəllim", "Turkology and Azerbaijani language and literature.", "Türkologiya, Azərbaycan dili və ədəbiyyatı.")
        + item("2005–2012", "Baku Slavic University", "Teaching Assistant to Assistant Professor", "Araşdırma görevlisindən müəllimə", "Turkology department teaching and research.", "Türkoloji şöbədə tədris və tədqiqat.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("2008", "Ph.D., Contemporary Turkic Dialects", "PhD, Çağdaş türk ləhcələri", "Baku Slavic University. Thesis: Syntax of Kadı Burhaneddin&#8217;s language.", "Bakı Slavyan Universiteti. Tez: Kadı Burhaneddin dilinin sintaksisi.")
        + edu("2003", "Master, Azerbaijani Literature", "Magistr, Azərbaycan ədəbiyyatı", "Baku State University. Thesis on Fuzuli&#8217;s rubais.", "Bakı Dövlət Universiteti. Füzuli rubailəri.")
        + edu("2001", "Bachelor, Azerbaijani Language & Literature", "Bakalavr, Azərbaycan dili və ədəbiyyatı", "Baku State University.", "Bakı Dövlət Universiteti.")
        + "</div>",
    )
    body = h + profile + exp + edu_sec
    html = page("Curriculum Vitae — Ilkin Gulusoy", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Ilkin Gulusoy, Assoc. Prof. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Kars, Turkey", "İlkin Gulusoy, dosent &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Qars, Türkiyə"),
    )


def build_hacali_necefoglu() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Professor — Inorganic Chemistry", "Professor — Qeyri-üzvi kimya")
        + rank_item("Affiliation", "Əlaqə", "Kafkas University", "Qafqaz Universiteti")
        + rank_item("E-mail", "E-poçt", "alinecef@hotmail.com", "alinecef@hotmail.com")
        + rank_item("Location", "Yer", "Kars, Turkey", "Qars, Türkiyə")
    )
    h = hero(
        "Hacali Necefoğlu, Prof.",
        "Hacalı Nəcəfoğlu, prof.",
        "Professor of inorganic chemistry at Kafkas University. Head of External Relations, Caucasus and Central Asia Research Center, and Department of Inorganic Chemistry. 200+ WoS/Scopus articles; H-index 20 (WoS).",
        "Qafqaz Universitetində qeyri-üzvi kimya professoru. Xarici əlaqələr, Qafqaz və Orta Asiya Araşdırma Mərkəzi və Qeyri-üzvi kimya kafedrasının rəhbəri. 200+ WoS/Scopus məqalə; H-indeks 20 (WoS).",
        "hacali-necefoglu.png",
        "Hacali Necefoğlu",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Prof. Hacali Necefoğlu (born 13 February 1955) earned B.Sc. in chemistry (1977) and Ph.D. in inorganic chemistry (1982) at Azerbaijan State University / Azerbaijan Academy of Sciences. Academic ranks at Kafkas University: assistant professor (1995), associate professor (1997), professor (2003). Research on synthesis and characterization of metal carboxylate complexes with nicotinamide and related ligands — crystallography, thermal analysis, biological properties. 200+ articles in WoS/Scopus journals; H-index 20 (WoS); supervised 11 PhD and 19 MSc theses. Two patents (1988). 104 international conference presentations. Also author of 3 humanities books and editor of 7 books.", "Prof. Hacalı Nəcəfoğlu (1955-ci il 13 fevral) ADU/AEA-də kimya bakalavrı (1977) və anorganik kimya doktorluğu (1982). Qafqaz Universitetində yrd. dosent (1995), dosent (1997), professor (2003). Nikotinamid və metal karboksilat komplekslərinin sintezi və xarakterizasiyası — kristalloqrafiya, termik analiz, bioloji xüsusiyyətlər. WoS/Scopus-da 200+ məqalə; H-indeks 20; 11 PhD və 19 magistr rəhbərliyi. 2 patent (1988); 104 beynəlxalq konfrans. Humanitar sahədə 3 kitab, 7 kitab redaktoru.") + '</div>'
        + '<div class="stats">'
        + stat("200+", "WoS/Scopus Articles", "WoS/Scopus məqalə")
        + stat("H-20", "WoS H-index", "WoS H-indeks")
        + stat("11+19", "PhD + MSc Supervised", "PhD + magistr")
        + stat("2003", "Professor", "Professor")
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2003–", "Kafkas University", "Professor; Department Head; Center Director", "Professor; Kafedra müdiri; Mərkəz direktoru", "Inorganic Chemistry department; External Relations; Caucasus & Central Asia Research Center.", "Qeyri-üzvi kimya kafedrası; Xarici əlaqələr; Qafqaz və Orta Asiya Araşdırma Mərkəzi.")
        + item("1995–2003", "Kafkas University", "Assistant to Associate Professor", "Yrd. dosentdən dosentə", "Inorganic chemistry teaching and research.", "Anorganik kimya tədrisi və tədqiqatı.")
        + item("1977–1995", "Azerbaijan AS / ADU / Atatürk Univ.", "Researcher to Lecturer", "Tədqiqatçıdan müəllimə", "Laboratory and academic positions in Baku and Erzurum.", "Bakı və Erzurumda laboratoriya və akademik vəzifələr.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("1982", "Ph.D., Inorganic Chemistry", "PhD, Anorganik kimya", "Azerbaijan Academy of Sciences.", "Azərbaycan Elmlər Akademiyası.")
        + edu("1977", "B.Sc. & M.Sc., Chemistry", "Bakalavr və magistr, Kimya", "Azerbaijan State University — chemist; organic chemistry.", "Azərbaycan Dövlət Universiteti — kimyaçı; organik kimya.")
        + "</div>",
    )
    body = h + profile + exp + edu_sec
    html = page("Curriculum Vitae — Hacali Necefoğlu", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Hacali Necefoğlu, Prof. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Kars, Turkey", "Hacalı Nəcəfoğlu, prof. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; Qars, Türkiyə"),
    )


def build_ismixan_bayramov() -> str:
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Prof. Dr. — Statistics", "Prof. dr. — Statistika")
        + rank_item("Affiliation", "Əlaqə", "Izmir University of Economics", "İzmir İqtisad Universiteti")
        + rank_item("E-mail", "E-poçt", "ismihan.bayramoglu@ieu.edu.tr", "ismihan.bayramoglu@ieu.edu.tr")
        + rank_item("Location", "Yer", "Izmir, Turkey", "İzmir, Türkiyə")
    )
    h = hero(
        "Ismihan Bayramoglu, Prof. Dr.",
        "İsmixan Bayramov, prof. dr.",
        "Professor of probability and statistics at Izmir University of Economics. Founding dean of Faculty of Arts and Sciences (2001–2022); Editor-in-Chief of ISTATISTIK; 120+ SCI publications; supervisor of 17+ PhD graduates.",
        "İzmir İqtisad Universitetində ehtimal və statistika professoru. Elmlər fakültəsinin qurucu dekanı (2001–2022); ISTATISTIK jurnalının baş redaktoru; 120+ SCI nəşr; 17+ PhD məzunu rəhbərliyi.",
        "ismixan-bayramov.png",
        "Ismihan Bayramoglu",
        ranks,
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class=\"callout\">' + bib("Prof. Ismihan Bayramoglu (Bairamov) holds Ph.D. (1988, Kiev State University, cybernetics) on invariant confidence intervals. BSc/MSc (1981, Azerbaijan State University). Work at Azerbaijan Aerospace Agency (1983–1993), Ankara University (1993–2001), and Izmir University of Economics since 2001 — dean of Faculty of Arts and Sciences (2001–2022), chair of Mathematics (2001–2015). Research: probability, statistics, stochastic processes, record theory, copulas, reliability. 120+ articles (75+ in SCI/SCI-E); 3 international books; associate editor of Communications in Statistics journals; Editor-in-Chief of ISTATISTIK. Ankara University Scientific Prize (2000–2001). Supervised 17+ PhD students. ORCID: 0000-0002-8575-8405.", "Prof. İsmixan Bayramoğlu (Bairamov) PhD (1988, Kiyev DU, kibernetika) — invariant etibar intervalları. Bakalavr/magistr (1981, ADU). Azərbaycana Aerokosmik Agentlik (1983–1993), Ankara Universiteti (1993–2001), 2001-dən İzmir İqtisad Universiteti — Elmlər fakültəsi dekanı (2001–2022), Riyaziyyat kafedrası müdiri (2001–2015). Tədqiqat: ehtimal, statistika, stokastik proseslər, rekord nəzəriyyəsi, kopula, etibarlılıq. 120+ məqalə (75+ SCI/SCI-E); 3 beynəlxalq kitab; Communications in Statistics redaktoru; ISTATISTIK baş redaktoru. Ankara Universiteti elmi mükafatı (2000–2001). 17+ PhD rəhbərliyi.") + '</div>'
        + '<div class="stats">'
        + stat("120+", "Publications", "Nəşr")
        + stat("75+", "SCI Articles", "SCI məqalə")
        + stat("17+", "PhD Supervised", "PhD rəhbərliyi")
        + stat("2001–22", "Dean", "Dekan")
        + "</div>",
    )
    comp_sec = section(
        "Core Competencies",
        "Əsas kompetensiyalar",
        '<div class="competency-grid">'
        + comp("Probability & Statistics", "Ehtimal və statistika", [
            ("Order statistics and record theory", "Sıra statistikası və rekord nəzəriyyəsi"),
            ("Copulas and multivariate dependence", "Kopula və çoxölçülü asılılıq"),
            ("Nonparametric statistics", "Qeyriparametrik statistika"),
        ])
        + comp("Reliability Engineering", "Etibarlılıq mühəndisliyi", [
            ("System reliability and shock models", "Sistem etibarlılığı və şok modelləri"),
            ("Marshall-Olkin distributions", "Marshall-Olkin paylanmaları"),
        ])
        + comp("Editorial Leadership", "Redaksiya liderliyi", [
            ("Editor-in-Chief, ISTATISTIK", "ISTATISTIK baş redaktoru"),
            ("Associate Editor, Taylor & Francis journals", "Taylor & Francis jurnalları redaktoru"),
        ])
        + comp("Academic Administration", "Akademik idarəetmə", [
            ("Founding dean, Faculty of Arts and Sciences", "Elmlər fakültəsinin qurucu dekanı"),
            ("Chair, Mathematics Department", "Riyaziyyat kafedrası müdiri"),
        ])
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2001–", "Izmir University of Economics", "Professor", "Professor", "Faculty of Arts and Sciences; statistics and mathematics teaching.", "Elmlər fakültəsi; statistika və riyaziyyat tədrisi.")
        + item("2001–2022", "Izmir University of Economics", "Dean, Faculty of Arts and Sciences", "Elmlər fakültəsi dekanı", "Founding dean; faculty development and international cooperation.", "Qurucu dekan; fakültə inkişafı və beynəlxalq əməkdaşlıq.")
        + item("2001–2015", "Izmir University of Economics", "Chair, Mathematics Department", "Riyaziyyat kafedrası müdiri", "Department leadership and curriculum.", "Kafedra rəhbərliyi və kurikulum.")
        + item("1993–2001", "Ankara University", "Professor, Statistics", "Professor, Statistika", "Faculty of Science, Department of Statistics.", "Elmlər fakültəsi, Statistika şöbəsi.")
        + item("1983–1993", "Azerbaijan Aerospace Agency / ASU", "Scientist / Lecturer", "Elmi işçi / Müəllim", "Leading scientist at aerospace agency; lecturer at ASU and Petrol Academy.", "Aerokosmik agentlikdə aparıcı elmi işçi; ADU və Neft Akademiyasında müəllim.")
        + "</div>",
    )
    edu_sec = section(
        "Education",
        "Təhsil",
        '<div class="education-grid">'
        + edu("1988", "Ph.D., Computational Mathematics", "PhD, Hesablama riyaziyyatı", "Kiev State University. Dissertation on invariant confidence intervals.", "Kiyev Dövlət Universiteti. İnvariant etibar intervalları.")
        + edu("1981", "BSc/MSc, Applied Mathematics", "Bakalavr/Magistr, Tətbiqi riyaziyyat", "Azerbaijan State University.", "Azərbaycan Dövlət Universiteti.")
        + "</div>",
    )
    pubs = section(
        "Selected Publications",
        "Seçilmiş nəşrlər",
        '<div class="pub-block"><div class="pub-category"><ul>'
        + "<li>Bayramoglu &amp; Stepanov (2024) — asymptotic properties of record spacings. <em>Statistics and Probability Letters</em>.</li>"
        + "<li>Bayramoglu (2022) — fuzzy improved distribution function and order statistics. <em>J. Comput. Appl. Math.</em></li>"
        + "<li>Bayramoglu &amp; Gebizlioglu (2021) — max–min model in bivariate sequences. <em>J. Comput. Appl. Math.</em></li>"
        + "<li>Bayramoglu (2020) — joint distribution and reliability application. <em>Reliability Engineering &amp; System Safety</em>.</li>"
        + "<li>Bayramoglu &amp; Ozkut (2015) — Marshall-Olkin shocks reliability. <em>IEEE Trans. Reliability</em>.</li>"
        + "</ul></div></div>",
    )
    body = h + profile + comp_sec + exp + edu_sec + pubs
    html = page("Curriculum Vitae — Ismihan Bayramoglu", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi("Ismihan Bayramoglu, Prof. Dr. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Izmir", "İsmixan Bayramov, prof. dr. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; İzmir"),
    )


CV_BUILDERS = {
    "xelil_kelenter.html": build_xelil_kelenter,
    "kamal_akbarov.html": build_kamal_akbarov,
    "kamran_rustemov.html": build_kamran_rustemov,
    "ismayil_aliyev.html": build_ismayil_aliyev,
    "sevda_kerimova.html": build_sevda_kerimova,
    "ilham_akhundov.html": build_ilham_akhundov,
    "ilkin_qulusoy.html": build_ilkin_qulusoy,
    "hacali_necefoglu.html": build_hacali_necefoglu,
    "ismixan_bayramov.html": build_ismixan_bayramov,
}


if __name__ == "__main__":
    for fname, builder in CV_BUILDERS.items():
        out = CV_DIR / fname
        out.write_text(builder(), encoding="utf-8")
        print(f"Wrote {out} ({out.stat().st_size} bytes)")

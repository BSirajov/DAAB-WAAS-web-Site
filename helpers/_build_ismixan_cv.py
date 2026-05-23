# -*- coding: utf-8 -*-
from pathlib import Path
import re
import importlib.util

ROOT = Path(r"c:\Users\BSira\Documents\GitHub\DAAB-WAAS web site")
spec = importlib.util.spec_from_file_location("batch", ROOT / "helpers" / "_build_batch_cvs.py")
batch = importlib.util.module_from_spec(spec)
spec.loader.exec_module(batch)

bi = batch.bi
bib = batch.bib
rank_item = batch.rank_item
stat = batch.stat
comp = batch.comp
item = batch.item
edu = batch.edu
hero = batch.hero
section = batch.section
page = batch.page

def build():
    ranks = (
        rank_item("Academic Rank", "Akademik rütbə", "Prof. Dr. — Statistics", "Prof. dr. — Statistika")
        + rank_item("Affiliation", "Əlaqə", "Izmir University of Economics", "İzmir İqtisad Universiteti")
        + rank_item("E-mail", "E-poçt", "ismihan.bayramoglu@ieu.edu.tr", "ismihan.bayramoglu@ieu.edu.tr")
        + rank_item("Location", "Yer", "Izmir, Turkey", "İzmir, Türkiyə")
    )
    h = hero(
        "Ismihan Bayramoglu, Prof. Dr.",
        "İsmixan Bayramov, prof. dr.",
        "Professor of probability and statistics at Izmir University of Economics (born 1959). Founding dean of Faculty of Arts and Sciences (2001–2022); ISI Fellow (1999); Editor-in-Chief of ISTATISTIK; 68+ WoS articles; Google Scholar h-index 21.",
        "İzmir İqtisad Universitetində ehtimal və statistika professoru (1959-cu il təv.). Elmlər fakültəsinin qurucu dekanı (2001–2022); ISI Fellow (1999); ISTATISTIK baş redaktoru; 68+ WoS məqalə; Google Scholar h-indeks 21.",
        "ismixan-bayramov.png",
        "Ismihan Bayramoglu",
        ranks,
    )
    prof_en = (
        "Prof. Ismihan Bayramoglu (Bairamov, born 1959) earned BSc/MSc in Applied Mathematics (1981, Azerbaijan State University) "
        "and Ph.D. (1988, Kiev State University) on invariant confidence intervals and training-sample statistical criteria. "
        "Academic ranks: assistant professor (1988, Azerbaijan Academy of Sciences), associate professor (1992), professor (1999, Ankara University). "
        "Career at Azerbaijan Academy Cybernetics and Space Research institutes (1981–1993), Ankara University Faculty of Science Statistics (1993–2001), "
        "and Izmir University of Economics since 2001 — founding dean of Faculty of Arts and Sciences (Sep 2001–Apr 2022), Mathematics department chair (2001–2015). "
        "Research: probability, statistics, order statistics, record theory, copulas, reliability engineering. "
        "68+ articles in Web of Science journals; Google Scholar: 1625+ citations, h-index 21, i10-index 43. "
        "Elected Fellow of the International Statistical Institute (1999). Ankara University Science Prize (2001). "
        "Supervised 10 master&#8217;s and 17 doctoral theses. TÜBİTAK project 109T675 on stress-strength reliability models."
    )
    prof_az = (
        "Prof. İsmixan Bayramoğlu (Bairamov, 1959-cu il təv.) ADU-da tətbiqi riyaziyyat bakalavr/magistr (1981), "
        "Kiyev DU-da PhD (1988) — invariant etibar intervalları və təlim nümunələrinə əsaslanan statistik meyarlar. "
        "Akademik unvanlar: yrd. dosent (1988, AEA), dosent (1992), professor (1999, Ankara Universiteti). "
        "AEA Kibernetika və Kosmik Tədqiqat institutları (1981–1993), Ankara Universiteti Statistika (1993–2001), "
        "2001-dən İzmir İqtisad Universiteti — Elmlər fakültəsi qurucu dekanı (2001 sentyabr–2022 aprel), Riyaziyyat bölüm başkanı (2001–2015). "
        "Tədqiqat: ehtimal, statistika, sıra statistikası, rekord nəzəriyyəsi, kopula, etibarlılıq mühəndisliyi. "
        "Web of Science-da 68+ məqalə; Google Scholar: 1625+ sitat, h-indeks 21, i10-indeks 43. "
        "Beynəlxalq Statistika İnstitutunun seçilmiş üzvü (Fellow, 1999). Ankara Universiteti Elmi Mükafatı (2001). "
        "10 magistr və 17 doktora tezisinə rəhbərlik. TÜBİTAK 109T675 layihəsi."
    )
    profile = section(
        "Academic Profile",
        "Akademik profil",
        '<div class="callout">' + bib(prof_en, prof_az) + '</div>'
        + '<div class="stats">'
        + stat("68+", "WoS Articles", "WoS məqalə")
        + stat("h-21", "Google Scholar", "Google Scholar")
        + stat("17", "PhD Theses", "PhD tezisi")
        + stat("1999", "ISI Fellow", "ISI Fellow")
        + "</div>",
    )
    comp_sec = section(
        "Core Competencies",
        "Əsas kompetensiyalar",
        '<div class="competency-grid">'
        + comp("Research Areas", "Tədqiqat sahələri", [
            ("Order statistics, records, exceedances", "Sıra statistikası, rekordlar, aşmalar"),
            ("Copulas and multivariate dependence", "Kopula və çoxölçülü asılılıq"),
            ("Reliability and survival analysis", "Etibarlılıq və sağ qalma analizi"),
        ])
        + comp("Editorial Roles", "Redaksiya rolları", [
            ("Editor-in-Chief, ISTATISTIK", "ISTATISTIK baş redaktoru"),
            ("Associate Editor, Communications in Statistics (Taylor & Francis)", "Communications in Statistics redaktoru"),
            ("Guest editor, special issues (Comm. Stat.; J. Comput. Appl. Math.)", "Xüsusi say redaktoru"),
        ])
        + comp("Teaching", "Tədris", [
            ("Probability Theory I & II", "Olasılık Teorisi I və II"),
            ("Stochastic Processes; Statistical Theory", "Stokastik Süreçler; İstatistik Teorisi"),
            ("Probabilistic System Analysis (graduate)", "Olasılıksal Sistem Analizi (magistr)"),
        ])
        + comp("Memberships & Honors", "Üzvlük və mükafatlar", [
            ("International Statistical Institute Fellow (1999)", "ISI Fellow (1999)"),
            ("Ankara University Science Prize (2001)", "Ankara Universiteti Elmi Mükafatı (2001)"),
            ("Plenary/keynote speaker at international conferences", "Beynəlxalq konfrans plenary/keynote məruzəçisi"),
        ])
        + "</div>",
    )
    exp = section(
        "Professional Experience",
        "Peşəkar fəaliyyət",
        '<div class="timeline">'
        + item("2001–", "Izmir University of Economics", "Professor, Faculty of Arts and Sciences", "Professor, Elmlər fakültəsi", "Mathematics department; undergraduate and graduate statistics.", "Riyaziyyat bölümü; bakalavr və magistr statistika.")
        + item("2001–2022", "Izmir University of Economics", "Dean, Faculty of Arts and Sciences", "Elmlər fakültəsi dekanı", "Founding dean (Sep 2001 – Apr 2022).", "Qurucu dekan (2001 sentyabr – 2022 aprel).")
        + item("2001–2015", "Izmir University of Economics", "Chair, Mathematics Department", "Matematik Bölüm Başkanı", "Department leadership and curriculum development.", "Bölüm rəhbərliyi və kurikulum.")
        + item("1999–2001", "Ankara University", "Professor (Turkish citizen)", "Professor (T.C. vətəndaşı)", "Faculty of Science, Department of Statistics.", "Fen Fakültesi, İstatistik Bölümü.")
        + item("1993–1999", "Ankara University", "Foreign Faculty Member", "Yabancı uyruklu öğretim üyesi", "Faculty of Science, Statistics.", "Fen Fakültesi, İstatistik.")
        + item("1988–1993", "Azerbaijan Space Research Institute / ASU", "Senior Scientist, Assoc. Prof.", "Baş bilim uzmanı, dosent", "Leading scientist; part-time lecturer at ASU and Petroleum Academy.", "Aparıcı elmi işçi; ADU və Neft Akademiyasında yarımştat.")
        + item("1983–1988", "Azerbaijan Space Research Institute", "Scientist / Asst. Prof.", "Bilim uzmanı / yrd. dosent", "Space research and applied mathematics.", "Kosmik tədqiqat və tətbiqi riyaziyyat.")
        + item("1981–1983", "Azerbaijan Academy of Sciences, Cybernetics Institute", "Researcher", "Araştırmacı", "Early research career in cybernetics.", "Kibernetika üzrə erkən tədqiqat.")
        + "</div>",
    )
    edu_sec = section(
        "Education & Academic Ranks",
        "Təhsil və akademik unvanlar",
        '<div class="education-grid">'
        + edu("1988", "Ph.D., Applied Mathematics", "PhD, Tətbiqi riyaziyyat", "Kiev State University. Invariant confidence intervals.", "Kiyev Dövlət Universiteti. İnvariant etibar intervalları.")
        + edu("1981", "BSc/MSc, Applied Mathematics", "Bakalavr/Magistr, Tətbiqi riyaziyyat", "Azerbaijan State University.", "Azərbaycan Dövlət Universiteti.")
        + edu("1999", "Professor", "Professor", "Ankara University (as Turkish citizen).", "Ankara Universiteti (T.C. vətəndaşı).")
        + edu("1992", "Associate Professor", "Dosent", "Azerbaijan Academy of Sciences, Baku.", "Azərbaycan Elmlər Akademiyası, Bakı.")
        + "</div>",
    )
    sup = section(
        "Supervised Theses",
        "Rəhbərlik edilmiş tezislər",
        '<div class="callout">'
        + bib(
            "<strong>10 master&#8217;s theses</strong> (Ankara, Ege, Izmir University of Economics) and <strong>17 doctoral theses</strong> "
            "(Ankara, Dokuz Eylül, Ege, Izmir University of Economics) in order statistics, record theory, copulas, reliability, "
            "and exceedance statistics. Notable graduates include Prof. Serkan Eryilmaz, Prof. Suleyman Gurler, and Dr. Gizem Kemalbay.",
            "<strong>10 magistr</strong> (Ankara, Ege, İzmir İqtisad Universiteti) və <strong>17 doktora</strong> "
            "(Ankara, Dokuz Eylül, Ege, İzmir İqtisad Universiteti) tezisinə rəhbərlik — sıra statistikası, rekord nəzəriyyəsi, "
            "kopula, etibarlılıq və aşma statistikası. Məzunlar arasında Prof. Serkan Eryılmaz, Prof. Suleyman Gürler, Dr. Gizem Kemalbay."
        )
        + "</div>",
    )
    visits = section(
        "International Research Visits",
        "Beynəlxalq tədqiqat səfərləri",
        '<div class="callout">'
        + bib(
            "Rider University, NJ & George Washington University (Feb 1997); McMaster University, Canada (Jul–Sep 2002, Aug 2004); "
            "Illinois State University, USA (May 2014); KU Leuven, Belgium (Jan–Feb 2024). "
            "Invited/plenary speaker at conferences across Europe, North America, and Asia.",
            "Rider Universiteti və Corctaun Universiteti (1997 fevral); McMaster Universiteti, Kanada (2002, 2004); "
            "Illinois Dövlət Universiteti, ABŞ (2014 may); KU Leuven, Belçika (2024 yanvar–fevral). "
            "Avropa, Şimali Amerika və Asiyada dəvətli/plenary məruzəçi."
        )
        + "</div>",
    )
    pubs = section(
        "Selected Publications",
        "Seçilmiş nəşrlər",
        '<div class="pub-block"><div class="pub-category"><ul>'
        + "<li>Bayramoglu &amp; Stepanov (2024). Asymptotic properties of record spacings. <em>Statistics and Probability Letters</em>, 208, 110052.</li>"
        + "<li>Erem &amp; Bayramoglu (2023). A consistent statistical test based on bivariate random samples. <em>Hacettepe J. Math. Stat.</em>, 52(1), 209–228.</li>"
        + "<li>Bayramoglu (2022). Fuzzy improved distribution function and order statistics. <em>J. Comput. Appl. Math.</em>, 411.</li>"
        + "<li>Bayramoglu &amp; Gebizlioglu (2021). A max–min model in bivariate random sequences. <em>J. Comput. Appl. Math.</em>, 388, 113304.</li>"
        + "<li>Bayramoglu (2020). Joint distribution of a random sample and an order statistic. <em>Reliability Engineering &amp; System Safety</em>, 193, 106594.</li>"
        + "<li>Bayramoglu &amp; Ozkut (2015). Reliability of coherent systems under Marshall-Olkin shocks. <em>IEEE Trans. Reliability</em>, 64(1), 435–443.</li>"
        + "<li>Bairamov (2013). Reliability and MRL of complex systems. <em>IEEE Trans. Reliability</em>, 62, 276–285.</li>"
        + "<li>Bairamov &amp; Kotz (2003). New measure of linear local dependence. <em>Statistics</em>, 37(3), 243–258.</li>"
        + "</ul></div>"
        + '<div class="callout" style="margin-top:12px;">'
        + bib(
            "ORCID: 0000-0002-8575-8405 · Google Scholar · Publons · Academia.edu",
            "ORCID: 0000-0002-8575-8405 · Google Scholar · Publons · Academia.edu"
        )
        + "</div></div>",
    )
    body = h + profile + comp_sec + exp + edu_sec + sup + visits + pubs
    html = page("Curriculum Vitae — Ismihan Bayramoglu", body)
    return html.replace(
        "FOOTER_PLACEHOLDER",
        bi(
            "Ismihan Bayramoglu, Prof. Dr. &ensp;·&ensp; Curriculum Vitae &ensp;·&ensp; Izmir",
            "İsmixan Bayramov, prof. dr. &ensp;·&ensp; Tərcümeyi-hal &ensp;·&ensp; İzmir",
        ),
    )

out = ROOT / "cv" / "ismixan_bayramov.html"
out.write_text(build(), encoding="utf-8")
print(f"Wrote {out} ({out.stat().st_size} bytes)")

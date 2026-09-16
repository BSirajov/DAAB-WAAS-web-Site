"""Bilingual body for the informatics topic guide pages.

Authoritative source: documents/Popular_Topics_in_Informatics_Integrated_AZ.docx
"""
from __future__ import annotations

from html import escape as esc


def T(lang: str, az: str, en: str) -> str:
    return az if lang == "az" else en


def p(text: str) -> str:
    return f"<p>{text}</p>"


def note(text: str, kind: str = "") -> str:
    cls = "cta-note" + (f" cta-note--{kind}" if kind else "")
    return f'<p class="{cls}">{text}</p>'


def bullets(items: list[str]) -> str:
    return "<ul>" + "".join(f"<li>{item}</li>" for item in items) + "</ul>"


def numbered_text(items: list[str]) -> str:
    return "<ol>" + "".join(f"<li>{item}</li>" for item in items) + "</ol>"


def topic_ol(items: list[tuple[str, str]]) -> str:
    lis = "".join(f'<li><a href="#{sid}">{esc(title)}</a></li>' for sid, title in items)
    return f'<ol class="cta-topic-list">{lis}</ol>'


def group(sid: str, title: str) -> str:
    return f'<section class="cta-sub" id="{sid}"><h3>{esc(title)}</h3></section>'


def term(
    lang: str,
    title: str,
    body: str,
    examples: list[str] | None = None,
    sid: str | None = None,
    num: int | None = None,
) -> str:
    heading = f"{num}. {title}" if num is not None else title
    id_attr = f' id="{sid}"' if sid else ""
    parts = [
        f'<section class="cta-sub"{id_attr}>',
        f"<h3>{esc(heading)}</h3>",
        f"<p>{body}</p>",
    ]
    label = T(lang, "Nümunə.", "Example.")
    extra = T(lang, "Başqa nümunə.", "Another example.")
    for i, example in enumerate(examples or []):
        parts.append(
            f'<p class="cta-example"><strong>{label if i == 0 else extra}</strong> {example}</p>'
        )
    parts.append("</section>")
    return "\n".join(parts)


def table(
    headers: list[str],
    rows: list[list[str]],
    compact: bool = False,
    table_id: str = "",
) -> str:
    cls = "cta-table cta-table--compact" if compact else "cta-table"
    tid = f' data-daab-resize-id="{esc(table_id)}"' if table_id else ""
    head = "".join(
        f'<th scope="col" class="col-c{i}">{h}</th>' for i, h in enumerate(headers, 1)
    )
    body = "".join("<tr>" + "".join(f"<td>{c}</td>" for c in row) + "</tr>" for row in rows)
    return (
        f'<div class="cta-table-wrap" tabindex="0">'
        f'<table class="{cls}" data-daab-resizable-table="1"{tid}>'
        f"<thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>"
    )


def code_block(lines: list[str]) -> str:
    return f'<pre class="cta-code"><code>{esc(chr(10).join(lines))}</code></pre>'


TOC = [
    ("about", {"en": "How to use this guide", "az": "Bələdçidən istifadə"}, None),
    ("differences", {"en": "Where the sources differ", "az": "Mənbələr arasındakı fərqlər"}, None),
    (
        "sources",
        {"en": "Evidence behind the topics", "az": "Mövzu seçiminin əsaslandığı mənbələr"},
        [
            ("sources-csta", {"en": "CSTA school standards", "az": "CSTA məktəb standartları"}),
            ("sources-cs2023", {"en": "CS2023 university guidance", "az": "CS2023 universitet tövsiyələri"}),
            ("sources-ap", {"en": "AP Computer Science Principles", "az": "AP Computer Science Principles"}),
            ("sources-surveys", {"en": "Stack Overflow and GitHub", "az": "Stack Overflow və GitHub"}),
            ("sources-research", {"en": "Learning research", "az": "Öyrənmə tədqiqatları"}),
        ],
    ),
    ("priority", {"en": "Thirty recommended topics", "az": "Tövsiyə olunan 30 əsas mövzu"}, None),
    (
        "school",
        {"en": "For school learners", "az": "Məktəblilər və orta məktəb şagirdləri üçün"},
        [
            ("school-thinking", {"en": "Thinking like a computer", "az": "Kompüter kimi düşünmək"}),
            ("school-code", {"en": "First programs", "az": "İlk proqramlar"}),
            ("school-data", {"en": "How computers store information", "az": "Kompüterlər məlumatı necə saxlayır"}),
            ("school-net", {"en": "Networks and safety", "az": "Şəbəkələr və təhlükəsizlik"}),
            ("school-ai", {"en": "AI and data", "az": "Süni intellekt və verilənlər"}),
            ("school-make", {"en": "Making things", "az": "Nəsə qurmaq"}),
            ("school-society", {"en": "Computing and society", "az": "Hesablama və cəmiyyət"}),
        ],
    ),
    (
        "university",
        {"en": "For university students", "az": "Universitet tələbələri üçün"},
        [
            ("uni-run", {"en": "How programs run", "az": "Proqramlar necə işləyir"}),
            ("uni-dsa", {"en": "Data structures and algorithms", "az": "Verilənlər strukturları və alqoritmlər"}),
            ("uni-db", {"en": "Data and databases", "az": "Verilənlər və verilənlər bazaları"}),
            ("uni-sys", {"en": "Systems", "az": "Sistemlər"}),
            ("uni-ai", {"en": "Machine learning and large models", "az": "Maşın öyrənməsi və iri modellər"}),
            ("uni-soft", {"en": "Software work", "az": "Proqram işi"}),
            ("uni-theory", {"en": "Theory of computation", "az": "Hesablama nəzəriyyəsi"}),
        ],
    ),
    ("difficult", {"en": "Why these topics are difficult", "az": "Mövzuların öyrənilməsini çətinləşdirən səbəblər"}, None),
    ("first-series", {"en": "A first series of twelve articles", "az": "İlk nəşrlər üçün plan"}, None),
    ("languages", {"en": "Suggested teaching languages", "az": "Tədris üçün tövsiyə olunan dillər"}, None),
    ("proposal", {"en": "Preparing a topic proposal", "az": "Mövzu təklifinin hazırlanması"}, None),
    ("glossary", {"en": "Terms and abbreviations", "az": "Terminlər və ixtisarlar"}, None),
    ("references", {"en": "Sources and references", "az": "Mənbələr və istinadlar"}, None),
    ("related", {"en": "Related competition pages", "az": "Müsabiqənin əlaqəli səhifələri"}, None),
]


PRIORITY_ROWS = [
    ("1", {"en": "Generative AI and large language models", "az": "Generativ süni intellekt və böyük dil modelləri"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("2", {"en": "Algorithms and computational problem-solving", "az": "Alqoritmlər və hesablama vasitəsilə məsələ həlli"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("3", {"en": "Variables, assignment, data types and program state", "az": "Dəyişənlər, mənimsətmə, verilənlərin tipləri və proqramın vəziyyəti"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("4", {"en": "Finding errors, tests and reading error messages", "az": "Səhvlərin tapılması, testlər və xəta mesajlarının oxunması"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("5", {"en": "Cybersecurity, privacy and safe digital behaviour", "az": "Kibertəhlükəsizlik, məxfilik və təhlükəsiz rəqəmsal davranış"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("6", {"en": "Data science, interpreting data and visualisation", "az": "Verilənlər elmi, verilənlərin şərhi və vizuallaşdırılması"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("7", {"en": "Conditions, Boolean logic and decision-making", "az": "Şərtlər, Bul məntiqi və qərarvermə"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "High", "az": "Yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("8", {"en": "Loops, repetition and stopping", "az": "Dövrlər, təkrarlanma və dayanma"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("9", {"en": "Functions, parameters, return values and scope", "az": "Funksiyalar, parametrlər, qaytarılan qiymətlər və görünmə sahəsi"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("10", {"en": "How the Internet and the Web work", "az": "İnternetin və Vebin işləməsi"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("11", {"en": "Machine learning, training data, models and predictions", "az": "Maşın öyrənməsi, təlim verilənləri, modellər və proqnozlar"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("12", {"en": "Data structures and their uses", "az": "Verilənlər strukturları və tətbiqləri"}, {"en": "University", "az": "Universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("13", {"en": "Algorithm efficiency and Big-O", "az": "Alqoritmlərin səmərəliliyi və Big-O"}, {"en": "University", "az": "Universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("14", {"en": "Databases, modelling and SQL", "az": "Verilənlər bazaları, modelləşdirmə və SQL"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("15", {"en": "Object-oriented programming", "az": "Obyektyönlü proqramlaşdırma"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("16", {"en": "Recursion", "az": "Rekursiya"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "Medium–high", "az": "Orta–yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("17", {"en": "Memory, references, pointers, the stack and dynamic memory", "az": "Yaddaş, istinadlar, göstəricilər, stek və dinamik yaddaş"}, {"en": "University", "az": "Universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("18", {"en": "Concurrent, asynchronous and parallel programming", "az": "Eynizamanlı, asinxron və paralel proqramlaşdırma"}, {"en": "University", "az": "Universitet"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("19", {"en": "Binary numbers and digital representation", "az": "İkilik saylar və rəqəmsal məlumatın təqdimatı"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "High", "az": "Yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("20", {"en": "Web programming, APIs and client–server applications", "az": "Veb proqramlaşdırma, API və müştəri–server tətbiqləri"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("21", {"en": "Operating systems, processes, memory and file systems", "az": "Əməliyyat sistemləri, proseslər, yaddaş və fayl sistemləri"}, {"en": "University", "az": "Universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("22", {"en": "Cloud computing, containers and distributed systems", "az": "Bulud hesablaması, konteynerlər və paylanmış sistemlər"}, {"en": "University", "az": "Universitet"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("23", {"en": "Software engineering, Git and collaborative development", "az": "Proqram mühəndisliyi, Git və birgə proqram hazırlama"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("24", {"en": "Computer architecture, the processor, memory and instructions", "az": "Kompüter arxitekturası, prosessor, yaddaş və əmrlər"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "Medium–high", "az": "Orta–yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("25", {"en": "Dynamic programming and designing complex algorithms", "az": "Dinamik proqramlaşdırma və mürəkkəb alqoritmlərin qurulması"}, {"en": "University", "az": "Universitet"}, {"en": "Medium–high", "az": "Orta–yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("26", {"en": "Cryptography, encryption, hashing and digital signatures", "az": "Kriptoqrafiya, şifrələmə, heşləmə və rəqəmsal imzalar"}, {"en": "Upper-secondary and university", "az": "Yuxarı siniflər və universitet"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("27", {"en": "Automata, computability and complexity classes", "az": "Avtomatlar, hesablana bilmə və mürəkkəblik sinifləri"}, {"en": "University", "az": "Universitet"}, {"en": "Medium", "az": "Orta"}, {"en": "Very high", "az": "Çox yüksək"}),
    ("28", {"en": "Ethics, algorithmic bias and the social effects of computing", "az": "Etika, alqoritmik qərəz və hesablamanın sosial təsirləri"}, {"en": "Both groups", "az": "Hər iki qrup"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "High", "az": "Yüksək"}),
    ("29", {"en": "Game development and interactive graphics", "az": "Oyunların hazırlanması və interaktiv qrafika"}, {"en": "School learners and beginners", "az": "Məktəblilər və yeni başlayanlar"}, {"en": "Very high", "az": "Çox yüksək"}, {"en": "Medium–high", "az": "Orta–yüksək"}),
    ("30", {"en": "Robotics, physical computing and the Internet of Things", "az": "Robot texnikası, fiziki hesablama və Əşyaların İnterneti"}, {"en": "School learners and university", "az": "Məktəblilər və universitet"}, {"en": "High", "az": "Yüksək"}, {"en": "High", "az": "Yüksək"}),
]


SCHOOL_LIST = [
    ("school-1", {"az": "Alqoritm nədir — və gündəlik məsələni addımlara necə çevirməli", "en": "What an algorithm is — and how to turn an everyday problem into steps"}),
    ("school-2", {"az": "Bölmə, qanunauyğunluq və abstraksiya", "en": "Decomposition, patterns and abstraction"}),
    ("school-3", {"az": "Dəyişənlər — dəyişən saxlanılan dəyərlər", "en": "Variables as changing stored values"}),
    ("school-4", {"az": "Mənimsətmə ilə riyazi bərabərliyin fərqi", "en": "The difference between assignment and mathematical equality"}),
    ("school-5", {"az": "Şərtlər və Bul ifadələri", "en": "Conditions and Boolean expressions"}),
    ("school-6", {"az": "İç-içə şərtlər və mürəkkəb məntiq", "en": "Nested conditions and compound logic"}),
    ("school-7", {"az": "Dövrlər necə işləyir və sonsuz dövr nədən yaranır", "en": "How loops work and why an infinite loop starts"}),
    ("school-8", {"az": "Funksiya ilə sadəcə nəticə çap edən əmr", "en": "A function versus a command that only prints a result"}),
    ("school-9", {"az": "Təsadüfi kod dəyişmək əvəzinə sistemli sazlama", "en": "Systematic debugging instead of changing code at random"}),
    ("school-10", {"az": "İkilik ədədlər, bit, bayt və onaltılıq yazılış", "en": "Binary numbers, bits, bytes and hexadecimal"}),
    ("school-11", {"az": "Mətn, şəkil, səs və video rəqəmsal necə təqdim olunur", "en": "How text, images, sound and video are represented digitally"}),
    ("school-12", {"az": "İtkili və itkisiz sıxılma", "en": "Lossy and lossless compression"}),
    ("school-13", {"az": "İnternet, Veb və brauzerin fərqi", "en": "The difference between the Internet, the Web and a browser"}),
    ("school-14", {"az": "IP ünvanı, DNS, marşrutlaşdırıcı, paketlər və HTTP", "en": "IP addresses, DNS, routers, packets and HTTP"}),
    ("school-15", {"az": "Parollar, fişinq, zərərli proqram, məxfilik və iki amilli autentifikasiya", "en": "Passwords, phishing, malware, privacy and two-factor authentication"}),
    ("school-16", {"az": "Şifrələmə, heşləmə və rəqəmsal imzalar", "en": "Encryption, hashing and digital signatures"}),
    ("school-17", {"az": "Süni intellekt adi proqramdan nə ilə fərqlənir", "en": "How AI differs from ordinary software"}),
    ("school-18", {"az": "Təlim verilənləri və maşın öyrənməsində nümunələrin rolu", "en": "Training data and the role of examples in machine learning"}),
    ("school-19", {"az": "Süni intellekt niyə hallüsinasiya edir və ya qərəzi təkrarlayır", "en": "Why AI can hallucinate or repeat bias"}),
    ("school-20", {"az": "Süni intellektin verdiyi məlumatı və kodu necə yoxlamalı", "en": "How to check information and code produced by AI"}),
    ("school-21", {"az": "Verilənlərin toplanması, qrafiklər, yanıltıcı təsvir və qərəz", "en": "Collecting data, graphs, misleading pictures and bias"}),
    ("school-22", {"az": "Sayt, oyun, mobil tətbiq və robototexnikanın əsasları", "en": "The basics of websites, games, mobile apps and robotics"}),
    ("school-23", {"az": "Müəllif hüququ, rəqəmsal kimlik, dezinformasiya və məsuliyyətli istifadə", "en": "Copyright, digital identity, disinformation and responsible use"}),
]


UNI_LIST = [
    ("uni-1", {"az": "Proqramın icra modelləri və vəziyyətin izlənməsi", "en": "Program execution models and tracing state"}),
    ("uni-2", {"az": "Əhatə dairəsi, ömür, parametr ötürmə və təxəllüs", "en": "Scope, lifetime, parameter passing and aliasing"}),
    ("uni-3", {"az": "İstinadlar, göstəricilər və yaddaş idarəsi", "en": "References, pointers and memory management"}),
    ("uni-4", {"az": "Rekursiya və rekursiv çağırış steki", "en": "Recursion and the recursive call stack"}),
    ("uni-5", {"az": "Obyekt kimliyi, siniflər, obyektlər, irsiyyət və polimorfizm", "en": "Object identity, classes, objects, inheritance and polymorphism"}),
    ("uni-6", {"az": "Siyahılar, bağlı strukturlar, steklər, növbələr, ağaclar, heap-lər və qraflar", "en": "Lists, linked structures, stacks, queues, trees, heaps and graphs"}),
    ("uni-7", {"az": "Sıralama, axtarış və qraf alqoritmləri", "en": "Sorting, searching and graph algorithms"}),
    ("uni-8", {"az": "Big-O, ən pis hal və yaddaş–vaxt mübadiləsi", "en": "Big-O, worst case and the space–time trade-off"}),
    ("uni-9", {"az": "Acgöz alqoritmlər, böl və həll et, dinamik proqramlaşdırma", "en": "Greedy algorithms, divide and conquer, and dynamic programming"}),
    ("uni-10", {"az": "Relyasion modelləşdirmə, açarlar, birləşmələr və normallaşdırma", "en": "Relational modelling, keys, joins and normalisation"}),
    ("uni-11", {"az": "SQL-də aqreqasiya, alt sorğular və pəncərə funksiyaları", "en": "Aggregation, subqueries and window functions in SQL"}),
    ("uni-12", {"az": "Tranzaksiyalar, izolyasiya, kilidləmə və verilənlər bazasının uyğunluğu", "en": "Transactions, isolation, locking and database consistency"}),
    ("uni-13", {"az": "Proseslər, axınlar, planlaşdırma və virtual yaddaş", "en": "Processes, threads, scheduling and virtual memory"}),
    ("uni-14", {"az": "Yarış vəziyyətləri, sinxronlaşdırma, qarşılıqlı kilidlənmə və qeyri-determinizm", "en": "Race conditions, synchronisation, deadlock and nondeterminism"}),
    ("uni-15", {"az": "Şəbəkə protokolları, marşrutlaşdırma, etibarlılıq və sıxlıq", "en": "Network protocols, routing, reliability and congestion"}),
    ("uni-16", {"az": "Autentifikasiya, avtorizasiya, şifrələmə və təhlükəsiz proqram layihələndirməsi", "en": "Authentication, authorisation, encryption and secure software design"}),
    ("uni-17", {"az": "Paylanmış sistemlər, replikasiya, uyğunluq və konsensus", "en": "Distributed systems, replication, consistency and consensus"}),
    ("uni-18", {"az": "Bulud hesablaması, konteynerlər, orkestrasiya və yerləşdirmə", "en": "Cloud computing, containers, orchestration and deployment"}),
    ("uni-19", {"az": "Maşın öyrənməsinin qiymətləndirilməsi, həddindən artıq və yetərsiz öyrənmə", "en": "Evaluating machine learning, overfitting and underfitting"}),
    ("uni-20", {"az": "Verilənlər sızması, sinif balanssızlığı, model qərəzi və izah edilə bilmə", "en": "Data leakage, class imbalance, model bias and explainability"}),
    ("uni-21", {"az": "Böyük dil modellərində tokenləşdirmə, vektor təmsilləri, diqqət, axtarış və hallüsinasiya", "en": "Tokenisation, vector representations, attention, retrieval and hallucination in large language models"}),
    ("uni-22", {"az": "Proqramın yoxlanması, arxitektura, versiyaların idarə edilməsi və davamlı inteqrasiya", "en": "Testing software, architecture, version control and continuous integration"}),
    ("uni-23", {"az": "Funksional, məntiqi və eynizamanlı proqramlaşdırma paradiqmaları", "en": "Functional, logic and concurrent programming paradigms"}),
    ("uni-24", {"az": "Kompilyatorlar, interpretatorlar və proqramlaşdırma dillərinin semantikası", "en": "Compilers, interpreters and programming-language semantics"}),
    ("uni-25", {"az": "Avtomatlar, hesablana bilmə, reduksiya, P, NP və NP-tamlıq", "en": "Automata, computability, reductions, P, NP and NP-completeness"}),
]



def render_body(lang: str) -> str:
    rows = "".join(
        f"<tr><td>{n}</td><td>{esc(t[lang])}</td><td>{esc(a[lang])}</td><td>{esc(i[lang])}</td><td>{esc(d[lang])}</td></tr>"
        for n, t, a, i, d in PRIORITY_ROWS
    )
    school_ol = topic_ol([(sid, titles[lang]) for sid, titles in SCHOOL_LIST])
    uni_ol = topic_ol([(sid, titles[lang]) for sid, titles in UNI_LIST])
    return f"""
<section class="cta-card" id="about">
<h2>{T(lang, "Bələdçidən istifadə", "How to use this guide")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Dünya Azərbaycanlı Alimlər Birliyinin (DAAB) bu səhifəsi informatika üzrə tədris materialı hazırlamaq istəyən müəllimlərə, mütəxəssislərə və «Çətin mövzu, aydın izah» müsabiqəsinin iştirakçılarına mövzu seçməkdə kömək edir. Burada təhsil baxımından əhəmiyyətli və praktikada aktual olan mövzular, onların öyrənilməsindəki çətinliklər və aydın izah üçün nümunələr bir araya gətirilir.",
"This page from the World Association of Azerbaijani Scientists (WAAS / DAAB) helps teachers, specialists and participants in the “Complex Topics, Clear Explanations” competition choose an informatics topic. It brings together topics that matter in education and in practice, the difficulties of learning them, and examples that can support a clear explanation."))}
{p(T(lang,
"Səhifə işçi bələdçidir. Siyahı mümkün mövzuları məhdudlaşdırmır. İştirakçılar göstərilən istiqamətlərdən birini seçə və ya təhsil əhəmiyyətini əsaslandıraraq yeni mövzu təklif edə bilərlər. Materialın dəyəri auditoriyanın konkret sualına cavab verməsi və öyrənənə yeni bilik və ya bacarıq qazandırması ilə müəyyən olunur.",
"The page is a working guide. It does not close the list of possible topics. Participants may choose one of these directions or propose a new topic and justify its educational value. A piece of material is valuable when it answers a concrete question for its audience and gives the learner new knowledge or a new skill."))}
{note(T(lang,
"İnformatika mövzularının populyarlığı və çətinliyi üzrə hamı tərəfindən qəbul edilmiş vahid qlobal reytinq yoxdur. Burada «maraq» və ya «populyarlıq» öyrənənlərin ehtiyacları, tədris proqramlarının prioritetləri və texnologiya sahəsindəki fəaliyyət barədə göstəricilərin ümumi şərhidir; internet axtarışlarının sayını bildirmir. Otuz mövzudan ibarət cədvəldəki sıra və «yüksək», «çox yüksək» kimi qiymətlər istiqamətləndirici qiymətləndirmələrdir, vahid üsulla hesablanmış ballar deyil.",
"There is no universally accepted global ranking of informatics topics by popularity or difficulty. Here “interest” or “popularity” is a reading of learner need, curriculum priorities and activity in technology. It is not a count of internet searches. The order of the thirty topics, and labels such as “high” or “very high”, are directional judgements, not scores from a single measurement."))}
{p(T(lang,
"Mövzu seçərkən üç məsələni birlikdə nəzərə alın: mövzunun öyrənən üçün əhəmiyyəti, tətbiq sahəsi və başa düşülməsində yaranan çətinlik. Əvvəlcə mənbələrin nəyi göstərdiyini oxuyun. Sonra prioritet cədvəlinə baxın, məktəb və ya universitet siyahısından altmövzu seçin. Hər siyahı izah və nümunələrdən əvvəl gəlir.",
"When you choose a topic, hold three things together: why it matters to the learner, where it is used, and where understanding usually breaks. Read first what the sources show. Then look at the priority table and pick a subtopic from the school or university list. Each list comes before the explanations and examples."))}
{p(T(lang,
"Məzmun inteqrasiya olunmuş bələdçidən gəlir. O, yenidən işlənmiş Word sənədini və əvvəlki veb səhifəni birləşdirir. Mənbələr bir-birini tamamlayanda məlumat eyni bölmədə verilir. Fərqli söz, qruplaşma və ya qətiyyət seçəndə fərq gizlədilmir.",
"The content comes from the integrated guide. That guide combined a reworked Word document with the earlier web page. Where the sources complement each other, the information sits in the same section. Where they chose different words, groupings or degrees of certainty, the difference is not hidden."))}
</div></section>
<section class="cta-card" id="differences">
<h2>{T(lang, "Mənbələr arasındakı fərqlər", "Where the sources differ")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Aşağıdakı cədvəl iki mənbənin eyni fakta fərqli söz, qruplaşma və ya qətiyyətlə yanaşdığı yerləri toplayır. Bu, səhv və ya düzgün versiya seçimi deyil. İşlək izahda daha ehtiyatlı və ya daha dəqiq ifadə əsas götürülür, o biri qısa qeyd kimi saxlanılır.",
"The table below collects places where the two sources treated the same fact with different wording, grouping or certainty. This is not a choice between a wrong version and a right one. The working explanation uses the more cautious or more precise wording and keeps the other form as a short note."))}
{table(
    [
        T(lang, "Məsələ", "Issue"),
        T(lang, "Fərq", "Difference"),
        T(lang, "Bu səhifədə", "On this page"),
    ],
    [
        [
            T(lang, "Python tövsiyəsi", "Python recommendation"),
            T(lang, "Yenidən işlənmiş sənəd Python-u praktik başlanğıc sayır və vahid «ən yaxşı dil» hökmündən çəkinir. Əvvəlki veb səhifə onu hazırda ən uyğun ümumi tədris dili adlandırmışdı.",
              "The reworked document treats Python as a practical starting point and avoids calling it the single “best language”. The earlier web page called it the most suitable general teaching language at present."),
            T(lang, "Hər iki ifadə dil bölməsində saxlanılır.", "Both statements are kept in the language section."),
        ],
        [
            T(lang, "TypeScript göstəricisi", "TypeScript figure"),
            T(lang, "Yenidən işlənmiş sənəd 2025-ci ilin avqustunda GitHub istifadə göstəricisinə görə TypeScript-in Python və JavaScript-i keçdiyini yazır. Əvvəlki səhifə «ən çox istifadə olunan dil» demiş, platformanı dəqiqləşdirməmişdi.",
              "The reworked document says that in August 2025 TypeScript overtook Python and JavaScript on GitHub’s usage measure. The earlier page said it was the most-used language and did not name the platform."),
            T(lang, "GitHub Octoverse 2025 ifadəsi əsas götürülür.", "The GitHub Octoverse 2025 wording is the base."),
        ],
        [
            T(lang, "CSTA «ixtisaslar»", "CSTA “specialties”"),
            T(lang, "Əvvəlki səhifə süni intellekt, kibertəhlükəsizlik və s. üzrə ixtisaslar yazırdı. Yenidən işlənmiş sənəd bunların ali təhsil ixtisası deyil, məktəb səviyyəsində ixtisaslaşma istiqamətləri olduğunu vurğulayır.",
              "The earlier page named specialties in AI, cybersecurity and related fields. The reworked document stresses that these are school-level specialisation tracks, not university degrees."),
            T(lang, "Siyahı saxlanılır; ehtiyat izah əlavə edilir.", "The list is kept; the caution is added."),
        ],
        [
            T(lang, "CSTA-da süni intellekt", "AI in CSTA"),
            T(lang, "Yenidən işlənmiş sənəd süni intellektin baza səviyyəsində istiqamətlərə inteqrasiya olunduğunu, yuxarı siniflərdə dərinləşdiyini yazır. Əvvəlki səhifə standartların süni intellekti prioritet saydığını vurğulayırdı.",
              "The reworked document says AI is integrated into the strands at a basic level and deepened in the upper years. The earlier page stressed that the standards treat AI as a priority."),
            T(lang, "Hər iki vurğu CSTA bölməsində yan-yanadır.", "Both emphases sit together in the CSTA section."),
        ],
        [
            T(lang, "Universitet mövzularının qruplaşması", "Grouping of university topics"),
            T(lang, "Əvvəlki səhifə 25 nömrələnmiş bənd istifadə edir: nəzəriyyə 25-ci bənddir. Yenidən işlənmiş sənəd paradiqmaları icra ilə, avtomatları isə alqoritmlərlə bir qrupda vermişdi.",
              "The earlier page used 25 numbered items, with theory as item 25. The reworked document grouped paradigms with execution and automata with algorithms."),
            T(lang, "Nömrələmə 25 bənd olaraq saxlanılır; qrup fərqi universitet bölməsində qeyd olunur.", "The 25-item numbering is kept; the grouping difference is noted in the university section."),
        ],
        [
            T(lang, "Deadlock və şəbəkə tıxacı", "Deadlock and network congestion"),
            T(lang, "Yenidən işlənmiş sənəd qarşılıqlı kilidlənmə və sıxlıq yazır. Əvvəlki səhifə tıxac və tıxaclıq yazırdı. Eyni kök iki fərqli anlayışı qarışdıra bilər.",
              "The reworked document uses mutual deadlock and congestion. The earlier page used two Azerbaijani words from the same root, tıxac and tıxaclıq. That root can mix two different ideas."),
            T(lang, "Hər iki cüt izahda saxlanılır.", "Both pairs are kept in the explanation."),
        ],
        [
            T(lang, "Termin cütləri", "Term pairs"),
            T(lang, "Polimorfizm / çoxformalıq; iki amilli autentifikasiya / iki faktorlu təsdiq; Big-O / Böyük-O; uyğunluq / tutarlılıq; izolyasiya / izolə; orkestrasiya / orkestrləşdirmə; konsensus / razılaşma; obyektyönlü / obyektyönümlü; heap / dinamik yaddaş.",
              "Polymorphism / çoxformalıq; two-factor authentication / iki faktorlu təsdiq; Big-O / Böyük-O; consistency / tutarlılıq; isolation / izolə; orchestration / orkestrləşdirmə; consensus / razılaşma; object-oriented / obyektyönümlü; heap / dynamic memory."),
            T(lang, "İlk keçiddə hər iki forma verilir.", "Both forms appear at the first mention."),
        ],
        [
            T(lang, "Müsabiqə keçidləri", "Competition links"),
            T(lang, "Yenidən işlənmiş sənəd yerli işçi ünvan da göstərmişdi. Veb səhifə ictimai keçidlərdən istifadə edir.",
              "The reworked document also listed a local development address. The web page uses the public links."),
            T(lang, "İctimai keçidlər əsasdır; yerli ünvan inkişaf nüsxəsi kimi qeyd olunur.", "Public links are primary; the local address is noted as a development copy."),
        ],
    ],
    table_id="informatics-differences",
)}
</div></section>
<section class="cta-card" id="sources">
<h2>{T(lang, "Mövzu seçiminin əsaslandığı mənbələr", "Evidence behind the topics")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Mövzuların seçimi üç mənbə qrupuna əsaslanır. Hər qrup fərqli suala cavab verir və digərlərini tamamlayır. Təhsil standartı bir mövzunun öyrədilməsinin vacibliyini göstərə bilər, lakin onun nə qədər populyar və ya çətin olduğunu birbaşa ölçmür.",
"The topic choices rest on three groups of sources. Each group answers a different question and completes the others. A curriculum standard can show that a topic should be taught; it does not by itself measure how popular or how difficult the topic is."))}
{table(
    [
        T(lang, "Mənbə qrupu", "Source group"),
        T(lang, "Əsas sual", "Main question"),
        T(lang, "Töhfəsi", "What it contributes"),
    ],
    [
        [
            T(lang, "Təhsil standartları və proqram tövsiyələri", "Curriculum standards and programme guidance"),
            T(lang, "Nəyi bilmək və bacarmaq lazımdır?", "What should people know and be able to do?"),
            T(lang, "Əsas anlayışları və uyğun təhsil səviyyəsini göstərir.", "Shows the core ideas and a suitable level of study."),
        ],
        [
            T(lang, "Peşəkar fəaliyyət və maraq göstəriciləri", "Professional activity and interest signals"),
            T(lang, "Hansı texnologiyalar istifadə olunur və diqqət çəkir?", "Which technologies are used and attract attention?"),
            T(lang, "Mövzunun müasir tətbiqlərlə əlaqəsini göstərir.", "Shows how the topic connects to current practice."),
        ],
        [
            T(lang, "Öyrənmə və tədris tədqiqatları", "Learning and teaching research"),
            T(lang, "Öyrənənlər harada və niyə çətinlik çəkir?", "Where do learners struggle, and why?"),
            T(lang, "Aydın izaha ehtiyacı olan anlayışları müəyyənləşdirməyə kömək edir.", "Helps identify ideas that need a clear explanation."),
        ],
    ],
    compact=True,
    table_id="informatics-source-groups",
)}
<section class="cta-sub" id="sources-csta">
<h3>{T(lang, "CSTA məktəb standartları", "CSTA school standards")}</h3>
{p(T(lang,
"<strong>CSTA</strong> — Computer Science Teachers Association, yəni İnformatika Müəllimləri Assosiasiyasıdır. <strong>PK–12</strong> məktəbəqədər mərhələdən 12-ci sinfə qədər olan təhsil pillələrini ifadə edir. PK «pre-kindergarten», K isə «kindergarten» sözlərinin qısaltmasıdır. Bu bölgü Azərbaycan təhsil sisteminin sinifləri ilə avtomatik eyniləşdirilməməlidir. <a href=\"#ref-1\">[1]</a>",
"<strong>CSTA</strong> is the Computer Science Teachers Association. <strong>PK–12</strong> covers the years from pre-kindergarten to grade 12. PK stands for pre-kindergarten and K for kindergarten. That division should not be treated as the same as the grades of the Azerbaijani school system. <a href=\"#ref-1\">[1]</a>"))}
{p(T(lang, "CSTA-nın 2026-cı il standartları məktəb informatikasını beş istiqamət ətrafında qurur:", "CSTA’s 2026 standards organise school computing around five strands:"))}
{bullets([
    T(lang, "Alqoritmlər və layihələndirmə;", "Algorithms and design;"),
    T(lang, "Proqramlaşdırma;", "Programming;"),
    T(lang, "Verilənlər və təhlil;", "Data and analysis;"),
    T(lang, "Sistemlər və təhlükəsizlik;", "Systems and security;"),
    T(lang, "Hesablama və cəmiyyət.", "Computing and society."),
])}
{p(T(lang,
"Süni intellekt baza səviyyəsində bu istiqamətlərə inteqrasiya olunur. Əvvəlki səhifə eyni standartların süni intellekti prioritet saydığını da vurğulayırdı. Bu iki ifadə ziddiyyət deyil: inteqrasiya baza səviyyəsini, prioritet isə vurğunu təsvir edir. <a href=\"#ref-1\">[1]</a>",
"Artificial intelligence is integrated into these strands at a basic level. The earlier page also stressed that the same standards treat AI as a priority. The two statements do not conflict: integration describes the basic level, and priority describes the emphasis. <a href=\"#ref-1\">[1]</a>"))}
{p(T(lang,
"Yuxarı siniflərdə dərinləşdirilmiş öyrənmə üçün süni intellekt, kibertəhlükəsizlik, verilənlər elmi, oyunların hazırlanması, fiziki hesablama və proqram təminatının hazırlanması nəzərdə tutulur. Bunlar ali təhsil ixtisasları deyil, məktəb səviyyəsində ixtisaslaşma istiqamətləridir.",
"For deeper study in the upper years the standards name artificial intelligence, cybersecurity, data science, game development, physical computing and software development. These are school-level specialisation tracks, not university degrees."))}
{p(T(lang,
"<strong>Fiziki hesablama</strong> proqramın sensorlar və elektron qurğular vasitəsilə real mühitlə qarşılıqlı işləməsidir. Məsələn, torpağın rütubətini ölçüb suvarmanı işə salan qurğu bu istiqamətə uyğun layihədir.",
"<strong>Physical computing</strong> is a program working with the real environment through sensors and electronic devices. A device that measures soil moisture and then starts watering is a project in this direction."))}
</section>
<section class="cta-sub" id="sources-cs2023">
<h3>{T(lang, "CS2023 universitet tövsiyələri", "CS2023 university guidance")}</h3>
{p(T(lang,
"<strong>CS2023</strong> — Computer Science Curricula 2023, kompüter elmləri üzrə tədris proqramı tövsiyələridir. Sənəd üç peşəkar təşkilatın birgə işidir.",
"<strong>CS2023</strong> is Computer Science Curricula 2023, guidance for computer-science programmes. The document is joint work by three professional organisations."))}
{table(
    [T(lang, "İxtisar", "Abbreviation"), T(lang, "Tam adı və izahı", "Full name and meaning")],
    [
        ["ACM", T(lang, "Association for Computing Machinery — kompüter elmləri və texnologiyaları üzrə elmi-peşəkar assosiasiya.", "Association for Computing Machinery — a scholarly and professional association for computing.")],
        ["IEEE-CS", T(lang, "IEEE Computer Society — Elektrik və Elektronika Mühəndisləri İnstitutunun kompüter sahəsi üzrə cəmiyyəti. IEEE: Institute of Electrical and Electronics Engineers.", "IEEE Computer Society — the computing society of the Institute of Electrical and Electronics Engineers.")],
        ["AAAI", T(lang, "Association for the Advancement of Artificial Intelligence — Süni İntellektin İnkişafı Assosiasiyası.", "Association for the Advancement of Artificial Intelligence.")],
    ],
    compact=True,
    table_id="informatics-orgs",
)}
{p(T(lang,
"CS2023 əsasən bakalavr təhsilinə yönəlib. Adında «2023» olsa da, yekun sənəd 2024-cü ildə təsdiqlənib. O, alqoritmlər, süni intellekt, verilənlərin idarə edilməsi, şəbəkələr, əməliyyat sistemləri, təhlükəsizlik və proqram mühəndisliyi daxil olmaqla 17 bilik sahəsini əhatə edir. <a href=\"#ref-2\">[2]</a>, <a href=\"#ref-23\">[23]</a>",
"CS2023 is aimed mainly at undergraduate study. Although the name says 2023, the final document was approved in 2024. It covers 17 knowledge areas, including algorithms, artificial intelligence, data management, networks, operating systems, security and software engineering. <a href=\"#ref-2\">[2]</a>, <a href=\"#ref-23\">[23]</a>"))}
{p(T(lang,
"Bu yanaşmada biliklərin tətbiqi, əməkdaşlıq, məsuliyyət və peşəkar davranış da nəzərə alınır. Materialı planlaşdırarkən «Hansı məlumatı təqdim edirəm?» sualı ilə yanaşı «Öyrənən bu materialdan sonra nə edə biləcək?» sualını vermək buna görə faydalıdır. <a href=\"#ref-24\">[24]</a>",
"This approach also takes in applying knowledge, collaboration, responsibility and professional conduct. When you plan a piece of material it is therefore useful to ask not only “What information am I presenting?” but also “What will the learner be able to do after this?” <a href=\"#ref-24\">[24]</a>"))}
</section>
<section class="cta-sub" id="sources-ap">
<h3>AP Computer Science Principles</h3>
{p(T(lang,
"<strong>AP</strong> — Advanced Placement, məktəblilər üçün universitetin giriş səviyyəsinə uyğun kurs və imtahan proqramıdır. <strong>CSP</strong> — Computer Science Principles, «Kompüter elmlərinin əsasları» deməkdir. Proqramı College Board təqdim edir. <a href=\"#ref-3\">[3]</a>",
"<strong>AP</strong> is Advanced Placement, a course and examination programme that gives school students work at the start of university level. <strong>CSP</strong> is Computer Science Principles. The College Board offers the programme. <a href=\"#ref-3\">[3]</a>"))}
{p(T(lang, "AP CSP beş əsas mövzunu birləşdirir:", "AP CSP brings together five Big Ideas:"))}
{bullets([
    T(lang, "Yaradıcı həllərin hazırlanması;", "Creative development;"),
    T(lang, "Verilənlər;", "Data;"),
    T(lang, "Alqoritmlər və proqramlaşdırma;", "Algorithms and programming;"),
    T(lang, "Kompüter sistemləri və şəbəkələr;", "Computer systems and networks;"),
    T(lang, "Hesablama texnologiyalarının təsiri.", "The impact of computing."),
])}
{p(T(lang,
"Kurs proqramlaşdırma ilə yanaşı internetin işləməsi, verilənlərdən nəticə çıxarılması və texnologiyanın cəmiyyətə təsiri barədə ilkin anlayış yaradır. CSTA məktəb təhsilini, AP CSP universitetə giriş səviyyəli hazırlığı, CS2023 isə bakalavr təhsilini istiqamətləndirir. Bu fərq mövzunun dərinliyini seçmək üçün əhəmiyyətlidir. <a href=\"#ref-1\">[1]</a>–<a href=\"#ref-3\">[3]</a>",
"Besides programming, the course builds a first picture of how the internet works, how to draw conclusions from data, and how technology affects society. CSTA guides school computing, AP CSP guides preparation at the start of university, and CS2023 guides undergraduate study. That difference matters when you choose how deep a topic should go. <a href=\"#ref-1\">[1]</a>–<a href=\"#ref-3\">[3]</a>"))}
</section>
<section class="cta-sub" id="sources-surveys">
<h3>{T(lang, "Stack Overflow və GitHub", "Stack Overflow and GitHub")}</h3>
{p(T(lang,
"<strong>Stack Overflow</strong> proqramlaşdırma suallarının müzakirə olunduğu platformadır. Onun Developer Survey hesabatı proqramçıların alətlərdən istifadəsi, iş üsulları və münasibətləri barədə illik sorğudur. 2025-ci ilin nəticələrində 177 ölkədən 49 009 cavab istifadə olunub. İştirakçılar əsasən platformanın öz kanalları vasitəsilə cəlb edildiyindən nəticələr bütün proqramçıların tam təmsilçi mənzərəsi sayılmamalıdır. <a href=\"#ref-4\">[4]</a>, <a href=\"#ref-25\">[25]</a>",
"<strong>Stack Overflow</strong> is a platform where people discuss programming questions. Its Developer Survey is an annual survey of how programmers use tools, how they work and what they think. The 2025 results used 49,009 responses from 177 countries. Because people were reached mainly through the platform’s own channels, the results should not be treated as a complete picture of all programmers. <a href=\"#ref-4\">[4]</a>, <a href=\"#ref-25\">[25]</a>"))}
{p(T(lang,
"Süni intellektdən istifadə barədə suala cavab verənlərin 84 faizi bu alətlərdən istifadə etdiyini və ya istifadə etməyi planlaşdırdığını bildirib. Dəqiqliyə etibar barədə ayrıca sualda 46 faiz etimadsızlıq, 33 faiz isə etimad ifadə edib. 84 faiz göstəricisi yalnız hazırda istifadə edənləri bildirmir. <a href=\"#ref-26\">[26]</a>",
"Of those who answered the question on using AI, 84 percent said they were using these tools or planned to use them. On a separate question about trust in accuracy, 46 percent expressed distrust and 33 percent expressed trust. The 84 percent figure does not count only people who already use the tools. <a href=\"#ref-26\">[26]</a>"))}
{p(T(lang,
"Bu nəticələrdən «Süni intellektin yaratdığı kodu necə yoxlamaq olar?» və «İnandırıcı cavab niyə səhv ola bilər?» kimi mövzu təklifləri çıxarmaq mümkündür. Bunlar sorğunun birbaşa tövsiyələri deyil, nəticələrin tədris məqsədilə şərhidir.",
"From these results one can draw teaching topics such as “How can you check code written by AI?” and “Why can a convincing answer still be wrong?” Those are not recommendations from the survey itself. They are a teaching reading of the results."))}
{p(T(lang,
"<strong>GitHub</strong> proqram kodunun saxlanması və birgə hazırlanması platformadır. <strong>Octoverse</strong> onun illik fəaliyyət hesabatının adıdır, ixtisar deyil. 2025-ci il hesabatı süni intellekt layihələrinin artmasını və həmin ilin avqustunda TypeScript-in GitHub-un istifadə göstəricisinə görə Python və JavaScript-i keçməsini vurğulayır. Hesabatda Python-un yeni süni intellekt repozitoriyalarının təxminən yarısında istifadə olunduğu da göstərilir. <strong>Repozitoriya</strong> layihənin kodunu və dəyişiklik tarixçəsini saxlayan mühitdir. <a href=\"#ref-5\">[5]</a>",
"<strong>GitHub</strong> is a platform for storing program code and working on it together. <strong>Octoverse</strong> is the name of its yearly activity report, not an abbreviation. The 2025 report highlights the growth of AI projects and says that in August of that year TypeScript overtook Python and JavaScript on GitHub’s usage measure. It also reports that Python is used in about half of new AI repositories. A <strong>repository</strong> is the place that holds a project’s code and the history of changes. <a href=\"#ref-5\">[5]</a>"))}
{note(T(lang,
"Fərq. Əvvəlki səhifə TypeScript-in 2025-ci ildə «ən çox istifadə olunan dil» olduğunu yazmış, platformanı dəqiqləşdirməmişdi. Bu səhifə GitHub Octoverse 2025 ifadəsindən istifadə edir. Hər iki mənbə eyni hesabata istinad edir. Bu göstəricilər platformadakı fəaliyyəti təsvir edir; əmək bazarının tələbatını, mövzunun təhsil dəyərini və ya öyrənmə çətinliyini birbaşa ölçmür.",
"Difference. The earlier page said TypeScript was the most-used language in 2025 and did not name the platform. This page uses the GitHub Octoverse 2025 wording. Both sources point to the same report. These figures describe activity on a platform. They do not directly measure labour-market demand, educational value or how hard a topic is to learn."), "editorial")}
</section>
<section class="cta-sub" id="sources-research">
<h3>{T(lang, "Öyrənmə tədqiqatları", "Learning research")}</h3>
{p(T(lang,
"<strong>Empirik tədqiqat</strong> real müşahidələrə və toplanmış məlumatlara əsaslanan araşdırmadır. Tədrisdə bu, öyrənənlərlə müsahibələr, tapşırıq cavablarının təhlili və dərsdən əvvəl və sonra aparılan ölçmələr ola bilər.",
"An <strong>empirical study</strong> is research based on real observation and collected data. In teaching this may mean interviews with learners, analysis of task answers, and measurements before and after a class."))}
{p(T(lang,
"<strong>Konsepsiya inventarı</strong> (<em>concept inventory</em>) əsas anlayışların nə dərəcədə başa düşüldüyünü və yanlış təsəvvürləri müəyyən edən diaqnostik testdir. Səhv cavab variantları da düşüncə səhvlərini üzə çıxarmaq üçün hazırlanır. Dinamik proqramlaşdırma üzrə belə bir alətin hazırlanmasında əvvəlki tədqiqatlarda müəyyən olunmuş yanlış təsəvvürlərdən istifadə edilib. <a href=\"#ref-27\">[27]</a>",
"A <strong>concept inventory</strong> is a diagnostic test that asks how well core ideas are understood and what misconceptions are present. Wrong answer choices are written to reveal those thought-errors. A tool of this kind for dynamic programming used misconceptions found in earlier studies. <a href=\"#ref-27\">[27]</a>"))}
{p(T(lang, "Nümunə olaraq aşağıdakı əmrləri ardıcıllıqla nəzərdən keçirin:", "As an example, look at these commands in order:"))}
{code_block(["a = 5", "b = a", "a = 8"])}
{p(T(lang,
"Sonda <code>b</code>-nin qiyməti 5-dir. <code>b</code>-yə <code>a</code>-nın həmin andakı qiyməti mənimsədilib; sonrakı əmr yalnız <code>a</code>-nı dəyişir. «<code>b</code> də 8 olar» cavabı mənimsətmənin daim yenilənən əlaqə kimi başa düşüldüyünü göstərə bilər.",
"At the end the value of <code>b</code> is 5. <code>b</code> was given the value that <code>a</code> had at that moment; the later command changes only <code>a</code>. The answer “<code>b</code> becomes 8 as well” can show that assignment was understood as a link that stays updated."))}
{p(T(lang,
"Testin yaşa, dilə və öyrədilən mövzulara uyğunluğu yoxlanmalıdır. <strong>SCS1</strong> — Second CS1, giriş proqramlaşdırmasında anlayışları ölçən qiymətləndirmə vasitəsidir; <strong>CS1</strong> ilkin kompüter elmləri və ya proqramlaşdırma kursunu bildirir. SCS1 üzrə tədqiqat alətin tətbiq sərhədlərini və öyrənmə artımını qiymətləndirmək üçün əvvəl və sonra ölçmələrinin əhəmiyyətini vurğulayır. <a href=\"#ref-28\">[28]</a>",
"A test must be checked for fit with age, language and the topics that are taught. <strong>SCS1</strong> — Second CS1 — is an assessment of ideas in introductory programming; <strong>CS1</strong> is a name for a first computer-science or programming course. Research on SCS1 stresses the limits of the tool and the value of measuring before and after teaching if you want to judge learning gains. <a href=\"#ref-28\">[28]</a>"))}
</section>
</div></section>
<section class="cta-card" id="priority">
<h2>{T(lang, "Tövsiyə olunan 30 əsas mövzu", "Thirty recommended topics")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Bu cədvəl mövzulara ümumi baxış verir. Sıra ilkin prioritet təklifidir, statistik reytinq deyil. «Hər iki qrup» məktəbliləri və universitet tələbələrini bildirir; eyni mövzu bu qruplara fərqli dərinlikdə izah olunmalıdır. «Yuxarı siniflər» və «universitet» bölgüsü sərt qəbul şərti deyil. Əvvəlki səhifə bəzi sətirlərdə «kollec» də əlavə etmişdi.",
"This table gives an overview of the topics. The order is a first suggestion of priority, not a statistical ranking. “Both groups” means school learners and university students; the same topic should be explained at different depths for those groups. “Upper-secondary” and “university” are not hard admission rules. The earlier page also added “college” on some rows."))}
<div class="cta-table-wrap" tabindex="0"><table class="cta-table" data-daab-resizable-table="1" data-daab-resize-id="informatics-priority">
<thead><tr><th scope="col" class="col-c1">{T(lang, "Sıra", "Order")}</th><th scope="col" class="col-c2">{T(lang, "Mövzu", "Topic")}</th><th scope="col" class="col-c3">{T(lang, "Əsas auditoriya", "Main audience")}</th><th scope="col" class="col-c4">{T(lang, "Maraq", "Interest")}</th><th scope="col" class="col-c5">{T(lang, "İzah çətinliyi", "Explanation difficulty")}</th></tr></thead>
<tbody>{rows}</tbody>
</table></div>
</div></section>
<section class="cta-card" id="school">
<h2>{T(lang, "Məktəblilər və orta məktəb şagirdləri üçün", "For school learners")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Bu mövzular şagirdlər və orta məktəb şagirdləri üçün xüsusilə faydalıdır. Məktəb auditoriyası üçün konkret situasiyadan başlamaq və sonra ümumi anlayışa keçmək əlverişlidir. Yenidən işlənmiş sənəd eyni 23 bəndi tematik qruplarda toplayır; əvvəlki səhifə onları nömrələyib hər bəndə nümunə verir. Aşağıda əvvəlcə tam siyahı, sonra eyni sırada izah və nümunələr gəlir. Nümunələr materialın qurulmasına kömək edən təkliflərdir, məcburi tapşırıq deyil.",
"These topics are especially useful for pupils and secondary-school students. For a school audience it helps to begin with a concrete situation and then move to the general idea. The reworked document gathered the same 23 items in thematic groups; the earlier page numbered them and gave each item an example. Below, the full list comes first. Then each item is explained in the same order, with examples. The examples are suggestions for building material, not required tasks."))}
<h3>{T(lang, "Mövzu siyahısı", "Topic list")}</h3>
{school_ol}
{note(T(lang,
"CSTA 2026. Yeni CSTA standartları məktəb informatikasını alqoritmlər və layihələndirmə, proqramlaşdırma, verilənlər və təhlil, sistemlər və təhlükəsizlik, həmçinin hesablama və cəmiyyət ətrafında qurur. Onlar süni intellekti prioritet sayır və süni intellekt, kibertəhlükəsizlik, verilənlər elmi, oyun işlənməsi, fiziki hesablama və proqram təminatı üzrə dərinləşmə istiqamətləri müəyyən edir. Bunlar ali təhsil ixtisasları deyil, məktəb səviyyəsində ixtisaslaşma istiqamətləridir. (CSTA 2026 Standards) <a href=\"#ref-1\">[1]</a>",
"CSTA 2026. The new CSTA standards organise school computing around algorithms and design, programming, data and analysis, systems and security, and computing and society. They treat AI as a priority and name deeper tracks in AI, cybersecurity, data science, game development, physical computing and software development. These are school-level specialisation tracks, not university degrees. (CSTA 2026 Standards) <a href=\"#ref-1\">[1]</a>"))}
{_school_explanations(lang)}
</div></section>
<section class="cta-card" id="university">
<h2>{T(lang, "Universitet tələbələri üçün", "For university students")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Bu auditoriya üçün təkcə mexanizmin işləməsini deyil, alternativ həllər arasındakı fərqi və seçim səbəblərini də izah etmək vacibdir. Əvvəlki səhifə mövzuları kollec və universitet təhsili üçün xüsusilə vacib sayırdı; yenidən işlənmiş sənəd eyni bəndləri yeddi qrupda birləşdirir.",
"For this audience it is important to explain not only how a mechanism works, but also the difference between alternative solutions and why one is chosen. The earlier page treated these topics as especially important for college and university study; the reworked document gathered the same items in seven groups."))}
{note(T(lang,
"Quruluş fərqi. Əvvəlki səhifə 25 bəndi belə düzür: icra (1–5), verilənlər strukturları (6–9), bazalar (10–12), sistemlər (13–18), maşın öyrənməsi (19–21), proqram işi (22–24), nəzəriyyə (25). Yenidən işlənmiş sənəd paradiqmaları və kompilyatorları icra qrupuna, avtomatlar, P və NP-ni isə alqoritmlər qrupuna salır. Məzmun eynidir; aşağıdakı nömrələmə 25 bəndi saxlayır ki, siyahı izahlarla eyni sırada qalsın.",
"Difference of structure. The earlier page ordered the 25 items as execution (1–5), data structures (6–9), databases (10–12), systems (13–18), machine learning (19–21), software work (22–24) and theory (25). The reworked document placed paradigms and compilers with execution, and automata, P and NP with algorithms. The content is the same. The numbering below keeps the 25 items so that the list and the explanations stay in the same order."), "editorial")}
<h3>{T(lang, "Mövzu siyahısı", "Topic list")}</h3>
{uni_ol}
{_university_explanations(lang)}
</div></section>
{_closing_sections(lang)}
"""



def _school_explanations(lang: str) -> str:
    return "\n".join([
        group("school-thinking", T(lang, "Kompüter kimi düşünmək", "Thinking like a computer")),
        term(lang, T(lang, "Alqoritm nədir — və gündəlik məsələni addımlara necə çevirməli", "What an algorithm is — and how to turn an everyday problem into steps"),
             T(lang,
               "<strong>Alqoritm</strong> məqsədə çatmaq üçün müəyyən ardıcıllıqla yerinə yetirilən, sonlu və aydın addımlardır. Çətin olan sözün özü deyil, gündəlik işi maşının təxmin etmədən yerinə yetirə biləcəyi addımlara çevirməkdir.",
               "An <strong>algorithm</strong> is a finite list of clear steps, carried out in a definite order, to reach a goal. The hard part is not the word itself, but turning an everyday task into steps that a machine can follow without guessing."),
             [T(lang, "Çay dəmləmək: suyu qaynat, stəkana paket qoy, suyu tök, gözlə, paketi çıxar. Hansısa addım əskikdirsə — «nə qədər gözlə?» — alqoritm natamamdır.",
                "To make tea: boil water, put a bag in a cup, pour the water, wait, remove the bag. If a step is missing — “wait how long?” — the algorithm is incomplete.")],
             sid="school-1", num=1),
        term(lang, T(lang, "Bölmə, qanunauyğunluq və abstraksiya", "Decomposition, patterns and abstraction"),
             T(lang,
               "<strong>Bölmə</strong> böyük məsələni kiçik hissələrə ayırmaqdır. <strong>Qanunauyğunluq</strong> təkrarlananı görməkdir. <strong>Abstraksiya</strong> həmin məqsəd üçün vacib xüsusiyyətləri saxlayıb ikinci dərəcəli detalları kənara qoymaqdır.",
               "<strong>Decomposition</strong> means breaking a large problem into smaller ones. A <strong>pattern</strong> is what repeats. <strong>Abstraction</strong> means keeping the features that matter for the goal and setting the secondary details aside."),
             [T(lang, "Məktəbə ən qısa yolu seçərkən küçələrin əlaqəsi və məsafəsi vacibdir, binaların rəngi isə adətən vacib deyil.",
                "When you choose the shortest route to school, the links between streets and the distances matter; the colour of the buildings usually does not."),
              T(lang, "Məktəb gəzintisini planlamaq: biletlər, yemək və cədvəl (bölmə); hər avtobusun çıxış vaxtı olmalıdır (qanunauyğunluq); oturacağın rəngini yox, «neçə yer var» sualını saxlamaq (abstraksiya).",
                "Planning a school trip: tickets, food and a timetable (decomposition); every bus ride needs a start time (pattern); ignore seat colours and keep “how many seats” (abstraction).")],
             sid="school-2", num=2),
        group("school-code", T(lang, "İlk proqramlar", "First programs")),
        term(lang, T(lang, "Dəyişənlər — dəyişən saxlanılan dəyərlər", "Variables as changing stored values"),
             T(lang,
               "<strong>Dəyişən</strong> proqramın sonradan dəyişə biləcəyi dəyəri saxlayan adlı yerdir. Bu, cəbrdən gələn sirli simvol deyil, adı olan yaddaşdır.",
               "A <strong>variable</strong> is a named place that holds a value the program can change later. It is not a mystery symbol from algebra; it is storage with a name."),
             [T(lang, "<code>score = 0</code>, sonra <code>score = score + 10</code>. <code>score</code> adlı yerdə artıq 10 var.",
                "<code>score = 0</code>, then later <code>score = score + 10</code>. The place named <code>score</code> now holds 10."),
              T(lang, "<code>a = 5</code>, <code>b = a</code>, <code>a = 8</code>. Sonda <code>b</code> 5 qalır, çünki <code>b</code>-yə <code>a</code>-nın həmin andakı qiyməti yazılıb.",
                "<code>a = 5</code>, <code>b = a</code>, <code>a = 8</code>. At the end <code>b</code> is still 5, because <code>b</code> was given the value that <code>a</code> had at that moment.")],
             sid="school-3", num=3),
        term(lang, T(lang, "Mənimsətmə ilə riyazi bərabərliyin fərqi", "The difference between assignment and mathematical equality"),
             T(lang,
               "<strong>Mənimsətmə</strong> dəyəri dəyişənə yazır. Bir çox dildə bərabərlik işarəsi riyaziyyatdakı kimi «hər iki tərəf artıq eynidir» demir.",
               "<strong>Assignment</strong> writes a value into a variable. In many languages the equals sign does not claim that both sides are already the same, as in mathematics."),
             [T(lang, "<code>x = x + 1</code> tənlik kimi mənasızdır, mənimsətmə kimi isə «indiki <code>x</code>-i götür, bir əlavə et, nəticəni yenə <code>x</code>-ə yaz» deməkdir.",
                "<code>x = x + 1</code> is nonsense as an equation, but as assignment it means “take the current <code>x</code>, add one, store the result back in <code>x</code>.”")],
             sid="school-4", num=4),
        term(lang, T(lang, "Şərtlər və Bul ifadələri", "Conditions and Boolean expressions"),
             T(lang,
               "<strong>Şərt</strong> bəli-xeyr sualı verir. <strong>Bul</strong> (<em>Boolean</em>) dəyəri yalnız doğrudur və ya yanlışdır. Proqram növbəti addımı bu cavaba görə seçir.",
               "A <strong>condition</strong> asks a yes-or-no question. A <strong>Boolean</strong> value is only true or false. The program chooses the next step from that answer."),
             [T(lang, "Əgər temperatur &gt; 30-dursa, «isti» yaz; əks halda «normal» yaz.",
                "If temperature &gt; 30, write “hot”; otherwise write “normal”.")],
             sid="school-5", num=5),
        term(lang, T(lang, "İç-içə şərtlər və mürəkkəb məntiq", "Nested conditions and compound logic"),
             T(lang,
               "Şərtlər bir-birinin içində ola bilər, bir neçə yoxlama isə «və» və ya «və ya» ilə birləşdirilə bilər. Çətinlik qərar sırasını aydın saxlamaqdır.",
               "Conditions can sit inside other conditions, and several tests can be joined with “and” or “or”. The difficulty is keeping the order of decisions clear."),
             [T(lang, "Həftə içidirsə və yağış yağırsa, avtobusa min; həftə içidirsə və quru havadırsa, piyada get; əks halda evdə qal.",
                "If it is a weekday and it is raining, take the bus; if it is a weekday and it is dry, walk; otherwise stay home.")],
             sid="school-6", num=6),
        term(lang, T(lang, "Dövrlər necə işləyir və sonsuz dövr nədən yaranır", "How loops work and why an infinite loop starts"),
             T(lang,
               "<strong>Dövr</strong> eyni addımları təkrarlayır. Onun dayanma yolu olmalıdır. <strong>Sonsuz dövr</strong> dayanma şərti heç vaxt doğru olmayanda baş verir.",
               "A <strong>loop</strong> repeats the same steps. It must have a way to stop. An <strong>infinite loop</strong> starts when the stopping condition never becomes true."),
             [T(lang, "«Çən dolmayana qədər su tök» yalnız hər tökülən su səviyyəni qaldırırsa işləyir. Kran bağlıdırsa, dövr bitmir.",
                "“While the tank is not full, pour water” works only if each pour actually raises the level. If the tap is closed, the loop never ends.")],
             sid="school-7", num=7),
        term(lang, T(lang, "Funksiya ilə sadəcə nəticə çap edən əmr", "A function versus a command that only prints a result"),
             T(lang,
               "<strong>Funksiya</strong> girişlər (<strong>parametrlər</strong>) ala və nəticə (<strong>qaytarılan qiymət</strong>) verə bilən adlı iş parçasıdır. Ekrana rəqəm yazmaq onu sonrakı istifadə üçün qaytarmaq deyil.",
               "A <strong>function</strong> is a named piece of work that can take inputs (<strong>parameters</strong>) and give back a result (a <strong>return value</strong>). Writing a number on the screen is not the same as returning it for later use."),
             [T(lang, "<code>add(2, 3)</code> funksiyası təkcə «5» göstərməməli, 5-i qaytarmalıdır ki, proqramın başqa hissəsi onu saxlaya bilsin.",
                "A function <code>add(2, 3)</code> should return 5 so another part of the program can store it, not only display “5”.")],
             sid="school-8", num=8),
        term(lang, T(lang, "Təsadüfi kod dəyişmək əvəzinə sistemli sazlama", "Systematic debugging instead of changing code at random"),
             T(lang,
               "<strong>Sazlama</strong> (<em>debugging</em>) səhvləri təsadüfi sətir dəyişməklə yox, fərziyyəni yoxlamaqla tapmaqdır. Əvvəlcə gözlənilən nəticə müəyyənləşdirilir, sonra faktiki nəticə ilə müqayisə olunur. Bunu öyrənmək də, öyrətmək də çətindir, çünki təcrübəli proqramçılar çox vaxt açıqlamadıqları üsullara arxalanır. <a href=\"#ref-10\">[10]</a>",
               "<strong>Debugging</strong> is finding errors by testing a hypothesis, not by changing lines at random. First you fix the expected result, then you compare it with the actual result. This is hard to learn and hard to teach, because experienced programmers often rely on methods they do not spell out. <a href=\"#ref-10\">[10]</a>"),
             [T(lang, "Cəm səhvdirsə, əvvəl birinci girişi, sonra toplamanı, sonra göstərişi — bir-bir — yoxla; bütün proqramı yenidən yazma.",
                "If a total is wrong, check the first input, then the addition, then the display — one step at a time — instead of rewriting the whole program.")],
             sid="school-9", num=9),
        group("school-data", T(lang, "Kompüterlər məlumatı necə saxlayır", "How computers store information")),
        term(lang, T(lang, "İkilik ədədlər, bit, bayt və onaltılıq yazılış", "Binary numbers, bits, bytes and hexadecimal"),
             T(lang,
               "Kompüterlər məlumatı <strong>bit</strong>lərlə — 0 və ya 1 — saxlayır. Səkkiz bit bir <strong>bayt</strong>dır. <strong>Onaltılıq</strong> (16-lıq) eyni ikilik dəyərləri qısa yazmaq üsuludur.",
               "Computers store information as <strong>bits</strong> — 0 or 1. Eight bits make a <strong>byte</strong>. <strong>Hexadecimal</strong> (base 16) is a shorter way to write the same binary values."),
             [T(lang, "Adi mətn kodlaşdırmasında A hərfi 01000001 baytıdır, onaltılıqda çox vaxt 41 yazılır.",
                "In a common text encoding the letter A is the byte 01000001, often written as 41 in hexadecimal.")],
             sid="school-10", num=10),
        term(lang, T(lang, "Mətn, şəkil, səs və video rəqəmsal necə təqdim olunur", "How text, images, sound and video are represented digitally"),
             T(lang,
               "Kompüter şəkli «görmür», mahnını «eşitmir». O, rəng, parlaqlıq və ya hava təzyiqinin nümunələrini ədədlərlə saxlayır, sonra həmin ədədlərdən media yenidən qurulur. Təsviri piksellər və onların rəng qiymətləri ilə izah etmək mümkündür.",
               "A computer does not “see” a picture or “hear” a song. It stores numbers that stand for samples of colour, brightness or air pressure, then rebuilds the media from those numbers. A picture can be explained as pixels and their colour values."),
             [T(lang, "Ağ-qara şəkil 0 və 1-lərdən ibarət tor ola bilər: 0 ağ, 1 qara.",
                "A black-and-white image can be a grid of 0s and 1s: 0 for white, 1 for black.")],
             sid="school-11", num=11),
        term(lang, T(lang, "İtkili və itkisiz sıxılma", "Lossy and lossless compression"),
             T(lang,
               "<strong>Sıxılma</strong> faylı kiçildir. <strong>Itkisiz</strong> sıxılmada ilkin məlumat tam bərpa olunur. <strong>İtkili</strong> sıxılmada həcmi azaltmaq üçün məlumatın bir hissəsi atılır.",
               "<strong>Compression</strong> makes a file smaller. In <strong>lossless</strong> compression the original data can be restored completely. In <strong>lossy</strong> compression some of the data is thrown away so the file becomes smaller."),
             [T(lang, "Mətnin ZIP arxivi adətən itkisizdir. Güclü sıxılmış foto bir qədər yumşaq görünə bilər, çünki rəng təfərrüatının bir hissəsi atılıb.",
                "A ZIP archive of text is usually lossless. A strongly compressed photo may look slightly softer because some colour detail was discarded.")],
             sid="school-12", num=12),
        group("school-net", T(lang, "Şəbəkələr və təhlükəsizlik", "Networks and safety")),
        term(lang, T(lang, "İnternet, Veb və brauzerin fərqi", "The difference between the Internet, the Web and a browser"),
             T(lang,
               "<strong>İnternet</strong> bir-biri ilə əlaqələnmiş şəbəkələr sistemidir. <strong>Veb</strong> həmin infrastruktur üzərində işləyən xidmətlərdən biridir: ünvanlarla bağlı səhifələr. <strong>Brauzer</strong> isə veb məzmununa baxmağa imkan verən proqramdır.",
               "The <strong>Internet</strong> is a system of networks linked to one another. The <strong>Web</strong> is one service that runs on that infrastructure: pages tied to addresses. A <strong>browser</strong> is the program that lets you look at that web content."),
             [T(lang, "İnternet yol şəbəkəsidir; Veb yol kənarındakı mağazalardır; brauzer mağazaya getdiyin avtomobildir.",
                "The Internet is the road system; the Web is the shops along the road; the browser is the car you use to visit a shop.")],
             sid="school-13", num=13),
        term(lang, T(lang, "IP ünvanı, DNS, marşrutlaşdırıcı, paketlər və HTTP", "IP addresses, DNS, routers, packets and HTTP"),
             T(lang,
               "<strong>IP ünvanı</strong> maşının şəbəkə nömrəsidir. <strong>DNS</strong> (<em>Domain Name System</em>) domen adını şəbəkə ünvanına uyğunlaşdırır. <strong>Marşrutlaşdırıcı</strong> <strong>paketləri</strong> — kiçik məlumat dilimlərini — ötürür. <strong>HTTP</strong> (<em>Hypertext Transfer Protocol</em>) veb resursları üçün sorğu və cavab qaydalarını müəyyənləşdirir.",
               "An <strong>IP address</strong> is a machine’s network number. <strong>DNS</strong> (Domain Name System) maps a domain name to a network address. A <strong>router</strong> forwards <strong>packets</strong> — small slices of data. <strong>HTTP</strong> (Hypertext Transfer Protocol) sets the request-and-response rules for web resources."),
             [T(lang, "Səhifə ünvanını yazanda əvvəl DNS-dən nömrə soruşulur, sonra HTTP həmin maşından səhifəni istəyir, səhifə paketlər şəklində gəlir.",
                "When you type a page address, DNS is asked for the number, then HTTP asks that machine for the page, which arrives in packets.")],
             sid="school-14", num=14),
        term(lang, T(lang, "Parollar, fişinq, zərərli proqram, məxfilik və iki amilli autentifikasiya", "Passwords, phishing, malware, privacy and two-factor authentication"),
             T(lang,
               "<strong>Fişinq</strong> aldadıcı mesaj və ya saytla parol və ya başqa sirri əldə etməyə cəhddir. <strong>Zərərli proqram</strong> zərər vurmaq və ya casusluq etmək üçün yazılmış proqramdır. <strong>İki amilli autentifikasiya</strong> (həm də: iki faktorlu təsdiq) fərqli kateqoriyalardan iki yoxlama vasitəsindən istifadə edir.",
               "<strong>Phishing</strong> is an attempt to obtain a password or another secret through a deceptive message or site. <strong>Malware</strong> is software written to harm or spy. <strong>Two-factor authentication</strong> (also called two-factor confirmation) uses two checks from different categories."),
             [T(lang, "Məktəb hesabına girişdə parol birinci yoxlamadır; ayrıca cihaz və ya tətbiq vasitəsilə təsdiq ikinci amil ola bilər.",
                "On a school account the password is the first check; a confirmation through a separate device or app can be the second factor."),
              T(lang, "Məktəb portalına bənzəyən, amma naməlum saytda «parolunu təsdiqlə» deyən mesaj adi fişinq nümunəsidir.",
                "A message that looks like a school portal but asks you to “confirm your password” on an unknown site is a common phishing pattern.")],
             sid="school-15", num=15),
        term(lang, T(lang, "Şifrələmə, heşləmə və rəqəmsal imzalar", "Encryption, hashing and digital signatures"),
             T(lang,
               "<strong>Şifrələmə</strong> məlumatın məxfiliyini qoruyur: onu yalnız düzgün açarı olan oxuya bilir. <strong>Heşləmə</strong> məlumatın qısa rəqəmsal izini yaradır; izdən əsli faydalı şəkildə bərpa etmək olmur. <strong>Rəqəmsal imza</strong> bütövlüyü və mənşəyi yoxlamağa xidmət edir.",
               "<strong>Encryption</strong> protects the confidentiality of data: only someone with the right key can read it. <strong>Hashing</strong> makes a short digital fingerprint of the data; you cannot usefully turn that fingerprint back into the original. A <strong>digital signature</strong> helps check integrity and origin."),
             [T(lang, "Mesajlaşma tətbiqi mətni yolda şifrələyə bilər. Sayt parolun özünü yox, heşini saxlaya bilər.",
                "A messaging app may encrypt the text on the way. A site may store a hash of your password rather than the password itself.")],
             sid="school-16", num=16),
        group("school-ai", T(lang, "Süni intellekt və verilənlər", "AI and data")),
        term(lang, T(lang, "Süni intellekt adi proqramdan nə ilə fərqlənir", "How AI differs from ordinary software"),
             T(lang,
               "Adi proqram insanın yazdığı qaydaları izləyir. Bir çox <strong>süni intellekt</strong> sistemi, xüsusən <strong>maşın öyrənməsi</strong>, davranışını tam yazılı qayda kitabından yox, <strong>təlim verilənlərindən</strong> — böyük nümunə dəstlərindən — qurur. Süni intellektin bütün üsulları eyni qaydada işləmir.",
               "Ordinary software follows rules a person wrote. Many <strong>AI</strong> systems, especially <strong>machine learning</strong>, build their behaviour from <strong>training data</strong> — large sets of examples — rather than from a complete handwritten rule book. Not every AI method works in the same way."),
             [T(lang, "Spam süzgəcinə bütün mümkün zibil cümlələr verilmir. Ona çoxlu spam və adi məktub nümunəsi göstərilir, sonra yeni məktubun hansına daha çox bənzədiyi qiymətləndirilir.",
                "A spam filter is not given every possible junk sentence. It is shown many examples of spam and ordinary mail, then it estimates which new message looks more like spam.")],
             sid="school-17", num=17),
        term(lang, T(lang, "Təlim verilənləri və maşın öyrənməsində nümunələrin rolu", "Training data and the role of examples in machine learning"),
             T(lang,
               "Təlimdə istifadə olunan nümunələr sistemin nə edə biləcəyini və harada yanılacağını formalaşdırır. Nümunələr dar və ya qərəzli olsa, cavablar da belə olacaq.",
               "The examples used in training shape what the system can do and where it will go wrong. If the examples are narrow or biased, the answers will be too."),
             [T(lang, "Yalnız yay fotoları ilə öyrədilmiş model qarı şəkildəki qüsur kimi səhv adlandıra bilər.",
                "A model trained only on summer photos may mislabel snow as a defect in the picture."),
              T(lang, "Yalnız bir şəraitdə çəkilmiş şəkillərlə öyrədilmiş model başqa şəraitdə zəif nəticə göstərə bilər.",
                "A model trained only on pictures taken in one setting may perform poorly in another setting.")],
             sid="school-18", num=18),
        term(lang, T(lang, "Süni intellekt niyə hallüsinasiya edir və ya qərəzi təkrarlayır", "Why AI can hallucinate or repeat bias"),
             T(lang,
               "<strong>Hallüsinasiya</strong> süni intellekt sisteminin inandırıcı görünən, lakin yanlış və ya əsassız məlumat yaratmasıdır. Sistem yoxlanılmış fakta baxmır, ehtimal olunan söz sırasını proqnozlaşdırır. Təlim verilənlərindəki <strong>qərəzi də təkrarlaya</strong> bilər. İzahda düzgün səslənən cavabla yoxlanmış cavab arasındakı fərq göstərilməlidir.",
               "A <strong>hallucination</strong> is when an AI system produces information that sounds convincing but is false or unsupported. The system is not looking up a checked fact; it is predicting a likely sequence of words. It can also <strong>repeat bias</strong> present in the training data. An explanation should show the difference between an answer that sounds right and an answer that has been checked."),
             [T(lang, "Söhbət botu real görünən məqalə adı uydura bilər, və ya verilənlərdə tez-tez görünən stereotipi təkrarlaya bilər.",
                "A chatbot may invent a paper title that sounds real, or repeat a stereotype that appeared often in the data.")],
             sid="school-19", num=19),
        term(lang, T(lang, "Süni intellektin verdiyi məlumatı və kodu necə yoxlamalı", "How to check information and code produced by AI"),
             T(lang,
               "Süni intellektin çıxışını qaralama sayın. İddiaları etibarlı mənbə ilə tutuşdurun, koda isə etibar etməzdən əvvəl onu işə salın. Bu, yalnız mütəxəssis yox, məktəb səviyyəli bacarıq kimi göstərilir. Stack Overflow 2025 nəticələri də bu yoxlamanı praktik mövzu kimi əsaslandırır. <a href=\"#ref-4\">[4]</a>, <a href=\"#ref-26\">[26]</a>",
               "Treat AI output as a draft. Check claims against a reliable source, and run code before you trust it. This is listed as a school-level skill, not only a specialist one. The 2025 Stack Overflow results also support this check as a practical topic. <a href=\"#ref-4\">[4]</a>, <a href=\"#ref-26\">[26]</a>"),
             [T(lang, "Model tarix və ya düstur yazırsa, istinad olunan səhifəni açın və ya düsturu tanış nümunə ilə yoxlayın.",
                "If a model writes a date or a formula, open the cited page or test the formula with a known example.")],
             sid="school-20", num=20),
        term(lang, T(lang, "Verilənlərin toplanması, qrafiklər, yanıltıcı təsvir və qərəz", "Collecting data, graphs, misleading pictures and bias"),
             T(lang,
               "Süni intellektsiz də verilənlər yanıltmağa bilər. Qrafik miqyası gizlədə, seçmə bir qrupu buraxa, rəngli diaqram isə zəif qanunauyğunluğu güclü göstərə bilər.",
               "Data can mislead even without AI. A graph can hide the scale, a sample can miss a group, and a colourful chart can make a weak pattern look strong."),
             [T(lang, "0-dan yox, 90-dan başlayan sütun diaqramı yaxın iki nəticəni uzaq göstərə bilər.",
                "A bar chart that starts at 90 instead of 0 can make two close results look far apart.")],
             sid="school-21", num=21),
        group("school-make", T(lang, "Nəsə qurmaq", "Making things")),
        term(lang, T(lang, "Sayt, oyun, mobil tətbiq və robototexnikanın əsasları", "The basics of websites, games, mobile apps and robotics"),
             T(lang,
               "Bunlar yuxarıdakı ideyaların real auditoriya ilə qarşılaşdığı ilk praktik mühitlərdir: açılan səhifə, xal toplayan oyun, ayarı saxlayan telefon tətbiqi, hiss edib hərəkət edən robot. Onlar əsaslar kimi göstərilir; hər şagirdin dördünü də qurması tələb deyil. Sadə oyun layihəsi şərtləri, dövrləri və hadisələri birlikdə izah edə bilər.",
               "These are the first practical settings in which the ideas above meet a real audience: a page that loads, a game that keeps score, a phone app that stores a setting, or a robot that senses and moves. They are listed as fundamentals, not as a demand that every pupil build all four. A simple game project can explain conditions, loops and events together."),
             [T(lang, "Sadə oyunda belə dəyişən (xal), dövr (oyun davam edir) və şərt (udulub) lazımdır.",
                "Even a simple game needs a variable (the score), a loop (the game continues) and a condition (the player has won).")],
             sid="school-22", num=22),
        group("school-society", T(lang, "Hesablama və cəmiyyət", "Computing and society")),
        term(lang, T(lang, "Müəllif hüququ, rəqəmsal kimlik, dezinformasiya və məsuliyyətli istifadə", "Copyright, digital identity, disinformation and responsible use"),
             T(lang,
               "Hesablama yalnız texnika deyil. Şagirdlər əsərin kimə məxsus olduğunu, onlayn kimliyin necə kopyalana biləcəyini, yalan iddiaların necə yayıldığını və məsuliyyətli istifadənin nə olduğunu da bilməlidirlər. Layihənin şəkil, səs və mətn mənbələrinin göstərilməsi müəllif hüquqları ilə texniki işi əlaqələndirir.",
               "Computing is not only technique. Pupils also need to know who owns a work, how an online identity can be copied, how false claims spread, and what responsible use looks like. Showing the sources of images, sound and text in a project ties copyright to the technical work."),
             [T(lang, "Şəkli məktəb işinə kredit vermədən qoymaq, onu yükləmək asan olsa belə, müəllif hüququnu poza bilər.",
                "Putting an image into a school project without credit can breach copyright even if the image was easy to download.")],
             sid="school-23", num=23),
    ])



def _university_explanations(lang: str) -> str:
    return "\n".join([
        group("uni-run", T(lang, "Proqramlar necə işləyir", "How programs run")),
        term(lang, T(lang, "Proqramın icra modelləri və vəziyyətin izlənməsi", "Program execution models and tracing state"),
             T(lang,
               "Proqram <strong>vəziyyətin</strong> — dəyişənlərin cari qiymətlərinin və növbəti əmrin — ardıcıl dəyişməsidir. <strong>İzləmə</strong> hər addımdan sonra həmin vəziyyəti yazmaqdır. Sonrakı bir çox yanlış anlama bu prosesin zehni modelinin olmaması ilə bağlanır. <a href=\"#ref-8\">[8]</a>, <a href=\"#ref-9\">[9]</a>",
               "A program is a sequence of changes to <strong>state</strong> — the current values of variables and the next instruction. <strong>Tracing</strong> means writing down that state after each step. Many later misconceptions are linked to the lack of a mental model of this process. <a href=\"#ref-8\">[8]</a>, <a href=\"#ref-9\">[9]</a>"),
             [T(lang, "<code>x = 2</code>; <code>x = x * 3</code> üçün iz: əvvəl <code>x</code> yoxdur; birinci sətirdən sonra <code>x</code> 2-dir; ikinci sətirdən sonra <code>x</code> 6-dır.",
                "For <code>x = 2</code>; <code>x = x * 3</code> a trace is: start with no <code>x</code>; after the first line <code>x</code> is 2; after the second line <code>x</code> is 6.")],
             sid="uni-1", num=1),
        term(lang, T(lang, "Əhatə dairəsi, ömür, parametr ötürmə və təxəllüs", "Scope, lifetime, parameter passing and aliasing"),
             T(lang,
               "<strong>Əhatə dairəsi</strong> və ya <strong>görünmə sahəsi</strong> adın harada əlçatan olduğunu bildirir. <strong>Ömür</strong> saxlanan dəyərin və ya obyektin nə qədər mövcud olduğudur. <strong>Parametr ötürmə</strong> girişlərin funksiyaya necə düşməsidir. <strong>Təxəllüs</strong> (<em>aliasing</em>) iki adın eyni obyektə işarə etməsidir.",
               "<strong>Scope</strong> is where a name is visible. <strong>Lifetime</strong> is how long a stored value or object exists. <strong>Parameter passing</strong> is how inputs enter a function. <strong>Aliasing</strong> means two names refer to the same object, so a change through one name is visible through the other."),
             [T(lang, "Funksiya siyahı alıb element əlavə edirsə, çağıranın siyahısı da dəyişə bilər — hər iki ad eyni siyahıya baxırdı.",
                "If a function receives a list and appends an item, the caller’s list may change too — both names pointed at the same list."),
              T(lang, "İki dəyişən eyni obyektə yönəlirsə, obyekt dəyişdikdə hər iki istinad vasitəsilə həmin dəyişiklik görünür. İstinadların birini başqa obyektə yönəltmək isə fərqli əməliyyatdır.",
                "If two variables point at the same object, a change to the object is visible through both references. Pointing one of the references at a different object is a different operation.")],
             sid="uni-2", num=2),
        term(lang, T(lang, "İstinadlar, göstəricilər və yaddaş idarəsi", "References, pointers and memory management"),
             T(lang,
               "<strong>İstinad</strong> və ya <strong>göstərici</strong> dəyərin özünü yox, yerini saxlayır; dəqiq davranış dildən asılıdır. <strong>Yaddaş idarəsi</strong> həmin yerin nə vaxt yaradılıb azad olunacağına qərardır. Dolayı müraciət bir neçə ildən sonra da çətin qala bilər. <a href=\"#ref-14\">[14]</a>",
               "A <strong>reference</strong> or <strong>pointer</strong> holds the location of a value, not the value itself; the exact behaviour depends on the language. <strong>Memory management</strong> is deciding when that storage is created and released. Indirection can remain difficult even after several years of study. <a href=\"#ref-14\">[14]</a>"),
             [T(lang, "İki dəyişən eyni müştəri qeydinə baxa bilər. Ünvanı hansı dəyişənlə dəyişsən, eyni qeyd dəyişir.",
                "Two variables can point at one customer record. Updating the address through either variable changes the same record.")],
             sid="uni-3", num=3),
        term(lang, T(lang, "Rekursiya və rekursiv çağırış steki", "Recursion and the recursive call stack"),
             T(lang,
               "<strong>Rekursiya</strong> funksiyanın birbaşa və ya dolayı yolla özünü çağırmasıdır; əlavə çağırış tələb etməyən <strong>baza halı</strong>na qədər. Hər çağırış daxili çağırış bitənə qədər <strong>çağırış steki</strong>ndə gözləyir. İzahda həm yeni çağırışların yaranmasını, həm də nəticələrin geri qayıtmasını göstərmək lazımdır. <a href=\"#ref-13\">[13]</a>",
               "<strong>Recursion</strong> is a function calling itself, directly or indirectly, until a <strong>base case</strong> that needs no further call. Each call waits on the <strong>call stack</strong> until the inner call finishes. An explanation should show both the new calls being created and the results coming back. <a href=\"#ref-13\">[13]</a>"),
             [T(lang, "<code>factorial(4)</code> <code>factorial(3)</code>-ü, o da <code>factorial(2)</code>-ni gözləyir, ta <code>factorial(1)</code> 1 qaytarana qədər.",
                "<code>factorial(4)</code> waits for <code>factorial(3)</code>, which waits for <code>factorial(2)</code>, until <code>factorial(1)</code> returns 1.")],
             sid="uni-4", num=4),
        term(lang, T(lang, "Obyekt kimliyi, siniflər, obyektlər, irsiyyət və polimorfizm", "Object identity, classes, objects, inheritance and polymorphism"),
             T(lang,
               "<strong>Sinif</strong> təsvirdir; <strong>obyekt</strong> isə bir nüsxədir. <strong>Kimlik</strong> iki obyektin eyni ədədləri saxlayıb-saxlamamasından çox, hansı obyekt olduğunu soruşur. <strong>İrsiyyət</strong> bir sinfin o birinin quruluşunu yenidən istifadəsinə imkan verir. <strong>Polimorfizm</strong> (həm də: çoxformalıq) eyni interfeysin müxtəlif obyektlərdə fərqli davranış verməsinə imkan yaradır. <strong>Konstruktor</strong> obyekt yaradılarkən onun başlanğıc vəziyyətinin qurulmasında iştirak edir. <a href=\"#ref-12\">[12]</a>",
               "A <strong>class</strong> is a description; an <strong>object</strong> is one instance. <strong>Identity</strong> asks which object you have, not only whether two objects hold the same numbers. <strong>Inheritance</strong> lets a class reuse another’s structure. <strong>Polymorphism</strong> lets the same interface produce different behaviour in different objects. A <strong>constructor</strong> takes part in setting an object’s starting state when it is created. <a href=\"#ref-12\">[12]</a>"),
             [T(lang, "Dairə və düzbucaqlı hər ikisi «sahə» deyə bilər, amma hər biri onu fərqli hesablayır.",
                "Circle and Rectangle can both answer “area”, but each calculates it differently.")],
             sid="uni-5", num=5),
        group("uni-dsa", T(lang, "Verilənlər strukturları və alqoritmlər", "Data structures and algorithms")),
        term(lang, T(lang, "Siyahılar, bağlı strukturlar, steklər, növbələr, ağaclar, heap-lər və qraflar", "Lists, linked structures, stacks, queues, trees, heaps and graphs"),
             T(lang,
               "<strong>Verilənlər strukturu</strong> bəzi əməliyyatların ucuz qalması üçün dəyərləri təşkil etmə üsuludur. Siyahı sıranı saxlayır; stek son gələn birinci çıxır; növbə birinci gələn birinci çıxır; ağac və heap iyerarxiyanı, qraf isə əlaqələri modelləşdirir. Burada <strong>heap</strong> verilənlər strukturu kimi yığını bildirir; eyni söz yaddaş bölgəsi üçün də işlənir. <a href=\"#ref-11\">[11]</a>",
               "A <strong>data structure</strong> is a way of organising values so that some operations stay cheap. A list keeps order; a stack is last-in, first-out; a queue is first-in, first-out; trees and heaps organise hierarchy; a graph models connections. Here a <strong>heap</strong> is a structure; the same word is also used for a region of memory. <a href=\"#ref-11\">[11]</a>"),
             [T(lang, "Brauzerin Geri düyməsi stek kimidir: açdığın son səhifəyə birinci qayıdırsan.",
                "A browser’s Back button behaves like a stack: the last page you opened is the first one you return to.")],
             sid="uni-6", num=6),
        term(lang, T(lang, "Sıralama, axtarış və qraf alqoritmləri", "Sorting, searching and graph algorithms"),
             T(lang,
               "Bunlar elementləri sıraya salmaq, tapmaq və ya əlaqələr üzrə gəzmək üçün standart üsullardır. Tələbə həm üsulu, həm də onun nə vaxt doğru olduğunu görməlidir.",
               "These are standard methods for putting items in order, finding an item, or walking along connections. A student needs to see both the method and when it is the right method."),
             [T(lang, "Sıralanmış sinif siyahısında ad tapmaq üçün ikili axtarışdan istifadə oluna bilər: qalan siyahını dəfələrlə yarıya bölmək.",
                "Finding a name in a sorted class list can use binary search: repeatedly cut the remaining list in half.")],
             sid="uni-7", num=7),
        term(lang, T(lang, "Big-O, ən pis hal və yaddaş–vaxt mübadiləsi", "Big-O, worst case and the space–time trade-off"),
             T(lang,
               "<strong>Big-O</strong> (həm də: Böyük-O) giriş böyüdükcə alqoritmin resurs tələbinin artımına yuxarı sərhəd vermək üçün istifadə olunur; dəqiq saniyə sayı deyil. <strong>Ən pis hal</strong> ən bahalı qanuni girişi soruşur. <strong>Yaddaş–vaxt mübadiləsi</strong> vaxt qazanmaq üçün daha çox yaddaş, və ya əksi, istifadə etməkdir.",
               "<strong>Big-O</strong> is used to give an upper bound on how an algorithm’s demand for resources grows as the input grows; it is not a count of exact seconds. <strong>Worst-case</strong> analysis asks about the most expensive legal input. A <strong>space–time trade-off</strong> means using more memory to save time, or the reverse."),
             [T(lang, "Hər elementi bir dəfə baxmaq xətti vaxtdır. Hər cütə baxmaq siyahı uzandıqca daha sürətlə bahalaşır.",
                "Looking at every item once is linear time. Looking at every pair of items grows much faster as the list lengthens.")],
             sid="uni-8", num=8),
        term(lang, T(lang, "Acgöz alqoritmlər, böl və həll et, dinamik proqramlaşdırma", "Greedy algorithms, divide and conquer, and dynamic programming"),
             T(lang,
               "<strong>Acgöz</strong> üsul yerli ən yaxşı addımı götürür. <strong>Böl və həll et</strong> məsələni parçalayır, hissələri həll edir və birləşdirir. <strong>Dinamik proqramlaşdırma</strong> kəsişən altməsələlərin nəticələrini saxlayır ki, yenidən hesablanmasın. Üsul seçimi və rekurrent əlaqə adi çətinliklər sırasındadır. <a href=\"#ref-20\">[20]</a>, <a href=\"#ref-27\">[27]</a>",
               "A <strong>greedy</strong> method takes the locally best step. <strong>Divide and conquer</strong> splits a problem, solves the parts, and combines them. <strong>Dynamic programming</strong> stores answers to overlapping subproblems so they are not recomputed. Choosing the technique and writing the recurrence are common difficulties. <a href=\"#ref-20\">[20]</a>, <a href=\"#ref-27\">[27]</a>"),
             [T(lang, "Ən az sikkə ilə xırdalamaq, sikkə sistemi imkan verirsə, acgöz ola bilər; bəzi sistemlər daha diqqətli, saxlanılan həll üsulu tələb edir.",
                "Making change with the fewest coins can be greedy if the coin system allows it; some systems need a more careful stored-solution method.")],
             sid="uni-9", num=9),
        group("uni-db", T(lang, "Verilənlər və verilənlər bazaları", "Data and databases")),
        term(lang, T(lang, "Relyasion modelləşdirmə, açarlar, birləşmələr və normallaşdırma", "Relational modelling, keys, joins and normalisation"),
             T(lang,
               "<strong>Relyasion</strong> baza məlumatı cədvəllərdə saxlayır. <strong>Açar</strong> sətri unikal tanıyır. <strong>Birləşmə</strong> (<em>JOIN</em>) bir neçə cədvəlin sətirlərini birləşdirir. <strong>Normallaşdırma</strong> təkrarlanma və yenilənmə problemlərini azaltmaq üçün cədvəllərin təşkilidir.",
               "A <strong>relational</strong> database stores data in tables. A <strong>key</strong> uniquely identifies a row. A <strong>join</strong> combines rows from more than one table. <strong>Normalisation</strong> organises tables so that repetition and update problems are reduced."),
             [T(lang, "Tələbələr və fənlər cədvəlləri qeydiyyat cədvəlində görüşür. Eyni tələbənin bir neçə kursa yazılması nəticədə niyə bir neçə sətir yarandığını göstərir.",
                "A Students table and a Courses table meet in an Enrolment table. Enrolling the same student on several courses shows why the result can contain several rows.")],
             sid="uni-10", num=10),
        term(lang, T(lang, "SQL-də aqreqasiya, alt sorğular və pəncərə funksiyaları", "Aggregation, subqueries and window functions in SQL"),
             T(lang,
               "<strong>SQL</strong> (<em>Structured Query Language</em>) verilənlər bazasına sorğu vermək üçün istifadə olunan dildir. <strong>Aqreqasiya</strong> çoxlu qiymətdən cəm, say və orta kimi ümumi nəticə çıxarır. <strong>Alt sorğu</strong> başqa sorğunun içində yerləşir. <strong>Pəncərə funksiyası</strong> əlaqəli sətirlər üzrə hesab apararaq ayrı sətirləri nəticədə saxlayır. Geniş təhlildə tələbə səhvləri tez-tez birləşmə, alt sorğu və GROUP BY ilə bağlıdır. <a href=\"#ref-16\">[16]</a>",
               "<strong>SQL</strong> (Structured Query Language) is the language used to ask questions of a database. <strong>Aggregation</strong> summarises many values as a sum, a count or an average. A <strong>subquery</strong> sits inside another query. A <strong>window function</strong> computes across related rows while still keeping the separate rows in the result. Large-scale analysis found frequent student errors with joins, subqueries and GROUP BY. <a href=\"#ref-16\">[16]</a>"),
             [T(lang, "Universitetin tələbə və qeydiyyat cədvəlləri JOIN əməliyyatını izah etməyə yaraya bilər. Əvvəlcə birləşmənin sətir sayını artırdığını, sonra GROUP BY-nin həmin sətirləri kurs və ya tələbə üzrə yığdığını göstərmək olar.",
                "University student and enrolment tables can explain a JOIN. First show that the join increases the number of rows, then show how GROUP BY gathers those rows by course or by student.")],
             sid="uni-11", num=11),
        term(lang, T(lang, "Tranzaksiyalar, izolyasiya, kilidləmə və verilənlər bazasının uyğunluğu", "Transactions, isolation, locking and database consistency"),
             T(lang,
               "<strong>Tranzaksiya</strong> əlaqəli əməliyyatları vahid iş kimi idarə edir: birlikdə başa çatmalı və ya birlikdə uğursuz olmalıdır. <strong>İzolyasiya</strong> (həm də: izolə) paralel tranzaksiyaların bir-birinin aralıq nəticələrini necə görə bildiyini müəyyənləşdirir. <strong>Kilidləmə</strong> eyni məlumat üzərində toqquşmanın qarşısını alır. <strong>Uyğunluq</strong> (həm də: tutarlılıq) dəyişiklikdən sonra saxlanan faktların qaydalara əməl etməsidir.",
               "A <strong>transaction</strong> treats related operations as one piece of work: they should finish together or fail together. <strong>Isolation</strong> decides how far parallel transactions may see one another’s intermediate results. <strong>Locking</strong> prevents a clash on the same data. <strong>Consistency</strong> means the stored facts still obey the rules after the change."),
             [T(lang, "Bank köçürməsi bir hesabdan çıxarış etməməli, o biri hesaba da əlavə etməyibsə.",
                "A bank transfer should not subtract from one account unless it also adds to the other.")],
             sid="uni-12", num=12),
        group("uni-sys", T(lang, "Sistemlər", "Systems")),
        term(lang, T(lang, "Proseslər, axınlar, planlaşdırma və virtual yaddaş", "Processes, threads, scheduling and virtual memory"),
             T(lang,
               "<strong>Proses</strong> icra olunan proqramın mühitidir; adətən öz yaddaşı olur. <strong>Axın</strong> həmin mühitdə icra yoludur. <strong>Planlaşdırma</strong> prosessorun növbəti işinin hansı olacağına qərar verir. <strong>Virtual yaddaş</strong> proqramın gördüyü ünvanları fiziki yaddaşdan ayırır. Tələbələr bu mexanizmləri əzbərləyə, amma həllər arasında seçim etməkdə çətinlik çəkə bilərlər. <a href=\"#ref-17\">[17]</a>",
               "A <strong>process</strong> is the environment of a running program; it usually has its own memory. A <strong>thread</strong> is a line of execution inside that environment. <strong>Scheduling</strong> decides which work the processor runs next. <strong>Virtual memory</strong> separates the addresses a program sees from physical memory. Students may memorise these mechanisms and still struggle to choose between solutions. <a href=\"#ref-17\">[17]</a>"),
             [T(lang, "Brauzer hər vərəqə üçün ayrı proses saxlaya bilər ki, bir səhifənin çökməsi o birilərini aparmasın.",
                "A browser can keep one process per tab so that one crashed page does not take down the others.")],
             sid="uni-13", num=13),
        term(lang, T(lang, "Yarış vəziyyətləri, sinxronlaşdırma, qarşılıqlı kilidlənmə və qeyri-determinizm", "Race conditions, synchronisation, deadlock and nondeterminism"),
             T(lang,
               "Bir neçə işin icrası üst-üstə düşdükdə nəticə addımların ardıcıllığından asılı ola bilər. <strong>Yarış vəziyyəti</strong> nəticənin icra ardıcıllığından asılı olmasıdır. <strong>Sinxronlaşdırma</strong> axınları əlaqələndirir. <strong>Qarşılıqlı kilidlənmə</strong> (həm də: tıxac) işlərin bir-birinin saxladığı resursları gözləyərək dayanmasıdır. <strong>Qeyri-determinizm</strong> səhv proqramın bəzi işəsalmalarda düzgün görünə bilməsi deməkdir. Proqramın bir dəfə düzgün işləməsi bütün mümkün icra ardıcıllıqlarında düzgün olduğunu sübut etmir. <a href=\"#ref-15\">[15]</a>",
               "When several pieces of work overlap, the result can depend on the order of the steps. A <strong>race condition</strong> is that dependence on order. <strong>Synchronisation</strong> coordinates threads. <strong>Deadlock</strong> (also called tıxac in the earlier Azerbaijani page) is a standstill in which each side waits for a resource the other holds. <strong>Nondeterminism</strong> means an incorrect program may appear to work on some runs. One correct run does not prove that every legal order is correct. <a href=\"#ref-15\">[15]</a>"),
             [T(lang, "İki axın da «1 yer qalıb» oxuyur və hər ikisi son yeri satır.",
                "Two threads both read “1 seat left” and both sell the last seat."),
              T(lang, "İki axının eyni sayğacı yeniləməsini addımlara bölmək yarış vəziyyətini göstərir.",
                "Splitting the update of the same counter by two threads into steps shows a race condition.")],
             sid="uni-14", num=14),
        term(lang, T(lang, "Şəbəkə protokolları, marşrutlaşdırma, etibarlılıq və sıxlıq", "Network protocols, routing, reliability and congestion"),
             T(lang,
               "<strong>Protokol</strong> maşınlar arasında razılaşdırılmış söhbətdir. <strong>Marşrutlaşdırma</strong> yolu seçir. <strong>Etibarlılıq</strong> itən məlumatın tapılıb-tapılmayacağını və yenidən göndəriləcəyini soruşur. <strong>Sıxlıq</strong> (həm də: tıxaclıq) ortaq yolun həddən artıq yüklənməsidir.",
               "A <strong>protocol</strong> is an agreed conversation between machines. <strong>Routing</strong> chooses a path. <strong>Reliability</strong> asks whether lost data is detected and resent. <strong>Congestion</strong> is overload on a shared path."),
             [T(lang, "Video zəng yol tıxandıqda əbədi donmaq əvəzinə şəkil keyfiyyətini sala bilər.",
                "A video call may drop picture quality when the path is congested rather than freeze forever.")],
             sid="uni-15", num=15),
        term(lang, T(lang, "Autentifikasiya, avtorizasiya, şifrələmə və təhlükəsiz proqram layihələndirməsi", "Authentication, authorisation, encryption and secure software design"),
             T(lang,
               "<strong>Autentifikasiya</strong> «Siz kimsiniz?», <strong>avtorizasiya</strong> isə «Nə etməyə icazəniz var?» sualına cavab verir. Şifrələmə məlumatı yolda və ya saxlancda qoruyur. Təhlükəsiz layihə bunları əvvəldən sistemin hissəsi sayır. Kibertəhlükəsizlikdə zəiflik, təhdid, risk və qorunma tədbiri qarışdırıla bilər. <a href=\"#ref-19\">[19]</a>",
               "<strong>Authentication</strong> answers “Who are you?” <strong>Authorisation</strong> answers “What are you allowed to do?” Encryption protects data on the way or in storage. Secure design treats these as part of the system from the start. In cybersecurity, vulnerability, threat, risk and a protective measure are often mixed up. <a href=\"#ref-19\">[19]</a>"),
             [T(lang, "Giriş kimliyi sübut edir; tələbə olmaq başqa tələbənin qiymətini dəyişmək hüququ vermir.",
                "Logging in proves identity; being a student still does not grant the right to change another student’s marks.")],
             sid="uni-16", num=16),
        term(lang, T(lang, "Paylanmış sistemlər, replikasiya, uyğunluq və konsensus", "Distributed systems, replication, consistency and consensus"),
             T(lang,
               "Paylanmış sistemdə hissələr müxtəlif kompüterlərdə işləyir və şəbəkə ilə əlaqə saxlayır. <strong>Replikasiya</strong> məlumatın surətlərini müxtəlif yerlərdə saxlamaqdır. Nüsxələr razılaşmaya bilər, ona görə <strong>uyğunluq</strong> qaydası və bəzən növbəti dəyər üçün <strong>konsensus</strong> (həm də: razılaşma) üsulu lazımdır.",
               "In a distributed system the parts run on different computers and communicate over a network. <strong>Replication</strong> keeps copies of data in more than one place. Those copies can disagree, so the system needs a <strong>consistency</strong> rule and sometimes a <strong>consensus</strong> method for agreeing on the next value."),
             [T(lang, "İki surətin müvəqqəti əlaqəsiz qalması məlumatların uyğunlaşdırılmasını izah etmək üçün yaxşı başlanğıcdır.",
                "Two copies that are temporarily out of contact are a good starting point for explaining how data is brought back into agreement."),
              T(lang, "Bir neçə serverdə saxlanan sənəddə iki nəfər eyni anda yazırsa, kimin düzəlişinin qalacağına qərar verilməlidir.",
                "If two people type at once in a document saved on several servers, the system must decide whose edit remains.")],
             sid="uni-17", num=17),
        term(lang, T(lang, "Bulud hesablaması, konteynerlər, orkestrasiya və yerləşdirmə", "Cloud computing, containers, orchestration and deployment"),
             T(lang,
               "<strong>Bulud hesablaması</strong> server, saxlanc və şəbəkəni xidmət kimi icarəyə verir. <strong>Konteyner</strong> tətbiqi asılılıqları ilə birlikdə işlətməyi asanlaşdırır. <strong>Orkestrasiya</strong> (həm də: orkestrləşdirmə) çoxlu konteynerin yerləşdirilməsi, işə salınması və idarə edilməsinin əlaqələndirilməsidir. <strong>Yerləşdirmə</strong> yeni versiyanı xidmətə qoymaqdır.",
               "<strong>Cloud computing</strong> rents servers, storage and networks as a service. A <strong>container</strong> makes it easier to run an application together with what it depends on. <strong>Orchestration</strong> coordinates the placing, starting and managing of many containers. <strong>Deployment</strong> is putting a new version into service."),
             [T(lang, "Kurs saytı konteynerdə işləyə bilər ki, eyni obraz həm noutbukda, həm də buludda işləsin.",
                "A course website may run in a container so that the same image works on a laptop and in the cloud.")],
             sid="uni-18", num=18),
        group("uni-ai", T(lang, "Maşın öyrənməsi və iri modellər", "Machine learning and large models")),
        term(lang, T(lang, "Maşın öyrənməsinin qiymətləndirilməsi, həddindən artıq və yetərsiz öyrənmə", "Evaluating machine learning, overfitting and underfitting"),
             T(lang,
               "<strong>Həddindən artıq öyrənmə</strong> (<em>overfitting</em>) modelin təlim məlumatının özəlliklərinə həddən çox uyğunlaşıb yeni nümunələrdə yanılmasıdır. <strong>Yetərsiz öyrənmə</strong> (<em>underfitting</em>) modelin əsas əlaqələri kifayət qədər öyrənməməsidir. Qiymətləndirmə modelin görmədiyi verilənlərlə aparılmalıdır.",
               "<strong>Overfitting</strong> means the model fitted the peculiarities of the training data too closely and then fails on new examples. <strong>Underfitting</strong> means the model did not learn the main relationships well enough. Evaluation must use data the model has not already seen."),
             [T(lang, "Keçən ilin sinifindəki hər tələbəni tanıyan, amma yeni tələbəni yerləşdirə bilməyən model artıq uyğunlaşıb.",
                "A model that names every student in last year’s class but cannot place a new student has overfitted.")],
             sid="uni-19", num=19),
        term(lang, T(lang, "Verilənlər sızması, sinif balanssızlığı, model qərəzi və izah edilə bilmə", "Data leakage, class imbalance, model bias and explainability"),
             T(lang,
               "<strong>Verilənlər sızması</strong> modelə proqnoz anında olmayacağı məlumatı təsadüfən verməkdir. <strong>Sinif balanssızlığı</strong> nümunə kateqoriyalarının sayca qeyri-bərabər olmasıdır. <strong>Qərəz</strong> nəticələrin müəyyən qruplar üçün sistemli şəkildə təhrif olunması ola bilər. <strong>İzah edilə bilmə</strong> nəticəyə təsir edən amillərin insanlar üçün açıqlana bilməsidir.",
               "<strong>Data leakage</strong> is accidentally giving the model information it would not have at prediction time. <strong>Class imbalance</strong> means the example categories are unequal in number. <strong>Bias</strong> here can be a systematic distortion of results for certain groups. <strong>Explainability</strong> is being able to say, in a way people can follow, which factors affected the result."),
             [T(lang, "Sınaq məlumatının təlimə qarışması qiymətləndirmə kontekstində verilənlər sızmasına nümunədir.",
                "Mixing the test data into training is an example of leakage in evaluation."),
              T(lang, "Tibbi model xəstəxana adını görürsə, əlamətlərdən yox, həmin xəstəxananın tipik xəstələrindən «proqnoz» verə bilər.",
                "If a medical model sees the hospital name, it may “predict” from that hospital’s typical patients rather than from the symptoms.")],
             sid="uni-20", num=20),
        term(lang, T(lang, "Böyük dil modellərində tokenləşdirmə, vektor təmsilləri, diqqət, axtarış və hallüsinasiya", "Tokenisation, vector representations, attention, retrieval and hallucination in large language models"),
             T(lang,
               "<strong>LLM</strong> — Large Language Model, yəni böyük dil modelidir. <strong>Tokenləşdirmə</strong> mətni modelin emal etdiyi hissələrə bölür; token həmişə bütöv söz olmur. <strong>Vektor təmsili</strong> (həm də: yerləşdirmə vektoru, <em>embedding</em>) həmin hissələri ədədlərlə ifadə edir. <strong>Diqqət mexanizmi</strong> kontekstdəki hissələr arasındakı əlaqələri çəkiləndirir. Xarici mənbədən məlumat gətirilməsi cavab üçün əlavə əsas verə bilər, lakin düzgünlüyə avtomatik zəmanət yaratmır.",
               "An <strong>LLM</strong> is a large language model. <strong>Tokenisation</strong> splits text into the pieces the model processes; a token is not always a whole word. A <strong>vector representation</strong> (also called an embedding) expresses those pieces as numbers. An <strong>attention mechanism</strong> weighs relations among pieces in the context. Fetching information from an outside source can give an answer extra grounding, but it does not automatically guarantee correctness."),
             [T(lang, "Eyni söz bir və ya bir neçə token ola bilər; buna görə bəzi modellər qeyri-adi yazılış və ya kodlarda büdrəyir.",
                "The same word may become one token or several, which is why some models stumble on unusual spellings or codes.")],
             sid="uni-21", num=21),
        group("uni-soft", T(lang, "Proqram işi", "Software work")),
        term(lang, T(lang, "Proqramın yoxlanması, arxitektura, versiyaların idarə edilməsi və davamlı inteqrasiya", "Testing software, architecture, version control and continuous integration"),
             T(lang,
               "<strong>Yoxlama</strong> kodun nəzərdə tutulanı edib-etmədiyinə baxır. <strong>Arxitektura</strong> iri miqyaslı quruluşdur. <strong>Versiya nəzarəti</strong> (çox vaxt Git) kimin nəyi dəyişdiyini yazır. <strong>Davamlı inteqrasiya</strong> (<em>Continuous Integration</em>, CI) kod dəyişikliklərini müntəzəm birləşdirib avtomatlaşdırılmış yoxlamalardan keçirməsidir.",
               "<strong>Testing</strong> checks that code does what was intended. <strong>Architecture</strong> is the large-scale structure. <strong>Version control</strong> (often Git) records who changed what. <strong>Continuous integration</strong> (CI) regularly merges code changes and runs automated checks."),
             [T(lang, "Komanda giriş səhifəsini kimin son dəyişdiyini və o dəyişiklikdən sonra testlərin keçib-keçmədiyini görə bilər.",
                "A team can see who last changed a login page and whether the tests still pass after that change.")],
             sid="uni-22", num=22),
        term(lang, T(lang, "Funksional, məntiqi və eynizamanlı proqramlaşdırma paradiqmaları", "Functional, logic and concurrent programming paradigms"),
             T(lang,
               "<strong>Paradiqma</strong> proqramın qurulmasına ümumi yanaşmadır. Funksional üslub funksiya və dəyərləri, məntiqi üslub münasibət və axtarışı, eynizamanlı üslub isə vaxtca kəsişən işi önə çıxarır. <strong>Eynizamanlılıq</strong> bir neçə işin irəliləməsinin üst-üstə düşməsidir; <strong>paralellik</strong> işlərin həqiqətən eyni anda icrasıdır.",
               "A <strong>paradigm</strong> is a general approach to building a program. Functional style emphasises functions and values; logic style emphasises relations and search; concurrent style emphasises work that overlaps in time. <strong>Concurrency</strong> is the overlapping progress of several pieces of work; <strong>parallelism</strong> is work that truly runs at the same time."),
             [T(lang, "Eyni «ən qısa yol» məsələsi funksional dildə funksiya tərkibi, məntiqi dildə məhdudiyyət, eynizamanlı modeldə isə bir neçə axtarışın üst-üstə düşməsi kimi görünə bilər.",
                "The same “shortest path” problem can look like function composition in a functional language, like a constraint in a logic language, and like several searches overlapping in a concurrent model.")],
             sid="uni-23", num=23),
        term(lang, T(lang, "Kompilyatorlar, interpretatorlar və proqramlaşdırma dillərinin semantikası", "Compilers, interpreters and programming-language semantics"),
             T(lang,
               "<strong>Interpretator</strong> proqramı birbaşa yerinə yetirir. <strong>Kompilyator</strong> onu əvvəlcə başqa formaya çevirir. <strong>Semantika</strong> dil konstruksiyalarının nə məna daşıdığını müəyyən edir — proqramın necə yazıldığından çox, nə etməyə icazəsi olduğu.",
               "An <strong>interpreter</strong> carries out a program directly. A <strong>compiler</strong> first translates it into another form. <strong>Semantics</strong> is the meaning of the language’s constructions — what a program is allowed to do, not only how it is written."),
             [T(lang, "Eyni qısa proqramı əvvəl sətir-sətir izləmək, sonra «bu dil <code>x = x + 1</code> deyərkən dəqiq nə edir?» sualını vermək semantikanı kompilyasiya və ya interpretasiya mexanizmindən ayırmağa kömək edir.",
                "First tracing the same short program line by line, then asking “what exactly does this language do with <code>x = x + 1</code>?”, helps separate semantics from the mechanism of compilation or interpretation.")],
             sid="uni-24", num=24),
        group("uni-theory", T(lang, "Hesablama nəzəriyyəsi", "Theory of computation")),
        term(lang, T(lang, "Avtomatlar, hesablana bilmə, reduksiya, P, NP və NP-tamlıq", "Automata, computability, reductions, P, NP and NP-completeness"),
             T(lang,
               "<strong>Avtomat</strong> vəziyyət və keçidlərlə təsvir olunan formal modeldir. <strong>Hesablana bilmə</strong> məsələnin alqoritmlə həllinin mümkün olub-olmadığını araşdırır. <strong>Reduksiya</strong> (həm də: ixtisar) bir məsələni başqa məsələ vasitəsilə həll etməyə uyğun çevirmədir. <strong>P</strong> polinomial vaxtda həll edilən qərar məsələləridir. <strong>NP</strong> üçün müsbət cavabın uyğun sübutu polinomial vaxtda yoxlana bilir. NP «polinomial olmayan» demək deyil. <strong>NP-tam</strong> məsələ NP-dədir və bütün NP məsələləri ona polinomial vaxtda reduksiya edilə bilir.",
               "An <strong>automaton</strong> is a formal model described by states and transitions. <strong>Computability</strong> asks whether a problem can be solved by an algorithm at all. A <strong>reduction</strong> is a transformation that lets one problem be solved through another. <strong>P</strong> is the class of decision problems solvable in polynomial time. For <strong>NP</strong>, a suitable proof of a yes-answer can be checked in polynomial time. NP does not mean “not polynomial”. An <strong>NP-complete</strong> problem is in NP, and every NP problem can be reduced to it in polynomial time."),
             [T(lang, "A məsələsinin hər nümunəsini B məsələsinin nümunəsinə çevirə bilsən, B üçün sürətli üsul A üçün də sürətli üsul verər.",
                "If you can turn every instance of problem A into an instance of problem B, then a fast method for B would also give a fast method for A.")],
             sid="uni-25", num=25),
    ])



REFS = [
    ("1", "CSTA’s 2026 PK–12 Standards", "https://csteachers.org/pk12standards/"),
    ("2", "ACM/IEEE-CS/AAAI CS2023 — knowledge areas", "https://csed.acm.org/knowledge-areas/"),
    ("3", "AP Computer Science Principles", "https://apcentral.collegeboard.org/courses/ap-computer-science-principles"),
    ("4", "2025 Stack Overflow Developer Survey", "https://survey.stackoverflow.co/2025/technology"),
    ("5", "GitHub Octoverse 2025", "https://github.blog/news-insights/octoverse/octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/"),
    ("6", "Qian and Lehman’s literature review", "https://doi.org/10.1145/3077618"),
    ("7", "20-year CS1 replication study", "https://doi.org/10.1145/3730405"),
    ("8", "Sorva’s notional-machine research", "https://doi.org/10.1145/2483710.2483713"),
    ("9", "Study of variable evaluation", "https://doi.org/10.1145/3017680.3017724"),
    ("10", "Systematic review of debugging instruction", "https://doi.org/10.1145/3690652"),
    ("11", "DSA systematic review", "https://doi.org/10.1080/08993408.2026.2633989"),
    ("12", "Long-term OOP study", "https://doi.org/10.1080/08993400500224310"),
    ("13", "Recursion concept inventory", "https://doi.org/10.1080/08993408.2017.1414728"),
    ("14", "Indirection study", "https://doi.org/10.15388/infedu.2507.015"),
    ("15", "Concurrency study", "https://doi.org/10.15388/infedu.2021.29"),
    ("16", "SQL misconception study", "https://doi.org/10.1145/2899415.2899464"),
    ("17", "Operating-systems concept inventory", "https://doi.org/10.1145/2538862.2538886"),
    ("18", "Number-representation study", "https://doi.org/10.1080/08993408.2011.611712"),
    ("19", "Cybersecurity misconception study", "https://digitalcommons.kennesaw.edu/jcerp/vol2018/iss1/5/"),
    ("20", "Replication study on dynamic programming", "https://doi.org/10.1080/08993408.2022.2079865"),
    ("21", "Study of pupils’ AI conceptions", "https://doi.org/10.1016/j.caeai.2022.100095"),
    ("22", None, "https://daab-waas.com/az/complex-topics.html"),
    ("23", "CS2023 official page", "https://csed.acm.org/"),
    ("24", "CS2023 knowledge and competency model", "https://csed.acm.org/wp-content/uploads/2024/04/1.3-Introduction-to-Knowledge-Model.pdf"),
    ("25", "Survey methodology", "https://survey.stackoverflow.co/2025/methodology"),
    ("26", "Survey AI section", "https://survey.stackoverflow.co/2025/ai"),
    ("27", "Dynamic-programming concept inventory", "https://arxiv.org/abs/2411.14655"),
    ("28", "Validation and use of SCS1", "https://www.sci.sdsu.edu/crmse/msed/papers/parker2-parker-guzdial-engleman_SCS1.pdf"),
    ("29", None, "https://daab-waas.com/az/complex-topics-informatics.html"),
    ("30", None, "https://daab-waas.com/az/complex-topics-approach.html"),
]



def _closing_sections(lang: str) -> str:
    first12 = numbered_text([
        T(lang, "Generativ süni intellekt və ChatGPT tipli sistemlər necə işləyir", "How generative AI and ChatGPT-like systems work"),
        T(lang, "Süni intellekt niyə inandırıcı görünən yanlış cavablar verir", "Why AI gives answers that sound convincing but are wrong"),
        T(lang, "Proqram işləyərkən kompüterdə nə baş verir", "What happens inside the computer when a program runs"),
        T(lang, "Dəyişənlər və <code>x = x + 1</code> əmrinin mənası", "Variables and the meaning of <code>x = x + 1</code>"),
        T(lang, "Kod yazmazdan əvvəl alqoritmi necə qurmaq olar", "How to build an algorithm before writing code"),
        T(lang, "Dövrlər necə işləyir və sonsuz dövr niyə yaranır", "How loops work and why an infinite loop starts"),
        T(lang, "Funksiyalar, parametrlər, ekrana çıxarılan nəticələr və qaytarılan qiymətlər", "Functions, parameters, printed output and return values"),
        T(lang, "Proqram səhvlərini tapmaq və düzəltmək üçün praktik üsul", "A practical method for finding and fixing program errors"),
        T(lang, "İnternet veb səhifəni istifadəçiyə necə çatdırır", "How the Internet delivers a web page to the user"),
        T(lang, "Kompüter mətn, təsvir və səsi necə təqdim edir", "How a computer represents text, pictures and sound"),
        T(lang, "Parollar, şifrələmə və rəqəmsal imzalar necə işləyir", "How passwords, encryption and digital signatures work"),
        T(lang, "Verilənlər necə yanlış nəticəyə gətirə bilər və qərəzli təhlili necə tanımaq olar", "How data can lead to a wrong conclusion, and how to recognise biased analysis"),
    ])
    glossary_items = [
        ("AI / SI", T(lang, "Artificial Intelligence və süni intellekt. İnsan zəkası ilə əlaqələndirilən tapşırıqları yerinə yetirən hesablama üsulları və sistemləri.", "Artificial Intelligence. Computing methods and systems that carry out tasks associated with human intelligence.")),
        ("API", T(lang, "Application Programming Interface. Proqramların bir-biri ilə məlumat və əmrlər mübadiləsi üçün interfeys.", "Application Programming Interface. An interface for programs to exchange data and commands.")),
        ("CPU", T(lang, "Central Processing Unit. Əmrləri icra edən mərkəzi prosessor.", "Central Processing Unit. The processor that carries out instructions.")),
        ("DNS", T(lang, "Domain Name System. Domen adlarını IP ünvanları ilə əlaqələndirən sistem.", "Domain Name System. The system that links domain names to IP addresses.")),
        ("HTTP", T(lang, "Hypertext Transfer Protocol. Vebdə sorğu və cavab mübadiləsi üçün protokol.", "Hypertext Transfer Protocol. The protocol for request and response on the Web.")),
        ("IP", T(lang, "Internet Protocol. Şəbəkələr arasında paketlərin ünvanlanması və ötürülməsi üçün protokol.", "Internet Protocol. The protocol for addressing and forwarding packets between networks.")),
        ("IoT", T(lang, "Internet of Things. Sensor və qurğuların şəbəkə vasitəsilə məlumat mübadiləsi apardığı Əşyaların İnterneti.", "Internet of Things. Sensors and devices exchanging data over a network.")),
        ("SQL", T(lang, "Structured Query Language. Verilənlər bazalarında məlumatla işləmək üçün sorğu dili.", "Structured Query Language. The query language for working with data in databases.")),
        ("LLM", T(lang, "Large Language Model. Mətnlə işləyən böyük dil modeli.", "Large Language Model. A large model that works with text.")),
        ("OOP", T(lang, "Object-Oriented Programming. Verilənləri və əməliyyatları obyektlər ətrafında quran yanaşma.", "Object-Oriented Programming. An approach that organises data and operations around objects.")),
        ("DSA", T(lang, "Data Structures and Algorithms. Verilənlər strukturları və alqoritmlər.", "Data Structures and Algorithms.")),
        ("CI", T(lang, "Kontekstdən asılı olaraq Continuous Integration — davamlı inteqrasiya, və ya Concept Inventory — anlayışları ölçən diaqnostik test.", "Depending on context: Continuous Integration, or a Concept Inventory — a diagnostic test of ideas.")),
        ("CS1 / SCS1", T(lang, "CS1 ilkin kompüter elmləri və ya proqramlaşdırma kursudur. SCS1 — Second CS1 həmin səviyyədə anlayışları ölçən alətdir.", "CS1 is a first computer-science or programming course. SCS1 — Second CS1 — is a tool that measures ideas at that level.")),
        ("Big-O", T(lang, "Girişin ölçüsü artdıqca resurs tələbinin artımına asimptotik yuxarı sərhəd verən işarələmə. Həm də Böyük-O yazılır.", "Notation that gives an asymptotic upper bound on how resource demand grows as the input grows.")),
        ("P / NP", T(lang, "P polinomial vaxtda həll edilən qərar məsələləridir. NP üçün müsbət cavabın uyğun sübutu polinomial vaxtda yoxlana bilir. NP «polinomial olmayan» demək deyil.", "P is decision problems solvable in polynomial time. For NP, a suitable proof of a yes-answer can be checked in polynomial time. NP does not mean “not polynomial”.")),
        (T(lang, "NP-tamlıq və reduksiya", "NP-completeness and reduction"), T(lang, "NP-tam məsələ NP-dədir və bütün NP məsələləri ona polinomial vaxtda reduksiya edilə bilir. Veb səhifə eyni anlayışı bəzən ixtisar adlandırmışdı.", "An NP-complete problem is in NP, and every NP problem can be reduced to it in polynomial time.")),
        (T(lang, "Bul məntiqi", "Boolean logic"), T(lang, "Doğru və yanlış qiymətlərinə, eləcə də VƏ, VƏ YA, DEYİL əməliyyatlarına əsaslanan məntiq.", "Logic based on true and false values and on AND, OR and NOT.")),
        (T(lang, "Görünmə sahəsi və yaşam müddəti", "Scope and lifetime"), T(lang, "Görünmə sahəsi adın harada əlçatan olduğunu, yaşam müddəti isə obyektin nə qədər mövcud olduğunu bildirir.", "Scope is where a name is available; lifetime is how long an object exists.")),
        (T(lang, "Parametr və qaytarılan qiymət", "Parameter and return value"), T(lang, "Parametr funksiyanın girişini qəbul edir. Qaytarılan qiymət nəticəni çağıran hissəyə ötürür.", "A parameter accepts a function’s input. A return value passes the result back to the caller.")),
        (T(lang, "İstinad, göstərici və aliasing", "Reference, pointer and aliasing"), T(lang, "İstinad və göstərici obyektə müraciət vasitələridir; dəqiq davranış dildən asılıdır. Aliasing eyni obyektə bir neçə adla çıxışdır.", "A reference or pointer is a way of referring to an object; exact behaviour depends on the language. Aliasing is access to the same object through more than one name.")),
        (T(lang, "Stek və heap", "Stack and heap"), T(lang, "Stek son daxil olanın ilk çıxması prinsipi ilə işləyir; çağırış steki funksiyaların icrasını izləyir. Heap yaddaş bölgəsi və ya ayrıca yığın strukturu ola bilər.", "A stack is last-in, first-out; the call stack tracks function execution. Heap may mean a memory region or a separate heap structure.")),
        (T(lang, "Rekursiya və baza halı", "Recursion and base case"), T(lang, "Rekursiya funksiyanın özünü çağırmasıdır. Baza halı yeni çağırışa ehtiyac olmayan dayanma vəziyyətidir.", "Recursion is a function calling itself. The base case is the stopping situation that needs no new call.")),
        (T(lang, "İrsiyyət və polimorfizm", "Inheritance and polymorphism"), T(lang, "İrsiyyət siniflər arasında xüsusiyyətlərin ötürülməsidir. Polimorfizm (çoxformalıq) eyni interfeysin fərqli davranış verməsinə imkan yaradır.", "Inheritance passes features between classes. Polymorphism lets the same interface produce different behaviour.")),
        (T(lang, "Normallaşdırma", "Normalisation"), T(lang, "Relyasion bazada təkrarlanma və yenilənmə problemlərini azaltmaq üçün cədvəllərin təşkili.", "Organising tables in a relational database so that repetition and update problems are reduced.")),
        ("JOIN", T(lang, "Əlaqəli cədvəllərin məlumatını birləşdirir. Aqreqasiya çoxlu qiymətdən cəm, say və orta çıxarır.", "Combines data from related tables. Aggregation draws a sum, count or average from many values.")),
        (T(lang, "Alt sorğu və pəncərə funksiyası", "Subquery and window function"), T(lang, "Alt sorğu başqa sorğunun içində yerləşir. Pəncərə funksiyası əlaqəli sətirlər üzrə hesab aparıb ayrı sətirləri saxlayır.", "A subquery sits inside another query. A window function computes across related rows and still keeps the separate rows.")),
        (T(lang, "Tranzaksiya və izolyasiya", "Transaction and isolation"), T(lang, "Tranzaksiya əlaqəli əməliyyatları vahid iş kimi idarə edir. İzolyasiya paralel tranzaksiyaların aralıq nəticələri necə görə bildiyini müəyyənləşdirir.", "A transaction treats related operations as one piece of work. Isolation decides how far parallel transactions may see intermediate results.")),
        (T(lang, "Eynizamanlılıq və paralellik", "Concurrency and parallelism"), T(lang, "Eynizamanlılıq işlərin irəliləməsinin üst-üstə düşməsidir. Paralellik işlərin həqiqətən eyni anda icrasıdır.", "Concurrency is overlapping progress. Parallelism is work that truly runs at the same time.")),
        (T(lang, "Yarış vəziyyəti və kilidlənmə", "Race condition and deadlock"), T(lang, "Yarış vəziyyətində nəticə icra ardıcıllığından asılı olur. Qarşılıqlı kilidlənmə (tıxac) işlərin bir-birini gözləyərək dayanmasıdır.", "In a race condition the result depends on execution order. Deadlock is a standstill in which each side waits for the other.")),
        (T(lang, "Proses, axın və virtual yaddaş", "Process, thread and virtual memory"), T(lang, "Proses icra olunan proqramın mühitidir; axın həmin mühitdə icra yoludur. Virtual yaddaş proqramın gördüyü ünvanları fiziki yaddaşdan ayırır.", "A process is the environment of a running program; a thread is a line of execution in that environment. Virtual memory separates the addresses a program sees from physical memory.")),
        (T(lang, "Autentifikasiya və avtorizasiya", "Authentication and authorisation"), T(lang, "Autentifikasiya kimliyi, avtorizasiya isə əməliyyatı etməyə icazəni yoxlayır.", "Authentication checks identity; authorisation checks permission to perform an action.")),
        (T(lang, "Fişinq və iki amilli autentifikasiya", "Phishing and two-factor authentication"), T(lang, "Fişinq aldadıcı mesaj və ya saytla məlumat əldə etməyə cəhddir. İki amilli autentifikasiya (iki faktorlu təsdiq) fərqli kateqoriyalardan iki yoxlama istifadə edir.", "Phishing is an attempt to obtain information through a deceptive message or site. Two-factor authentication uses two checks from different categories.")),
        (T(lang, "Şifrələmə, heşləmə və imza", "Encryption, hashing and signature"), T(lang, "Şifrələmə məlumatı açarla qoruyur. Heşləmə qısa rəqəmsal iz yaradır. Rəqəmsal imza bütövlüyü və imzalayanla əlaqəni yoxlamağa imkan verir.", "Encryption protects data with a key. Hashing makes a short digital fingerprint. A digital signature helps check integrity and the link to the signer.")),
        (T(lang, "Təlim və qiymətləndirmə", "Training and evaluation"), T(lang, "Təlim zamanı model nümunələrdən öyrənir. Qiymətləndirmə onun ayrıca məlumat üzərində necə işlədiyini yoxlayır.", "During training a model learns from examples. Evaluation checks how it works on separate data.")),
        (T(lang, "Həddindən artıq və yetərsiz öyrənmə", "Overfitting and underfitting"), T(lang, "Overfitting zamanı model təlim məlumatının özəlliklərinə həddən çox uyğunlaşır. Underfitting zamanı əsas əlaqələri kifayət qədər öyrənmir.", "In overfitting the model fits the peculiarities of the training data too closely. In underfitting it does not learn the main relationships well enough.")),
        (T(lang, "Sinif balanssızlığı və qərəz", "Class imbalance and bias"), T(lang, "Sinif balanssızlığı nümunə kateqoriyalarının sayca qeyri-bərabər olmasıdır. Qərəz nəticələrin müəyyən qruplar üçün sistemli təhrifidir.", "Class imbalance means example categories are unequal in number. Bias can be a systematic distortion of results for certain groups.")),
        (T(lang, "İzah edilə bilmə", "Explainability"), T(lang, "Modelin nəticəsinə təsir edən amillərin insanlar üçün başadüşülən şəkildə açıqlana bilməsi.", "Being able to say, in a way people can follow, which factors affected a model’s result.")),
        (T(lang, "Token, vektor təmsili və diqqət", "Token, vector representation and attention"), T(lang, "Token mətnin emal vahididir; həmişə bütöv söz olmur. Vektor təmsili onu ədədlərlə göstərir. Diqqət mexanizmi kontekst hissələri arasındakı əlaqələri çəkiləndirir.", "A token is a unit of text processing; it is not always a whole word. A vector representation shows it as numbers. Attention weighs relations among pieces of context.")),
        ("Git / GitHub", T(lang, "Git dəyişiklik tarixçəsini izləyən versiya idarəetmə sistemidir. GitHub Git layihələrinin saxlanması və birgə işlənməsi üçün platformadır.", "Git is a version-control system that tracks the history of changes. GitHub is a platform for storing Git projects and working on them together.")),
        (T(lang, "İkiyə tamamlayıcı kod", "Two’s complement"), T(lang, "Sabit bit sayında işarəli tam ədədlərin, o cümlədən mənfi ədədlərin təqdim edilməsi üsulu.", "A way of representing signed integers, including negative numbers, in a fixed number of bits.")),
        (T(lang, "Avtomat və hesablana bilmə", "Automaton and computability"), T(lang, "Avtomat vəziyyət və keçidlərlə təsvir olunan formal modeldir. Hesablana bilmə məsələnin alqoritmlə həllinin mümkün olub-olmadığını araşdırır.", "An automaton is a formal model of states and transitions. Computability asks whether a problem can be solved by an algorithm.")),
        (T(lang, "Müştəri və server", "Client and server"), T(lang, "Müştəri xidmət üçün sorğu göndərir, server həmin sorğunu emal edib cavab verir.", "A client sends a request for a service; a server processes that request and replies.")),
        (T(lang, "İnsan xüsusiyyətləri aid etmə", "Anthropomorphism"), T(lang, "Sistemə insan kimi düşüncə, niyyət və hisslər aid etmək. Süni intellekt barədə izahlarda bu fərziyyə mexanizmin başa düşülməsini çətinləşdirə bilər.", "Attributing human thought, intention and feeling to a system. In explanations of AI this assumption can make the mechanism harder to understand.")),
    ]
    gloss_html = '<dl class="cta-glossary">' + "".join(
        f"<div><dt>{esc(name)}</dt><dd>{text}</dd></div>" for name, text in glossary_items
    ) + "</dl>"

    ref22 = T(lang, "Müsabiqənin açıq dəvəti. Yenidən işlənmiş sənəddə yerli inkişaf ünvanı da göstərilib.", "The public invitation to the competition. The reworked document also listed a local development address.")
    ref29 = T(lang, "Bu mövzu bələdçisinin veb nüsxəsi", "The web copy of this topic guide")
    ref30 = T(lang, "Müsabiqənin təşkili — işçi plan", "Organisation of the competition — working plan")
    titles = {r[0]: r[1] for r in REFS}
    titles["22"] = ref22
    titles["29"] = ref29
    titles["30"] = ref30
    refs_html = '<ol class="cta-refs">' + "".join(
        f'<li id="ref-{num}">[{num}] {esc(titles[num]) if num not in ("22", "29", "30") else titles[num]} — <a href="{url}" target="_blank" rel="noopener noreferrer">{esc(url)}</a></li>'
        for num, _title, url in REFS
    ) + "</ol>"

    return f"""
<section class="cta-card" id="difficult">
<h2>{T(lang, "Mövzuların öyrənilməsini çətinləşdirən səbəblər", "Why these topics are difficult")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Mənbələr öyrənənlərin zəif olduğunu iddia etmir. Tədris tədqiqatlarının nəticəsini göstərir: ideyaların özü asanlıqla səhv oxunur, mütəxəssislər isə öz qısaltmalarını çox vaxt görmür. Bu nəticələr konkret araşdırmaların auditoriya və metodlarına bağlıdır. Onlardan yerli auditoriyada yoxlanacaq izah və tapşırıqlar hazırlamaq üçün istifadə etmək daha məqsədəuyğundur.",
"The sources do not claim that learners are weak. They report findings from teaching research: the ideas themselves are easy to misread, and experts often cannot see their own shortcuts. These findings are tied to the audiences and methods of particular studies. It is more useful to take them as a basis for explanations and tasks that you then check with a local audience."))}
<h3>{T(lang, "Proqramlaşdırmada üç əsas çətinlik", "Three main difficulties in programming")}</h3>
{p(T(lang,
"İlkin proqramlaşdırma üzrə ədəbiyyat icmalı çətinlikləri sintaksis, anlayışların mənimsənilməsi və məsələ həlli strategiyası ilə əlaqələndirir. <strong>Sintaksis</strong> dilin yazılış qaydalarıdır. Bu qaydaları bilmək proqramın niyə belə işlədiyini başa düşmək üçün təkbaşına kifayət etmir. Mənbə Qian və Lehmanın ədəbiyyat icmalına istinad edir. <a href=\"#ref-6\">[6]</a>",
"A literature review of introductory programming links the difficulties to syntax, conceptual knowledge and problem-solving strategy. <strong>Syntax</strong> is the written rules of the language. Knowing those rules is not enough, on its own, to understand why a program behaves as it does. The source points to Qian and Lehman’s literature review. <a href=\"#ref-6\">[6]</a>"))}
{p(T(lang,
"Əvvəlki araşdırmanı yenidən yoxlayan tədqiqatda müəllimlərin rekursiya, funksiyalar, dövrlər, səhvlərin tapılması və koddan əvvəl düşünmə və planlaşdırmanı öyrətməkdə çətinlik çəkdiyi göstərilir. <strong>Təkrar tədqiqat</strong> (<em>replication</em>) əvvəlki nəticələrin başqa vaxtda və ya şəraitdə yenidən müşahidə olunub-olunmadığını yoxlayır. <a href=\"#ref-7\">[7]</a>",
"A study that re-checked earlier research found that teachers struggle especially with teaching recursion, functions, loops, finding errors, and thinking and planning before code. A <strong>replication</strong> asks whether earlier results are seen again at another time or in another setting. <a href=\"#ref-7\">[7]</a>"))}
<h3>{T(lang, "Proqramın işləməsi haqqında düzgün təsəvvür", "A correct picture of how a program runs")}</h3>
{p(T(lang,
"Öyrənən kompüterin əmrləri necə yerinə yetirdiyinə dair düzgün zehni model qurmadıqda dəyişənlər, dövrlər, funksiyalar, istinadlar və rekursiya bir-biri ilə əlaqəsi zəif qaydalar kimi görünə bilər. <strong>Notional machine</strong> proqramın icrasını izah edən sadələşdirilmiş tədris modelidir. İcra ardıcıllığını, yaddaşdakı qiymətləri və çağırışları görünən etmək bu məqsədə xidmət edir. <a href=\"#ref-8\">[8]</a>, <a href=\"#ref-9\">[9]</a>",
"If a learner does not build a correct mental model of how the computer carries out commands, variables, loops, functions, references and recursion can look like weakly connected rules. A <strong>notional machine</strong> is a simplified teaching model of program execution. Making the order of execution, the values in memory and the calls visible serves that aim. <a href=\"#ref-8\">[8]</a>, <a href=\"#ref-9\">[9]</a>"))}
<h3>{T(lang, "Səhvlərin tapılması və düzəldilməsi", "Finding and fixing errors")}</h3>
{p(T(lang,
"Təcrübəli proqramçı səhv axtararkən çox vaxt özünün artıq avtomatlaşdırdığı düşüncə addımlarından istifadə edir. Bu addımlar açıq izah edilmədikdə yeni başlayan yalnız hazır düzəlişi görür. Tədrisdə ehtimalın necə qurulduğunu, hansı yoxlamanın seçildiyini və nəticənin necə şərh edildiyini göstərmək vacibdir. <a href=\"#ref-10\">[10]</a>",
"When an experienced programmer looks for an error, they often use thought-steps they have already automated. If those steps are not explained openly, a beginner sees only the finished fix. Teaching should show how a hypothesis is formed, which check is chosen, and how the result is read. <a href=\"#ref-10\">[10]</a>"))}
<h3>{T(lang, "Ayrı sahələrdə müəyyən edilmiş çətinliklər", "Difficulties identified in particular fields")}</h3>
{bullets([
    T(lang, "<strong>Verilənlər strukturları və alqoritmlər.</strong> 2026-cı il sistematik icmalında 92 yanlış təsəvvür və öyrənmə çətinliyi müəyyənləşdirilib. Bu say bütün tələbələrin eyni səhvləri etdiyini deyil, icmalın müxtəlif tədqiqatlarda belə problemlər topladığını göstərir. <a href=\"#ref-11\">[11]</a>",
      "<strong>Data structures and algorithms.</strong> A 2026 systematic review identified 92 misconceptions and learning difficulties. That number does not mean every student makes the same errors; it means the review gathered such problems from different studies. <a href=\"#ref-11\">[11]</a>"),
    T(lang, "<strong>Obyektyönlü proqramlaşdırma.</strong> Çaşqınlıq çox vaxt sinif ilə obyektin fərqi, konstruktorlar, obyektlərin bir-birindən qurulması və icra axını ətrafındadır. <a href=\"#ref-12\">[12]</a>",
      "<strong>Object-oriented programming.</strong> Confusion commonly surrounds the difference between class and object, constructors, building objects from other objects, and the flow of execution. <a href=\"#ref-12\">[12]</a>"),
    T(lang, "<strong>Rekursiya.</strong> İç-içə çağırışların izlənməsi, çağırışların geri qayıtması və dayanma şərti çətinlik yaradır. <a href=\"#ref-13\">[13]</a>",
      "<strong>Recursion.</strong> Following nested calls, seeing results come back, and the stopping condition all cause difficulty. <a href=\"#ref-13\">[13]</a>"),
    T(lang, "<strong>İstinadlar və göstəricilər.</strong> Dolayı müraciət, təxəllüs, görünmə sahəsi və parametr ötürülməsi bir neçə ildən sonra da çətin qala bilər. <a href=\"#ref-14\">[14]</a>",
      "<strong>References and pointers.</strong> Indirection, aliasing, scope and parameter passing can remain difficult even after several years. <a href=\"#ref-14\">[14]</a>"),
    T(lang, "<strong>Eynizamanlılıq və paralellik.</strong> Mümkün icra ardıcıllıqlarının müxtəlifliyi səhv proqramın bəzən düzgün görünməsinə səbəb olur. <a href=\"#ref-15\">[15]</a>",
      "<strong>Concurrency and parallelism.</strong> The variety of possible execution orders can make an incorrect program sometimes look correct. <a href=\"#ref-15\">[15]</a>"),
    T(lang, "<strong>SQL.</strong> Genişmiqyaslı təhlildə cədvəllərin birləşdirilməsi, alt sorğular və GROUP BY ilə bağlı səhvlər qeyd olunur. <a href=\"#ref-16\">[16]</a>",
      "<strong>SQL.</strong> Large-scale analysis recorded errors with joining tables, subqueries and GROUP BY. <a href=\"#ref-16\">[16]</a>"),
    T(lang, "<strong>Əməliyyat sistemləri.</strong> Mexanizmi əzbərləmək alternativ həllərin üstünlük və çatışmazlıqlarını izah etməyə həmişə kifayət etmir. <a href=\"#ref-17\">[17]</a>",
      "<strong>Operating systems.</strong> Memorising a mechanism is not always enough to explain the strengths and weaknesses of alternative solutions. <a href=\"#ref-17\">[17]</a>"),
    T(lang, "<strong>Ədəd təqdimatı.</strong> Mövqeli yazılış, ikiyə tamamlayıcı kod və daşma ilə bağlı yanlış təsəvvürlər kompüterin təşkili kursundan sonra da qala bilər. <strong>Daşma</strong> nəticənin ayrılmış bit sayına sığmamasıdır. <a href=\"#ref-18\">[18]</a>",
      "<strong>Number representation.</strong> Misconceptions about positional notation, two’s complement and overflow can remain after a computer-organisation course. <strong>Overflow</strong> is a result that does not fit in the number of bits set aside for it. <a href=\"#ref-18\">[18]</a>"),
    T(lang, "<strong>Kibertəhlükəsizlik.</strong> Zəiflik, təhdid, risk və qorunma tədbiri qarışdırıla bilər. Hücum edən tərəfin mümkün addımlarını düşünmək ayrıca bacarıq tələb edir. <a href=\"#ref-19\">[19]</a>",
      "<strong>Cybersecurity.</strong> Vulnerability, threat, risk and a protective measure can be mixed up. Thinking through the possible steps of an attacking side is a separate skill. <a href=\"#ref-19\">[19]</a>"),
    T(lang, "<strong>Dinamik proqramlaşdırma.</strong> Üsulun nə vaxt seçilməsi, altməsələlər arasındakı əlaqənin qurulması və səmərəsiz təkrarlardan qaçılması çətindir. <a href=\"#ref-20\">[20]</a>",
      "<strong>Dynamic programming.</strong> Choosing when to use the method, building the relation among subproblems, and avoiding inefficient repetition are difficult. <a href=\"#ref-20\">[20]</a>"),
    T(lang, "<strong>Süni intellekt.</strong> Məktəbli təsəvvürlərini araşdıran tədqiqat uşaqların sistemlərə insan xüsusiyyətləri aid edə və təlim verilənlərinin rolunu nəzərdən qaçıra bildiyini göstərir. <a href=\"#ref-21\">[21]</a>",
      "<strong>Artificial intelligence.</strong> A study of pupils’ ideas shows that children can attribute human qualities to systems and overlook the role of training data. <a href=\"#ref-21\">[21]</a>"),
])}
{p(T(lang, "Müsabiqə materialını yazanlar bu nəticələri tapşırıq kimi götürə bilər: yalnız tərifi yox, əskik zehni modeli izah edin.",
"Authors in this competition can treat these findings as a brief: explain the missing mental model, not only the definition."))}
</div></section>
<section class="cta-card" id="first-series">
<h2>{T(lang, "İlk nəşrlər üçün plan", "A first series of twelve articles")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Əlçatan tədris məqalələri hazırlamaq üçün aşağıdakı ardıcıllıq təklif olunur. Başlıqlar ən yüksək prioritet cədvəllə üst-üstə düşür və qeyri-mütəxəssisin sualı görməsi üçün yazılıb. Bu, nəşr üçün başlanğıc planıdır; müsabiqənin məcburi mövzu və ya ardıcıllıq tələbi deyil.",
"If the aim is accessible teaching articles, the following sequence is suggested. The titles overlap the highest-priority table and are written so that a non-specialist can see the question. This is a starting plan for publication, not a required topic list or order for the competition."))}
{first12}
{p(T(lang, "Auditoriyanın ehtiyacına görə mövzuların sırası dəyişdirilə və hər mövzu daha kiçik materiallara bölünə bilər.",
"The order can be changed to fit the audience, and each topic can be split into smaller pieces of material."))}
</div></section>
<section class="cta-card" id="languages">
<h2>{T(lang, "Tədris üçün tövsiyə olunan dillər", "Suggested teaching languages")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Hər iki mənbə eyni üç istiqaməti göstərir: proqramlaşdırma, verilənlər elmi və süni intellekt nümunələrində Python; veb nümunələrində JavaScript və TypeScript; verilənlər bazası mövzularında SQL. Aydın izah başqa dildən də istifadə edə bilər, əgər həmin dil seçilmiş auditoriyanın həqiqətən rastlaşdığı dildirsə.",
"Both sources point in the same three directions: Python for programming, data science and AI examples; JavaScript and TypeScript for web examples; SQL for database topics. A clear explanation can still use another language if that is the language the named audience actually meets."))}
{note(T(lang,
"Fərq, qətiyyət. Yenidən işlənmiş sənəd Python-u «praktik başlanğıc seçimi» adlandırır və bunu bütün auditoriyalar üçün vahid «ən yaxşı dil» hökmü kimi qəbul etməməyə çağırır. Əvvəlki səhifə Python-u «hazırda ən uyğun ümumi tədris dili» sayırdı. Bu səhifə hər iki ifadənı saxlayır və dili mövzunun məqsədinə, auditoriyanın əvvəlki biliyinə və nümunəni işlətmək imkanına görə seçməyi tövsiyə edir.",
"Difference of certainty. The reworked document calls Python a “practical starting choice” and asks readers not to treat that as a single “best language” for every audience. The earlier page called Python “the most suitable general teaching language at present”. This page keeps both statements and recommends choosing the language by the aim of the topic, the audience’s prior knowledge, and the chance to run the example."), "editorial")}
{p(T(lang,
"2025-ci il Stack Overflow sorğusunda Python istifadəsinin artması və GitHub hesabatında Python-un süni intellekt layihələrində geniş iştirakı bu dilin aktuallığını göstərir. TypeScript-in GitHub-dakı yüksəlişi veb nümunələrinə marağı da əsaslandıra bilər. <a href=\"#ref-4\">[4]</a>, <a href=\"#ref-5\">[5]</a>",
"The rise of Python use in the 2025 Stack Overflow survey, and Python’s wide presence in AI projects in the GitHub report, support the current relevance of that language. TypeScript’s rise on GitHub can also support interest in web examples. <a href=\"#ref-4\">[4]</a>, <a href=\"#ref-5\">[5]</a>"))}
</div></section>
<section class="cta-card" id="proposal">
<h2>{T(lang, "Mövzu təklifinin hazırlanması", "Preparing a topic proposal")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Bu bölmə yenidən işlənmiş sənəddə var və yuxarıdakı on iki məqalə tövsiyəsini tamamlayır. Hər mövzu üçün aşağıdakı beş suala qısa cavab hazırlamaq təklif olunur:",
"This section comes from the reworked document and completes the twelve-article suggestion above. For each topic it is useful to write a short answer to these five questions:"))}
{bullets([
    T(lang, "<strong>Auditoriya</strong> — material kimlər üçündür və hansı ilkin bilikləri tələb edir;",
      "<strong>Audience</strong> — who the material is for, and what prior knowledge it needs;"),
    T(lang, "<strong>Təhsil əhəmiyyəti</strong> — hansı anlayış və ya bacarığı öyrədir;",
      "<strong>Educational value</strong> — which idea or skill it teaches;"),
    T(lang, "<strong>Praktik əlaqə</strong> — həmin bilik harada istifadə olunur;",
      "<strong>Practical link</strong> — where that knowledge is used;"),
    T(lang, "<strong>Öyrənmə çətinliyi</strong> — hansı yanlış təsəvvürü və ya anlaşılmazlığı aradan qaldırır;",
      "<strong>Learning difficulty</strong> — which misconception or confusion it removes;"),
    T(lang, "<strong>Gözlənilən nəticə</strong> — öyrənən materialdan sonra nəyi izah və ya tətbiq edə biləcək.",
      "<strong>Intended outcome</strong> — what the learner will be able to explain or apply afterwards."),
])}
{p(T(lang,
"Məsələn, «Funksiya ilə nəticəni ekrana çıxarmaq arasındakı fərq» mövzusu ilkin proqramlaşdırma öyrənənlərə ünvanlana bilər. Materialın məqsədi qaytarılan qiymətin başqa hesablamada istifadə oluna bildiyini göstərməkdir. Biri yalnız ekrana yazan, digəri isə qiymət qaytaran iki qısa funksiya bu fərqi görünən edə bilər.",
"For example, “the difference between a function and printing a result” can be aimed at people learning introductory programming. The aim of the material is to show that a returned value can be used in another calculation. Two short functions, one that only writes to the screen and one that returns a value, can make that difference visible."))}
{p(T(lang,
"İzahı gündəlik sual və ya kiçik problemlə başlamaq, əsas anlayışları təqdim etmək, nümunəni addımlarla açmaq və sonda qısa yoxlama tapşırığı vermək olar. Bu quruluş tövsiyədir və mövzuya uyğun dəyişdirilə bilər. Mövzunun hər üç mənbə qrupunda eyni vaxtda önə çıxması şərt deyil. Rekursiya gündəlik texnologiya xəbərlərində az görünsə də, onun aydın izahı ciddi təhsil dəyəri daşıya bilər.",
"You can start the explanation with an everyday question or a small problem, present the core ideas, open the example step by step, and end with a short check. That structure is a suggestion and can change with the topic. A topic does not have to stand out in all three source groups at once. Recursion appears little in everyday technology news, yet a clear explanation of it can have serious educational value."))}
</div></section>
<section class="cta-card" id="glossary">
<h2>{T(lang, "Terminlər və ixtisarlar", "Terms and abbreviations")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Bu lüğət mətndə və mövzu siyahılarında işlənən əsas texniki terminləri qısa şəkildə izah edir. Təşkilat adları və təhsil çərçivələri yuxarıdakı mənbə bölməsində açıqlanır. Sinonimlər mötərizədə göstərilib.",
"This glossary explains the main technical terms used in the text and in the topic lists. Organisation names and curriculum frameworks are opened in the sources section above. Synonyms appear in parentheses."))}
{gloss_html}
</div></section>
<section class="cta-card" id="references">
<h2>{T(lang, "Mənbələr və istinadlar", "Sources and references")}</h2>
<div class="cta-card-body">
{p(T(lang,
"Mətn daxilindəki nömrələr aşağıdakı mənbələrə uyğundur. Tədqiqatlar üçün qısa təsviri adlar saxlanılıb; onlar tam biblioqrafik başlıq kimi təqdim edilmir.",
"The numbers in the text match the sources below. For research items the short descriptive names from the source document are kept; they are not presented as full bibliographic titles."))}
{refs_html}
{p(T(lang,
"Bu səhifə yeni mənbə deyil. O, yuxarıdakı sənədləri və inteqrasiya olunmuş bələdçini — yenidən işlənmiş Word sənədi ilə əvvəlki veb səhifənin birləşməsini — bir araya gətirir.",
"This page is not a new source. It brings together the documents above and the integrated guide — the combination of the reworked Word document and the earlier web page."))}
</div></section>
<section class="cta-card" id="related">
<h2>{T(lang, "Müsabiqənin əlaqəli səhifələri", "Related competition pages")}</h2>
<div class="cta-card-body">
<p class="cta-related">{T(lang,
'Açıq dəvət <a href="complex-topics.html">Çətin mövzu, aydın izah</a> səhifəsindədir. Müsabiqənin necə təşkil olunacağına dair işçi plan <a href="complex-topics-approach.html">Müsabiqənin təşkili</a> səhifəsindədir.',
'The public invitation is on <a href="complex-topics.html">Complex Topics, Clear Explanations</a>. The working plan for how the competition is organised is on <a href="complex-topics-approach.html">Organisation of competition</a>.')}</p>
{p(T(lang,
"Flayer və işçi plan təsdiqlənmiş Əsasnamə deyil. Bu səhifə də mövzu seçiminə kömək edən işçi bələdçidir.",
"The flyer and the working plan are not an approved regulation. This page, too, is a working guide that helps with choosing a topic."))}
</div></section>
"""

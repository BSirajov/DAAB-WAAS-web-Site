"""Comprehensive Azerbaijani-to-English translator for prominent-figure profile HTML pages.

Usage:
    from _az_profile_translator import translate_profile_html
    en_html = translate_profile_html(az_html, name="Isaac Newton")
"""
from __future__ import annotations
import html
import re

try:
    from _prominent_figure_en_strings import (
        PHRASE_REPLACEMENTS,
        translate_field,
        translate_country,
        FOOTER_EN,
    )
    from _prominent_figure_pronouns_en import apply_singular_pronouns
    from _world_contribution_en import (
        WORLD_CONTRIBUTION_EN,
        contribution_to_work_desc,
        translate_work_desc_az,
    )
except ImportError:
    def translate_field(x: str) -> str: return x
    def translate_country(x: str) -> str: return x
    def apply_singular_pronouns(x: str) -> str: return x
    FOOTER_EN = ""
    PHRASE_REPLACEMENTS = []
    WORLD_CONTRIBUTION_EN = {}
    def contribution_to_work_desc(x: str) -> str: return x
    def translate_work_desc_az(x: str) -> str | None: return None

AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")
# Person names and Latin titles (Unicode letters allowed)
NAME_LIKE = r"[\w\s\.\-\(\)\'’]{2,80}?"

# ---------------------------------------------------------------------------
# 1. UI STRING REPLACEMENTS  (applied to the whole HTML, longest first)
# ---------------------------------------------------------------------------

UI_REPLACEMENTS: list[tuple[str, str]] = [
    # --- footer / branding ---
    ("Dünya Azərbaycanlı Alimlər Birliyi", "World Association of Azerbaijani Scientists"),
    ("DAAB İdarə Heyətinin Sədri", "Chair of the WAAS Executive Board"),
    ("Prof. Dr. Məsud Əfəndiyev", "Prof. Dr. Masud Afandiyev"),
    ("Bütün hüquqlar qorunur", "All rights reserved"),
    ("© 2026 DAAB", "© 2026 WAAS"),
    ("Feneryolu Mahallesi", "Feneryolu Mahallesi"),
    ("İstanbul, Türkiyə", "Istanbul, Türkiye"),
    ("Kadıköy, İstanbul", "Kadıköy, Istanbul"),
    ("footer-title\">Əlaqə", "footer-title\">Contact"),
    ("footer-title\">Ünvan", "footer-title\">Address"),
    ("footer-title\">Rəhbərlik", "footer-title\">Leadership"),
    # --- hero tags ---
    ("Azərbaycan və türk dünyası", "Azerbaijani & Turkic heritage"),
    ("Dünya alimləri", "World scientists"),
    # --- section titles (SVG icons left untouched) ---
    ("Əsas əsərləri və fəaliyyəti</div>", "Key works and contributions</div>"),
    ("Həyatından maraqlı hadisələr</div>", "Notable aspects of the life and work</div>"),
    ("📚 Qaynaqlar", "📚 Sources"),
    # --- article h4 headings ---
    ("<h4>Həyat yolu</h4>", "<h4>Life and career</h4>"),
    ("<h4>Elmi və yaradıcılıq fəaliyyəti</h4>", "<h4>Scholarly and creative work</h4>"),
    ("<h4>Elmi fəaliyyəti</h4>", "<h4>Scholarly activity</h4>"),
    ("<h4>Cəmiyyətə təsiri</h4>", "<h4>Contribution to society</h4>"),
    # --- works list item names ---
    ("<em>Elmi və intellektual irs</em>", "<em>Scientific and intellectual legacy</em>"),
    ("<em>Bəşəriyyətə təsir</em>", "<em>Impact on humanity</em>"),
    # --- event titles ---
    ("Elmi axtarışın simvolu", "A symbol of scientific inquiry"),
    ("Elmi axtarış</div>", "A spirit of inquiry</div>"),
    ("Dünya miqyasında təsir</div>", "Global influence</div>"),
    ("Bəşəriyyətə təsir</div>", "Impact on humanity</div>"),
    # --- quote source ---
    ("irsinin ümumi ideyası", "— a guiding principle drawn from this legacy"),
    # --- sources section ---
    ("Bu profil açıq və etibarlı mənbələr əsasında hazırlanmışdır. Saytda real portret və foto materialları yerləşdirilərkən müəlliflik hüququ və lisenziya statusu ayrıca yoxlanılmalıdır.",
     "This profile is compiled from open and reliable reference sources. Where authentic portraits and photographs are published on the site, copyright status and licensing terms should be separately verified."),
    ("Akademik mənbələr və ensiklopedik nəşrlər", "Academic sources and encyclopedic publications"),
    ("WorldCat və akademik nəşrlər", "WorldCat and academic publications"),
    # --- sidebar labels ---
    ("info-title\">Şəxsi Məlumat", "info-title\">Personal information"),
    ("info-title\">Cəmiyyətə Töhfələr", "info-title\">Contributions to society"),
    ("info-title\">Həmçinin Baxın", "info-title\">See also"),
    ("info-label\">Tam adı", "info-label\">Full name"),
    ("info-label\">Doğum tarixi", "info-label\">Year of birth"),
    ("info-label\">Vəfat tarixi", "info-label\">Year of death"),
    ("info-label\">Xalq / mənsubiyyət", "info-label\">People / origin"),
    ("info-label\">Dövr / dövlət", "info-label\">Period / context"),
    ("info-label\">Sahə", "info-label\">Field"),
    # --- contribution list items ---
    ("Elmi və intellektual irsin zənginləşməsinə xidmət etdi",
     "Enriched the scientific and intellectual heritage"),
    ("Bəşəriyyətin tərəqqisinə təsir göstərən ideyalar yaratdı",
     "Created ideas that advanced the progress of humanity"),
    # --- navigation labels ---
    ("nav-dir\">Əvvəlki profil", "nav-dir\">Previous profile"),
    ("nav-dir\">Növbəti profil", "nav-dir\">Next profile"),
    # --- sidebar period/context values ---
    ("Azərbaycan və türk dünyası", "Azerbaijani & Turkic heritage"),
    ("Dünya alimləri", "World scientists"),
    ("Dünya elmi", "World science"),
    # --- title tag and meta ---
    ("<html lang=\"az\"", "<html lang=\"en\""),
    ("Görkəmli Şəxsiyyətlər", "Prominent Figures"),
    ("Görkəmli şəxsiyyətlər", "Prominent figures"),
    ("Ensiklopediya", "Encyclopedia"),
    ("Azərbaycan", "Azerbaijan"),
    ("Məzmuna keç", "Skip to content"),
    ("Onun fəaliyyəti ümumbəşəri tərəqqi tarixində yadda qalan iz buraxmışdır.",
     "This work left a lasting mark in the history of universal human progress."),
]


def _tf(field_az: str) -> str:
    """Translate a field string that may contain · separators."""
    parts = [p.strip() for p in field_az.split("\u00b7")]
    return " & ".join(translate_field(p) for p in parts)


# ---------------------------------------------------------------------------
# 2. TEMPLATE SENTENCE PATTERNS  (regex, applied after UI strings)
# ---------------------------------------------------------------------------
# Each entry: (compiled_regex, replacement_string_or_callable)

TEMPLATE_PATTERNS: list[tuple[re.Pattern, object]] = [

    # world group – intro (name + optional dates + country/region)
    (re.compile(
        rf'({NAME_LIKE}(?:\s*\([^)]*\))?)\s+([^<]+?) elmi və intellektual ənənəsini dünya miqyasında tanıdan görkəmli şəxsiyyətlərdən biridir\.'
    ),
     lambda m: (
         f'{m.group(1).strip()} is one of the outstanding figures who brought the scientific and '
         f'intellectual tradition of {translate_country(m.group(2).strip())} to international prominence.'
     )),

    # world group – historical significance
    (re.compile(
        r'Tarixi baxımdan ([^<]+?) elmin təkcə bilik toplusu deyil, həm də müşahidə, sübut, təcrübə və ardıcıl düşüncə mədəniyyəti olduğunu göstərən simalardan sayılır\.'
    ),
     lambda m: (
         f'Historically, {m.group(1).strip()} is counted among those figures who demonstrate that science '
         f'is not merely a body of knowledge, but also a culture of observation, evidence, experiment, '
         f'and systematic reasoning.'
     )),

    # world group – field activity
    (re.compile(r'Onun fəaliyyəti əsasən ([^<\.]{2,80}?) sahəsi ilə bağlı olmuş, yaşadığı dövrün elmi suallarına yeni yanaşma gətirmişdir\.'),
     lambda m: f'This work was primarily associated with {_tf(m.group(1))}, offering new approaches to the scientific questions of the period.'),

    # world group – field ideas (field names contain no sentence periods)
    (re.compile(r'([^<\.]{2,80}?) sahəsində formalaşdırdığı ideyalar daha geniş elmi mühitə təsir etmiş, müxtəlif ölkələrdə tədqiqat, təhsil və texnologiya inkişafına ilham vermişdir\.'),
     lambda m: f'The ideas developed in {_tf(m.group(1).strip())} influenced the broader scholarly environment and inspired advances in research, education, and technology across many countries.'),

    # world group – main contribution
    (re.compile(r'Onun əsas töhfəsi (.+?) ilə bağlıdır\.'),
     lambda m: f"The principal contribution is associated with {_translate_contribution(m.group(1).strip())}."),

    # world group – contribution valuation
    (re.compile(r'Bu töhfə yalnız konkret bir kəşf və ya nəzəriyyə kimi deyil, həm də sonrakı tədqiqatçılar üçün yeni suallar, metodlar və anlayışlar yaratmış elmi dönüş nöqtəsi kimi qiymətləndirilir\.'),
     'This contribution is valued not merely as a specific discovery or theory, but as a defining turning point — one that generated new questions, methods, and conceptual frameworks for subsequent researchers.'),

    # world group – legacy widening
    (re.compile(
        rf'({NAME_LIKE}) haqqında maraqlı cəhətlərdən biri onun elmi irsinin zaman keçdikcə daha geniş kontekstdə dəyərləndirilməsidir\.'
    ),
     lambda m: f"One of the remarkable aspects of {m.group(1).strip()}'s legacy is that it has been re-evaluated in an increasingly broad context as time has passed."),

    # world group – beyond own era
    (re.compile(r'Bir çox böyük alimlər kimi, onun fəaliyyəti də yalnız öz dövrünün ehtiyacları ilə məhdudlaşmamış, sonrakı nəsillərin elmi dilinə, tədqiqat üsullarına və bəşəriyyətin tərəqqi anlayışına təsir göstərmişdir\.'),
     'Like many distinguished scholars, this contribution was not limited to the needs of a single era; it shaped the scholarly language, research methods, and conceptions of progress of subsequent generations.'),

    # world group – closing merit
    (re.compile(rf'Buna görə də ({NAME_LIKE}) dünya elminin görkəmli nümayəndələri sırasında təqdim olunmağa layiqdir\.'),
     lambda m: f'For these reasons, {m.group(1).strip()} merits recognition among the distinguished representatives of world scholarship.'),

    # azturk group – intro (name — heritage irsinə mənsub, field sahəsində)
    # Em/en dash only — ASCII hyphen must not match (would corrupt class="work-desc">).
    (re.compile(rf'({NAME_LIKE})\s*[\u2014\u2013]\s*([^<]+?) irsinə mənsub, ([^<]+?) sahəsində tanınmış görkəmli şəxsiyyətdir\.'),
     lambda m: f'{m.group(1).strip()} is a distinguished figure of {translate_country(m.group(2).strip())} heritage, widely recognized in the field of {_tf(m.group(3))}.'),

    # azturk group – turkic memory
    (re.compile(r'Onun həyatı və fəaliyyəti türk dünyasının elmi, ədəbi və mədəni yaddaşında mühüm yer tutur\.'),
     "This figure's life and work occupy an important place in the scientific, literary, and cultural memory of the Turkic world."),

    # azturk group – tradition contribution
    (re.compile(rf'({NAME_LIKE}) öz sahəsində formalaşmış ənənəyə töhfə vermiş, milli və ümumtürk mədəni yaddaşında iz qoymuş şəxsiyyət kimi təqdim edilir\.'),
     lambda m: f'{m.group(1).strip()} is presented as a figure who contributed to the established traditions of this field and left an enduring mark on both national and broader Turkic cultural memory.'),

    # azturk group – works section header
    (re.compile(r'Əsas əsərləri və fəaliyyət istiqamətləri sırasında ([^<]+?) sahəsində fəaliyyəti; Maarifçilik, mədəniyyət və ya elmi irsə töhfələri; Türk dünyasının ortaq yaddaşında rolu kimi nümunələr xüsusi qeyd olunur\.'),
     lambda m: f'Among the principal areas of this work, particular note is given to activities in {_tf(m.group(1))}; contributions to Enlightenment thought, culture, and scholarly heritage; and to the role in the shared memory of the Turkic world.'),

    # shared – intellectual influence
    (re.compile(
        rf'({NAME_LIKE}) öz dövrünün intellektual mühitinə təsir göstərmiş, sonrakı nəsillər üçün bilik, axtarış və yaradıcılıq nümunəsinə çevrilmişdir\.'
    ),
     lambda m: f'{m.group(1).strip()} profoundly influenced the intellectual climate of the era and became a model of knowledge, inquiry, and creative achievement for later generations.'),

    # shared – examples indicator
    (re.compile(r'Bu nümunələr onun sahəsində yaratdığı elmi, ədəbi və ya mədəni təsirin başlıca göstəriciləridir\.'),
     'These examples are the primary indicators of the scholarly, literary, or cultural influence generated in this field.'),

    # event – new inquiry
    (re.compile(rf'({NAME_LIKE}) öz sahəsində yeni düşüncə və araşdırma istiqamətlərini gücləndirdi\.'),
     lambda m: f'{m.group(1).strip()} strengthened new directions of thought and scholarly inquiry in this field.'),

    # event – legacy recalled
    (re.compile(r'Onun irsi müxtəlif elmi və mədəni mühitlərdə xatırlanır\.'),
     'This legacy continues to be recalled in diverse scholarly and cultural settings.'),

    # event – extends knowledge
    (re.compile(rf'({NAME_LIKE}) bilik sərhədlərini genişləndirən ideya və araşdırmaları ilə tanınır\.'),
     lambda m: f'{m.group(1).strip()} is remembered for ideas and research that extended the frontiers of knowledge.'),

    # event – scholarly legacy countries
    (re.compile(r'Onun elmi irsi müxtəlif ölkələrdə tədqiqat və təhsil mühitinə təsir göstərmişdir\.'),
     'This scholarly legacy has influenced research and educational environments in many countries.'),

    # quote
    (re.compile(r'Elm, mədəniyyət və düşüncə insanlığın gələcəyini formalaşdıran ən böyük qüvvələrdəndir\.'),
     'Science, culture, and thought are among the greatest forces shaping the future of humanity.'),

    # works – knowledge dissemination
    (re.compile(rf'({NAME_LIKE}) biliklərin inkişafına və yayılmasına mühüm təsir göstərmişdir\.'),
     lambda m: f'{m.group(1).strip()} exerted a profound influence on the development and dissemination of knowledge.'),

    # works – universal progress
    (re.compile(r'Onun fəaliyyəti ümumbəşəri tərəqqi tarixində yadda qalan iz buraxmışdır\.'),
     'This work left a lasting mark in the history of universal human progress.'),

    # works name – country contributions
    (re.compile(r'<em>(.+?) sahəsində töhfələr</em>'),
     lambda m: f'<em>Contributions in {translate_country(m.group(1).strip())}</em>'),

    # sidebar – country contribution
    (re.compile(r'([^<>"]+?) sahəsində mühüm töhfə verdi'),
     lambda m: f'Made an important contribution in {translate_country(m.group(1).strip())}'),

    # sidebar – field value (country, field format)
    (re.compile(r'info-val">([\w\s/\-\u0100-\u024F]+), ([\w\s\u00B7\u0100-\u024F]+)</span>'),
     lambda m: f'info-val">{translate_country(m.group(1))}, {translate_field(m.group(2))}</span>'),

    # legacy – not limited to own era
    (re.compile(r'Bu şəxsiyyətin irsi yalnız öz dövrü ilə məhdudlaşmamış, sonrakı nəsillərin düşüncəsinə, mədəniyyətinə və elmi-ictimai inkişafına təsir göstərmişdir\.'),
     "This figure's legacy was not confined to that era; it exerted a lasting influence on the thought, culture, and scholarly-social development of later generations."),

    (re.compile(r'Onun adı türk dünyasının ortaq mədəni yaddaşında mühüm yer tutur\.'),
     "This figure's name occupies an important place in the shared cultural memory of the Turkic world."),
]

# Section heading: "{Name} haqqında" → "About {Name}"
SECTION_TITLE_ABOUT_RE = re.compile(
    r'(class="section-title"><svg.*?</svg>)(.+?) haqqında</div>',
    re.DOTALL,
)


def fix_section_title_about(html: str) -> str:
    """Replace AZ section title pattern with English 'About {Name}'."""
    return SECTION_TITLE_ABOUT_RE.sub(
        lambda m: f"{m.group(1)}About {m.group(2).strip()}</div>",
        html,
    )


# ---------------------------------------------------------------------------
# 3. UNIQUE BIOGRAPHICAL SENTENCE TRANSLATIONS
#    Each tuple: (exact_az_sentence, en_translation)
#    Sorted by length (longest first) within each group so that longer
#    sentences match before their sub-phrases.
# ---------------------------------------------------------------------------

UNIQUE_TRANSLATIONS: list[tuple[str, str]] = [
    # === abdulla_shaiq ===
    ("Azərbaycan uşaq ədəbiyyatının və milli pedaqoji fikrin inkişafında mühüm rol oynamış şair, yazıçı və müəllim.",
     "A poet, writer, and teacher who played a pivotal role in the development of Azerbaijani children's literature and national pedagogical thought."),
    ("Abdulla Şaiq Azərbaycan uşaqları üçün ana dilində bədii və tərbiyəvi mətnlər yazmışdır.",
     "Abdulla Şaiq composed literary and educational texts in the mother tongue for Azerbaijani children."),
    ("O, müəllim, dərslik müəllifi və maarifçi kimi milli təhsilin inkişafına xidmət etmişdir.",
     "As a teacher, textbook author, and enlightenment thinker, he dedicated his career to the advancement of national education."),
    ("Şaiqin əsərləri sadə dil, humanist ruh və tərbiyəvi məzmunla seçilir.",
     "Şaiq's works are distinguished by their accessible language, humanist spirit, and didactic purpose."),

    # === aziz_sancar ===
    ("Aziz Sancar 1946-cı ildə Türkiyənin Mardin vilayətində doğuldu və İstanbul Universitetində tibb təhsili aldıqdan sonra elmi fəaliyyətini molekulyar biologiya və biokimya istiqamətində davam etdirdi.",
     "Aziz Sancar was born in 1946 in the Mardin province of Türkiye and, after completing his medical studies at Istanbul University, continued his scientific career in molecular biology and biochemistry."),
    ("ABŞ-da apardığı tədqiqatlar onu DNT zədələnmələrinin hüceyrə tərəfindən necə tanındığını və necə bərpa edildiyini araşdıran aparıcı alimlərdən birinə çevirdi.",
     "His research in the United States established him as one of the leading scientists investigating how cells recognize and repair DNA damage."),
    ("Sancarın elmi fəaliyyəti əsasən nukleotid eksiziya bərpası, fotoliyaza mexanizmləri, hüceyrə ritmləri və DNT təmir sistemlərinin molekulyar əsasları ilə bağlıdır.",
     "Sancar's scientific work is primarily associated with nucleotide excision repair, photolyase mechanisms, circadian rhythms, and the molecular foundations of DNA repair systems."),
    ("Bu tədqiqatlar xərçəng biologiyası, genetik sabitlik və hüceyrə səviyyəsində zədələnməyə cavab mexanizmlərinin anlaşılmasına ciddi töhfə verdi.",
     "This research made a substantial contribution to the understanding of cancer biology, genetic stability, and cellular damage-response mechanisms."),
    ("2015-ci ildə Kimya üzrə Nobel mükafatına layiq görülməsi onun bu sahədəki işlərinin beynəlxalq miqyasda qəbulunu təsdiqlədi.",
     "His receipt of the Nobel Prize in Chemistry in 2015 confirmed the international recognition of his work in this field."),
    ("Aziz Sancar elm adamı kimi təkcə laboratoriya nəticələri ilə deyil, həm də gənc tədqiqatçılar üçün nümunəvi akademik həyat yolu ilə seçilir.",
     "As a scientist, Aziz Sancar is distinguished not only by his laboratory achievements but also by his exemplary academic career as a model for younger researchers."),
    ("Onun fəaliyyəti türk dünyasında fundamental elmin qlobal elmi gündəmdə necə mühüm yer tuta biləcəyini göstərən güclü nümunələrdəndir.",
     "His career stands as a powerful demonstration of how fundamental science originating from the Turkic world can attain a prominent place on the global scientific agenda."),

    # === behruz_kengerli ===
    ("Azərbaycan professional rəssamlığının banilərindən biri, qısa ömrünə baxmayaraq güclü bədii irs qoymuş sənətkar.",
     "One of the founders of professional Azerbaijani painting — an artist who left a powerful artistic legacy despite a brief life."),
    ("Bəhruz Kəngərli Azərbaycan təsviri sənətində professional məktəbin formalaşmasına təsir göstərmiş ilk rəssamlardandır.",
     "Bəhruz Kəngərli was among the first artists to exert a formative influence on the development of a professional school of Azerbaijani fine art."),
    ("O, portret, mənzərə və qaçqınlar mövzusunda təsirli əsərlər yaratmışdır.",
     "He created compelling works on the themes of portraiture, landscape, and the plight of refugees."),
    ("Qısa ömrü onun yaradıcılığını yarımçıq qoysa da, Kəngərli milli rəssamlıq tarixində xüsusi yer tutur.",
     "Although his brief life left his artistic output incomplete, Kəngərli occupies an enduring place in the history of national painting."),

    # === bekir_chobanzade ===
    ("Bəkir Çobanzadə 1893-cü ildə Krımda doğulmuş, Krım tatar mədəni mühitində formalaşmış, daha sonra Osmanlı, Avropa və Azərbaycan elmi-ədəbi mühitləri ilə əlaqələr qurmuş görkəmli türkoloq, dilçi və şair idi.",
     "Bekir Chobanzade was born in Crimea in 1893, was shaped by the Crimean Tatar cultural milieu, and later established connections with Ottoman, European, and Azerbaijani scholarly and literary circles. He was a distinguished Turkologist, linguist, and poet."),
    ("Onun elmi maraqları türk dillərinin müqayisəli öyrənilməsi, dialektologiya, ədəbiyyat tarixi və dil siyasəti məsələlərini əhatə edirdi.",
     "His scholarly interests encompassed the comparative study of Turkic languages, dialectology, literary history, and questions of language policy."),
    ("Çobanzadə Azərbaycan elmi həyatında xüsusilə türkologiya və dilçilik məktəbinin inkişafına töhfə verdi.",
     "Chobanzade made a significant contribution to Azerbaijani academic life, particularly to the development of the Turkology and linguistics school."),
    ("O, türk dillərinin quruluşu, fonetik və morfoloji xüsusiyyətləri, ədəbi dilin formalaşması və xalq danışıq materiallarının elmi təsnifi üzərində işləyirdi.",
     "He worked on the structure of Turkic languages, their phonetic and morphological features, the formation of literary language, and the scholarly classification of spoken vernacular materials."),
    ("Şair kimi \"Boran\" kimi əsərlərində Krım tatar xalqının tarixi taleyini, mühacirət və milli yaddaş mövzularını bədii şəkildə ifadə etmişdir.",
     "As a poet, in works such as Boran (The Storm), he gave artistic expression to the historical fate of the Crimean Tatar people, treating themes of emigration and national memory."),
    ("1930-cu illərin siyasi repressiyaları onun həyatına faciəli son qoysa da, Bəkir Çobanzadənin elmi və ədəbi irsi türkoloji düşüncənin mühüm səhifələrindən biri olaraq qalır.",
     "Although the political repressions of the 1930s brought a tragic end to his life, Bekir Chobanzade's scholarly and literary legacy remains one of the significant chapters of Turkological thought."),
    ("Onun profili bu kataloqda türk xalqlarının dil, ədəbiyyat və akademik yaddaş tarixini təmsil edən əsas simalardan biri kimi verilir.",
     "His profile is presented in this catalogue as one of the principal figures representing the history of Turkic languages, literature, and academic memory."),

    # === bilge_xaqan ===
    ("Bilgə Xaqan (683–734) — İkinci Göytürk Xaqanlığının ən parlaq hökmdarı; türk yazılı ədəbiyyatının ilk böyük nümayəndəsi.",
     "Bilge Khagan (683–734) — the most illustrious ruler of the Second Göktürk Khaganate and one of the earliest great representatives of Turkic written literature."),
    ("Qardaşı Kül Tiginlə birlikdə Göytürk dövlətini yenidən qurmuş, çökən xaqanlığı dirçəltmişdir.",
     "Together with his brother Kül Tigin, he rebuilt the Göktürk state and revived a khaganate that had been on the verge of collapse."),
    ("Onun adından yazılmış Orxon kitabələri türk dilinin ən qədim ədəbi abidələridir — bir hökmdarın öz xalqına vəsiyyəti, xəbərdarlığı və sevgi dolu müraciətidir.",
     "The Orkhon inscriptions composed in his name are among the earliest literary monuments of the Turkic language — a ruler's testament, admonition, and declaration of devotion to his people."),
    ("Bilgə Xaqan — 683-cü ildə dünyaya gəlmiş, İkinci Göytürk Xaqanlığını (682–744) canlandırmış böyük türk dövlət adamı və siyasi mütəfəkkir.",
     "Bilge Khagan — born in 683, he was the great Turkic statesman and political thinker who revitalized the Second Göktürk Khaganate (682–744)."),
    ("\"Bilgə\" sözü türkcədə \"müdrik\", \"bilikli\" mənasını verir — bu ad onun xarakterini dəqiq təsvir edir.",
     "The word 'Bilge' means 'wise' or 'learned' in Turkic — a title that precisely describes his character."),
    ("O, güclü bir sərkərdə olmaqla yanaşı, dövlət idarəçiliyini dərin düşüncəylə aparan bir hökmdar idi.",
     "He was not only a formidable military commander but also a ruler who governed the state with profound deliberation."),
    ("683-cü ildə atası İlteriş Xaqanın vəfatından sonra böyük qardaşı Moxilian xaqan taxtına oturmuş, özü isə \"şad\" (şahzadə) rütbəsini almışdır.",
     "After the death of his father İlterish Khagan in 683, his elder brother Mochilian ascended the khaganal throne, while Bilge himself received the title of 'shad' (prince)."),
    ("Qardaşı Kül Tiginlə birlikdə onlarla döyüşdə türk xalqlarını aparmış, Çin, Türgiş, Qırgız, Tatabı kimi güclü düşmənlər üzərində qələbələr qazanmışdır.",
     "Together with his brother Kül Tigin, he led the Turkic peoples in dozens of battles, winning victories over powerful adversaries such as China, the Turgesh, the Kyrgyz, and the Tatabi."),
    ("716-cı ildə ağır xəstəlikdən vəfat edən böyük qardaşının ardından \"Bilgə Xaqan\" titulu ilə xaqan olmuşdur.",
     "After his elder brother died of grave illness in 716, he became Khagan with the title of 'Bilge Khagan.'"),
    ("Bilgə Xaqan kitabələrdə türk xalqına müraciət edərək deyir: \"Türk milleti, aç idiysen tok oldu; çıplak idiysen giyindi.\"",
     "In the inscriptions, Bilge Khagan addresses the Turkic people: 'Turkic people — if you were hungry, you became fed; if you were naked, you became clothed.'"),
    (" — Bu, tarixin ilk sosial hesabat mətnlərindən biridir.",
     " — This stands among the earliest texts of social accountability in history."),

    # === biruni ===
    ("Əl-Biruni (973–1048) — İslam qızıl dövrünün ən universal dahilərindən biri.",
     "Al-Biruni (973–1048) — one of the most universally gifted intellects of the Islamic Golden Age."),
    ("Xarəzmdən (bugünkü Özbəkistan) olan bu türk alimi, riyaziyyat, astronomiya, fizika, coğrafiya, tarix, əczaçılıq, dilçilik sahələrini eyni ustalıqla mənimsəmişdir.",
     "This Turkic scholar from Khwarazm (present-day Uzbekistan) mastered mathematics, astronomy, physics, geography, history, pharmacology, and linguistics with equal brilliance."),
    ("Yer kürəsinin radiusunu o dövr üçün놀랍도록 dəqiq hesablamış, Hindistanı on illik sahə tədqiqatı ilə araşdıraraq dünya elminə tanıtmışdır.",
     "He calculated the radius of the Earth with remarkable precision for his era, and introduced India to world scholarship through a decade of first-hand field research."),
    ("Türk mənşəli olan alim, Xarəzmşahlar sarayında böyümüş, gənc yaşlarından riyaziyyat, astronomiya və fəlsəfəni dərindən öyrənmişdir.",
     "Of Turkic origin, the scholar grew up at the court of the Khwarazmshahs and from an early age immersed himself deeply in mathematics, astronomy, and philosophy."),
    ("Biruni ömrü boyu çətin siyasi şərtlər içərisindəydi.",
     "Throughout his life, Biruni operated under difficult political conditions."),
    ("Qəznəvi hökmdarı Sultan Mahmud onu zorla sarayına götürmüş, 13 il yanından buraxmamışdır.",
     "The Ghaznavid ruler Sultan Mahmud took him to his court by force and kept him there for thirteen years."),
    ("Lakin Biruni bu məcburi qalışdan faydalanmış — Əfqanıstan və Hindistana gedən hərbi ekspedisiyalarla birlikdə gəzmiş, Hindistanı şəxsən öyrənmişdir.",
     "Yet Biruni turned this compelled sojourn to advantage — accompanying military expeditions to Afghanistan and India, he studied India first-hand."),
    ("Yer kürəsinin radiusunu təqribən 6339,6 km hesablamışdır.",
     "He calculated the radius of the Earth at approximately 6,339.6 km."),
    ("Müasir ölçmə 6371 km-dir.",
     "The modern measurement is 6,371 km."),
    ("Bu, XI əsr üçün misilsiz dəqiqliklə aparılmış hesablamadır.",
     "This represents a calculation of unparalleled precision for the eleventh century."),

    # === bulbul ===
    ("Azərbaycan professional vokal məktəbinin banilərindən biri, muğamla Avropa opera texnikasını birləşdirən sənətkar.",
     "One of the founders of the professional Azerbaijani vocal school — an artist who merged mugham with European operatic technique."),
    ("Bülbül Azərbaycan opera sənətinin inkişafında əsas simalardan biridir.",
     "Bülbül is one of the central figures in the development of Azerbaijani opera."),
    ("O, muğam ifaçılığını professional vokal texnikası ilə birləşdirərək yeni məktəb yaratdı.",
     "He merged mugham performance with professional vocal technique, establishing a new school of singing."),
    ("Pedaqoq və tədqiqatçı kimi Azərbaycan vokal sənətinin sistemləşməsinə töhfə verdi.",
     "As a pedagogue and researcher, he contributed to the systematization of Azerbaijani vocal art."),

    # === cahit_arf ===
    ("Türk riyaziyyatının ən böyük nümayəndələrindən biri, cəbr və ədədlər nəzəriyyəsində \"Arf invariantı\" ilə tanınan alim.",
     "One of the foremost representatives of Turkish mathematics — a scholar renowned in algebra and number theory for the Arf invariant."),
    ("Cahit Arf Türkiyədə müasir riyaziyyat məktəbinin formalaşmasında mühüm rol oynamışdır.",
     "Cahit Arf played a significant role in the formation of the modern mathematics school in Türkiye."),
    ("Onun adı \"Arf invariantı\", \"Arf halqaları\" və \"Arf bağlanışı\" kimi riyazi terminlərdə yaşayır.",
     "His name lives on in mathematical terminology through the Arf invariant, Arf rings, and Arf closure."),
    ("O, elmi tədqiqatla yanaşı gənc riyaziyyatçıların yetişməsinə də böyük təsir göstərmişdir.",
     "Alongside his research, he exerted a profound influence on the formation of new generations of mathematicians."),

    # === celil_memmedquluzade ===
    ("Cəlil Məmmədquluzadə Azərbaycan realist nəsrinin böyük ustadı, \"Molla Nəsrəddin\" jurnalının yaradıcısıdır.",
     "Jalil Mammadguluzadeh is the great master of Azerbaijani realist prose and the founder of the Molla Nasraddin journal."),
    ("Məmmədquluzadə Azərbaycan ədəbiyyatında realist nəsr və satirik publisistikanın aparıcı simasıdır.",
     "Mammadguluzadeh is the leading figure of realist prose and satirical journalism in Azerbaijani literature."),
    ("\"Molla Nəsrəddin\" jurnalı onun rəhbərliyi ilə bütün müsəlman Şərqində maarifçi-satirik düşüncənin mərkəzinə çevrildi.",
     "Under his direction, the Molla Nasraddin journal became the centre of Enlightenment-satirical thought throughout the Muslim East."),
    ("Onun əsərləri cəmiyyətin geriliyini sadə, təsirli və çox zaman acı yumorla göstərir.",
     "His works expose the backwardness of society with simple, effective, and often biting humour."),

    # === chingiz_aytmatov ===
    ("Qırğız ədəbiyyatını dünya səviyyəsinə çıxaran böyük yazıçı, insanlıq, vicdan və yaddaş mövzularının ustası.",
     "The great writer who elevated Kyrgyz literature to world standing — a master of the themes of humanity, conscience, and memory."),
    ("Çingiz Aytmatov qırğız xalqının mifoloji və tarixi yaddaşını modern roman dili ilə birləşdirdi.",
     "Chinghiz Aytmatov brought together the mythological and historical memory of the Kyrgyz people with the language of the modern novel."),
    ("Onun əsərlərində insanın vicdanı, təbiətlə əlaqəsi, müharibə yaddaşı və mənəvi məsuliyyət əsas mövzulardır.",
     "In his works, the principal themes are human conscience, the bond between humanity and nature, the memory of war, and moral responsibility."),
    ("Aytmatovun əsərləri çoxsaylı dillərə tərcümə olunmuş və dünya ədəbiyyatında geniş oxunmuşdur.",
     "Aytmatov's works have been translated into numerous languages and are widely read in world literature."),

    # === ebu_bekr_tehrani ===
    ("Əbu Bəkr Tehrani XV əsr tarixçisi, \"Kitabi-Diyarbəkriyyə\" əsərinin müəllifi və Qaraqoyunlu-Ağqoyunlu dövrü tarixinin mühüm qaynaqlarından birini yaratmış salnaməçidir.",
     "Abu Bakr Tehrani was a fifteenth-century historian, author of Kitab-i Diyarbakriyya, and one of the chroniclers who created one of the key primary sources for the history of the Karakoyunlu-Akkoyunlu period."),
    ("Əbu Bəkr Tehrani haqqında bioqrafik məlumatlar məhduddur, lakin onun \"Kitabi-Diyarbəkriyyə\" əsəri orta əsr Azərbaycan və Ön Asiya tarixi üçün qiymətli mənbədir.",
     "Biographical information about Abu Bakr Tehrani is limited, but his Kitab-i Diyarbakriyya is a valuable source for the medieval history of Azerbaijan and the Near East."),
    ("Əsər siyasi hadisələri, hökmdarların fəaliyyətini və bölgənin dövlətçilik tarixini izah edir.",
     "The work chronicles political events, the activities of rulers, and the history of statecraft in the region."),
    ("Bu salnamə tədqiqatçılar üçün Qaraqoyunlu və Ağqoyunlu tarixinin anlaşılmasında əsas qaynaqlardan sayılır.",
     "This chronicle is considered one of the principal sources for scholars seeking to understand the history of the Karakoyunlu and Akkoyunlu confederacies."),

    # === ebulfez_elchibey ===
    ("Əbülfəz Elçibəy ixtisasca şərqşünas alim idi və ərəb dünyası tarixi üzrə tədqiqatlar aparmışdır.",
     "Abulfaz Elchibey was by training an orientalist scholar who conducted research in the history of the Arab world."),
    ("1980–1990-cı illərdə Azərbaycan milli azadlıq hərəkatının ön sıralarında dayanmışdır.",
     "In the 1980s and 1990s, he stood at the forefront of the Azerbaijani national liberation movement."),
    ("1992-ci ildə Azərbaycan Respublikasının prezidenti seçilmiş, türk dünyası birliyi və milli suverenlik ideyalarını müdafiə etmişdir.",
     "In 1992, he was elected President of the Republic of Azerbaijan and championed the ideas of Turkic world unity and national sovereignty."),

    # === ehmed_cavad ===
    ("Azərbaycan Dövlət Himninin sözlərinin müəllifi, istiqlal və vətənpərvərlik poeziyasının görkəmli nümayəndəsi.",
     "The author of the lyrics of the Azerbaijani State Anthem and an outstanding representative of independence and patriotic poetry."),
    ("Əhməd Cavad Azərbaycan istiqlal düşüncəsinin poetik simalarından biridir.",
     "Ahmad Javad is one of the poetic voices of Azerbaijani independence thought."),
    ("Onun \"Çırpınırdı Qara dəniz\" kimi şeirləri türk dünyasında geniş tanınmışdır.",
     "His poems, such as The Black Sea Was Raging, became widely known throughout the Turkic world."),
    ("1937-ci il repressiyaları zamanı güllələnmiş, sonradan bəraət almışdır.",
     "He was executed during the 1937 repressions and was subsequently rehabilitated."),

    # === ehmed_yesevi ===
    ("Əhməd Yəsəvi (1093–1166) — türk dünyasının ən böyük sufi şairi və mənəvi rəhbəri.",
     "Ahmad Yasawi (1093–1166) — the greatest Sufi poet and spiritual leader of the Turkic world."),
    ("Yəsi (bugünkü Türküstan, Qazaxıstan) şəhərindən olan bu mübarək şəxsiyyət, Orta Asiyanın türk xalqları arasında İslamı yayan mənəvi hərəkatın banisidir.",
     "This revered figure from Yasi (present-day Türkistan, Kazakhstan) is the founder of the spiritual movement that spread Islam among the Turkic peoples of Central Asia."),
    ("'Divani Hikmət' adlı şeir kitabı türk dilindəki ilk böyük sufi ədəbiyyat nümunəsidir — sadə, anlaşıqlı türkcə ilə yazılan bu şeirlər ürəkdən ürəyə yayılmışdır.",
     "His collection of poems known as Divan-i Hikmet is the first great example of Sufi literature in the Turkic language — written in plain, accessible Turkic, these verses spread from heart to heart."),
    ("Əhməd Yəsəvi — 1093-cü ildə Yəsi şəhərində (bugünkü Qazaxıstanın Türküstan şəhəri) anadan olmuşdur.",
     "Ahmad Yasawi was born in 1093 in the city of Yasi (present-day Türkistan, Kazakhstan)."),
    ("Erkən yaşlarında atasını itirmiş, Buxaraya gedərək dövrünün böyük sufi şeyxi Yusif Həmədaninin yanında təhsil almışdır.",
     "Having lost his father at an early age, he travelled to Bukhara to study under Yusuf Hamadani, one of the great Sufi masters of his time."),
    ("Şeyxinin vəfatından sonra Yəsiyə qayıtmış, burada böyük bir ruhani cəmaat qurmuşdur.",
     "After his master's death, he returned to Yasi, where he established a large spiritual community."),
    ("Yəsəvi 63 yaşına — Həzrət Peyğəmbərin vəfat yaşına — çatanda xalq arasında yaşamağa özünü layiq görmədiyini söyleyərək yerin altına — bir növ yeraltı xilvetkaha — çəkilmişdir.",
     "When Yasawi reached the age of 63 — the age at which the Prophet passed away — he declared himself unworthy of living among the people and retreated to an underground cell, a form of subterranean hermitage."),
    ("Ömrünün son 30 ilini burada keçirmiş, lakin insanlarla əlaqəsini kəsməmişdir.",
     "He spent the last thirty years of his life there, yet never severed his connection with the people."),
    ("\"Hikmət aytay deb yürdüm, yürüdüm tüni-kündüz...\" — Yəsəvinin şeirləri sadə türkcə ilə yazılmış, lakin dərin bir sufi fəlsəfəsi daşıyır.",
     "\"I wandered by day and by night, seeking to speak words of wisdom...\" — Yasawi's verses are written in plain Turkic yet carry a profound Sufi philosophy."),

    # === el_ferabi ===
    ("Əl-Fərabi (872–950) — İslam fəlsəfəsinin ən böyük nümayəndəsi; Aristoteldən sonra 'İkinci müəllim' adını qazanmış ensiklopedist.",
     "Al-Farabi (872–950) — the greatest representative of Islamic philosophy; an encyclopedist acclaimed as the 'Second Teacher' after Aristotle."),
    ("Fərab şəhərindən (bugünkü Qazaxıstan/Türküstana) olan bu türk alimi, fəlsəfə, məntiq, musiqi nəzəriyyəsi, siyasət, astronomiya, riyaziyyat və dilçilik sahələrini eyni dərəcədə dərindən mənimsəmişdir.",
     "This Turkic scholar from Farab (in present-day Kazakhstan/Türkistan) mastered philosophy, logic, music theory, political science, astronomy, mathematics, and linguistics with equal depth."),
    ("Onun 'Xoşbəxt Şəhər' (Əl-Mədinətül-Fazilə) əsəri İslam siyasi fəlsəfəsinin zirvəsidir.",
     "His work The Virtuous City (Al-Madinah al-Fadilah) is the summit of Islamic political philosophy."),
    ("Əl-Fərabi — tam adı Əbu Nəsr Məhəmməd ibn Məhəmməd Fərabi — 872-ci ildə Fərab şəhərinin yaxınlığında anadan olmuşdur.",
     "Al-Farabi — full name Abu Nasr Muhammad ibn Muhammad al-Farabi — was born around 872 near the city of Farab."),
    ("Bu şəhər bugünkü Qazaxıstanın Türküstan vilayətindədir.",
     "This city is located in the Türkistan region of present-day Kazakhstan."),
    ("Türk soylu olan alim, gənclik illərini Türküstanda keçirmiş, sonra Bağdada, oradan Hələb və Dəməşqə getmişdir.",
     "Of Turkic stock, the scholar spent his youth in Türkistan before travelling to Baghdad, and later to Aleppo and Damascus."),
    ("Fərabi Aristotelin bütün əsərlərinə şərhlər yazaraq onları İslam dünyasına tanıtmışdır.",
     "Al-Farabi wrote commentaries on all of Aristotle's works, thereby introducing them to the Islamic world."),
    ("Məhz bu yüksək elmi nüfuzu ona \"İkinci müəllim\" (əl-Muallim əs-Sani) ləqəbini qazandırmışdır — birinci müəllim Aristotel idi.",
     "It was this towering scholarly authority that earned him the epithet 'Second Teacher' (al-Muallim al-Thani) — the first teacher being Aristotle."),
    ("İbn Sina gəncliyindəki xatirələrini anlatarkən yazır: \"Aristotelin Metafizikasını qırx dəfə oxudum, heç bir şey anlamadım. Bir kitab satıcısının məsləhətiylə Fərabinin şərhini aldım — bir dəf",
     "Ibn Sina recounts in his memoirs: 'I read Aristotle's Metaphysics forty times without understanding it. At the advice of a bookseller, I purchased al-Farabi's commentary — and at once"),

    # === eliaga_vahid ===
    ("XX əsr Azərbaycan qəzəlinin ən məşhur nümayəndəsi, klassik poeziya ənənəsini müasir dövrdə yaşadan şair.",
     "The most celebrated representative of twentieth-century Azerbaijani ghazal — a poet who kept the classical poetry tradition alive in the modern era."),
    ("Əliağa Vahid Füzuli ənənəsinin XX əsrdə ən tanınmış davamçısıdır.",
     "Aliagha Vahid is the most recognized continuator of the Fuzuli tradition in the twentieth century."),
    ("Onun qəzəlləri xalq arasında geniş yayılmış, muğam ifaçılığında sevilmişdir.",
     "His ghazals became widely popular and are beloved in the tradition of mugham performance."),
    ("Vahid klassik formaları qoruyaraq gündəlik həyat duyğularını və məhəbbət lirikasını sadə dillə ifadə etmişdir.",
     "Preserving classical forms, Vahid expressed the emotions of everyday life and love lyrics in an accessible idiom."),

    # === elishir_nevai ===
    ("Əlişir Nəvai 1441-ci ildə Heratda aristokrat hərbi ailədə dünyaya gəldi və Teymurilər dövrünün saray, kitab və elm mühiti içində formalaşdı.",
     "Alisher Navoi was born in 1441 in Herat into an aristocratic military family, and came of age within the courtly, literary, and scholarly milieu of the Timurid era."),
    ("Herat və Məşhəd kimi mərkəzlərdə aldığı təhsil, Hüseyn Bayqara sarayı ilə əlaqələri və Cami başda olmaqla dövrün irfan–ədəbiyyat çevrəsi onun dünyagörüşünü müəyyənləşdirdi.",
     "His education in centres such as Herat and Mashhad, his connections with the court of Sultan Husayn Bayqara, and his engagement with the intellectual-literary circle of the age — led by Jami — shaped his worldview."),
    ("Nəvai yalnız şair deyil, həm də dövlət idarəçiliyində iştirak edən, mədrəsə, kitabxana və ictimai tikililəri himayə edən böyük mədəniyyət xadimi idi.",
     "Navoi was not merely a poet, but also a great cultural patron who participated in state governance and sponsored madrasas, libraries, and public buildings."),
    ("Onun əsas tarixi xidməti çağatay türkcəsini yüksək ədəbi dil səviyyəsinə qaldırmasıdır.",
     "His principal historical contribution is the elevation of Chagatai Turkic to the level of a refined literary language."),
    ("Dörd divanı, beş məsnəvidən ibarət \"Xəmsə\"si, \"Lisan üt-Tayr\", \"Məcalisün-nəfais\" və \"Mühakimətül-lüğəteyn\" kimi əsərləri türk ədəbi dilinin poetik, fəlsəfi və elmi ifadə imkanlarını genişləndirdi.",
     "His four divans, the quintet of masnavis known as the Khamsa, along with works such as Lisan ut-Tayr, Majalis un-Nafais, and Muhakamat ul-Lughatayn, expanded the poetic, philosophical, and scholarly expressive capacity of the Turkic literary language."),
    ("\"Mühakimətül-lüğəteyn\"də Nəvai türk dilinin fars dili ilə müqayisədə ifadə gücünü müdafiə edərək dil şüurunu ədəbi-estetik proqram səviyyəsinə yüksəltdi.",
     "In Muhakamat ul-Lughatayn, Navoi defended the expressive power of the Turkic language in comparison with Persian, elevating linguistic consciousness to the level of a literary and aesthetic programme."),
    ("Nəvainin həyatı ədəbiyyat, dövlətçilik və xeyriyyəçilik arasında nadir tarazlıq nümunəsidir.",
     "Navoi's life is a rare example of balance between literature, statecraft, and philanthropy."),

    # === evliya_celebi ===
    ("Evliya Çələbi 40 ildən çox səyahət etmiş Osmanlı səyyahı, on cildlik \"Səyahətnamə\"nin müəllifidir.",
     "Evliya Çelebi was an Ottoman traveller who journeyed for more than forty years and authored the ten-volume Seyahatname (Book of Travels)."),
    ("Evliya Çələbi Osmanlı dünyasının ən böyük səyyah-yazıçısıdır.",
     "Evliya Çelebi is the greatest traveller-writer of the Ottoman world."),
    ("Onun \"Səyahətnamə\"si Balkanlardan Qafqaza, Yaxın Şərqdən Şimali Afrikaya qədər geniş coğrafiyanı əhatə edir.",
     "His Seyahatname encompasses a vast geography stretching from the Balkans to the Caucasus and from the Middle East to North Africa."),
    ("Əsərdə şəhərlər, dillər, adətlər, peşələr, musiqi və gündəlik həyat haqqında zəngin təsvirlər var.",
     "The work contains rich descriptions of cities, languages, customs, professions, music, and daily life."),
    ("O, bəzən rəvayət və yumoru faktlarla qarışdırsa da, əsəri mədəniyyət tarixi üçün əvəzsiz mənbədir.",
     "Although he sometimes mingles legend and humour with fact, his work is an invaluable source for cultural history."),

    # === fikret_emirov ===
    ("Simfonik muğam janrının yaradıcılarından biri, Azərbaycan musiqisini dünya səhnəsinə çıxaran böyük bəstəkar.",
     "One of the creators of the symphonic mugham genre — a great composer who brought Azerbaijani music to the world stage."),
    ("Fikrət Əmirov Azərbaycan muğamını simfonik düşüncə ilə birləşdirərək yeni janr yaratdı.",
     "Fikrat Amirov merged Azerbaijani mugham with symphonic thought, creating a new genre."),
    ("\"Şur\" və \"Kürd Ovşarı\" simfonik muğamları milli musiqinin orkestr imkanlarını genişləndirdi.",
     "His symphonic mugham works Shur and Kurd Ovshary expanded the orchestral possibilities of national music."),
    ("Onun balet, opera, simfonik və kamera əsərləri Azərbaycan musiqi xəzinəsinin mühüm hissəsidir.",
     "His ballets, operas, symphonic, and chamber works form an important part of the Azerbaijani musical treasury."),

    # === fuat_koprulu ===
    ("Türk ədəbiyyatı tarixi və türkologiya sahəsinin ən böyük alimlərindən biri, Köprülü məktəbinin yaradıcısı.",
     "One of the greatest scholars in the fields of Turkish literary history and Turkology — the founder of the Köprülü school."),
    ("Fuat Köprülü türk ədəbiyyatı tarixini elmi metodlarla araşdıran ən böyük tədqiqatçılardan biridir.",
     "Fuat Köprülü is one of the foremost scholars who investigated the history of Turkish literature with rigorous academic methods."),
    ("O, xalq ədəbiyyatı, təsəvvüf, Osmanlı dövlətinin yaranması və türk mədəniyyətinin tarixi kökləri üzrə fundamental əsərlər yazmışdır.",
     "He wrote foundational works on folk literature, Sufism, the origins of the Ottoman state, and the historical roots of Turkic culture."),
    ("Köprülü məktəbi Türkiyədə humanitar elmlərin modernləşməsinə böyük təsir göstərdi.",
     "The Köprülü school exerted a profound influence on the modernization of the humanities in Türkiye."),

    # === fuzuli ===
    ("Füzuli Azərbaycan ədəbiyyatının ən yüksək zirvələrindən biri, üç dildə yazmış böyük lirik şair və \"Leyli və Məcnun\" poemasının müəllifidir.",
     "Fuzuli stands among the highest peaks of Azerbaijani literature — a great lyric poet who wrote in three languages and author of the poem Layla and Majnun."),
    ("Füzuli Azərbaycan, fars və ərəb dillərində poetik irs yaratmış nadir dahilərdəndir.",
     "Fuzuli is one of the rare intellects who created a poetic legacy in Azerbaijani, Persian, and Arabic."),
    ("Onun qəzəlləri sevgi, iztirab, mənəvi kamillik və insan qəlbinin dərinliklərini əks etdirir.",
     "His ghazals reflect love, suffering, spiritual refinement, and the profound depths of the human heart."),
    ("\"Leyli və Məcnun\" poeması Şərq məhəbbət dastanının ən kamil bədii təcəssümlərindən biridir.",
     "His poem Layla and Majnun is one of the most perfect artistic embodiments of the Eastern love epic."),
    ("Füzuli poeziyası sadə hissi dərin fəlsəfi mənaya çevirir və buna görə əsrlər boyu oxunur.",
     "Fuzuli's poetry transforms simple emotion into profound philosophical meaning, which is why it has been read across the centuries."),

    # === hesen_bey_zerdabi ===
    ("Azərbaycan milli mətbuatının banisi, \"Əkinçi\" qəzetinin yaradıcısı və maarifçi təbiətşünas alim.",
     "The founder of Azerbaijani national press, creator of the Akinchi newspaper, and an enlightenment naturalist."),
    ("Zərdabi Azərbaycan xalqının maariflənməsini milli inkişafın əsas şərti sayırdı.",
     "Zardabi regarded the enlightenment of the Azerbaijani people as the fundamental precondition for national progress."),
    ("1875-ci ildə nəşr etdirdiyi \"Əkinçi\" qəzeti Azərbaycan dilində ilk qəzet kimi tarixə düşdü.",
     "The Akinchi newspaper, which he published in 1875, entered history as the first newspaper in the Azerbaijani language."),
    ("O, təbiətşünas, müəllim və ictimai xadim kimi kənd təsərrüfatı, təhsil və mədəniyyət sahələrinə töhfə verdi.",
     "As a naturalist, teacher, and public figure, he contributed to agriculture, education, and culture."),

    # === heyder_eliyev ===
    ("Müstəqil Azərbaycan dövlətçiliyinin formalaşmasında mühüm rol oynamış siyasi xadim və dövlət rəhbəri.",
     "A statesman and head of state who played a pivotal role in shaping the foundations of the independent Azerbaijani state."),
    ("Heydər Əliyev Azərbaycanın XX əsr siyasi tarixinin ən təsirli şəxsiyyətlərindən biridir.",
     "Heydar Aliyev is one of the most influential figures in Azerbaijan's political history of the twentieth century."),
    ("Sovet dövründə və müstəqillik illərində dövlət idarəçiliyində mühüm vəzifələr tutmuşdur.",
     "He held key positions in state governance both during the Soviet period and throughout the years of independence."),
    ("1993-cü ildən sonra müstəqil Azərbaycan dövlət institutlarının möhkəmlənməsi, beynəlxalq əlaqələr və enerji siyasəti onun adı ilə bağlıdır.",
     "From 1993 onwards, the consolidation of independent Azerbaijani state institutions, the development of international relations, and energy policy are closely associated with his name."),

    # === huseyn_cavid ===
    ("Azərbaycan romantik dramaturgiyasının zirvəsi, \"İblis\", \"Peyğəmbər\" və \"Şeyx Sənan\" kimi fəlsəfi dramların müəllifi.",
     "The pinnacle of Azerbaijani romantic drama — author of the philosophical plays Iblis, Prophet, and Sheikh Sanan."),
    ("Hüseyn Cavid Azərbaycan ədəbiyyatında fəlsəfi-romantik dramın ən böyük ustadıdır.",
     "Huseyn Javid is the greatest master of philosophical-romantic drama in Azerbaijani literature."),
    ("Onun əsərlərində insan, azadlıq, xeyir və şər, din və mənəviyyat kimi böyük suallar qoyulur.",
     "His works pose great questions concerning the human condition, freedom, good and evil, faith, and spirituality."),
    ("Stalin repressiyaları dövründə həbs edilərək sürgündə vəfat etməsi Cavid taleyini milli yaddaşın ağrılı səhifəsinə çevirmişdir.",
     "His arrest during the Stalinist repressions and death in exile have made his fate one of the most painful pages of national memory."),

    # === ibn_sina ===
    ("İbn Sina (980–1037) — bütün dövrlərin ən böyük həkimlərindən biri; 'Şeyxür-Rəis' (Alimlər Şahı) ləqəbini qazanmış ensiklopedist.",
     "Ibn Sina (980–1037) — one of the greatest physicians of all time; an encyclopedist acclaimed as the 'Sheikh al-Rais' (Prince of Scholars)."),
    ("Buxara yaxınlığında türk ailəsindən dünyaya gəlmiş bu dahi, 10 yaşında Quranı əzbərləmiş, 18 yaşında tam formalaşmış həkim olmuşdur.",
     "Born near Bukhara into a Turkic family, this prodigy had memorized the Quran by the age of ten and was a fully formed physician by eighteen."),
    ("'Tibb Qanunları' (əl-Qanun fit-Tibb) əsəri 600 ilə yaxın Avropa universitetlərinin əsas tibb dərsliyi olmuşdur.",
     "His Canon of Medicine (al-Qanun fi al-Tibb) served as the principal medical textbook in European universities for close to six hundred years."),
    ("İbn Sina — tam adı Əbu Əli Hüseyn ibn Abdullah ibn Sina — 980-ci ildə Buxara yaxınlığındakı Əfşana kəndində anadan olmuşdur.",
     "Ibn Sina — full name Abu Ali Husayn ibn Abdullah ibn Sina — was born in 980 in the village of Afshana near Bukhara."),
    ("Atası Abdullahın Balxdan gəlmiş bir türk olduğu rəvayət edilir.",
     "His father Abdullah is said to have been a Turk from Balkh."),
    ("Ailə tez Buxaraya köçmüş; İbn Sina burada istisnai bir zəka ilə böyümüşdür.",
     "The family soon moved to Bukhara, where Ibn Sina grew up as a child of exceptional intellect."),
    ("10 yaşında Quranı əzbərləmiş, 16 yaşında müstəqil tibbi tədqiqatlar aparır, 18 yaşında isə artıq tam formalaşmış həkim kimi tanınırdı.",
     "He had memorized the Quran at ten, was conducting independent medical research at sixteen, and by eighteen was already recognized as a fully formed physician."),
    ("Bir dəfə Samanilər hökmdarını müalicə etmiş, mükafat olaraq saray kitabxanasından istifadə haqqı almışdır — bu, onun elmi inkişafını misilsiz dərəcədə sürətləndirmişdir.",
     "Having once treated the Samanid ruler, he received as reward the right to use the royal library — an opportunity that accelerated his scholarly development immeasurably."),
    ("İbn Sina deyirdi: \"Hər çətin məsələyə rast gəldim, məscidə getdim, namaz qıldım, Allahdan kömək diləd im — problemi həll edəndən sonra yatdım; yuxuda cavabı gördüm.\"",
     "Ibn Sina said: 'Whenever I encountered a difficult problem, I went to the mosque, prayed, and sought God's help — then after solving it I slept; and in my sleep I saw the answer.'"),

    # === ismail_qaspirali ===
    ("İsmail Qaspıralı türk dünyasının böyük maarifçisi, \"Dildə, fikirdə, işdə birlik\" şüarının müəllifi və \"Tərcüman\" qəzetinin qurucusudur.",
     "Ismail Gasprinsky was the great educator of the Turkic world, author of the motto 'Unity in language, thought, and action,' and founder of the Tercuman newspaper."),
    ("Qaspıralı türk-müsəlman xalqlarının modern təhsil və mətbuat vasitəsilə oyanışını müdafiə edirdi.",
     "Gasprinsky championed the awakening of Turkic-Muslim peoples through modern education and the press."),
    ("Onun \"Tərcüman\" qəzeti Krımdan Qafqaza və Orta Asiyaya qədər geniş oxucu kütləsi qazandı.",
     "His Tercuman newspaper gained a wide readership stretching from Crimea to the Caucasus and Central Asia."),
    ("Cədid məktəbləri vasitəsilə yeni tədris üsulu və dünyəvi biliklərin yayılması ideyasını irəli sürdü.",
     "Through the Jadid schools, he promoted the idea of new teaching methods and the dissemination of secular knowledge."),

    # === katib_celebi ===
    ("Katib Çələbi Osmanlı ensiklopedisti, coğrafiyaçı və biblioqrafı, \"Kəşfüz-Zünun\" və \"Cihannüma\" əsərlərinin müəllifidir.",
     "Katip Çelebi was an Ottoman encyclopedist, geographer, and bibliographer — author of Kashf al-Zunun and Cihannuma."),
    ("Katib Çələbi İslam və Osmanlı elmi ənənəsində bilikləri sistemləşdirən ən mühüm şəxsiyyətlərdən biridir.",
     "Katip Çelebi is one of the most important figures in the Islamic and Ottoman scholarly tradition for systematizing knowledge."),
    ("\"Kəşfüz-Zünun\" minlərlə kitab və elm sahəsi haqqında məlumat verən nəhəng biblioqrafik ensiklopediyadır.",
     "Kashf al-Zunun is a vast bibliographic encyclopedia providing information on thousands of books and fields of learning."),
    ("\"Cihannüma\" Osmanlı coğrafiya düşüncəsini dünya coğrafiyası ilə əlaqələndirən mühüm əsərdir.",
     "Cihannuma is an important work that connects Ottoman geographical thought with world geography."),

    # === kul_tigin ===
    ("Kül Tigin (684–731) — İkinci Göytürk Xaqanlığının ən böyük sərkərdəsi; qardaşı Bilgə Xaqanın sağ qolu.",
     "Kül Tigin (684–731) — the greatest military commander of the Second Göktürk Khaganate and the right hand of his brother Bilge Khagan."),
    ("Bütün döyüşlərini qalibliklə bitirmiş, türk xalqlarının azadlığı uğrunda ömrünü sərf etmiş qəhrəman.",
     "A hero who concluded every battle in victory and devoted his life to the freedom of the Turkic peoples."),
    ("Onun şərəfinə qardaşı Bilgə Xaqan tərəfindən yazılmış Orxon kitabəsi türk dilinin ən qədim yazılı abidəsidir — bir hökmdarın böyük qardaşına sonsuz sevgi ilə yazdığı dastanvar mətn.",
     "The Orkhon inscription composed in his honour by his brother Bilge Khagan is one of the earliest written monuments of the Turkic language — an epic text written by a ruler with boundless devotion to his elder brother."),
    ("Kül Tigin — 684-cü ildə İlteriş Xaqanın oğlu olaraq dünyaya gəlmiş, türk tarixinin ən böyük hərbi dahilərindən biri kimi tanınmışdır.",
     "Kül Tigin was born in 684 as the son of İlterish Khagan and is recognized as one of the greatest military geniuses in Turkic history."),
    ("Kiçik yaşlarından döyüş meydanlarında böyümüş; at üstündəki ustalığı, cəsarəti və sürəti onu efsanəvi bir şəxsiyyətə çevirmişdir.",
     "He grew up on battlefields from an early age; his mastery on horseback, his courage, and his swiftness turned him into a legendary figure."),
    ("Qardaşı Bilgə Xaqanın siyasi idarəçiliyini hərbi gücü ilə tamamlamışdır.",
     "He complemented his brother Bilge Khagan's political governance with his military strength."),
    ("Türklərin Çinlilərə, Tatabılara, Türgişlərə, Qırgızlara qarşı apardığı bütün böyük döyüşlərdə Kül Tigin ön cəbhədə idi.",
     "In all the great battles fought by the Turks against the Chinese, the Tatabi, the Turgesh, and the Kyrgyz, Kül Tigin stood at the forefront."),
    ("Bir döyüşdə beş at altında öldürülmüş, özü isə yaralanmasına baxmayaraq qılıncını əldən buraxmamışdır.",
     "In one battle, five horses were killed beneath him, yet he refused to drop his sword despite his wounds."),
    ("Kitabədə yazılır: \"Kül Tigin qara aygır minib hücum etdi. O atı orada vurub öldürdülər. İkinci ata mindi, o da vuruldu. Üçüncü ata mindi...\" — Döyüş eposu kimi yazılmış bu parçalar türk nəsrinin ilk şah əsərləridir.",
     "The inscription records: 'Kül Tigin mounted the black stallion and charged. That horse was struck and killed there. He mounted a second horse; it too was struck. He mounted a third horse...' — Written in the manner of a battle epic, these passages are among the first masterpieces of Turkic prose."),

    # === lutfi_zade ===
    ("Lütfi Zadə 1921-ci ildə Bakıda doğuldu, gəncliyinin bir hissəsini İranda keçirdi, Tehran Universitetində elektrik mühəndisliyi üzrə təhsil aldı, daha sonra ABŞ-da MIT və Columbia Universitetlərində elmi hazırlığını davam etdirdi.",
     "Lotfi Zadeh was born in 1921 in Baku, spent part of his youth in Iran, studied electrical engineering at the University of Tehran, and later continued his academic training at MIT and Columbia University in the United States."),
    ("1959-cu ildən UC Berkeley-də çalışan alim burada elektrik mühəndisliyi, kompüter elmləri, idarəetmə nəzəriyyəsi və süni intellektin kəsişməsində dünya miqyaslı məktəb formalaşdırdı.",
     "From 1959, working at UC Berkeley, he built a world-class school at the intersection of electrical engineering, computer science, control theory, and artificial intelligence."),
    ("Zadənin 1965-ci ildə nəşr etdirdiyi \"Fuzzy Sets\" məqaləsi klassik ikiqiymətli məntiqdən fərqli olaraq obyektlərin bir çoxluğa mənsubiyyətinin 0 ilə 1 arasında dəyişən dərəcələrlə ifadə oluna biləcəyini göstərdi.",
     "Zadeh's 1965 paper Fuzzy Sets demonstrated that, unlike classical two-valued logic, the degree to which objects belong to a set can be expressed as a value varying continuously between 0 and 1."),
    ("Bu yanaşma qeyri-müəyyənliyi riyazi modelləşdirməyə imkan verdi və sonralar fuzzy logic, soft computing, computing with words, informasiya qranulasiyası və qərarvermə sistemləri kimi istiqamətlərin əsas nəzəri dayaqlarından birinə çevrildi.",
     "This approach made it possible to model uncertainty mathematically, and later became one of the principal theoretical foundations for fields such as fuzzy logic, soft computing, computing with words, information granulation, and decision-making systems."),
    ("İlk illərdə nəzəriyyəsi bəzən skeptik münasibətlə qarşılansa da, Zadə öz ideyasını ardıcıl şəkildə inkişaf etdirdi.",
     "Although his theory was sometimes met with scepticism in its early years, Zadeh developed his ideas with consistent determination."),
    ("Qeyri-səlis məntiq sənaye idarəetməsi, ekspert sistemləri, robototexnika, istehlak elektronikası və süni intellektdə geniş tətbiq sahəsi qazandı.",
     "Fuzzy logic found wide application in industrial control, expert systems, robotics, consumer electronics, and artificial intelligence."),
    ("Onun irsi Azərbaycan mənşəli bir alimin dünya elminə verdiyi ən mühüm töhfələrdən biri kimi tanınır.",
     "His legacy is recognized as one of the most important contributions that a scholar of Azerbaijani origin has made to world science."),

    # === mahmud_kasqari ===
    ("Mahmud Kaşğari (1005–1102) — türk dillərinin ilk böyük lüğət-ensiklopediyası olan 'Divanu Lüğat-it Türk'ün müəllifi.",
     "Mahmud al-Kashgari (1005–1102) — author of Diwan Lughat al-Turk, the first great lexical encyclopedia of the Turkic languages."),
    ("Türkoloji elminin banisi hesab edilən bu böyük alim, bütün türk ləhcələrini şəxsən tədqiq etmiş, onların söz xəzinəsini, qrammatikasını, şeirini, atalar sözlərini toplayaraq əbədiləşdirmişdir.",
     "Regarded as the founder of Turkological scholarship, this great scholar personally investigated all Turkic dialects and immortalized their vocabulary, grammar, poetry, and proverbs."),
    ("Əsərindəki dünya xəritəsi türk dünyasını mərkəzə alan ən qədim xəritələrdən biridir.",
     "The world map included in his work is one of the earliest maps to place the Turkic world at its centre."),
    ("Mahmud Kaşğari — Qaraxanlı türklərindən olan dilçi, coğrafiyaçı və ensiklopedist.",
     "Mahmud al-Kashgari was a linguist, geographer, and encyclopedist of Karakhanid Turkic origin."),
    ("\"Divanu Lüğat-it Türk\"ü (Türk Dillərinin Divanı) 1072–1074-cü illər arasında Bağdadda tamamlayaraq Abbasi xəlifəsi Muktədi Billaha ithaf etmişdir.",
     "He completed Diwan Lughat al-Turk (The Compendium of Turkic Languages) in Baghdad between 1072 and 1074, dedicating it to the Abbasid Caliph al-Muqtadi Billah."),
    ("Məqsədi Bağdad sarayında türk dilini tanıtmaq, ərəblərə türkcəni öyrətmək idi.",
     "His aim was to introduce the Turkic language to the Baghdad court and teach Arabic speakers Turkic."),
    ("Bu iş üçün o, əvvəlcə bütün türk yurdlarını gəzmiş — Kaşğardan tutmuş türk tayfalarının yaşadığı bütün bölgələrə qədər şəxsən gedərək dil nümunələri toplamışdır.",
     "For this purpose, he first travelled all the Turkic lands — personally visiting every region inhabited by Turkic tribes, from Kashgar onwards, to collect linguistic specimens."),
    ("Toplanmış material o dərəcədə zəngindir ki, bu gün artıq mövcud olmayan bir çox türk ləhcəsini yalnız Kaşğarinin əsərindən tanımaq mümkündür.",
     "The collected material is so rich that many Turkic dialects no longer extant today can only be known through Kashgari's work."),

    # === mimar_sinan ===
    ("Mimar Sinan Osmanlı klassik memarlığının ən böyük ustadı, Süleymaniyyə və Səlimiyyə məscidlərinin memarıdır.",
     "Mimar Sinan is the greatest master of Ottoman classical architecture — the architect of the Süleymaniye and Selimiye mosques."),
    ("Sinan yeniçəri ocağında mühəndislik təcrübəsi qazanmış, sonradan Osmanlı imperiyasının baş memarı olmuşdur.",
     "Sinan gained engineering experience in the Janissary corps before becoming the chief architect of the Ottoman Empire."),
    ("O, məscid, körpü, su kəməri, hamam və külliyələrdən ibarət yüzlərlə əsər yaratmışdır.",
     "He created hundreds of works including mosques, bridges, aqueducts, bathhouses, and mosque complexes."),
    ("Sinanın memarlığı funksionallıq, struktur dəqiqliyi və estetik harmoniya baxımından dünya memarlığının zirvələrindəndir.",
     "Sinan's architecture stands among the summits of world architecture in terms of functionality, structural precision, and aesthetic harmony."),

    # === mireli_qashqay ===
    ("Azərbaycan geologiya və mineralogiya elminin görkəmli nümayəndəsi, elmi məktəb yaradan alim.",
     "An outstanding representative of Azerbaijani geology and mineralogy — a scholar who founded a scientific school."),
    ("Mirəli Qaşqay Azərbaycan geologiya elminin inkişafında mühüm rol oynamışdır.",
     "Mirali Gashgay played a significant role in the development of Azerbaijani geological science."),
    ("O, mineralogiya, petrologiya və faydalı qazıntıların öyrənilməsi sahəsində tədqiqatlar aparmışdır.",
     "He conducted research in mineralogy, petrology, and the study of mineral resources."),
    ("Elmi təşkilatçı və akademik kimi Azərbaycan geologiya məktəbinin formalaşmasına töhfə vermişdir.",
     "As a scholarly organizer and academic, he contributed to the formation of the Azerbaijani school of geology."),

    # === mirze_elekber_sabir ===
    ("Sabir Azərbaycan satirik poeziyasının ən qüdrətli nümayəndəsi, \"Hophopnamə\" müəllifi və ictimai oyanışın poetik səsidir.",
     "Sabir is the most powerful representative of Azerbaijani satirical poetry — author of Hophopname and the poetic voice of social awakening."),
    ("Sabir \"Molla Nəsrəddin\" ədəbi məktəbinin ən parlaq şairlərindən idi.",
     "Sabir was one of the most brilliant poets of the Molla Nasraddin literary school."),
    ("O, cəhalət, fanatizm, sosial ədalətsizlik və ikiüzlülüyü kəskin satira ilə ifşa etdi.",
     "He exposed ignorance, fanaticism, social injustice, and hypocrisy with biting satire."),
    ("Onun poeziyası milli oyanış və ictimai düşüncə tarixində mühüm yer tutur.",
     "His poetry occupies an important place in the history of national awakening and social thought."),

    # === mirze_feteli_axundzade ===
    ("Azərbaycan dramaturgiyasının banisi, Şərqdə realist komediyanın yaradıcılarından biri və maarifçi mütəfəkkir.",
     "The founder of Azerbaijani drama, one of the creators of realist comedy in the East, and an Enlightenment thinker."),
    ("Axundzadə Azərbaycan ədəbiyyatında modern dramaturgiyanın əsasını qoydu.",
     "Akhundzadeh laid the foundations of modern drama in Azerbaijani literature."),
    ("Onun komediyaları cəmiyyətin geriliyini, xurafatı və nadanlığı satirik dillə ifşa edirdi.",
     "His comedies exposed social backwardness, superstition, and ignorance in a satirical idiom."),
    ("O, əlifba islahatı və maarifçilik ideyaları ilə Şərq modernləşməsi tarixində mühüm yer tutur.",
     "Through his alphabet reform and Enlightenment ideas, he occupies an important place in the history of Eastern modernization."),

    # === molla_penah_vaqif ===
    ("Azərbaycan realist şeirinin banilərindən biri, Qarabağ xanlığının vəziri və xalq dilinə yaxın poeziyanın böyük ustadı.",
     "One of the founders of Azerbaijani realist poetry, minister of the Karabakh khanate, and great master of poetry close to the vernacular."),
    ("Vaqif klassik şeirin ağır obrazlı dilini xalq danışığına yaxınlaşdırdı.",
     "Vagif brought the dense figurative language of classical poetry closer to vernacular speech."),
    ("O, Qarabağ xanlığında vəzir kimi də fəaliyyət göstərərək siyasi həyatda mühüm rol oynadı.",
     "He also served as minister of the Karabakh khanate, playing an important role in political life."),
    ("Onun şeirlərində həyatsevərlik, gözəllik duyğusu və realist müşahidə aparıcıdır.",
     "A love of life, a sense of beauty, and realist observation are the dominant qualities of his poetry."),

    # === mustafa_kamal_ataturk ===
    ("Türkiyə Respublikasının qurucusu, modern türk dövlətçiliyinin, hüquq və təhsil islahatlarının əsas memarı.",
     "The founder of the Republic of Türkiye and the principal architect of the modern Turkish state, legal, and educational reforms."),
    ("Mustafa Kamal Atatürk Osmanlı imperiyasının süqutundan sonra Türkiyə İstiqlal Müharibəsinə rəhbərlik etdi.",
     "Mustafa Kemal Atatürk led the Turkish War of Independence following the fall of the Ottoman Empire."),
    ("1923-cü ildə Türkiyə Respublikası elan edildi və Atatürk modern dövlət institutlarının qurulmasına başladı.",
     "In 1923, the Republic of Türkiye was proclaimed, and Atatürk set about building modern state institutions."),
    ("Onun islahatları hüquq, təhsil, əlifba, dünyəvilik və milli suverenlik ideyaları ətrafında formalaşdı.",
     "His reforms centred on law, education, the alphabet, secularism, and the idea of national sovereignty."),

    # === muxtar_euezov ===
    ("Qazax ədəbiyyatının klassiki, \"Abay yolu\" epopeyası ilə qazax xalqının mənəvi tarixini dünya ədəbiyyatına gətirən yazıçı.",
     "A classic of Kazakh literature — the writer who brought the spiritual history of the Kazakh people to world literature through the Abai Road epic."),
    ("Muxtar Əuezov qazax ədəbiyyatının ən böyük simalarından biridir.",
     "Mukhtar Auezov is one of the greatest figures of Kazakh literature."),
    ("Onun \"Abay yolu\" roman-epopeyası qazax şairi Abayın həyatı fonunda xalqın sosial və mənəvi tarixini təsvir edir.",
     "His novel-epic Abai Road depicts the social and spiritual history of the Kazakh people against the backdrop of the life of the poet Abai."),
    ("Əuezov həm yazıçı, həm dramaturq, həm də ədəbiyyatşünas kimi böyük irs qoymuşdur.",
     "Auezov left a great legacy as writer, playwright, and literary scholar alike."),

    # === namiq_kamal ===
    ("Namiq Kamal Osmanlı Tanzimat ədəbiyyatının aparıcı siması, vətən, azadlıq və hüquq ideyalarını ədəbiyyata gətirən yazıçı və mütəfəkkirdir.",
     "Namık Kemal is the leading figure of Ottoman Tanzimat literature — a writer and thinker who introduced the ideas of homeland, freedom, and rights into literature."),
    ("Namiq Kamal Osmanlı modernləşməsi dövründə ədəbiyyatı ictimai-siyasi fikir meydanına çevirdi.",
     "Namık Kemal transformed literature into an arena of socio-political thought during the era of Ottoman modernization."),
    ("Onun \"Vətən yaxud Silistre\" dramı vətənpərvərlik duyğusunu geniş kütlələrə çatdırdı.",
     "His drama Homeland, or Silistria conveyed the feeling of patriotism to broad audiences."),
    ("O, mətbuat, teatr və poeziya vasitəsilə konstitusiya, azadlıq və vətəndaşlıq ideyalarını müdafiə etdi.",
     "Through journalism, theatre, and poetry, he advocated the ideas of constitutionalism, freedom, and civic rights."),

    # === nehqsbend ===
    ("Bəhaəddin Nəqşbənd (1318–1389) — Nəqşbəndilik təriqətinin banisi; Orta Asiya mənəvi mədəniyyətinin ən böyük şəxsiyyətlərindən biri.",
     "Baha ud-Din Naqshband (1318–1389) — the founder of the Naqshbandi order; one of the greatest figures of Central Asian spiritual culture."),
    ("Buxara yaxınlığında Qəsr-i Arifan kəndindən anadan olan bu böyük sufi, 'Dildə xalq ilə, qəlbdə Allah ilə ol' prinsipini yaşayış tərzi halına gətirmiş; işlə, əmə klə, cəmiyyətin içindəolmaqla Allaha yaxınlaşmağı mümkün sayan bir təriqətin banisi olmuşdur.",
     "Born in the village of Qasr-i Arifan near Bukhara, this great Sufi embodied the principle 'Be with the people in word, with God in heart' as a way of life — he was the founder of an order that regarded approaching God through work, labour, and living within society as possible."),
    ("Bəhaəddin Nəqşbənd — 1318-ci ildə Buxara yaxınlığındakı Qəsr-i Arifan (bugünkü Özbəkistanda) kəndindəanadan olmuşdur.",
     "Baha ud-Din Naqshband was born in 1318 in the village of Qasr-i Arifan near Bukhara (in present-day Uzbekistan)."),
    ("\"Nəqşbənd\" ləqəbi iki mənada şərh edilir: ya ipəkyə naxış vuran ustanın nəslindəndir, ya da qəlbə Allah adının naxışını vuran mənasındadır.",
     "The epithet 'Naqshband' is interpreted in two senses: either as descending from a craftsman who embroiders patterns on silk, or as meaning 'one who engraves the name of God upon the heart.'"),
    ("Nəqşbəndilik təriqəti Yəsəvi ənənəsindənruhlansa da, onu farqlı edən əsas xüsusiyyət: bu təriqət xilvətdən (dünyadan uzaqlaşmaq) yox, \"xilvət dər əncomən\"dən (xalq arasındakəsintilik) keçir.",
     "Although the Naqshbandi order drew inspiration from the Yasawi tradition, the key feature that distinguishes it is that it proceeds not through khalwa (withdrawal from the world), but through 'khalwat dar anjuman' — inner seclusion amid the company of people."),
    ("Yəni sufi cəmiyyətin içindəyaşamalı, çalışmalı, əl emeyi ilə güzəranını qazanmalı, amma qəlbini daima Allaha bağlı saxlamalıdır.",
     "That is to say, the Sufi should live within society, work, earn a livelihood by the labour of one's hands, yet keep one's heart perpetually bound to God."),
    ("\"Dil yarda, qəl yarda\" — Qəlbdə Allahla birlikdə ol, lakin bədənlə insanlar içindəol. Nəqşbəndilik fəlsəfəsinin özəyi bu cümledədir.",
     "\"Be with the heart in the Divine, yet with the body among people.\" — The essence of the Naqshbandi philosophy is contained in this single sentence."),

    # === nesimi ===
    ("İmadəddin Nəsimi Azərbaycan, fars və ərəb dillərində yazmış böyük şair, hürufi fəlsəfəsinin ən qüdrətli poetik səsi idi.",
     "Imadaddin Nasimi was a great poet who wrote in Azerbaijani, Persian, and Arabic — the most powerful poetic voice of Hurufite philosophy."),
    ("Onun poeziyası insanın ilahi mahiyyətini, mənəvi azadlığı və daxili ucalığı tərənnüm edir.",
     "His poetry celebrates the divine essence of the human being, spiritual freedom, and inner elevation."),
    ("Nəsimi Azərbaycan klassik poeziyasında ana dilinin ifadə imkanlarını genişləndirən ən böyük simalardan biridir.",
     "Nasimi is one of the greatest figures who expanded the expressive possibilities of the mother tongue in Azerbaijani classical poetry."),
    ("O, hürufi ideyalarını yüksək bədii dillə xalqa çatdırmışdır.",
     "He conveyed Hurufite ideas to the people through a refined artistic idiom."),
    ("Şairin qəzəllərində insan kosmik varlıq kimi təqdim olunur: insanın simasında, sözündə və ruhunda ilahi hikmət axtarılır.",
     "In the poet's ghazals, the human being is presented as a cosmic entity: divine wisdom is sought in the human countenance, word, and spirit."),
    ("Nəsiminin faciəli ölümü onun adını azad düşüncə və mənəvi cəsarət rəmzinə çevirmişdir.",
     "Nasimi's tragic death transformed his name into a symbol of free thought and spiritual courage."),

    # === nesireddin_tusi ===
    ("Nəsirəddin Tusi (1201–1274) — Azərbaycanın ən böyük ensiklopedist alimi.",
     "Nasir al-Din al-Tusi (1201–1274) — the greatest encyclopedic scholar of Azerbaijan."),
    ("Riyaziyyat, astronomiya, fəlsəfə, etika, məntiq sahəsindəki fundamental töhfələri ilə bütün zamanların görkəmli zəkaları arasında yer alır.",
     "His fundamental contributions to mathematics, astronomy, philosophy, ethics, and logic place him among the distinguished intellects of all time."),
    ("Marağa rəsədxanasını qurmuş, trigonometrikanı müstəqil elm kimi formalaşdırmış, 'Əxlaq-i Nasiri' ilə etika fəlsəfəsinin klassikləri sırasına daxil olmuşdur.",
     "He established the Maragha observatory, developed trigonometry as an independent science, and with Akhlaq-i Nasiri joined the ranks of the classics of ethical philosophy."),
    ("Kopernikdən öncə planetlərin hərəkət modelini yenidən qurmağa cəhd etmişdir.",
     "He attempted to reconstruct the model of planetary motion before Copernicus."),
    ("Nəsirəddin Tusi — 1201-ci ildə bugünkü İranın Tus şəhərindəyanadan olmuşdur; lakin türk əsilli Azərbaycan alimi kimi tanınır.",
     "Nasir al-Din al-Tusi was born in 1201 in the city of Tus (in present-day Iran) but is recognized as an Azerbaijani scholar of Turkic origin."),
    ("Monqol hökmdarı Hülagünün dəstəyilə 1259-cu ildə Azərbaycanın Marağa şəhərindəqurduğu rəsədxana, dövrünün dünyasındakı ən müasir elmi müəssisəsi idi.",
     "The observatory he founded in 1259 in Maragha, Azerbaijan, with the support of the Mongol ruler Hulagu, was the most advanced scientific institution of its time."),
    ("Burada Çin, Farsıstan, Suriya, Bizansdan gəlmiş alimlər birgə çalışmışdır.",
     "Scholars from China, Persia, Syria, and Byzantium worked there together."),
    ("Trigonometrikanı müstəqil bir elm sahəsi kimi formalaşdırmışdır.",
     "He established trigonometry as an independent scientific discipline."),

    # === nizami_gencevi ===
    ("Nizami Gəncəvi — dünya ədəbiyyatının ən böyük klassiklərindən biri, \"Xəmsə\" müəllifi və Azərbaycan poetik-fəlsəfi fikrinin zirvəsidir.",
     "Nizami Ganjavi — one of the greatest classics of world literature, author of the Khamsa, and the summit of Azerbaijani poetic-philosophical thought."),
    ("Onun əsərlərində insan ləyaqəti, ədalət, elm, sevgi, hökmdar məsuliyyəti və mənəvi kamillik ideyaları yüksək bədii qüvvə ilə ifadə olunur.",
     "In his works, the ideas of human dignity, justice, knowledge, love, the responsibility of rulers, and spiritual refinement are expressed with great artistic power."),
    ("Nizami Gəncəvi XII əsrdə Gəncədə yaşamış, farsdilli klassik poeziyanın ən böyük ustadlarından biri kimi dünya ədəbiyyatına daxil olmuşdur.",
     "Nizami Ganjavi lived in Ganja in the twelfth century and entered world literature as one of the greatest masters of classical Persian-language poetry."),
    ("O, saray şairi olmaqdan daha çox müstəqil fikirli mütəfəkkir kimi tanınırdı.",
     "He was known less as a court poet and more as a thinker of independent mind."),
    ("Nizaminin \"Xəmsə\"si beş poemadan ibarət möhtəşəm bədii-fəlsəfi sistemdir.",
     "Nizami's Khamsa is a magnificent artistic-philosophical system comprising five narrative poems."),
    ("Bu əsərlərdə Şərq və Qərb mədəniyyəti, antik irs, İslam düşüncəsi və xalq hikməti bir araya gəlir.",
     "In these works, Eastern and Western culture, the classical heritage, Islamic thought, and folk wisdom converge."),
    ("Onun poeziyasında insanın daxili kamilliyi, ədalətli idarəçilik və bilik kultu aparıcı xəttdir.",
     "The inner perfection of the human being, just governance, and the cultivation of knowledge are the dominant threads of his poetry."),
    ("Nizami yalnız şair deyil, həm də böyük humanist mütəfəkkir idi.",
     "Nizami was not merely a poet but also a great humanist thinker."),

    # === omer_xeyyam ===
    ("Ömər Xəyyam (1048–1131) — riyaziyyat, astronomiya, fəlsəfə və şeir sahəsini bir araya gətirən nadir bir dahi.",
     "Omar Khayyam (1048–1131) — a rare genius who united mathematics, astronomy, philosophy, and poetry in a single life."),
    ("Xorasanlı türk alimi kimi kubik tənliklər üzərindəki əsərləri ilə riyaziyyat tarixinə girmiş; Cəlali təqviminin hazırlanmasına iştirak etmiş; lakin dünyaya rübailerinin melankoli fəlsəfəsiylə tanınmışdır.",
     "As a Khorasani Turkic scholar, he entered the history of mathematics through his work on cubic equations, participated in the creation of the Jalali calendar, yet became known to the world through the melancholy philosophy of his rubaiyat."),
    ("Edward FitzGeraldın ingilis tərcüməsi onu dünya şöhrətinə qovuşdurmuşdur.",
     "Edward FitzGerald's English translation brought him to world fame."),
    ("Ömər Xəyyam — 1048-ci ildə Nişapur şəhərində anadan olmuşdur.",
     "Omar Khayyam was born in 1048 in the city of Nishapur."),
    ("Türk mənşəli olduğu güman edilir; \"Xəyyam\" soyadı isə çadır toxuyanların nəslindən gəldiyinə işarədir.",
     "He is believed to have been of Turkic origin; the name 'Khayyam' alludes to descent from tentmakers."),
    ("Riyaziyyatda kubik tənlikləri həndəsi üsulla həll etmiş — bu, Avropalıların eyni məsələni həll etməsindən 500 il öncədir.",
     "In mathematics, he solved cubic equations by geometrical methods — five hundred years before Europeans solved the same problems."),
    ("Cəlali təqviminin hazırlanmasında baş astronomluq etmiş; bu təqvim Qreqorian təqvimindən daha dəqiqdir.",
     "He served as chief astronomer in the preparation of the Jalali calendar — a calendar more accurate than the Gregorian."),
    ("Lakin Xəyyam dünyaya daha çox rübailerinin şairı kimi tanınır.",
     "Yet Khayyam is known to the world above all as the poet of his rubaiyat."),
    ("\"Gəl, sabahı düşünmə; bu anı yaşa\" — bu fəlsəfə ilk baxışda hedonizm kimi görünsə də, əslində fani dünyanın anlamını dərindən sorgulayan bir düşüncədir.",
     "'Come, do not think of tomorrow; live this moment' — this philosophy may appear hedonistic at first glance, yet it is in truth a deeply searching meditation on the meaning of transient existence."),

    # === orhan_pamuk ===
    ("2006-cı il Nobel ədəbiyyat mükafatı laureatı, müasir türk romanının dünyada ən tanınmış nümayəndələrindən biri.",
     "The 2006 Nobel Laureate in Literature and one of the most internationally recognized representatives of the contemporary Turkish novel."),
    ("Orhan Pamuk romanlarında İstanbul, yaddaş, kimlik, Şərq-Qərb münasibətləri və fərdi taleyin mədəni kontekstini araşdırır.",
     "In his novels, Orhan Pamuk explores Istanbul, memory, identity, East-West relations, and the cultural context of individual fate."),
    ("2006-cı ildə Nobel ədəbiyyat mükafatına layiq görülərək bu mükafatı alan ilk türk yazıçısı oldu.",
     "In 2006, he was awarded the Nobel Prize in Literature, becoming the first Turkish writer to receive this honour."),
    ("Onun əsərləri dünyanın bir çox dilinə tərcümə edilmişdir.",
     "His works have been translated into many languages of the world."),

    # === piri_reis ===
    ("Piri Reis Osmanlı admiralı və kartoqrafı, 1513-cü il dünya xəritəsi və \"Kitab-ı Bahriye\" əsəri ilə dünya coğrafiya tarixində mühüm yer tutan şəxsiyyətdir.",
     "Piri Reis was an Ottoman admiral and cartographer who occupies an important place in the history of world geography through his 1513 world map and his work Kitab-i Bahriye."),
    ("Piri Reis dənizçi ailəsində yetişmiş, Osmanlı donanmasında xidmət etmiş və Aralıq dənizi coğrafiyasını dərindən öyrənmişdir.",
     "Piri Reis grew up in a seafaring family, served in the Ottoman navy, and acquired a deep knowledge of Mediterranean geography."),
    ("Onun 1513-cü il dünya xəritəsi Amerika qitəsini göstərən ən erkən xəritələrdən biri kimi məşhurdur.",
     "His 1513 world map is famous as one of the earliest maps to depict the American continent."),
    ("\"Kitab-ı Bahriye\" dənizçilər üçün limanlar, sahillər və marşrutlar haqqında qiymətli məlumat verən ensiklopedik əsərdir.",
     "Kitab-i Bahriye is an encyclopedic work providing valuable information for sailors on harbours, coastlines, and routes."),

    # === qara_qarayev ===
    ("Azərbaycan XX əsr bəstəkarlığının ən böyük nümayəndələrindən biri, balet və simfonik musiqi ustası.",
     "One of the greatest representatives of twentieth-century Azerbaijani composition — a master of ballet and symphonic music."),
    ("Qara Qarayev Azərbaycan musiqisində modern bəstəkarlıq dilinin formalaşmasına böyük təsir göstərmişdir.",
     "Kara Karayev exerted a profound influence on the formation of the modern compositional language in Azerbaijani music."),
    ("O, milli musiqi intonasiyalarını dünya klassik və modern musiqi üsulları ilə birləşdirdi.",
     "He brought together national musical intonations with the techniques of classical and modern world music."),
    ("\"Yeddi gözəl\" və \"İldırımlı yollarla\" baletləri onun yaradıcılığının zirvələrindəndir.",
     "His ballets The Seven Beauties and Along the Path of Thunder are among the peaks of his creative output."),

    # === reshid_behbudov ===
    ("Azərbaycan vokal sənətinin əfsanəsi, xalq və estrada musiqisini dünya səhnələrinə çıxaran böyük müğənni və aktyor.",
     "The legend of Azerbaijani vocal art — a great singer and actor who brought folk and popular music to world stages."),
    ("Rəşid Behbudov bənzərsiz səs tembri və səhnə mədəniyyəti ilə Azərbaycan musiqisini beynəlxalq arenada tanıtdı.",
     "Rashid Behbudov introduced Azerbaijani music to the international arena through his incomparable vocal timbre and stage culture."),
    ("O, \"Arşın mal alan\" filmindəki rolu ilə geniş şöhrət qazandı.",
     "He won wide acclaim for his role in the film Arshın Mal Alan."),
    ("Dünyanın bir çox ölkəsində çıxış edərək Azərbaycan mahnılarını müxtəlif xalqlara sevdirdi.",
     "Performing in many countries of the world, he won the affection of diverse peoples for Azerbaijani songs."),

    # === shah_ismayil_xetai ===
    ("Səfəvilər dövlətinin qurucusu və Azərbaycan türkcəsində yazmış qüdrətli şair.",
     "The founder of the Safavid state and a powerful poet who wrote in the Azerbaijani Turkic language."),
    ("Xətai təxəllüsü ilə yazdığı şeirlərdə dini-fəlsəfi düşüncə, döyüş ruhu və ana dilinə sevgi ifadə olunur.",
     "In the poems he composed under the pen name Khatai, religious-philosophical thought, martial spirit, and love of the mother tongue find expression."),
    ("Səfəvilər dövlətinin qurucusu kimi Şah İsmayıl Azərbaycan tarixində mərkəzləşdirilmiş dövlətçilik ənənəsinin ən mühüm simalarındandır.",
     "As the founder of the Safavid state, Shah Ismail is one of the most significant figures in the tradition of centralized statecraft in Azerbaijani history."),
    ("O, yalnız hökmdar deyil, Xətai təxəllüsü ilə yazan şair idi və Azərbaycan türkcəsinin saray və ədəbiyyat dili kimi nüfuzunu artırdı.",
     "He was not merely a ruler but also a poet writing under the pen name Khatai, who elevated the prestige of Azerbaijani Turkic as a language of court and literature."),
    ("Onun irsi siyasi tarix, ədəbiyyat və dini-fəlsəfi düşüncə baxımından çoxqatlıdır.",
     "His legacy is multi-layered in terms of political history, literature, and religious-philosophical thought."),

    # === tofiq_quliyev ===
    ("Azərbaycan kino və estrada musiqisinin ustadı, caz elementlərini milli musiqi ilə birləşdirən bəstəkar.",
     "A master of Azerbaijani film and popular music — a composer who blended jazz elements with national musical traditions."),
    ("Tofiq Quliyev Azərbaycan mahnı və kino musiqisinin ən sevilən simalarındandır.",
     "Tofig Guliyev is one of the most beloved figures of Azerbaijani song and film music."),
    ("O, caz intonasiyalarını milli melodika ilə birləşdirərək özünəməxsus üslub yaratdı.",
     "He merged jazz intonations with national melody, creating a distinctive personal style."),
    ("Onun filmlər üçün yazdığı musiqilər Azərbaycan tamaşaçı yaddaşında xüsusi yer tutur.",
     "The music he wrote for films occupies a special place in the memory of Azerbaijani audiences."),

    # === ulubey ===
    ("Ulubəy Teymurilər dövrünün hökmdar-alimi, Səmərqənd rəsədxanasının qurucusu və orta əsr astronomiyasının ən parlaq nümayəndələrindən biridir.",
     "Ulugh Beg was the scholar-ruler of the Timurid era, founder of the Samarkand observatory, and one of the most brilliant representatives of medieval astronomy."),
    ("Ulubəy hökmdar ailəsində doğulsa da, tarixdə daha çox astronom və riyaziyyatçı kimi tanınır.",
     "Although Ulugh Beg was born into a ruling family, he is better remembered in history as an astronomer and mathematician."),
    ("Onun Səmərqənddə yaratdığı elmi mühit XV əsr Mərkəzi Asiya Renessansının simvoludur.",
     "The scholarly milieu he created in Samarkand is a symbol of the Central Asian Renaissance of the fifteenth century."),
    ("Səmərqənd rəsədxanasında ulduzların koordinatları böyük dəqiqliklə ölçülmüş, astronomik cədvəllər hazırlanmışdır.",
     "At the Samarkand observatory, stellar coordinates were measured with great precision and astronomical tables were prepared."),
    ("Ulubəyin elmi irsi Şərq və Avropa astronomiyasına təsir göstərmiş, onun ulduz kataloqu uzun müddət istifadə olunmuşdur.",
     "Ulugh Beg's scientific legacy influenced Eastern and European astronomy alike, and his star catalogue remained in use for a long period."),

    # === uzeyir_hacibeyov ===
    ("Azərbaycan professional musiqisinin banisi, müsəlman Şərqində ilk operanın müəllifi və milli musiqi təhsilinin qurucusu.",
     "The founder of professional Azerbaijani music, author of the first opera in the Muslim East, and the founder of national music education."),
    ("Üzeyir Hacıbəyov Azərbaycan musiqisində Şərq muğam ənənəsi ilə Avropa klassik formalarını birləşdirdi.",
     "Uzeyir Hajibeyli united the Eastern mugham tradition with European classical forms in Azerbaijani music."),
    ("1908-ci ildə səhnələşdirilən \"Leyli və Məcnun\" operası müsəlman Şərqində ilk opera kimi qəbul edilir.",
     "The opera Layla and Majnun, staged in 1908, is recognized as the first opera in the Muslim East."),
    ("O, bəstəkar, publisist, pedaqoq və ictimai xadim kimi milli musiqi mədəniyyətinin bütün sistemini formalaşdırdı.",
     "As a composer, journalist, pedagogue, and public figure, he shaped the entire system of national musical culture."),

    # === yusif_balasaqunlu ===
    ("Yusif Balasaqunlu (1019–1085) — türk dilinin ən qədim ədəbi şah əsəri 'Qutadqu Bilik'in (Səadətə Aparan Elm) müəllifi.",
     "Yusuf Balasaguni (1019–1085) — author of Kutadgu Bilig (Wisdom that Brings Happiness), the earliest great literary masterpiece of the Turkic language."),
    ("Qaraxanlı türklərindən olan bu filosof-şair, 6645 beyitlik böyük əsərini Kaşğar sarayına ithaf etmişdir.",
     "This philosopher-poet of Karakhanid Turkic origin dedicated his great work of 6,645 couplets to the court of Kashgar."),
    ("Əsər yalnız ədəbiyyat deyil, həm də türk dilindəki ilk siyasi fəlsəfə traktatıdır: ədalətli idarəçilik, xoşbəxtlik, bilik və həyat arasındakı dərin münasibəti şeir formasında işləyir.",
     "The work is not merely literature but also the first political philosophy treatise in the Turkic language: it develops in verse form the profound relationship between just governance, happiness, knowledge, and life."),
    ("Yusif Balasaqunlu — bugünkü Qırğızıstanın Balasagun şəhərindən olan Qaraxanlı türk şairi və dövlət adamı.",
     "Yusuf Balasaguni was a Karakhanid Turkic poet and statesman from the city of Balasagun (in present-day Kyrgyzstan)."),
    ("\"Qutadqu Bilik\" (Qutlu Bilik / Səadətə Aparan Elm) adlı əsərini 1069-cu ildə tamamlayaraq Qaraxanlı xaqanı Tavğaç Buğra Xana ithaf etmişdir.",
     "He completed the work known as Kutadgu Bilig (Blessed Knowledge / Wisdom that Brings Happiness) in 1069 and dedicated it to the Karakhanid khagan Tabgach Bughra Khan."),
    ("Xan onu mükafatlandıraraq \"Xas Hacib\" (Xüsusi Saray Naziri) rütbəsi vermişdir.",
     "The khan rewarded him by conferring the title of 'Has Hajib' (Special Court Chamberlain)."),
    ("Əsər dörd alleqorik personaj üzərindən qurulmuşdur: Köntöldi (ədalət), Aytoldi (dövlət bəxti), Ögdülmüş (ağıl), Odğurmuş (qənaət).",
     "The work is structured around four allegorical figures: Kuntugdi (justice), Aytoildi (fortune of state), Ogdulmish (reason), and Odgurmish (contentment)."),
    ("Bu dörd fiqur arasındakı dialoqular vasitəsilə müəllif ideal hökmdar, ideal vəzir, ideal alim və ideal insan obrazlarını təsvir edir.",
     "Through the dialogues among these four figures, the author depicts the ideal ruler, the ideal minister, the ideal scholar, and the ideal human being."),

    # === yusif_memmedeliyev ===
    ("Azərbaycan kimya elminin görkəmli nümayəndəsi, neft-kimya tədqiqatları və Elmlər Akademiyasının inkişafı ilə tanınan alim.",
     "An outstanding representative of Azerbaijani chemistry — a scholar known for petroleum-chemistry research and the development of the Academy of Sciences."),
    ("Yusif Məmmədəliyev Azərbaycan neft-kimya elminin inkişafında mühüm rol oynamışdır.",
     "Yusif Mammadaliyev played a significant role in the development of Azerbaijani petroleum chemistry."),
    ("Onun tədqiqatları yüksək oktanlı yanacaq və neft məhsullarının kimyəvi emalı sahələri ilə bağlı idi.",
     "His research was concerned with high-octane fuels and the chemical processing of petroleum products."),
    ("O, Azərbaycan Elmlər Akademiyasının prezidenti kimi milli elmi institutların formalaşmasına töhfə vermişdir.",
     "As President of the Azerbaijan Academy of Sciences, he contributed to the formation of national scholarly institutions."),

    # === yusif_vezir_chemenzeminli ===
    ("Azərbaycan tarixi romanının inkişafında mühüm rol oynamış yazıçı, diplomat və ictimai xadim.",
     "A writer, diplomat, and public figure who played an important role in the development of the Azerbaijani historical novel."),
    ("Yusif Vəzir Çəmənzəminli Azərbaycan nəsrində tarixi mövzulara geniş yer verən yazıçılardandır.",
     "Yusif Vazir Chamanzaminli is among the writers who gave considerable scope to historical themes in Azerbaijani prose."),
    ("O, Azərbaycan Xalq Cümhuriyyəti dövründə diplomatik fəaliyyətdə də iştirak etmişdir.",
     "He also participated in diplomatic activities during the period of the Azerbaijan Democratic Republic."),
    ("Stalin repressiyaları dövründə həbs olunaraq sürgündə vəfat etmişdir.",
     "He was arrested during the Stalinist repressions and died in exile."),

    # === ziya_gokalp ===
    ("Türk sosiologiyasının və türkçülük ideologiyasının əsas nəzəriyyəçilərindən biri.",
     "One of the principal theorists of Turkish sociology and the Turkist ideology."),
    ("Ziya Gökalp Osmanlıdan Cümhuriyyətə keçid dövründə milli kimlik, mədəniyyət və modernləşmə mövzularını sistemləşdirdi.",
     "Ziya Gökalp systematized the themes of national identity, culture, and modernization during the transition from the Ottoman Empire to the Republic."),
    ("O, sosiologiyanı türk ictimai fikrinə gətirən əsas şəxslərdən sayılır.",
     "He is considered one of the key figures who introduced sociology to Turkish social thought."),
    ("\"Türkləşmək, İslamlaşmaq, Müasirləşmək\" ideyası onun düşüncə sisteminin mərkəzində dayanırdı.",
     "'Turkification, Islamisation, Modernisation' was the central idea of his system of thought."),
]

EXTRA_TRANSLATIONS: list[tuple[str, str]] = [
    ("Ərəb ölkələri tarixi və mənbəşünaslıq üzrə işlər.",
     "Works on the history of Arab countries and source studies."),
    ("Azərbaycan Xalq Cəbhəsi və istiqlal hərəkatı.",
     "The Azerbaijan Popular Front and the independence movement."),
    ("Siyasi və mədəni konsepsiya.",
     "A political and cultural concept."),
    ("O, türk xalqları arasında mədəni-siyasi yaxınlaşmanı vacib sayırdı.",
     "He regarded cultural and political rapprochement among Turkic peoples as essential."),
    ("Şərqşünaslıq sahəsində elmi fəaliyyət göstərdi",
     "Conducted scholarly work in Oriental studies"),
    ("Türk birliyi ideyasını müdafiə etdi",
     "Defended the idea of Turkic unity"),
    ("O, siyasi nüfuzunu mədəni quruculuğa yönəltmiş, alimləri, şairləri və sənətkarları dəstəkləmiş, sonrakı əsrlərdə Mərkəzi Asiya və bütün türk dünyasında klassik modelə çevrilmişdir.",
     "He directed his political influence toward cultural building, supported scholars, poets, and artists, and became a classical model across Central Asia and the wider Turkic world in later centuries."),
    ("Bu səbəbdən Nəvai yalnız öz dövrünün deyil, ümumtürk yazılı mədəniyyətinin əsas simalarından biri kimi qiymətləndirilir.",
     "For this reason, Navoi is valued not only as a figure of his own era but as one of the principal architects of the shared written culture of the Turkic world."),
    ("Onun satiraları riyakarlıq, ədalətsizlik və sosial nöqsanlara qarşı yönəlmişdi.",
     "His satirical poems were directed against hypocrisy, injustice, and social failings."),
    ("Şair xalq dilinə yaxın, canlı və istehzalı üslubla yazırdı.",
     "The poet wrote in a style close to the vernacular — lively and satirical."),
    ("Türk mənşəli olduğu güman edilir; \"Xəyyam\" soyadı isə çadır toxuyanların nəslindən gəldiyinə işarədir.",
     "He is believed to be of Turkic origin; the surname Khayyam is thought to indicate descent from tent makers."),
    ("Gəncliyindən riyaziyyat, astronomiya, fəlsəfə sahəsindəki istedadı ilə diqqəti cəlb etmiş, Səlcuqlu sarayında iş aparmışdır.",
     "From youth he attracted attention through talent in mathematics, astronomy, and philosophy, and worked at the Seljuk court."),
    ("\"Gəl, sabahı düşünmə; bu anı yaşa\" — bu fəlsəfə ilk baxışda hedonizm kimi görünsə də, əslində fani dünyanın anlamını dərindən sorgulayan bir düşüncədir.",
     "\"Come, do not think of tomorrow; live this moment\" — this philosophy may appear hedonistic at first glance, yet it is in fact a deeply probing meditation on the meaning of mortal life."),
    ("Gəncliyindən riyaziyyat, astronomiya, fəlsəfə sahəsindəki dərin bilikləri ilə məşhurlaşmış; Hülagü xanın elmi məsləhətçisi olmuşdur.",
     "Renowned from youth for deep knowledge in mathematics, astronomy, and philosophy, he served as scientific adviser to Hulegu Khan."),
    ("Marağa rəsədxanasını qurmuş, trigonometrikanı müstəqil elm kimi formalaşdırmış, 'Əxlaq-i Nasiri' ilə etika fəlsəfəsinin klassikləri sırasına daxil olmuşdur.",
     "He established the Maragha observatory, helped shape trigonometry as an independent science, and entered the classics of ethical philosophy with Akhlaq-i Nasiri."),
    ("Buxara yaxınlığında Qəsr-i Arifan kəndindən anadan olan bu böyük sufi, 'Dildə xalq ilə, qəlbdə Allah ilə ol' prinsipini yaşayış tərzi halına gətirmiş; işlə, əməklə, cəmiyyətin içində olmaqla Allaha yaxınlaşmağı öyrətmişdir.",
     "Born in the village of Qasr-i Arifan near Bukhara, this great Sufi made the principle 'With the people in speech, with God in heart' a way of life, teaching closeness to God through work, labour, and participation in society."),
    ("Elçibəyin fəaliyyəti akademik araşdırmadan milli hərəkat liderliyinə qədər genişləndi.",
     "Elchibey's career extended from academic research to leadership of the national movement."),
    ("716-cı ildə ağır xəstəlikdən vəfat edən böyük qardaşının ardından \"Bilgə Xaqan\" titulu ilə xaqan olmuşdur.",
     "After the death of his elder brother from a severe illness in 716, he ascended as khagan with the title Bilge Khagan."),
    ("Bilgə Xaqan kitabələrdə türk xalqına müraciət edərək deyir: \"Türk milleti, aç idiysen tok oldu; çıplak idiysen giyindi.\"",
     "In the inscriptions, Bilge Khagan addresses the Turkic people: 'Turkic people, if you were hungry you became sated; if you were naked you were clothed.'"),
    ("683-cü ildə atası İlteriş Xaqanın vəfatından sonra böyük qardaşı Moxilian xaqan taxtına oturmuş, özü isə \"şad\" (şahzadə) rütbəsini almışdır.",
     "After the death of his father Ilterish Khagan in 683, his elder brother Mochuo took the throne while he received the rank of shad (prince)."),
    ("\"Bilgə\" sözü türkcədə \"müdrik\", \"bilikli\" mənasını verir — bu ad onun xarakterini dəqiq təsvir edir.",
     "The word 'Bilge' means 'wise' or 'learned' in Turkic — a title that precisely describes his character."),
    ("Əl-Biruni — 973-cü ildə Xarəzm şəhərinin Birun (xarici) məhəlləsində anadan olmuş, məhz bu səbəbdən 'Biruni' (xarici məhəlləli) adını almışdır.",
     "Al-Biruni was born in 973 in the Birun (outer) quarter of Khwarezm — a origin reflected in the name Biruni ('from the outer quarter')."),
    ("\"Mən türk dillərini tam araşdırdım, onların düzgününü əyrisindən ayırd etdim. Bütün türk, türkmən, oğuz, çigil, yağma, qırğız tayfalarının dillərini öyrəndim.\" — Kaşğarinin önsözündən",
     "\"I have studied the Turkic languages thoroughly and distinguished their correct forms from incorrect ones. I learned the languages of all Turkic, Turkmen, Oghuz, Chigil, Yaghma, and Kyrgyz tribes.\" — From Kashgari's preface"),
    ("Buxara yaxınlığında Qəsr-i Arifan kəndindənanadan olan bu böyük sufi, 'Dildə xalq ilə, qəlbdə Allah ilə ol' prinsipini yaşayış tərzi halına gətirmiş; işlə, əmə klə, cəmiyyətin içindəolmaqla Allaha yaxınlaşmağı mümkün sayan bir təriqətin banisi olmuşdur.",
     "Born near Bukhara in the village of Qasr-i Arifan, this great Sufi made the principle 'Be with the people in speech, with God in heart' a way of life; through work, labour, and living within society, he founded an order that regarded closeness to God as attainable."),
]


# ---------------------------------------------------------------------------
# 4. TRANSLATION HELPERS
# ---------------------------------------------------------------------------

def _translate_contribution(az_phrase: str) -> str:
    if az_phrase in WORLD_CONTRIBUTION_EN:
        return WORLD_CONTRIBUTION_EN[az_phrase]
    return az_phrase


def _normalize_quotes(text: str) -> str:
    return text.translate(str.maketrans({
        "\u201c": '"', "\u201d": '"',
        "\u2018": "'", "\u2019": "'",
    }))


def _apply_phrase_replacements(text: str) -> str:
    out = _normalize_quotes(text)
    for az_phrase, en_phrase in _ALL_PHRASES:
        norm_az = _normalize_quotes(az_phrase)
        if norm_az in out:
            out = out.replace(norm_az, en_phrase)
    return out


def _apply_template_patterns(text: str) -> str:
    out = text
    for pattern, replacement in TEMPLATE_PATTERNS:
        if callable(replacement):
            out = pattern.sub(replacement, out)
        else:
            out = pattern.sub(str(replacement), out)
    return out


def translate_content_block(text: str) -> str:
    """Translate a single text/HTML fragment (no cross-page regex)."""
    text = html.unescape(text)
    if not text or not AZ_CHAR.search(text):
        return text
    out = _apply_phrase_replacements(text)
    out = _apply_template_patterns(out)
    if AZ_CHAR.search(out):
        mapped = translate_work_desc_az(_normalize_quotes(out))
        if mapped:
            return mapped
        for az_key, en_val in WORLD_CONTRIBUTION_EN.items():
            norm_key = _normalize_quotes(az_key)
            if norm_key in out:
                out = out.replace(norm_key, contribution_to_work_desc(en_val))
    return out


def _sync_container_blocks(en_html: str, az_html: str, class_name: str, tag: str) -> str:
    """Re-translate paired blocks from AZ source when EN still contains Azerbaijani."""
    az_pat = re.compile(rf'class="{re.escape(class_name)}">(.*?)</{tag}>', re.DOTALL)
    en_pat = re.compile(rf'(class="{re.escape(class_name)}">)(.*?)(</{tag}>)', re.DOTALL)
    az_blocks = az_pat.findall(az_html)
    if not az_blocks:
        return en_html

    idx = 0

    def repl(m: re.Match[str]) -> str:
        nonlocal idx
        az_block = az_blocks[idx] if idx < len(az_blocks) else m.group(2)
        idx += 1
        en_block = translate_content_block(az_block)
        return m.group(1) + en_block + m.group(3)

    return en_pat.sub(repl, en_html, count=len(az_blocks))


def _postprocess_labels_and_tags(html: str) -> str:
    out = html
    for az_phrase, en_phrase in PHRASE_REPLACEMENTS:
        if az_phrase in out:
            out = out.replace(az_phrase, en_phrase)

    def hero_repl(m: re.Match[str]) -> str:
        val = m.group(1).strip()
        if AZ_CHAR.search(val):
            val = translate_country(val)
        return f'hero-tag gold">{val}</span>'

    out = re.sub(r'hero-tag gold">([^<]+)</span>', hero_repl, out)

    def info_repl(m: re.Match[str]) -> str:
        val = m.group(1).strip()
        if not AZ_CHAR.search(val):
            return m.group(0)
        if ", " in val:
            country, field = val.split(", ", 1)
            val = f"{translate_country(country)}, {translate_field(field)}"
        else:
            translated = translate_country(val)
            val = translated if translated != val else translate_field(val)
        return f'info-val">{val}</span>'

    out = re.sub(r'info-val">([^<]+)</span>', info_repl, out)
    return out


# ---------------------------------------------------------------------------
# 5. MAIN TRANSLATION FUNCTION
# ---------------------------------------------------------------------------

_ALL_PHRASES: list[tuple[str, str]] = (
    sorted(UNIQUE_TRANSLATIONS + EXTRA_TRANSLATIONS, key=lambda p: -len(p[0]))
    + sorted(UI_REPLACEMENTS, key=lambda p: -len(p[0]))
)


def translate_profile_html(html: str, name: str = "", az_source: str | None = None) -> str:
    """Translate a full Azerbaijani profile HTML page to English."""
    az_source = az_source or html
    out = html

    out = out.replace('lang="az"', 'lang="en"')
    out = fix_section_title_about(out)

    out = _apply_phrase_replacements(out)
    out = _apply_template_patterns(out)

    for class_name, tag in (
        ("prose pf-profile-article", "div"),
        ("work-desc", "div"),
        ("event-text", "div"),
        ("contribution-item", "li"),
        ("quote-text", "div"),
        ("quote-source", "div"),
    ):
        out = _sync_container_blocks(out, az_source, class_name, tag)

    out = _postprocess_labels_and_tags(out)

    out = re.sub(
        r'(</h1></div>)<div class="page-hero-subtitle pf-hero-latin">[^<]*</div>',
        r"\1",
        out,
        count=1,
    )

    if FOOTER_EN and 'class="footer-pro"' in out:
        footer_start = out.find('<footer class="footer-pro">')
        footer_end = out.find('</footer>', footer_start)
        if footer_start != -1 and footer_end != -1:
            out = (
                out[:footer_start]
                + FOOTER_EN
                + out[footer_end + len("</footer>"):]
            )

    out = apply_singular_pronouns(out)
    return out

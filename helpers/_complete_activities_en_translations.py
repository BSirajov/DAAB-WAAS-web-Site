#!/usr/bin/env python3
"""Build ACTIVITIES_BODY_REPLACEMENTS for en/activities.html."""
from __future__ import annotations

ACTIVITIES_BODY_REPLACEMENTS: list[tuple[str, str]] = []

def _add(az: str, en: str) -> None:
    ACTIVITIES_BODY_REPLACEMENTS.append((az, en))

# ── Dates ─────────────────────────────────────────────────────────────
for az_m, en_m in (
    ("Aprel", "April"), ("Fevral", "February"), ("Yanvar", "January"), ("Mart", "March"),
    ("Dekabr", "December"), ("Oktyabr", "October"), ("Sentyabr", "September"),
    ("İyul", "July"), ("Noyabr", "November"), ("May", "May"),
):
    pass  # handled as full date strings below

_dates = [
    ("27 Aprel 2026", "27 April 2026"), ("11 Aprel 2026", "11 April 2026"),
    ("8 Aprel 2026", "8 April 2026"), ("15 Mart 2026", "15 March 2026"),
    ("24 Fevral 2026", "24 February 2026"), ("3 Fevral 2026", "3 February 2026"),
    ("13 Yanvar 2026", "13 January 2026"), ("22 Dekabr 2025", "22 December 2025"),
    ("17 Dekabr 2025", "17 December 2025"), ("4 Noyabr 2025", "4 November 2025"),
    ("3 Noyabr 2025", "3 November 2025"), ("29 Oktyabr 2025", "29 October 2025"),
    ("23 Oktyabr 2025", "23 October 2025"), ("20 Oktyabr 2025", "20 October 2025"),
    ("1 Oktyabr 2025", "1 October 2025"), ("3 Sentyabr 2025", "3 September 2025"),
    ("19 İyul 2025", "19 July 2025"), ("2 May 2025", "2 May 2025"),
    ("4 Fevral 2025", "4 February 2025"), ("23 Yanvar 2025", "23 January 2025"),
    ("20 Yanvar 2025", "20 January 2025"), ("17 Yanvar 2025", "17 January 2025"),
    ("Sentyabr 2024", "September 2024"), ("13 Dekabr 2024", "13 December 2024"),
    ("15 Oktyabr 2024", "15 October 2024"),
]
for a, e in _dates:
    _add(a, e)

# ── Headline, links, labels ───────────────────────────────────────────
_add(
    "NECDET ÜNÜVAR AKADEMİK KAMAL ABDULLA, PROFESSORLAR RAFİQ ƏLİYEV VƏ MƏSUD ƏFƏNDİYEV İLƏ KEÇİRİLƏN GÖRÜŞÜ ƏLAMƏTDAR HADİSƏ ADLANDIRIB.",
    "NECDET ÜNÜVAR HAS DESCRIBED THE MEETING WITH ACADEMICIAN KAMAL ABDULLA AND PROFESSORS RAFIQ ALIYEV AND MESSOUD EFENDIYEV AS A LANDMARK EVENT.",
)
_add("Prezidentin müvafiq Sərəncamı", "Presidential Order")
_add("AZƏRTAC xəbəri", "AZERTAC report")
_add("525.az xəbəri", "525.az report")
_add("science.gov.az — Açıqlama", "science.gov.az — Statement")
_add("Təhsil.Biz", "Tehsil.Biz")
_add("AzərTAC", "Azertag")
_add("Məsud Aşina", "Mesud Asina")
_add("Xəlil Kələntər", "Khalil Kelenter")
_add("Bəxtiyar Siracov", "Bakhtiyar Sirajov")
_add("Xədicə Zeynalova", "Khadija Zeynalova")
_add("📚 Canvas Öyrənmə İdarəetmə Sistemi — Faydalı Keçidlər", "📚 Canvas Learning Management System — Useful Links")
_add("Göteborg Universiteti Canvas Manual (İngilis dilində)", "University of Gothenburg Canvas Manual (in English)")
_add("Canvas tələbə təlimatları (provayderın rəsmi sənədi)", "Canvas student guide (official provider documentation)")
_add("📞 Müzakirə, təklif və əməkdaşlıq üçün əlaqə", "📞 Contact for discussion, suggestions and cooperation")

# ── Alt text ──────────────────────────────────────────────────────────
_alts = [
    ("Ankara Universiteti görüşü", "Ankara University meeting"),
    ("ATU-DAAB əməkdaşlıq", "ATU-WAAS cooperation"),
    ("Qarabağ Universiteti-DAAB görüşü", "Karabakh University-WAAS meeting"),
    ("BMU görüşü", "BMU meeting"),
    ("187 saylı məktəb görüşü", "School No. 187 meeting"),
    ("Qazax Mərkəzi şəkli", "Gazakh Centre photo"),
    ("Səadət Kərimi", "Saadat Karimi"),
    ("Telman Əliyev 90 illik yubiley", "Telman Aliyev 90th anniversary"),
    ("Məsud Əfəndiyev — NDU", "Messoud Efendiyev — NDU"),
    ("DAAB-UNEC onlayn görüş", "WAAS-UNEC online meeting"),
    ("Qarabağ Universiteti ilə onlayn görüş", "Online meeting with Karabakh University"),
    ("Qarabağ Universiteti", "Karabakh University"),
    ("Seymur Nəsirov Misir Təhsil Nazirliyi", "Seymur Nasirov Egypt Ministry of Education"),
]
for a, e in _alts:
    _add(a, e)

# ── Card body paragraphs ──────────────────────────────────────────────
_add(
    'Aprelin 24-də Ankara Universitetində Azərbaycan-Türkiyə elmi və mədəni əməkdaşlığının müasir tarixinə daha bir uğurla səhifə əlavə edilib. Həmin gün Ankara Universitetində Azərbaycanın görkəmli elm xadimləri – Xalq yazıçısı, akademik Kamal Abdulla və AMEA-nın müxbir üzvü, professor Rafiq Əliyevin həmmüəllif olduqları "Kitabi-Dədə Qorqud" və qeyri-səlis məntiq", "Qeyri-səlis məntiq və dil-nitq", eləcə də azərbaycanlı alimlərin Türkiyənin sabiq təhsil naziri, professor Ziya Selcuk ilə birgə qələmə aldıqları "Uşaqlar üçün qeyri-səlis məntiq" kitablarının təqdimatı və müzakirəsi keçirilib. Ankara Universitetinin rektoru Necdet Ünüvar akademik Kamal Abdulla, professorlar Rafiq Əliyev və Məsud Əfəndiyev ilə keçirilən görüşü əlamətdar hadisə adlandırıb.',
    'On 24 April, another successful chapter was added to the modern history of Azerbaijani–Turkish scientific and cultural cooperation at Ankara University. That day, Ankara University hosted the presentation and discussion of books co-authored by distinguished Azerbaijani scholars — People\'s Writer, Academician Kamal Abdulla, and corresponding member of ANAS, Professor Rafiq Aliyev: "Book of Dede Korkut and Fuzzy Logic", "Fuzzy Logic and Language-Speech", as well as "Fuzzy Logic for Children", which Azerbaijani scholars co-authored with Turkey\'s former Minister of Education, Professor Ziya Selcuk. Rector of Ankara University Necdet Ünüvar described the meeting with Academician Kamal Abdulla and Professors Rafiq Aliyev and Messoud Efendiyev as a landmark event.',
)
_add(
    'Azərbaycan Tibb Universiteti (ATU) ilə Dünya Azərbaycanlı Alimlər Birliyi (DAAB) arasında rəsmi əməkdaşlığı dəstəkləyən Anlaşma Memorandumu imzalanıb. ATU-nun rektoru, professor Gəray Gəraybəyli və DAAB-ın sədri, professor Məsud Əfəndiyev tərəfindən imzalanan sənəd təhsil, elm və mədəniyyət sahəsində qarşılıqlı, faydalı əməkdaşlığın təşkili və inkişafını nəzərdə tutur. Bundan əlavə, memorandum birgə elmi və tədqiqat proqramları, layihə və işlərin icrasını dəstəkləyir. Eyni zamanda müxtəlif sahələr üzrə, o cümlədən elmi tədqiqat, alim və mütəxəssislərin peşəkar inkişafı, akademik və inzibati heyətin, bakalavr, magistratura və rezidentura tələbələrinin mübadiləsi kimi istiqamətləri ehtiva edir.',
    'A Memorandum of Understanding supporting official cooperation between Azerbaijan Medical University (ATU) and the World Association of Azerbaijani Scientists (WAAS) has been signed. The document, signed by ATU Rector Professor Garay Garaybeyli and WAAS Chair Professor Messoud Efendiyev, provides for the organisation and development of mutually beneficial cooperation in education, science and culture. The memorandum also supports joint scientific and research programmes, projects and activities, including scientific research, professional development of scholars and specialists, and exchange of academic and administrative staff and undergraduate, master\'s and residency students.',
)
_add(
    'Aprelin 8-də Dünya Azərbaycanlı Alimlər Birliyi (DAAB) ilə mövcud əməkdaşlıq çərçivəsində Qarabağ Universitetində görüş keçirilib. Bu əməkdaşlıq yalnız ayrı-ayrı tədbirlərin təşkili ilə məhdudlaşmır, eyni zamanda Qarabağ Universitetinin beynəlxalq elmi mühitə inteqrasiyası, akademik potensialının gücləndirilməsi və müasir ali təhsil standartlarına uyğun inkişafı baxımından mühüm strateji əhəmiyyət daşıyır.',
    'On 8 April, a meeting was held at Karabakh University within the existing cooperation framework with the World Association of Azerbaijani Scientists (WAAS). This cooperation is not limited to organising individual events; it also carries significant strategic importance for Karabakh University\'s integration into the international scientific environment, strengthening its academic potential and development in line with modern higher education standards.',
)
_add(
    'Tərəflər arasında əvvəlki görüşlərdə ortaq elmi-tədqiqat layihələrinin həyata keçirilməsi, müasir laboratoriyaların yaradılması, onlayn dərs və seminarların təşkili, xaricdə fəaliyyət göstərən azərbaycanlı alimlərin tədris prosesinə cəlb edilməsi, eləcə də birgə konfrans, forum və simpoziumların keçirilməsi kimi mühüm əməkdaşlıq istiqamətləri müəyyən edilib və bu istiqamətlər üzrə konkret fəaliyyət planı formalaşdırılıb.',
    'At previous meetings, the parties identified key areas of cooperation, including joint research projects, establishing modern laboratories, organising online classes and seminars, engaging Azerbaijani scholars abroad in teaching, and holding joint conferences, forums and symposiums, and developed a concrete action plan in these areas.',
)
_add(
    'Görüşdə DAAB-ın sədri, Almaniyada fəaliyyət göstərən azərbaycanlı riyaziyyatçı-alim, professor Məsud Əfəndiyev və birliyin üzvü, İsveçdə yerləşən Qoteborq Universitetinin professoru Səadət Kərimi iştirak ediblər.',
    'The meeting was attended by WAAS Chair Professor Messoud Efendiyev, an Azerbaijani mathematician-scholar based in Germany, and WAAS member Professor Saadat Karimi of the University of Gothenburg in Sweden.',
)
_add(
    'Bakı Mühəndislik Universiteti (BMU) ilə Dünya Azərbaycanlı Alimlər Birliyinin (DAAB) üzvləri arasında onlayn görüş keçirilib. Görüşdə universitetlə xaricdə fəaliyyət göstərən azərbaycanlı alimlər arasında əməkdaşlıq imkanları müzakirə olunub. Görüş zamanı alimlərin tədris prosesinə cəlb olunması, tələbələr üçün master-klasların təşkili və birgə elmi tədqiqatların aparılması kimi məsələlər ön plana çıxarılıb. BMU-nun rektoru universitetin son illərdəki nailiyyətləri, beynəlxalq tərəfdaşlıqları və elmi fəaliyyətin genişləndirilməsi istiqamətindəki işlər barədə məlumat verib. Sonda tərəflər gələcək əməkdaşlığın inkişafı ilə bağlı ilkin razılıq əldə edərək koordinatorlar təyin ediblər.',
    'An online meeting was held between Baku Engineering University (BMU) and members of the World Association of Azerbaijani Scientists (WAAS). The meeting discussed cooperation opportunities between the university and Azerbaijani scholars working abroad. Key topics included engaging scholars in teaching, organising master classes for students and conducting joint scientific research. BMU\'s rector provided information on the university\'s recent achievements, international partnerships and efforts to expand scientific activity. The parties reached preliminary agreement on future cooperation and appointed coordinators.',
)
_add(
    'DAAB İdarə Heyətinin həmsədri Dr. Bəxtiyar Siracov Bakının 187 saylı ümumtəhsil məktəbinin müəllim və şagirdləri ilə onlayn görüş keçirmişdir. Görüş zamanı elmin önəmi, beynəlxalq elm arenasında azərbaycanlı alimlərin rolu və gənc nəslə tövsiyələr müzakirə olunmuşdur.',
    'WAAS Board of Directors Co-Chair Dr. Bakhtiyar Sirajov held an online meeting with the teachers and pupils of Baku General Education School No. 187. The meeting discussed the importance of science, the role of Azerbaijani scholars on the international stage and advice for the younger generation.',
)
_add(
    'Milli Aviasiya Akademiyasında "Fevral məruzələri 2026: Aviakosmik məsələlərin həllində gənclərin yaradıcı potensialı" adlı XI beynəlxalq elmi-praktik gənclər konfransının açılışı olub. Plenar iclasda DAAB-ın sədri, professor Məsud Əfəndiyev xaricdə yaşayan azərbaycanlı alimlərin Azərbaycan elm və təhsilinə inteqrasiyasının əhəmiyyətindən danışıb. O, DAAB-ın əsas məqsədlərindən birinin dünya üzrə fəaliyyət göstərən azərbaycanlı alimlər arasında əməkdaşlığı gücləndirmək olduğunu vurğulayıb.',
    'The opening ceremony of the XI International Scientific and Practical Youth Conference "February Lectures 2026: Creative Potential of Youth in Solving Aerospace Issues" was held at the National Aviation Academy. At the plenary session, WAAS Chair Professor Messoud Efendiyev spoke about the importance of integrating Azerbaijani scholars living abroad into Azerbaijan\'s science and education. He emphasised that one of WAAS\'s main goals is to strengthen cooperation among Azerbaijani scholars working worldwide.',
)
_add(
    'Azərbaycan Respublikası Prezidenti cənab İlham Əliyevin 7 yanvar 2026-cı il tarixli Sərəncamı ilə xalqlar arasında dostluğun möhkəmləndirilməsi və Azərbaycan diasporunun inkişafına göstərdikləri töhfələrə görə bir qrup azərbaycanlı yüksək dövlət təltifinə layiq görülmüşdür. Təltif edilənlər arasında DAAB-ın fəal üzvləri də xüsusi yer tutmuşdur: Məsud Aşina "Şöhrət" ordeni, Akif Alaferdov, Xəlil Kələntər, Bəxtiyar Siracov və Xədicə Zeynalova isə "Tərəqqi" medalı ilə mükafatlandırılmışlar.',
    'By Decree of the President of the Republic of Azerbaijan Ilham Aliyev dated 7 January 2026, a group of Azerbaijanis were awarded high state honours for strengthening friendship among peoples and contributing to the development of the Azerbaijani diaspora. Active WAAS members were among those honoured: Mesud Asina received the Order of Glory; Akif Alaferdov, Khalil Kelenter, Bakhtiyar Sirajov and Khadija Zeynalova were awarded the Progress Medal.',
)
_add(
    'Dekabrın 18-də Azərbaycan Memarlıq və İnşaat Universitetinin (AzMİU) yaradılmasının 50 illik yubileyi münasibətilə təntənəli yığıncaq keçirilib. Tədbirin iştirakçıları arasında olan dünya şöhrətli alim, DAAB İdarə Heyətinin sədri, AzMİU rektorunun müşaviri professor Məsud Əfəndiyev təəssüratlarını bölüşüb.',
    'On 18 December, a ceremonial gathering was held to mark the 50th anniversary of the founding of Azerbaijan University of Architecture and Construction (AzMIU). World-renowned scholar, WAAS Board of Directors Chair and Adviser to the AzMIU Rector Professor Messoud Efendiyev shared his impressions as one of the participants.',
)
_add(
    '"Azərbaycan Memarlıq və İnşaat Universitetinin keçdiyi 50 illik yol tədbirdə gözümüzün qarşısında canlandı. AzMİU Azərbaycan üçün önəmli bir universitetdir. Memarlıq və inşaat bizim qalib xalqımıza yaraşan, Azərbaycan üçün vacib olan komponentlərdən biridir. Tədbirdə Memarlıq və İnşaat Universiteti barədə çox gözəl fikirlər səsləndi, onun müstəsna rol oynadığı vurğulandı."',
    '"The 50-year journey of Azerbaijan University of Architecture and Construction came vividly to life at the event. AzMIU is an important university for Azerbaijan. Architecture and construction are components worthy of our victorious people and essential for Azerbaijan. Many fine words were spoken about the University at the event, and its exceptional role was emphasised."',
)
_add(
    'Məsud Əfəndiyev həm də bu ali məktəbin doktorantları və gənc tədqiqatçı alimləri ilə ikigünlük görüş keçirib. Görüş çərçivəsində doktorantların elmi-tədqiqat fəaliyyəti, beynəlxalq elmi inteqrasiya imkanları və qlobal elm arenasına çıxış mexanizmləri geniş müzakirə olunub. Gənc tədqiqatçıların elmi məqalələrinin "Web of Science" və "Scopus" kimi beynəlxalq indeksli jurnallarda dərc olunması məsələləri xüsusi diqqət mərkəzində olub.',
    'Messoud Efendiyev also held a two-day meeting with the university\'s doctoral students and young research scholars. Discussions covered doctoral research activity, opportunities for international scientific integration and pathways to the global scientific arena. Particular attention was given to publishing young researchers\' articles in internationally indexed journals such as Web of Science and Scopus.',
)
_add(
    'Professor Məsud Əfəndiyev məqalə yazılışı, resenziya prosesləri, elmi etik normalar və beynəlxalq akademik şəbəkələrə çıxış yolları barədə ətraflı tövsiyələr verib. Müzakirələr zamanı "Alexander von Humboldt" Fondu, DAAD (Alman Akademik Mübadilə Xidməti), "Horizon Europe və ERC" (European Research Council) proqramları, eləcə də digər beynəlxalq elmi-tədqiqat və innovasiya platformaları geniş müzakirə olunub. Qlobal elmi gündəmdə olan aktual tədqiqat istiqamətləri, multidisiplinar layihələr və beynəlxalq konsorsiumlarda iştirak imkanları da nəzərdən keçirilib.',
    'Professor Messoud Efendiyev gave detailed advice on writing articles, peer review processes, research ethics and access to international academic networks. Discussions also covered the Alexander von Humboldt Foundation, DAAD (German Academic Exchange Service), Horizon Europe and ERC (European Research Council) programmes, and other international research and innovation platforms. Current research priorities on the global agenda, multidisciplinary projects and opportunities to participate in international consortia were also reviewed.',
)
_add(
    'Qahirədə "Fətva və humanitar gerçəklik problemləri" şüarı ilə keçirilmiş beynəlxalq konfransda 50-dən çox ölkədən müftilər, şəriət alimləri və mütəxəssislər iştirak edib. Konfransda DAAB-ın həmsədri Seymur Nəsirov Azərbaycandakı tolerantlıq mühitindən danışıb. Misir müftisi tərəfindən seçilmiş alim və müftilər fəaliyyətlərinə görə təltif edilib; Seymur Nəsirov da mükafat alanlar sırasında olub.',
    'An international conference on "Fatwa and Humanitarian Reality Issues" was held in Cairo with muftis, Islamic scholars and specialists from more than 50 countries. WAAS Co-Chair Seymur Nasirov spoke at the conference about the climate of tolerance in Azerbaijan. Scholars and muftis selected by Egypt\'s Grand Mufti were honoured for their work; Seymur Nasirov was among the recipients.',
)
_add(
    'AMEA-nın 80 illik yubileyi çərçivəsində bir sıra ölkələrin Elmlər Akademiyaları ilə anlaşma memorandumlarının imzalanma mərasimi olub. Digər anlaşmalarla yanaşı, AMEA ilə Dünya Azərbaycanlı Alimlər Birliyi (DAAB) arasında da anlaşma memorandumu imzalanıb.',
    'As part of ANAS\'s 80th anniversary, a ceremony was held to sign memoranda of understanding with academies of sciences from several countries. Among other agreements, a memorandum of understanding was also signed between ANAS and the World Association of Azerbaijani Scientists (WAAS).',
)
_add(
    'Dünya elminin ən yüksək təltiflərdən biri sayılan Humboldt mükafatının ilk azərbaycanlı laureatı, Almaniyada "Helmholtz" Elmi-Tədqiqat Mərkəzinin Dinamik Sistemlər şöbəsinin müdiri, professor Məsud Əfəndiyev AMEA-nın 80 illik yubileyi ilə əlaqədar açıqlama verib.',
    'Professor Messoud Efendiyev, the first Azerbaijani laureate of the Humboldt Award — one of the highest honours in world science — and Head of the Dynamic Systems Division at the Helmholtz Research Centre in Germany, issued a statement on the occasion of ANAS\'s 80th anniversary.',
)
_add(
    'BDU-nun məzunu, Kanadanın York Universitetinin professoru, DAAB İdarə Heyətinin üzvü Yulduz Rəhimov ilə görüş keçirilib. Professor Yulduz Rəhimov fakültənin professor-müəllim heyəti, tələbə və doktorantları qarşısında "Ədədlər nəzəriyyəsi və kriptoqrafiya" mövzusunda ustad dərsi keçib.',
    'A meeting was held with Yulduz Rahimov, a graduate of Baku State University (BDU), Professor at York University in Canada and WAAS Board of Directors member. Professor Yulduz Rahimov delivered a master class on "Number Theory and Cryptography" for the faculty\'s academic staff, students and doctoral candidates.',
)
_add(
    'Tədqiqatçı-alim Seymur Nəsirov Misir Ərəb Respublikası ilə Azərbaycan Respublikası arasında elmi-mədəni əlaqələrin inkişafındakı xidmətlərinə görə Misir Təhsil Nazirliyinin medalı ilə təltif olunub. Mükafatı ona Bakıda Misir Mədəniyyət Mərkəzinin direktoru professor Tariq Əbu Futuh təqdim edib.',
    'Research scholar Seymur Nasirov was awarded the medal of Egypt\'s Ministry of Education for services to the development of scientific and cultural relations between the Arab Republic of Egypt and the Republic of Azerbaijan. The award was presented in Baku by Professor Tariq Abu Futuh, Director of the Egypt Culture Centre.',
)
_add(
    'Misir Prezidenti Əbdül Fəttah əl-Sisi azərbaycanlı tədqiqatçı-alim Seymur Nəsirovu birinci dərəcəli "Elm və Fənlər" ordeni ilə təltif edib. Misir Prezidentinin şəxsən özü tərəfindən verilən bu orden elmin inkişafı və yayılması sahəsindəki xidmətlərə görə görkəmli alimlərə təqdim edilir.',
    'President of Egypt Abdel Fattah el-Sisi awarded Azerbaijani research scholar Seymur Nasirov the first-class "Science and Arts" order. This order, presented personally by the President of Egypt, is awarded to distinguished scholars for services to the development and dissemination of science.',
)
_add(
    '2025-ci ilin May ayından başlayaraq DAAB-ın İdarə Heyətinin üzvü və mətbuat katibi, İsveçin Gothenburg Universitetinin dosenti, elmlər doktoru Səadət Kərimi Qarabağ Universitetinin bir qrupp müəllimlərinə "ALİ MƏKTƏB PEDAQOQİKASI" (TEACHING AND LEARNING IN HIGHER EDUCATION) fənni üzrə əhatəli kursun tədrisinə başlamışdır. Tədris əsasən İngilis dilində və Avropa İttifaqı qaydalarına uyğun olaraq distant formatda həyata keçirilmişdir. İştirak edən müəllimlərin əksəriyyəti xaricdə magister, doktorantura təhsili almış olmasına baxmayaraq, bu kursun əhəmiyyətini dərk etdiklərini və yaranan imkana görə minnətdarlıqlarını bildirirlər.',
    'Since May 2025, WAAS Board of Directors member and press secretary Dr. Saadat Karimi, Associate Professor at the University of Gothenburg in Sweden, has been teaching a comprehensive course on "HIGHER EDUCATION PEDAGOGY" (TEACHING AND LEARNING IN HIGHER EDUCATION) to a group of teachers at Karabakh University. Instruction has been delivered mainly in English, remotely and in accordance with European Union standards. Although most participating teachers have completed master\'s or doctoral studies abroad, they have expressed appreciation for the opportunity and recognised the importance of the course.',
)
_add(
    'Kursun məqsədi bakalavriat və magistratura pillələrində təhsilin keyfiyyətini gücləndirmək, tələbələrin öyrənilməsi və biliklərinin inkişafı üçün yaxşı şərait yaratmaq üçün ali məktəb müəllimlərini müəllim hazırlığı ilə təmin etməkdir. Kurs həmçinin elmi rəhbərlik (supervisor) işinin keyfiyyətini gücləndirməyi əhatə edir.',
    'The course aims to equip university teachers with pedagogical training to strengthen the quality of education at undergraduate and master\'s levels and to create favourable conditions for student learning and knowledge development. It also covers strengthening the quality of academic supervision.',
)
_add(
    'Kurs iki moduldan ibarətdir. Birinci modul 10 İyun 2025 tarixində imtahanlarla başa çatmışdır; ikinci modul avqustun ikinci yarısından noyabr ayının ilk həftəsinədək davam edəcək və sertifikatla nəticələnəcəkdir. Toplam 50 saatlıq kurs 15 kredit səviyyəsindədir: həftədə 3 saat leksiya, seminar və vorkşoplardan ibarət olub.',
    'The course consists of two modules. The first module concluded with examinations on 10 June 2025; the second module will run from the second half of August until the first week of November and will conclude with certification. The 50-hour course is at the 15-credit level and comprises three hours per week of lectures, seminars and workshops.',
)
_add(
    'Səadət Kərimi Qarabağ Universitetinə töhfə verə bildiyi üçün şərəf və məmnuniyyət hissi duyduğunu, Azərbaycan Respublikasının sürətli quruculuq işlərində, o cümlədən elm və təhsil sahəsində, yaxından iştirak edə bildiyi üçün xoşbəxt olduğunu bildirmişdir. Onun fikrincə, kursun mütəmadi olaraq hər semestrdə yeni işə qəbul olunmuş ali məktəb müəllimlərinə verilməsi məqsədəuyğundur. Bu kurs Azərbaycanın müxtəlif universitetlərindən müəllimlər tərəfindən distant şəkildə götürülə bilər.',
    'Saadat Karimi said she felt honoured and pleased to contribute to Karabakh University and to participate closely in the rapid construction efforts of the Republic of Azerbaijan, including in science and education. In her view, it would be appropriate to offer the course regularly each semester to newly appointed university teachers. Teachers from various universities across Azerbaijan could take the course remotely.',
)
_add(
    'Diasporla İş üzrə Dövlət Komitəsinin təşkilatçılığı ilə 85 ölkədən 1000-ə yaxın soydaşımızın iştirakı ilə videokonfrans keçirilib. Konfrans zamanı DAAB üzvləri Səidə Xəlilova (Oman), Rövşən İbrahimov (Cənubi Koreya) və Hacalı Nəcəfov (Türkiyə) "Diaspor fəaliyyətində xidmətə görə" medalı ilə təltif olunduqları elan edilib.',
    'A videoconference with nearly 1,000 compatriots from 85 countries was held under the auspices of the State Committee on Diaspora Affairs. During the conference, it was announced that WAAS members Saida Khalilova (Oman), Rovshan Ibrahimov (South Korea) and Hajali Najafov (Türkiye) had been awarded the medal "For service in diaspora activity".',
)
_add(
    'İsveçdə Azərbaycan Aydınlar Ocağı Norveç Nobel Komitəsinə Mixail Qorbaçovun Nobel sülh mükafatından məhrum edilməsi tələbi ilə rəsmi müraciət ünvanlamışdır.',
    'The Association of Azerbaijani Academics in Sweden (GOBUSTAN) has addressed an official appeal to the Norwegian Nobel Committee requesting that Mikhail Gorbachev be deprived of the Nobel Peace Prize.',
)
_add(
    'UNEC-in rektoru Prof. Ədalət Muradov:\n\nDünya Azərbaycanlı Alimlər Birliyinin (DAAB) bütün qitələrdən olan üzvləri ilə UNEC-in əməkdaşlıq imkanlarını müzakirə etdik. Ortaq elmi tədqiqatlar və onların nəticələrinin yayılması, gənc alimlərə dəstək, birgə jurnallar, elmi fəaliyyət sahəsində məlumat mübadilə mexanizminin yaradılması və digər məsələləri müzakirə etdik. UNEC-ə ayırdıqları vaxta və göstərdikləri dəstəyə görə DAAB-ın İdarə Heyətinin Sədri professor Məsud müəllim Əfəndiyev başda olmaqla müzakirədə iştirak edən hər bir DAAB üzvünə təşəkkür edirəm.',
    'UNEC Rector Prof. Adalet Muradov:\n\nWe discussed UNEC\'s cooperation opportunities with WAAS members from all continents. We discussed joint scientific research and dissemination of results, support for young scholars, joint journals, creating a mechanism for exchanging information in scientific activity and other matters. I thank every WAAS member who took part in the discussion, led by WAAS Board of Directors Chair Professor Messoud Efendiyev, for the time and support they devoted to UNEC.',
)
_add("525-ci Qəzet", "525 Newspaper")
_add("525-ci Qəzet", "525 Newspaper")
_add("525-ci Qəzet — Məsud Əfəndiyevlə müsahibə", "525 Newspaper — interview with Messoud Efendiyev")
_add(
    'Məqalədə Almaniyada fəaliyyət göstərən tanınmış azərbaycanlı alim, "Aleksander fon Humboldt" ("Kiçik Nobel mükafatı") mükafatının ilk azərbaycanlı laureatı Məsud Əfəndiyev haqqında geniş məlumat verilir. Alim Azərbaycanın elm və təhsil siyasətinin son illərdə sistemli və strateji xarakter aldığını, xüsusilə süni intellekt və informasiya texnologiyalarına diqqətin artdığını vurğulayır. O, Dünya Azərbaycanlı Alimlər Birliyi vasitəsilə xaricdə yaşayan azərbaycanlı alimlərin Azərbaycan elminin inkişafına töhfə verməyə çalışdıqlarını qeyd edir. Məqalədə həmçinin Naxçıvan Dövlət Universiteti ilə əməkdaşlıq perspektivləri, beynəlxalq elmi əlaqələrin genişləndirilməsi və gənclərin elmə təşviqinin əhəmiyyəti xüsusi vurğulanır. Məsud Əfəndiyev hesab edir ki, güclü elmi mühit, beynəlxalq əməkdaşlıq və keyfiyyətli tədqiqatlar gələcəkdə azərbaycanlı alimlərin daha böyük beynəlxalq uğurlar qazanmasına yol aça bilər.',
    'The article provides extensive information about Messoud Efendiyev, a distinguished Azerbaijani scholar based in Germany and the first Azerbaijani laureate of the Alexander von Humboldt Award ("small Nobel prize"). The scholar emphasises that Azerbaijan\'s science and education policy has taken on a systematic and strategic character in recent years, with growing attention to artificial intelligence and information technology. He notes that through WAAS, Azerbaijani scholars abroad seek to contribute to the development of science in Azerbaijan. The article also highlights cooperation prospects with Nakhchivan State University, expanding international scientific ties and the importance of encouraging young people in science. Messoud Efendiyev believes that a strong scientific environment, international cooperation and quality research can pave the way for greater international success for Azerbaijani scholars in the future.',
)
_add(
    '15 oktyabr 2024-cü il tarixində Dünya Azərbaycanlı Alimlər Birliyinin (DAAB) İdarə Heyətinin üzvləri və Qarabağ Universitetinin rəhbər heyəti arasında görüş keçirilib. DAAB-ın təşəbbüsü ilə onlayn formatda keçirilən görüş tədris, elmi-tədqiqat, eləcə də Qarabağ Universitetinin beynəlxalq səviyyədə tanınması və nüfuzunun gücləndirilməsi istiqamətlərində əməkdaşlıq imkanlarının müzakirəsi məqsədi daşıyıb.',
    'On 15 October 2024, a meeting was held between members of the WAAS Board of Directors and the leadership of Karabakh University. Initiated by WAAS and held online, the meeting aimed to discuss cooperation opportunities in teaching, research and strengthening the international recognition and standing of Karabakh University.',
)

# Yulduz ADA — six paragraphs
_add(
    'Dünya Azərbaycanlı Alimlər Birliyinin Elmi katibi, Kanadada yaşayan Azərbaycanlı alim, York Universitetinin Professoru Yulduz Rəhimov 29 oktyabr 2025-ci il tarixində ADA Universitetinin Qazax Mərkəzinə səfər edib. Səfər ADA Universitetinin Təsisçi Rektoru və Qazax Mərkəzinin yaradıcı ideya müəllifi olan Hafiz Paşayevin təşəbbüsü ilə həyata keçirilib. Ziyarətdə İtaliyanın Roma Tor Vergata Universitetinin magistrantı Nicat Rəhimli də iştirak etmişdir. Mərkəzin sədri Yeganə Göyüşova qonaqlara Mərkəzin fəaliyyəti, tarixi binaların bərpası və inkişaf məqsədləri haqqında geniş məlumat təqdim edib.',
    'Yulduz Rahimov, Scientific Secretary of WAAS, Azerbaijani scholar living in Canada and Professor at York University, visited ADA University\'s Gazakh Centre on 29 October 2025. The visit was organised on the initiative of Hafiz Pashayev, Founding Rector of ADA University and originator of the Gazakh Centre concept. Nicat Rahimli, a master\'s student at Roma Tor Vergata University in Italy, also took part. Centre Director Yegana Goyushova gave guests detailed information about the Centre\'s activities, restoration of historic buildings and development goals.',
)
_add(
    'Qazax Müəllimlər Seminariyasının tarixi binasında 2022-ci ilin oktyabrından fəaliyyət göstərən ADA Universiteti Qazax Mərkəzi həm regionun tarixi irsini qoruyur, həm də bölgəyə müasir və innovativ təhsil mühiti gətirir. Kompleksin memarlığı orijinal üslubuna uyğun olaraq yüksək səviyyədə bərpa olunub, ətraf ərazi abadlaşdırılaraq müasir kampus infrastrukturuna çevrilib. Tələbələr üçün rəqəmsal tədris avadanlıqları ilə təchiz edilmiş dərs otaqları, geniş kitabxana, oxu və müzakirə sahələri, komfortlu sosial məkanlar və dekorativ bitgilərlə bəzədilmiş yaşıl istirahət zonaları yaradılıb.',
    'Operating since October 2022 in the historic building of the Gazakh Teachers\' Seminary, ADA University Gazakh Centre both preserves the region\'s historical heritage and brings a modern, innovative educational environment to the area. The complex has been restored to a high standard in its original architectural style, and the surrounding area has been landscaped into modern campus infrastructure. Classrooms equipped with digital teaching tools, a spacious library, reading and discussion areas, comfortable social spaces and green recreation zones with ornamental plants have been created for students.',
)
_add(
    'Mərkəzdə yaşayan pedaqoji heyət üçün inşa edilmiş Müəllimlər Evi tam şəraitli yaşayış imkanları ilə təmin olunub. Tikinti prosesi zamanı, əvvəllər həmin ərazidə yaşayan sakinlər üçün ədalətli kompensasiya verilməsi layihənin sosial məsuliyyət prinsiplərinə uyğun şəkildə həyata keçirildiyini göstərir. Eyni zamanda ADA Qazax Mərkəzində tələbələr üçün nəzərdə tutulmuş yataqxana da tam şəraitli, funksional və müasir standartlara cavab verən yaşayış mühiti təmsil edir. Tələbə yataqxanası geniş otaqlar, istirahət sahələri, oxu və qrup işləri üçün müasir məkanlarla təchiz olunub, həmçinin əlilliyi olan tələbələr üçün xüsusi uyğunlaşdırılmış şərait nəzərdə tutulub.',
    'Teachers\' House, built for the pedagogical staff living at the Centre, provides fully equipped accommodation. Fair compensation for former residents during construction reflects the project\'s social responsibility principles. The student dormitory at ADA Gazakh Centre also offers a fully equipped, functional living environment meeting modern standards, with spacious rooms, recreation areas and modern spaces for reading and group work, as well as facilities adapted for students with disabilities.',
)
_add(
    'Mərkəzin tədris kompleksinə daxil olan XIX əsrə aid yerli əhəmiyyətli tarixi İsrafil Ağa hamamı da bərpadan sonra mədəniyyət və yaradıcılıq məkanına çevrilib. Hamamın daxilində Qazax xalçaçılıq məktəbinə aid nümunələri bir araya gətirən muzey və yerli gənclər üçün rəsm dərnəyi fəaliyyət göstərir. Bu tarixi məkan kiçik həcmli musiqili, ədəbi və mədəni tədbirlərin təşkili üçün ideal şəraitə malikdir və Seminariyanın tarixi ruhunu müasir yaradıcılıq ilə birləşdirir.',
    'The locally significant historic Israfil Agha bathhouse of the 19th century, part of the Centre\'s teaching complex, has been restored and converted into a cultural and creative space. It houses a museum bringing together examples from the Gazakh carpet school and an art club for local youth. This historic venue is ideal for small-scale musical, literary and cultural events and combines the Seminary\'s historic spirit with contemporary creativity.',
)
_add(
    'Səfər zamanı DAAB elmi katibi və ADA Universiteti Qazax Mərkəzinin rəhbərliyi arasında aparılan müzakirələr xüsusilə səmimi və ilhamverici atmosferdə keçib. Tərəflər elmi şəbəkənin genişləndirilməsi, birgə tədqiqat layihələrinin həyata keçirilməsi və akademik mübadilə imkanlarının artırılması ilə bağlı fikirlərini bölüşərkən həm Qazaxın tarixi elmi irsinə, həm də burada formalaşan yeni təhsil mühitinə böyük dəyər verildiyini vurğulayıblar. Regionun elmi-mədəni potensialının gücləndirilməsi, gənclərin elmə bağlılığının artırılması və Qazaxın intellektual mərkəz kimi yenidən dirçəlməsi istiqamətində irəli sürülən ideyalar görüşə xüsusi ruh qatıb. Səfər hər iki tərəf üçün yeni əməkdaşlıq imkanlarının formalaşdırılmasına töhfə verən əhəmiyyətli addım kimi yadda qalacaq.',
    'Discussions between the WAAS Scientific Secretary and the leadership of ADA University Gazakh Centre during the visit took place in a particularly warm and inspiring atmosphere. Sharing views on expanding the scientific network, implementing joint research projects and increasing academic exchange opportunities, both sides emphasised the great value of Gazakh\'s historic scientific heritage and the new educational environment forming there. Ideas put forward to strengthen the region\'s scientific and cultural potential, increase young people\'s commitment to science and revive Gazakh as an intellectual centre gave the meeting special spirit. The visit will be remembered as a significant step contributing to new cooperation opportunities for both sides.',
)

# Bakhtiyar BDU — paragraphs
_add(
    'Bakı Dövlət Universitetinin (BDU) Tətbiqi riyaziyyat və kibernetika fakültəsinin məzunu, DAAB İdarə Heyətinin həmsədri Dr. Bəxtiyar Siracovla görüş keçirilib.',
    'A meeting was held with Dr. Bakhtiyar Sirajov, a graduate of the Faculty of Applied Mathematics and Cybernetics at Baku State University (BDU) and WAAS Board of Directors Co-Chair.',
)
_add(
    'Tədbirdə BDU-nun elm və innovasiyalar üzrə prorektoru Hüseyn Məmmədov, Tətbiqi riyaziyyat və kibernetika fakültəsinin dekanı Ələkbər Əliyev, fakültənin müəllim və tələbələri iştirak ediblər.',
    'The event was attended by BDU Vice-Rector for Science and Innovation Huseyn Mammadov, Dean of the Faculty of Applied Mathematics and Cybernetics Alekber Aliyev, and the faculty\'s teachers and students.',
)
_add(
    'Fakültə dekanı Ələkbər Əliyev qeyd edib ki, Tətbiqi riyaziyyat və kibernetika fakültəsinin məzunları dünyanın müxtəlif ölkələrində, o cümlədən Azərbaycanda uğurla fəaliyyət göstərir, yüksək vəzifələrdə çalışırlar. Belə məzunlardan biri də Nobel Sülh Mükafatına layiq görülən Bəxtiyar Siracovdur. Ələkbər Əliyev Norveç Sülh Komitəsinin qərarı ilə 2005-ci ildə Nobel Sülh mükafatına layiq görülən və uzun illər Atom Enerjisi üzrə Beynəlxalq Agentliyin (AEBA) məsul əməkdaşı olan məzunumuzun həyat yolu haqqında tələbələrə məlumat verib, belə görüşlərin tələbələrin inkişafında önəmli rol oynadığını vurğulayıb.',
    'Dean Alekber Aliyev noted that graduates of the Faculty of Applied Mathematics and Cybernetics work successfully in various countries, including Azerbaijan, holding senior positions. One such graduate is Bakhtiyar Sirajov, a Nobel Peace Prize laureate. Alekber Aliyev told students about the life path of our graduate, who received the Nobel Peace Prize in 2005 by decision of the Norwegian Nobel Committee and worked for many years as a senior official at the International Atomic Energy Agency (IAEA), and emphasised that such meetings play an important role in students\' development.',
)
_add(
    'Bəxtiyar Siracov bildirib ki, 1974-1979-cu illərdə BDU-nun Tətbiqi riyaziyyat və kibernetika fakültəsində təhsil alıb. O, məzunu olduğu universitetdə tələbələrlə görüşdən məmnunluğunu ifadə edib. Qonaq tələbəlik illərindən tutmuş AEBA-dakı fəaliyyətinədək keçdiyi yol barədə ətraflı məlumat verib, elmin inkişafına gənclərin töhfəsinin vacibliyini vurğulayıb. O, bilik və təcrübələrindən bəhrələndiyi Azərbaycan alimlərini minnətdarlıqla yad edib, onların yetirmələrinin bu gün dünyanın nüfuzlu universitetlərində, elm mərkəzlərində çalışdığını fəxrlə bildirib.',
    'Bakhtiyar Sirajov said he studied at BDU\'s Faculty of Applied Mathematics and Cybernetics from 1974 to 1979. He expressed pleasure at meeting students at his alma mater. The guest gave detailed information about his path from student years to his work at the IAEA and emphasised the importance of young people\'s contribution to the development of science. He gratefully remembered the Azerbaijani scholars from whom he benefited and proudly noted that their students today work at prestigious universities and research centres around the world.',
)
_add(
    'Qeyd olunub ki, 2005-ci ildə Norveç Sülh Komitəsinin qərarı ilə AEBA və onun Baş Direktoru Məhəmməd əl-Baradei nüvə enerjisinin hərbi məqsədlər üçün istifadəsinin qarşısının alınmasında və nüvə enerjisindən dinc məqsədlər üçün təhlükəsiz şəkildə istifadə edilməsinin təmin edilməsində göstəridikləri xidmətlərə görə Nobel Sülh Mükafatına layiq görülüblər. Bəxtiyar Siracov da məhz o tarixdən AEBA-da çalışan digər əməkdaşlarla bərabər Nobel Sülh Mükafatını alanlar sırasındadır.',
    'It was noted that in 2005, by decision of the Norwegian Nobel Committee, the IAEA and its Director General Mohamed ElBaradei were awarded the Nobel Peace Prize for their services in preventing the military use of nuclear energy and ensuring its safe use for peaceful purposes. Bakhtiyar Sirajov has been among the Nobel Peace Prize recipients since that time, together with other IAEA staff.',
)
_add(
    'Sonra Bəxtiyar Siracov tələbələrin suallarını cavablandırıb.',
    'Bakhtiyar Sirajov then answered students\' questions.',
)

# February 2025 conference
_add(
    'Fevralın 4-də “Azərbaycan Hava Yolları” QSC-nin Milli Aviasiya Akademiyasında (MAA) Azərbaycan Gəncləri Gününə və ölkəmizin ilk telekommunikasiya peyki “Azerspace 1”in orbitə buraxılması tarixinə həsr olunan “Fevral məruzələri 2025: Aviakosmik məsələlərin həllində gənclərin yaradıcı potensialı” 10-cu beynəlxalq elmi-praktik gənclər konfransı işə başlayıb.',
    'On 4 February, the 10th International Scientific and Practical Youth Conference "February Lectures 2025: Creative Potential of Youth in Solving Aerospace Issues", dedicated to Azerbaijan Youth Day and the launch date of our country\'s first telecommunications satellite Azerspace 1, began at the National Aviation Academy (MAA) of Azerbaijan Airlines.',
)
_add(
    'AZƏRTAC xəbər verir ki, konfransa Rusiya, Qazaxıstan, Türkiyə, Ukrayna, Belarus, Almaniya, Böyük Britaniya, Fransa, İsrail və Azərbaycandan olmaqla 20-dən çox elm və təhsil müəssisəsi, o cümlədən 13 universitet, 7 tədqiqat mərkəzi, institut, dövlət qurumları və aparıcı təşkilatları təmsil edən 150-dən çox iştirakçı qatılıb.',
    'AZERTAC reports that more than 150 participants representing over 20 scientific and educational institutions from Russia, Kazakhstan, Türkiye, Ukraine, Belarus, Germany, the United Kingdom, France, Israel and Azerbaijan — including 13 universities, 7 research centres, institutes, government bodies and leading organisations — took part in the conference.',
)
_add(
    'Konfransda DAAB İdarə Heyətinin sədri Professor Məsud Əfəndiyev DAAB-ın fəaliyyətii barədə məruzə ilə çıxış etmişdir.',
    'At the conference, WAAS Board of Directors Chair Professor Messoud Efendiyev presented on the activities of WAAS.',
)

# Cairo book fair
_add(
    'Qahirə Beynəlxalq Kitab Sərgisi çərçivəsində Misir-Azərbaycan Dostluq Cəmiyyətinin sədri azərbaycanlı alim Seymur Nəsirovla görüş keçirilib.',
    'A meeting was held with Azerbaijani scholar Seymur Nasirov, Chair of the Egypt–Azerbaijan Friendship Society, within the Cairo International Book Fair.',
)
_add(
    'AZƏRTAC Misir-Azərbaycan Dostluq Cəmiyyətinə istinadla xəbər verir ki, Misirin Vəqflər Nazirliyi tərəfindən təşkil olunan görüşdə Misirin yüksəkvəzifəli şəxsləri, elm xadimləri və burada təhsil alan xarici tələbələr iştirak ediblər.',
    'AZERTAC reports, citing the Egypt–Azerbaijan Friendship Society, that senior Egyptian officials, scholars and foreign students studying in the country took part in the meeting organised by Egypt\'s Ministry of Endowments.',
)
_add(
    'Tədbirdə İslam İşləri Üzrə Ali Şuranın baş katibi professor Məhəmməd əl-Bəyyumi Seymur Nəsirovun elmi, ictimai və mədəni fəaliyyətlərinin Misir ictimaiyyəti tərəfindən yüksək qiymətləndirildiyini və onun ölkədə təhsil alan tələbələr üçün böyük bir nümunə olduğunu qeyd edib.',
    'At the event, Secretary General of the Supreme Council for Islamic Affairs Professor Muhammad al-Bayyumi noted that Seymur Nasirov\'s scientific, public and cultural activities are highly valued by Egyptian society and that he is a great example for students studying in the country.',
)

if __name__ == "__main__":
    print(len(ACTIVITIES_BODY_REPLACEMENTS))

# -*- coding: utf-8 -*-
"""Write the Complex Topics application pages in Azerbaijani and English."""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TOPICS = {
    "en": [
        (1, "Generative AI and large language models"),
        (2, "Algorithms and computational problem-solving"),
        (3, "Variables, assignment, data types and program state"),
        (4, "Finding errors, tests and reading error messages"),
        (5, "Cybersecurity, privacy and safe digital behaviour"),
        (6, "Data science, interpreting data and visualisation"),
        (7, "Conditions, Boolean logic and decision-making"),
        (8, "Loops, repetition and stopping"),
        (9, "Functions, parameters, return values and scope"),
        (10, "How the Internet and the Web work"),
        (11, "Machine learning, training data, models and predictions"),
        (12, "Data structures and their uses"),
        (13, "Algorithm efficiency and Big-O"),
        (14, "Databases, modelling and SQL"),
        (15, "Object-oriented programming"),
        (16, "Recursion"),
        (17, "Memory, references, pointers, the stack and dynamic memory"),
        (18, "Concurrent, asynchronous and parallel programming"),
        (19, "Binary numbers and digital representation"),
        (20, "Web programming, APIs and client–server applications"),
        (21, "Operating systems, processes, memory and file systems"),
        (22, "Cloud computing, containers and distributed systems"),
        (23, "Software engineering, Git and collaborative development"),
        (24, "Computer architecture, the processor, memory and instructions"),
        (25, "Dynamic programming and designing complex algorithms"),
        (26, "Cryptography, encryption, hashing and digital signatures"),
        (27, "Automata, computability and complexity classes"),
        (28, "Ethics, algorithmic bias and the social effects of computing"),
        (29, "Game development and interactive graphics"),
        (30, "Robotics, physical computing and the Internet of Things"),
    ],
    "az": [
        (1, "Məzmun yaradan süni intellekt və böyük dil modelləri"),
        (2, "Alqoritmlər və məsələlərin kompüter vasitəsilə həlli"),
        (3, "Dəyişənlər, mənimsətmə, verilənlər tipləri və proqramın vəziyyəti"),
        (4, "Proqramda səhvlərin tapılması, testlər və xəta mesajlarının anlaşılması"),
        (5, "Kibertəhlükəsizlik, şəxsi məlumatların məxfiliyi və rəqəmsal mühitdə təhlükəsiz davranış"),
        (6, "Verilənlər elmi, məlumatların təhlili və əyani təqdimatı"),
        (7, "Şərtlər, məntiqi əməliyyatlar və qərarvermə"),
        (8, "Dövrlər, təkrarlama və dayanma şərtləri"),
        (9, "Funksiyalar, parametrlər, qaytarılan qiymətlər və görünmə sahəsi"),
        (10, "İnternet və veb necə işləyir"),
        (11, "Maşın öyrənməsi, təlim verilənləri, modellər və proqnozlar"),
        (12, "Verilənlər strukturları və onların tətbiqi"),
        (13, "Alqoritmlərin səmərəliliyi və böyük O işarələməsi"),
        (14, "Verilənlər bazaları, modelləşdirmə və SQL"),
        (15, "Obyektyönlü proqramlaşdırma"),
        (16, "Rekursiya"),
        (17, "Yaddaş, istinadlar, göstəricilər, stek və dinamik yaddaş"),
        (18, "Tapşırıqların növbələşərək, asinxron və paralel icrası"),
        (19, "İkilik say sistemi və məlumatların rəqəmsal təsviri"),
        (20, "Veb proqramlaşdırma, API və müştəri–server tətbiqləri"),
        (21, "Əməliyyat sistemləri, proseslər, yaddaş və fayl sistemləri"),
        (22, "Bulud hesablamaları, konteynerlər və paylanmış sistemlər"),
        (23, "Proqram mühəndisliyi, Git və birgə proqram hazırlama"),
        (24, "Kompüterin quruluşu, prosessor, yaddaş və əmrlər"),
        (25, "Dinamik proqramlaşdırma və mürəkkəb alqoritmlərin qurulması"),
        (26, "Kriptoqrafiya, şifrələmə, heşləmə və rəqəmsal imza"),
        (27, "Avtomatlar, hesablanabilənlik və mürəkkəblik sinifləri"),
        (28, "Etika, alqoritmik qərəz və kompüter texnologiyalarının cəmiyyətə təsiri"),
        (29, "Oyunların hazırlanması və interaktiv qrafika"),
        (30, "Robototexnika, fiziki qurğuların proqramla idarə edilməsi və əşyaların interneti"),
    ],
}

COPY = {
    "en": {
        "html_lang": "en",
        "site": "WAAS",
        "title": "WAAS — Submit your application: Complex Topics, Clear Explanations",
        "description": "Application form for the open competition Complex Topics, Clear Explanations. Topics, formats and conditions follow the competition page.",
        "skip": "Skip to content",
        "menu": "Open menu",
        "nav": "Main navigation",
        "home_title": "Home page",
        "home_label": "WAAS home",
        "home_href": "index.html",
        "brand": '<span class="nav-brand-line">World Association of</span><span class="nav-brand-line">Azerbaijani Scientists</span>',
        "logo_alt": "WAAS Logo",
        "h1": 'Complex Topics, <span>Clear Explanations</span>',
        "subtitle": "Submit your application",
        "panel_title": "Application form",
        "panel_copy": "Use this form to apply for the open competition. The fields follow the competition page.",
        "search_label": "Search this form",
        "search_placeholder": "Search this form…",
        "search_band": "Search application form",
        "steps_label": "Application steps",
        "empty": "No results found.",
        "intro_lead": "Please complete the application. Fields marked with <span class=\"req\">*</span> are required.",
        "s1": "About you",
        "s2": "Participation",
        "s3": "The work",
        "s4": "Files and confirmation",
        "of": "Section {n} of 4",
        "collapse": "Collapse section: {name}",
        "intro": "This form is for the open competition <strong>Complex Topics, Clear Explanations</strong> (<a href=\"complex-topics.html\">competition page</a>). It uses the groups, formats and conditions published there. Prize amounts, a fixed file-size rule and separate judged categories are not confirmed on that page, so this form does not add them.",
        "name": "Name",
        "surname": "Surname",
        "dob": "Date of birth",
        "dob_calendar": "Open calendar",
        "email": "Email address",
        "country": "Country",
        "country_placeholder": "Select country",
        "city": "City",
        "city_placeholder": "Select country first",
        "city_manual_placeholder": "Enter your city",
        "org": "School, university or organisation",
        "optional": "(optional)",
        "org_hint": "Where applicable.",
        "photo": "Upload Photo",
        "photo_hint": "JPG or PNG, maximum 5 MB. You can choose a file from your device or from a cloud location offered by your file picker.",
        "photo_choose": "Choose file",
        "photo_replace": "Replace",
        "photo_remove": "Remove",
        "photo_ready": "Ready to submit",
        "category": "Participant group",
        "category_hint": "Select the group that best describes your current role.",
        "groups": [
            ("pupil", "School pupil"),
            ("student", "University or college student"),
            ("vocational", "Vocational learner"),
            ("teacher", "Teacher or trainer"),
            ("lecturer", "University lecturer"),
            ("scientist", "Scientist or researcher"),
            ("it", "IT professional"),
            ("creator", "Educational content creator"),
            ("other", "Other"),
        ],
        "group_other_label": "Name the group",
        "group_other_hint": "A short name is enough.",
        "bio": "Short biography",
        "bio_hint": "The competition page lists a short biography among the details an application may include.",
        "part": "Individual or team",
        "part_hint": "The page allows one person, or a recommended team of two or three. Whether two or three is a hard cap is not confirmed.",
        "individual": "Individual",
        "team": "Team",
        "team_name": "Team name",
        "member2": "Second author",
        "member3": "Third author",
        "member_email": "Email address",
        "member_hint": "Name every author. You are the main contact. A third author is optional.",
        "topic": "Topic",
        "topic_hint": "The 30 recommended topics from the topic guide, in the same wording. The guide says this list does not close the competition.",
        "topic_placeholder": "Select a topic",
        "topic_search": "Search topics",
        "topic_empty": "No topic matches. You can propose another topic in the field below.",
        "topic_guide": "Topic explanation",
        "topic_guide_placeholder": "Move through the list to read what the topic covers.",
        "other": "Propose another topic",
        "other_hint": "If your topic is not in the list above, write it here. A listed topic is then not required.",
        "other_why": "Brief explanation",
        "other_why_hint": "Say why the topic is hard to learn and worth a clear explanation.",
        "work_title": "Submission title",
        "audience": "Intended audience",
        "audience_after": "Choose who your material is mainly for.",
        "audience_other_label": "Say who the material is for",
        "audience_other_hint": "Write this audience briefly.",
        "audience_note": "Audience note",
        "audience_note_hint": "Optional. For example, age, educational level, or expected prior knowledge.",
        "audience_note_placeholder": "Pupils aged 12–15 with no programming experience.",
        "audiences": [
            ("primary", "Primary school pupils (grades I–IV)", "Simple explanations using stories, pictures, and examples from everyday life."),
            ("lower-secondary", "Pupils in grades V–IX", "Materials that explain the main ideas in clear language, with practical examples."),
            ("upper-secondary", "Pupils in grades X–XI", "Materials that explain topics in more detail and connect theoretical knowledge with applications."),
            ("college", "Students at vocational institutions and colleges", "Explanations focused on practical skills and professional activity."),
            ("university", "Higher-education students", "Systematic explanations that help students master topics studied at university."),
            ("teachers", "Teachers and trainers", "Educational materials that can be used in lessons and training."),
            ("adult", "Adults who want to learn something new or change career", "Simple, clear explanations that do not require specialist knowledge in advance."),
            ("public", "The general public", "Explanations for anyone interested in the topic, regardless of age or education."),
            ("other", "Other audience", "Say who the material is for."),
        ],
        "description": "Brief description",
        "description_hint": "Explain the concept, the intended audience, and how the material makes the topic easier to understand. Up to 5,000 characters.",
        "format": "Submission format",
        "format_hint": "Use one format or combine several. The ranges below are recommendations on the competition page, not fixed limits.",
        "formats": [
            ("article", "Article", "A written teaching text that a learner reads from start to finish. It explains one difficult idea in ordinary language, with definitions, a logical order, examples and a short conclusion. It may be a lecture written out, or an article meant to be studied alone. A useful range is about 2,000–5,000 words."),
            ("video", "Video lecture", "A recorded lesson in which someone explains the topic aloud, usually with a camera, slides, a screen or a board. The viewer watches and listens while the idea is built step by step, so speech, timing and pictures carry the explanation together. A useful range is about 8–20 minutes."),
            ("presentation", "Presentation", "A sequence of slides that shows one idea at a time, together with notes that say what should be explained on each slide. The slides carry the headings, diagrams and examples. The notes carry the sentences a teacher would say. A useful range is about 15–30 slides."),
            ("pack", "Teaching pack", "A set of pieces that belong together and teach one topic from more than one side, for example a short text, slides, a video, exercises and an answer guide. The learner can read, watch and then try the idea. Volume is agreed separately."),
            ("cartoon", "Educational cartoon", "A drawn story with characters, a setting and a short plot that teaches the idea by showing it happen. Pictures and dialogue do the explaining, so a learner who is not ready for a formal lecture can still follow the science. Volume is to be agreed."),
            ("animation", "Animation", "A moving picture that shows a process changing over time, such as data moving through a program, a packet crossing a network, or a loop repeating. The frames are drawn or generated so the viewer sees the change, with or without a spoken explanation. Volume is to be agreed."),
            ("comic", "Comic", "A story told in ordered panels. Each panel is a picture with a caption or speech, and the reader moves from one panel to the next. It suits a sequence of decisions, mistakes or steps that is easier to follow as a scene than as a paragraph. Volume is to be agreed."),
            ("infographic", "Infographic", "A designed page, or a short series of pages, that turns the topic into a picture a person can scan. Labels, arrows, numbers and simple diagrams show how the parts relate, so the main structure is visible without reading a long text. Volume is to be agreed."),
            ("interactive", "Interactive material", "A piece the learner operates, not only reads or watches. It may be a small program, a clickable diagram, a simulation or exercises that respond to what the person does. Trying an input and seeing the result is part of the explanation. Volume is to be agreed."),
        ],
        "language": "Submission language",
        "language_hint": "The material is usually in Azerbaijani or English. Both are accepted. If it is in another language, choose Other and name that language.",
        "lang_az": "Azerbaijani",
        "lang_en": "English",
        "lang_other": "Other",
        "language_other_label": "Name the language",
        "language_other_hint": "Write the language of the material.",
        "sources": "Main sources",
        "sources_hint": "The competition page asks for main sources. Important scientific, technical and statistical points need sources.",
        "ai": "Artificial intelligence",
        "ai_hint": "The competition page allows AI if it is disclosed and checked. Say whether it was not used, used in a limited way, or used substantially.",
        "ai_placeholder": "Choose one",
        "ai_none": "Not used",
        "ai_limited": "Used in a limited way",
        "ai_substantial": "Used substantially",
        "ai_detail": "Tool, purpose and scale",
        "ai_detail_hint": "Name the tool, what it was used for, and how much of the work it covered. You remain responsible for every fact.",
        "interest": "This is an expression of interest. The finished file is not ready yet.",
        "interest_hint": "The competition page allows an expression of interest before the finished file. A finished entry still needs the work itself.",
        "files": "Upload files",
        "files_hint": "The competition page has not fixed file types or a maximum size. This form can receive up to 3 files, each up to 8 MB: PDF, DOC, DOCX, PPT, PPTX, ODT, ODP, TXT, PNG, JPG, WEBP, GIF, MP4 or ZIP. A longer video or a larger pack should be given as a stable link.",
        "choose": "Choose files",
        "link": "Submission link",
        "link_hint": "A stable http or https link to the work. Use this for a video or a file larger than this form can send. Optional if you upload files, or if this is only an expression of interest.",
        "conditions": "I have read the <a href=\"complex-topics.html#who\">who may enter</a>, <a href=\"complex-topics.html#what\">what is submitted</a> and <a href=\"complex-topics.html#rights\">publication and ethics</a> sections, and I accept those published conditions.",
        "originality": "The work is mine or my team’s. Third-party text, images, diagrams and code are used properly.",
        "attribution": "I have the rights to the images, clips, diagrams and code samples in this work, and important sources are attributed.",
        "publication": "I understand that sending this application lets WAAS read and assess the work. I keep the copyright. This is not a publication licence. A separate agreement would follow only if the work is selected.",
        "privacy": "I have read the <a href=\"privacy.html\">Privacy notice</a> and understand that the personal data in this form will be used to run the competition.",
        "notice": "Your application is sent to info@daab-waas.com and is used to run the competition.",
        "button": "Submit your application",
        "success_title": "Application received",
        "success_text": "Thank you. Your application for Complex Topics, Clear Explanations has been received. Copyright stays with you. A separate publication agreement would follow only if the work is selected.",
        "back": "Return to the competition page",
        "footer_name": "World Association of Azerbaijani Scientists",
        "contact": "Contact",
        "address": "Address",
        "address_html": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, Istanbul, Türkiye",
        "leadership": "Leadership",
        "leader": "<strong>Prof. Dr. Messoud Efendiyev</strong><br/>Chair of the WAAS Executive Board<br/>Germany — James D. Murray Distinguished Professor",
        "legal_label": "Legal documents and sitemap",
        "legal": '<a href="/en/feedback.html">Feedback</a><a href="/en/privacy.html#page-title">Privacy notice</a><a href="/en/terms.html#page-title">Terms of use</a><a href="/en/cookies.html#page-title">Cookie policy</a><a href="/en/legal-notice.html#page-title">Legal notice (Imprint)</a><a href="/en/sitemap.html#page-title">Sitemap</a>',
        "copy": "© 2026 WAAS — All Rights Reserved",
        "canonical": "https://daab-waas.com/en/complex-topics-apply.html",
    },
    "az": {
        "html_lang": "az",
        "site": "DAAB",
        "title": "DAAB — Müraciətinizi göndərin: Çətin mövzu, aydın izah",
        "description": "«Çətin mövzu, aydın izah» açıq müsabiqəsinin müraciət forması. Mövzular, formatlar və şərtlər müsabiqə səhifəsinə əsaslanır.",
        "skip": "Məzmuna keç",
        "menu": "Menyunu aç",
        "nav": "Əsas naviqasiya",
        "home_title": "Ana səhifə",
        "home_label": "DAAB ana səhifə",
        "home_href": "index.html",
        "brand": '<span class="nav-brand-line">Dünya Azərbaycanlı</span><span class="nav-brand-line">Alimlər Birliyi</span>',
        "logo_alt": "DAAB Logo",
        "h1": 'Çətin mövzu, <span>aydın izah</span>',
        "subtitle": "Müraciətinizi göndərin",
        "panel_title": "Müraciət forması",
        "panel_copy": "Açıq müsabiqəyə bu forma ilə müraciət edin. Sahələr müsabiqə səhifəsinə əsaslanır.",
        "search_label": "Formada axtar",
        "search_placeholder": "Formada axtar…",
        "search_band": "Müraciət formasında axtarış",
        "steps_label": "Müraciət addımları",
        "empty": "Nəticə tapılmadı.",
        "intro_lead": "Zəhmət olmasa müraciəti tamamlayın. <span class=\"req\">*</span> ilə işarələnmiş sahələr mütləqdir.",
        "s1": "Siz",
        "s2": "İştirak",
        "s3": "İş",
        "s4": "Fayllar və təsdiq",
        "of": "{n}-ci bölmə, cəmi 4",
        "collapse": "Bölməni yığ: {name}",
        "intro": "Bu forma <strong>Çətin mövzu, aydın izah</strong> açıq müsabiqəsi üçündür (<a href=\"complex-topics.html\">müsabiqə səhifəsi</a>). Burada həmin səhifədə dərc olunmuş qruplar, formatlar və şərtlər istifadə olunur. Mükafat məbləği, sabit fayl həcmi və ayrı qiymətləndirilən kateqoriyalar orada təsdiqlənməyib, ona görə forma onları qayda kimi əlavə etmir.",
        "name": "Ad",
        "surname": "Soyad",
        "dob": "Doğum tarixi",
        "dob_calendar": "Təqvimi aç",
        "email": "E-poçt ünvanı",
        "country": "Ölkə",
        "country_placeholder": "Ölkə seçin",
        "city": "Şəhər",
        "city_placeholder": "Əvvəlcə ölkə seçin",
        "city_manual_placeholder": "Şəhərin adını yazın",
        "org": "Məktəb, universitet və ya təşkilat",
        "optional": "(istəyə bağlı)",
        "org_hint": "Aid olduğu halda.",
        "photo": "Foto yükləyin",
        "photo_hint": "JPG və ya PNG, ən çox 5 MB. Faylı cihazınızdan və ya fayl seçicisinin təklif etdiyi bulud məkanından seçə bilərsiniz.",
        "photo_choose": "Fayl seçin",
        "photo_replace": "Əvəz et",
        "photo_remove": "Sil",
        "photo_ready": "Göndərməyə hazırdır",
        "category": "İştirakçı qrupu",
        "category_hint": "Hazırkı fəaliyyətinizə ən uyğun qrupu seçin.",
        "groups": [
            ("pupil", "Şagird"),
            ("student", "Tələbə"),
            ("vocational", "Peşə təhsili alan şəxs"),
            ("teacher", "Müəllim və ya təlimçi"),
            ("lecturer", "Ali məktəb müəllimi"),
            ("scientist", "Alim və ya tədqiqatçı"),
            ("it", "İnformasiya texnologiyaları mütəxəssisi"),
            ("creator", "Tədris və maarifləndirici materialların müəllifi"),
            ("other", "Digər"),
        ],
        "group_other_label": "Qrupun adını yazın",
        "group_other_hint": "Qısa ad kifayətdir.",
        "bio": "Qısa tərcümeyi-hal",
        "bio_hint": "Müsabiqə səhifəsi müraciətdə qısa tərcümeyi-halı da göstərir.",
        "part": "Fərdi və ya komanda",
        "part_hint": "Səhifə fərdi işə, yaxud tövsiyə olunan 2–3 nəfərlik komandaya icazə verir. İki və ya üçün sərt hədd olması təsdiqlənməyib.",
        "individual": "Fərdi",
        "team": "Komanda",
        "team_name": "Komandanın adı",
        "member2": "İkinci müəllif",
        "member3": "Üçüncü müəllif",
        "member_email": "E-poçt ünvanı",
        "member_hint": "Bütün müəlliflərin adını yazın. Əsas əlaqə şəxsi sizsiniz. Üçüncü müəllif istəyə bağlıdır.",
        "topic": "Mövzu",
        "topic_hint": "Mövzu bələdçisindəki 30 tövsiyə olunan mövzu, eyni yazılışla. Bələdçi bu siyahının müsabiqəni bağlamadığını bildirir.",
        "topic_placeholder": "Mövzu seçin",
        "topic_search": "Mövzu axtarın",
        "topic_empty": "Uyğun mövzu tapılmadı. Aşağıdakı sahədə başqa mövzu təklif edə bilərsiniz.",
        "topic_guide": "Mövzunun izahı",
        "topic_guide_placeholder": "Siyahıdan keçdikcə mövzunun izahı burada görünəcək.",
        "other": "Başqa mövzu təklif et",
        "other_hint": "Mövzunuz yuxarıdakı siyahıda yoxdursa, onu bura yazın. Bu halda siyahıdan seçim mütləq deyil.",
        "other_why": "Qısa izah",
        "other_why_hint": "Mövzunun niyə çətin öyrənildiyini və aydın izaha ehtiyacı olduğunu yazın.",
        "work_title": "İşin başlığı",
        "audience": "Hədəf auditoriyası",
        "audience_after": "Materialınızın əsasən kimlər üçün nəzərdə tutulduğunu seçin.",
        "audience_other_label": "Kimlər üçün nəzərdə tutulduğunu qeyd edin",
        "audience_other_hint": "Seçdiyiniz auditoriyanı qısa yazın.",
        "audience_note": "Auditoriya qeydi",
        "audience_note_hint": "İstəyə bağlı. Məsələn, yaş, təhsil səviyyəsi və ya gözlənilən ilkin bilik.",
        "audience_note_placeholder": "12–15 yaşlı, proqramlaşdırma təcrübəsi olmayan şagirdlər.",
        "audiences": [
            ("primary", "İbtidai sinif şagirdləri (I–IV siniflər)", "Hekayələr, şəkillər və gündəlik həyatdan nümunələrlə sadə izahlar."),
            ("lower-secondary", "V–IX sinif şagirdləri", "Əsas anlayışları aydın dillə və praktik nümunələrlə izah edən materiallar."),
            ("upper-secondary", "X–XI sinif şagirdləri", "Mövzuları daha ətraflı açıqlayan, nəzəri bilikləri tətbiqlərlə əlaqələndirən materiallar."),
            ("college", "Peşə təhsili müəssisələrinin və kolleclərin tələbələri", "Praktik bacarıqlara və peşə fəaliyyətinə yönəlmiş izahlar."),
            ("university", "Ali məktəb tələbələri", "Universitetdə öyrənilən mövzuların mənimsənilməsinə kömək edən sistemli izahlar."),
            ("teachers", "Müəllimlər və təlimçilər", "Dərslərdə və təlimlərdə istifadə oluna biləcək maarifləndirici materiallar."),
            ("adult", "Yeni biliklər öyrənmək və ya peşəsini dəyişmək istəyən böyüklər", "Əvvəlcədən xüsusi bilik tələb etməyən, sadə və anlaşıqlı izahlar."),
            ("public", "Geniş ictimaiyyət", "Yaşından və təhsilindən asılı olmayaraq mövzuya maraq göstərən hər kəs üçün izahlar."),
            ("other", "Digər auditoriya", "Kimlər üçün nəzərdə tutulduğunu qeyd edin."),
        ],
        "description": "Qısa təsvir",
        "description_hint": "Konsepsiyanı, hədəf auditoriyanı və materialın mövzunu necə daha anlaşılan etdiyini yazın. Ən çox 5 000 simvol.",
        "format": "Təqdimat formatı",
        "format_hint": "Bir format seçin və ya bir neçəsini birləşdirin. Aşağıdakı həcmlər müsabiqə səhifəsindəki tövsiyələrdir, sabit hədd deyil.",
        "formats": [
            ("article", "Məqalə", "Öyrənənin əvvəldən sona oxuduğu yazılı tədris mətnidir. Çətin bir fikri adi dillə, təriflər, məntiqi ardıcıllıq, nümunələr və qısa nəticə ilə izah edir. Yazılmış mühazirə mətni və ya tək oxunan məqalə ola bilər. Faydalı həcm təxminən 2 000–5 000 sözdür."),
            ("video", "Videomühazirə", "Mövzunun şifahi izah olunduğu yazıya alınmış dərsdir. Müəllif adətən kamera, slayd, ekran və ya lövhə ilə fikri addım-addım danışır. İzah nitq, vaxt və görüntü ilə birlikdə qurulur. Faydalı müddət təxminən 8–20 dəqiqədir."),
            ("presentation", "Təqdimat", "Hər dəfə bir fikir göstərən slayd ardıcıllığıdır və hər slaydda nəyin izah olunacağını bildirən qeydlər olur. Slaydlar başlıq, sxem və nümunəni daşıyır. Qeydlər isə müəllimin deyəcəyi cümlələri saxlayır. Faydalı həcm təxminən 15–30 slayddır."),
            ("pack", "Tədris paketi", "Bir mövzunu bir neçə tərəfdən öyrədən və birlikdə işlənən materiallar dəstidir: məsələn qısa mətn, slayd, video, tapşırıq və cavab bələdçisi. Öyrənən oxuya, baxa və sonra fikri özü sınaya bilər. Həcm ayrıca razılaşdırılır."),
            ("cartoon", "Tədris cizgi filmi", "Personajları, məkanı və qısa süjeti olan çəkilmiş hekayədir. Fikri hadisənin içində göstərərək öyrədir. İzahı şəkillər və dialoq aparır, ona görə rəsmi mühazirəyə hazır olmayan oxucu da elmi məğzi izləyə bilər. Həcm razılaşdırılacaq."),
            ("animation", "Animasiya", "Zamanla dəyişən prosesi göstərən hərəkətli təsvirdir: məsələn proqramın içində gedən məlumat, şəbəkədən keçən paket və ya təkrarlanan dövr. Kadrlar elə qurulur ki, tamaşaçı dəyişikliyi görsün. Səsli izah ola bilər və ya olmaya bilər. Həcm razılaşdırılacaq."),
            ("comic", "Komiks", "Ardıcıl panellərlə danışılan hekayədir. Hər panel şəkil və qısa mətndən ibarətdir, oxucu paneldən panelə keçir. Qərarlar, səhvlər və ya addımlar abzasdan çox səhnə kimi izləniləndə əlverişlidir. Həcm razılaşdırılacaq."),
            ("infographic", "İnfoqrafika", "Mövzunu bir baxışda oxunan şəklə çevirən səhifə, yaxud qısa səhifələr silsiləsidir. Yazılar, oxlar, rəqəmlər və sadə sxemlər hissələrin necə bağlı olduğunu göstərir. Əsas quruluş uzun mətn oxumadan görünür. Həcm razılaşdırılacaq."),
            ("interactive", "İnteraktiv material", "Öyrənənin yalnız oxumadığı və ya baxmadığı, özünün işlətdiyi materialdır. Kiçik proqram, basılan sxem, simulyasiya və ya edilən hərəkətə cavab verən tapşırıq ola bilər. Giriş vermək və nəticəni görmək izahın bir hissəsidir. Həcm razılaşdırılacaq."),
        ],
        "language": "İşin dili",
        "language_hint": "Material adətən Azərbaycan və ya ingilis dilində olur. Hər iki dil qəbul edilir. Başqa dildirsə, Digər seçin və həmin dilin adını yazın.",
        "lang_az": "Azərbaycan dili",
        "lang_en": "İngilis dili",
        "lang_other": "Digər",
        "language_other_label": "Dilin adını yazın",
        "language_other_hint": "Materialın dilini yazın.",
        "sources": "Əsas mənbələr",
        "sources_hint": "Müsabiqə səhifəsi əsas mənbələri soruşur. Mühüm elmi, texniki və statistik məqamların mənbəsi göstərilməlidir.",
        "ai": "Süni intellekt",
        "ai_hint": "Müsabiqə səhifəsi süni intellektə açıqlanırsa və yoxlanılırsa icazə verir. İstifadə olunmayıb, məhdud, yoxsa əhəmiyyətli dərəcədə istifadə olunub, onu seçin.",
        "ai_placeholder": "Birini seçin",
        "ai_none": "İstifadə olunmayıb",
        "ai_limited": "Məhdud istifadə",
        "ai_substantial": "Əhəmiyyətli istifadə",
        "ai_detail": "Alət, məqsəd və miqyas",
        "ai_detail_hint": "Alətin adını, nə üçün işlədildiyini və işin nə qədərini əhatə etdiyini yazın. Hər fakta görə məsuliyyət sizdə qalır.",
        "interest": "Bu, ilkin maraq bəyanatıdır. Hazır fayl hələ yoxdur.",
        "interest_hint": "Müsabiqə səhifəsi hazır fayldan əvvəl ilkin marağa icazə verir. Tam müraciət üçün işin özü lazımdır.",
        "files": "Faylları yükləyin",
        "files_hint": "Müsabiqə səhifəsi fayl növünü və maksimum həcmi hələ müəyyən etməyib. Bu forma ən çox 3 fayl, hər biri ən çox 8 MB qəbul edir: PDF, DOC, DOCX, PPT, PPTX, ODT, ODP, TXT, PNG, JPG, WEBP, GIF, MP4 və ya ZIP. Daha uzun video və ya daha böyük paket üçün sabit keçid verin.",
        "choose": "Fayl seçin",
        "link": "İşin keçidi",
        "link_hint": "İşə aparan sabit http və ya https keçidi. Video və ya bu formanın göndərə bilməyəcəyi böyük fayl üçün bundan istifadə edin. Fayl yüklənibsə, yaxud bu yalnız ilkin maraqdırsa, istəyə bağlıdır.",
        "conditions": "<a href=\"complex-topics.html#who\">Kimlər</a>, <a href=\"complex-topics.html#what\">nə təqdim edilir</a> və <a href=\"complex-topics.html#rights\">yayım və etika</a> bölmələrini oxudum və dərc olunmuş şərtləri qəbul edirəm.",
        "originality": "İş mənə və ya komandamıza məxsusdur. Üçüncü tərəfin mətni, şəkli, sxemi və kodu qaydaya uyğun istifadə olunub.",
        "attribution": "Bu işdəki şəkil, klip, sxem və kod nümunələri üzərində hüququm var və mühüm mənbələr göstərilib.",
        "publication": "Bu müraciətin göndərilməsinin DAAB-a işi oxumaq və qiymətləndirmək imkanı verdiyini başa düşürəm. Müəlliflik hüququ məndə qalır. Bu, yayım lisenziyası deyil. Ayrı razılaşma yalnız iş seçilərsə bağlanacaq.",
        "privacy": "<a href=\"privacy.html\">Məxfilik bildirişini</a> oxudum və bu formadakı şəxsi məlumatların müsabiqənin təşkili üçün istifadə olunacağını başa düşürəm.",
        "notice": "Müraciət info@daab-waas.com ünvanına göndərilir və müsabiqənin təşkili üçün istifadə olunur.",
        "button": "Müraciətinizi göndərin",
        "success_title": "Müraciət qəbul edildi",
        "success_text": "Təşəkkür edirik. Çətin mövzu, aydın izah müsabiqəsinə müraciətiniz qəbul olundu. Müəlliflik hüququ sizdə qalır. Ayrı yayım razılaşması yalnız iş seçilərsə bağlanacaq.",
        "back": "Müsabiqə səhifəsinə qayıdın",
        "footer_name": "Dünya Azərbaycanlı Alimlər Birliyi",
        "contact": "Əlaqə",
        "address": "Ünvan",
        "address_html": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə",
        "leadership": "Rəhbərlik",
        "leader": "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Almaniya — James D. Murray mükafatlı professoru",
        "legal_label": "Hüquqi sənədlər və saytın xəritəsi",
        "legal": '<a href="/az/feedback.html">Rəy bildirin</a><a href="/az/privacy.html#page-title">Məxfilik bildirişi</a><a href="/az/terms.html#page-title">İstifadə şərtləri</a><a href="/az/cookies.html#page-title">Kuki siyasəti</a><a href="/az/legal-notice.html#page-title">Hüquqi rekvizitlər</a><a href="/az/sitemap.html#page-title">Saytın xəritəsi</a>',
        "copy": "© 2026 DAAB — Bütün hüquqlar qorunur",
        "canonical": "https://daab-waas.com/az/complex-topics-apply.html",
    },
}


def json_topics(lang):
    import json
    items = [{"id": str(n), "label": label} for n, label in TOPICS[lang]]
    return json.dumps(items, ensure_ascii=False)


def json_guides(lang):
    name = "ct-topic-guides-az.json" if lang == "az" else "ct-topic-guides.json"
    return (ROOT / "js" / name).read_text(encoding="utf-8").strip()


def radio(name, value, label, required=False):
    req = " required" if required else ""
    return (
        f'<div class="opt-item"><input type="radio" name="{name}" id="{name}-{value}" value="{value}"{req}>'
        f'<label for="{name}-{value}">{label}</label></div>'
    )


def checkbox_format(key, label, guide):
    return (
        f'<div class="opt-item"><input type="checkbox" name="formats[]" id="format-{key}" value="{key}">'
        f'<label for="format-{key}"><span class="format-title">{label}</span>'
        f'<span class="format-detail">{guide}</span></label></div>'
    )


def audience_option(value, title, detail):
    return (
        f'<div class="opt-item"><input type="checkbox" name="audience" id="audience-{value}" value="{value}">'
        f'<label for="audience-{value}"><span class="audience-title">{title}</span>'
        f'<span class="audience-detail">{detail}</span></label></div>'
    )


def section(n, title, body, copy):
    small = copy["of"].format(n=n)
    return f'''
    <div class="form-section active" id="sec-{n}">
      <div class="section-header">
        <div class="section-num">{n}</div>
        <div class="section-title">{title}<small>{small}</small></div>
        <button type="button" class="app-section-toggle" aria-expanded="true" aria-controls="sec-{n}-body" aria-label="{copy["collapse"].format(name=title)}" data-section-label="{title}">
          <svg class="app-section-toggle__icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M6 9l6 6 6-6"/></svg>
        </button>
      </div>
      <div class="section-body" id="sec-{n}-body">{body}</div>
    </div>'''


def page(lang):
    c = COPY[lang]
    other = "az" if lang == "en" else "en"
    formats = "\n            ".join(checkbox_format(key, label, guide) for key, label, guide in c["formats"])
    groups = "\n            ".join(
        radio("category", value, label, index == 0)
        for index, (value, label) in enumerate(c["groups"])
    )
    audiences = "\n            ".join(audience_option(value, title, detail) for value, title, detail in c["audiences"])
    if c.get("audience_hint"):
        audience_lead = f'<span class="field-hint" id="audience-hint">{c["audience_hint"]}</span>'
        audience_describedby = "audience-hint"
    else:
        audience_lead = ""
        audience_describedby = "audience-after"
    audience_after = ""
    if c.get("audience_after"):
        audience_after = f'<p class="field-hint" id="audience-after">{c["audience_after"]}</p>'
    steps = [
        (1, c["s1"]),
        (2, c["s2"]),
        (3, c["s3"]),
        (4, c["s4"]),
    ]
    step_html = "\n".join(
        f'<li><a href="#sec-{n}"><span class="tl-date forum-register-pill__num">{n}</span> {title}</a></li>'
        for n, title in steps
    )
    body1 = f'''
        <div class="intro-box">{c["intro"]}<p>{c["intro_lead"]}</p></div>
        <div class="ct-pair ct-pair--4">
          <div class="field-group">
            <label class="field-label" for="given-name">{c["name"]} <span class="req">*</span></label>
            <input type="text" id="given-name" name="first_name" autocomplete="given-name" maxlength="120" required>
          </div>
          <div class="field-group">
            <label class="field-label" for="surname">{c["surname"]} <span class="req">*</span></label>
            <input type="text" id="surname" name="surname" autocomplete="family-name" maxlength="120" required>
          </div>
          <div class="field-group">
            <label class="field-label" for="dob">{c["dob"]} <span class="req">*</span></label>
            <div class="dob-field">
              <input type="text" id="dob" name="dob" required autocomplete="bday" inputmode="numeric" maxlength="10" placeholder="dd/mm/yyyy" spellcheck="false">
              <span class="dob-calendar-wrap">
                <button type="button" id="dob_calendar_btn" class="dob-calendar-btn" aria-label="{c["dob_calendar"]}" aria-controls="dob">
                  <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="18" rx="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
                </button>
                <input type="date" id="dob_picker" class="dob-native-picker" tabindex="-1" aria-hidden="true">
              </span>
            </div>
          </div>
          <div class="field-group">
            <label class="field-label" for="email">{c["email"]} <span class="req">*</span></label>
            <input type="email" id="email" name="email" autocomplete="email" maxlength="200" required>
          </div>
        </div>
        <div class="ct-pair">
          <div class="field-group">
            <label class="field-label" for="country">{c["country"]} <span class="req">*</span></label>
            <select id="country" name="country" required data-country-select="1" autocomplete="off">
              <option value="">{c["country_placeholder"]}</option>
            </select>
          </div>
          <div class="field-group">
            <label class="field-label" for="city">{c["city"]} <span class="req">*</span></label>
            <select id="city" name="city" required disabled data-city-select="1">
              <option value="">{c["city_placeholder"]}</option>
            </select>
            <input type="text" id="city_manual" name="city_manual" class="city-manual-fallback" hidden maxlength="200" placeholder="{c["city_manual_placeholder"]}" autocomplete="address-level2">
          </div>
        </div>
        <div class="ct-org-photo">
          <div class="field-group">
            <label class="field-label" for="organisation">{c["org"]} <span class="field-label-optional">{c["optional"]}</span></label>
            <span class="field-hint" id="org-hint">{c["org_hint"]}</span>
            <input type="text" id="organisation" name="organisation" autocomplete="organization" maxlength="200" aria-describedby="org-hint">
          </div>
          <div class="app-file-card" data-file-kind="photo">
            <label class="field-label" for="photofile">{c["photo"]} <span class="req">*</span></label>
            <p class="field-hint" id="photofile-hint">{c["photo_hint"]}</p>
            <input class="app-file-input" type="file" id="photofile" name="photo_file" accept=".jpg,.jpeg,.png,image/jpeg,image/png" aria-describedby="photofile-hint photofile-status photofile-error">
            <button type="button" class="app-btn app-btn-secondary app-file-choose" data-file-target="photofile">{c["photo_choose"]}</button>
            <div class="app-file-selected" id="photofile-status" hidden>
              <img class="app-file-thumb" id="photofile-thumb" alt="" hidden>
              <div class="app-file-meta">
                <span class="app-file-name"></span>
                <span class="app-file-ready">{c["photo_ready"]}</span>
              </div>
              <div class="app-file-tools">
                <button type="button" class="app-file-replace" data-file-target="photofile">{c["photo_replace"]}</button>
                <button type="button" class="app-file-remove" data-file-kind="photo">{c["photo_remove"]}</button>
              </div>
            </div>
            <p class="app-file-error" id="photofile-error" hidden role="alert"></p>
          </div>
        </div>
        <fieldset class="field-group">
          <legend class="field-label">{c["category"]} <span class="req">*</span></legend>
          <span class="field-hint" id="category-hint">{c["category_hint"]}</span>
          <div class="options-list options-list--groups" role="radiogroup" aria-describedby="category-hint">
            {groups}
          </div>
          <div id="category-other-wrap" class="ct-conditional" hidden>
            <div class="field-group">
              <label class="field-label" for="category-other-text">{c["group_other_label"]} <span class="req">*</span></label>
              <span class="field-hint" id="category-other-hint">{c["group_other_hint"]}</span>
              <input type="text" id="category-other-text" name="category_other" maxlength="200" aria-describedby="category-other-hint">
            </div>
          </div>
        </fieldset>
        <div class="field-group">
          <label class="field-label" for="biography">{c["bio"]} <span class="field-label-optional">{c["optional"]}</span></label>
          <span class="field-hint" id="bio-hint">{c["bio_hint"]}</span>
          <textarea id="biography" name="biography" maxlength="1000" aria-describedby="bio-hint"></textarea>
        </div>'''
    body2 = f'''
        <fieldset class="field-group">
          <legend class="field-label">{c["part"]} <span class="req">*</span></legend>
          <span class="field-hint" id="part-hint">{c["part_hint"]}</span>
          <div class="options-list options-list--two" aria-describedby="part-hint">
            {radio("participation", "individual", c["individual"], True)}
            {radio("participation", "team", c["team"])}
          </div>
        </fieldset>
        <div id="team-fields" class="ct-conditional" hidden>
          <p class="field-hint">{c["member_hint"]}</p>
          <div class="field-group">
            <label class="field-label" for="team-name">{c["team_name"]} <span class="req">*</span></label>
            <input type="text" id="team-name" name="team_name" maxlength="120">
          </div>
          <div class="ct-pair">
            <div class="field-group">
              <label class="field-label" for="member2-name">{c["member2"]} <span class="req">*</span></label>
              <input type="text" id="member2-name" name="member2_name" maxlength="120" autocomplete="off">
            </div>
            <div class="field-group">
              <label class="field-label" for="member2-email">{c["member_email"]} <span class="field-label-optional">{c["optional"]}</span></label>
              <input type="email" id="member2-email" name="member2_email" maxlength="200" autocomplete="off">
            </div>
          </div>
          <div class="ct-pair">
            <div class="field-group">
              <label class="field-label" for="member3-name">{c["member3"]} <span class="field-label-optional">{c["optional"]}</span></label>
              <input type="text" id="member3-name" name="member3_name" maxlength="120" autocomplete="off">
            </div>
            <div class="field-group">
              <label class="field-label" for="member3-email">{c["member_email"]} <span class="field-label-optional">{c["optional"]}</span></label>
              <input type="email" id="member3-email" name="member3_email" maxlength="200" autocomplete="off">
            </div>
          </div>
        </div>'''
    body3 = f'''
        <div class="ct-topic-row">
          <div class="field-group">
            <label class="field-label" for="topic_picker">{c["topic"]} <span class="req">*</span></label>
            <div class="phone-code-picker country-picker topic-picker" id="topic-picker">
              <button type="button" id="topic_picker" class="phone-code-picker-btn" aria-haspopup="listbox" aria-expanded="false" aria-controls="topic-list" aria-describedby="topic-hint">
                <span class="phone-code-picker-value"><span class="phone-code-picker-text" id="topic-picker-text">{c["topic_placeholder"]}</span></span>
                <span class="phone-code-picker-chevron" aria-hidden="true"></span>
              </button>
              <div class="phone-code-picker-panel country-picker-panel" id="topic-panel" hidden>
                <div class="country-picker-search-wrap">
                  <input type="search" id="topic-search" class="country-picker-search" placeholder="{c["topic_search"]}" autocomplete="off" spellcheck="false" aria-label="{c["topic_search"]}" aria-autocomplete="list" aria-controls="topic-list">
                </div>
                <ul id="topic-list" class="phone-code-picker-list" role="listbox"></ul>
                <div class="country-picker-empty" id="topic-empty" hidden>{c["topic_empty"]}</div>
              </div>
            </div>
            <input type="hidden" id="topic-id" name="topic_id" value="">
            <span class="field-hint" id="topic-hint">{c["topic_hint"]}</span>
          </div>
          <div class="field-group">
            <label class="field-label" for="topic-guide">{c["topic_guide"]}</label>
            <textarea id="topic-guide" class="topic-guide" readonly aria-readonly="true" aria-live="polite" placeholder="{c["topic_guide_placeholder"]}"></textarea>
          </div>
        </div>
        <div class="field-group">
          <label class="field-label" for="other-title">{c["other"]} <span class="field-label-optional">{c["optional"]}</span></label>
          <span class="field-hint" id="other-hint">{c["other_hint"]}</span>
          <input type="text" id="other-title" name="other_title" maxlength="200" aria-describedby="other-hint">
        </div>
        <div id="other-topic" class="ct-conditional" hidden>
          <div class="field-group">
            <label class="field-label" for="other-explanation">{c["other_why"]} <span class="req">*</span></label>
            <span class="field-hint" id="other-why-hint">{c["other_why_hint"]}</span>
            <textarea id="other-explanation" name="other_explanation" maxlength="1000" aria-describedby="other-why-hint"></textarea>
          </div>
        </div>
        <div class="field-group">
          <label class="field-label" for="submission-title">{c["work_title"]} <span class="req">*</span></label>
          <input type="text" id="submission-title" name="submission_title" maxlength="200" required>
        </div>
        <fieldset class="field-group">
          <legend class="field-label">{c["audience"]} <span class="req">*</span></legend>
          {audience_lead}
          <div class="options-list options-list--audience" role="group" aria-describedby="{audience_describedby}">
            {audiences}
          </div>
          {audience_after}
          <div id="audience-other-wrap" class="ct-conditional" hidden>
            <div class="field-group">
              <label class="field-label" for="audience-other-text">{c["audience_other_label"]} <span class="req">*</span></label>
              <span class="field-hint" id="audience-other-hint">{c["audience_other_hint"]}</span>
              <input type="text" id="audience-other-text" name="audience_other" maxlength="200" aria-describedby="audience-other-hint">
            </div>
          </div>
          <div class="field-group">
            <label class="field-label" for="audience-note">{c["audience_note"]} <span class="field-label-optional">{c["optional"]}</span></label>
            <span class="field-hint" id="audience-note-hint">{c["audience_note_hint"]}</span>
            <input type="text" id="audience-note" name="audience_note" maxlength="300" placeholder="{c["audience_note_placeholder"]}" aria-describedby="audience-note-hint">
          </div>
        </fieldset>
        <div class="field-group">
          <label class="field-label" for="description">{c["description"]} <span class="req">*</span></label>
          <span class="field-hint" id="description-hint">{c["description_hint"]}</span>
          <textarea id="description" name="description" maxlength="5000" aria-describedby="description-hint" required></textarea>
        </div>
        <fieldset class="field-group">
          <legend class="field-label">{c["format"]} <span class="req">*</span></legend>
          <span class="field-hint" id="format-hint">{c["format_hint"]}</span>
          <div class="options-list options-list--formats" aria-describedby="format-hint">
            {formats}
          </div>
        </fieldset>
        <fieldset class="field-group">
          <legend class="field-label">{c["language"]} <span class="req">*</span></legend>
          <span class="field-hint" id="language-hint">{c["language_hint"]}</span>
          <div class="options-list options-list--two" aria-describedby="language-hint">
            {radio("submission_language", "az", c["lang_az"], True)}
            {radio("submission_language", "en", c["lang_en"])}
            {radio("submission_language", "other", c["lang_other"])}
          </div>
          <div id="language-other-wrap" class="ct-conditional" hidden>
            <div class="field-group">
              <label class="field-label" for="language-other-text">{c["language_other_label"]} <span class="req">*</span></label>
              <span class="field-hint" id="language-other-hint">{c["language_other_hint"]}</span>
              <input type="text" id="language-other-text" name="language_other" maxlength="80" aria-describedby="language-other-hint">
            </div>
          </div>
        </fieldset>
        <div class="field-group">
          <label class="field-label" for="sources">{c["sources"]} <span class="field-label-optional">{c["optional"]}</span></label>
          <span class="field-hint" id="sources-hint">{c["sources_hint"]}</span>
          <textarea id="sources" name="sources" maxlength="2000" aria-describedby="sources-hint"></textarea>
        </div>
        <div class="field-group">
          <label class="field-label" for="ai-use">{c["ai"]} <span class="req">*</span></label>
          <span class="field-hint" id="ai-hint">{c["ai_hint"]}</span>
          <select id="ai-use" name="ai_use" aria-describedby="ai-hint" required>
            <option value="">{c["ai_placeholder"]}</option>
            <option value="none">{c["ai_none"]}</option>
            <option value="limited">{c["ai_limited"]}</option>
            <option value="substantial">{c["ai_substantial"]}</option>
          </select>
        </div>
        <div id="ai-detail-wrap" class="field-group ct-conditional" hidden>
          <label class="field-label" for="ai-detail">{c["ai_detail"]} <span class="req">*</span></label>
          <span class="field-hint" id="ai-detail-hint">{c["ai_detail_hint"]}</span>
          <textarea id="ai-detail" name="ai_detail" maxlength="1000" aria-describedby="ai-detail-hint"></textarea>
        </div>'''
    body4 = f'''
        <div class="field-group">
          <div class="opt-item">
            <input type="checkbox" id="interest-only" name="interest_only" value="yes">
            <label for="interest-only">{c["interest"]}</label>
          </div>
          <span class="field-hint">{c["interest_hint"]}</span>
        </div>
        <div class="app-file-uploads">
          <div class="app-file-card">
            <label class="field-label" for="submission-files">{c["files"]}</label>
            <p class="field-hint" id="files-hint">{c["files_hint"]}</p>
            <input class="app-file-input" type="file" id="submission-files" name="submission_files[]" multiple accept=".pdf,.doc,.docx,.ppt,.pptx,.odt,.odp,.txt,.png,.jpg,.jpeg,.webp,.gif,.mp4,.zip" aria-describedby="files-hint file-error">
            <button type="button" class="app-btn app-btn-secondary app-file-choose" id="choose-files">{c["choose"]}</button>
            <ul class="ct-file-list" id="file-list"></ul>
            <p class="app-file-error" id="file-error" hidden role="alert"></p>
          </div>
        </div>
        <div class="field-group">
          <label class="field-label" for="submission-link">{c["link"]} <span class="field-label-optional">{c["optional"]}</span></label>
          <span class="field-hint" id="link-hint">{c["link_hint"]}</span>
          <input type="url" id="submission-link" name="submission_link" maxlength="500" placeholder="https://" aria-describedby="link-hint">
        </div>
        <div class="field-group"><div class="opt-item"><input type="checkbox" id="conditions" name="conditions" value="yes" required><label for="conditions">{c["conditions"]}</label></div></div>
        <div class="field-group"><div class="opt-item"><input type="checkbox" id="originality" name="originality" value="yes" required><label for="originality">{c["originality"]}</label></div></div>
        <div class="field-group"><div class="opt-item"><input type="checkbox" id="attribution" name="attribution" value="yes" required><label for="attribution">{c["attribution"]}</label></div></div>
        <div class="field-group"><div class="opt-item"><input type="checkbox" id="publication" name="publication" value="yes" required><label for="publication">{c["publication"]}</label></div></div>
        <div class="field-group"><div class="opt-item opt-item-privacy-confirm"><input type="checkbox" id="privacy" name="privacy" value="yes" required><label for="privacy">{c["privacy"]}</label></div></div>
        <p class="app-submit-notice">{c["notice"]}</p>
        <div class="app-submit-status" id="app-submit-status" role="status" aria-live="polite" hidden></div>
        <div class="app-honeypot" aria-hidden="true"><label for="website">Website</label><input type="text" id="website" name="website" tabindex="-1" autocomplete="off"></div>
        <input type="hidden" name="page_url" id="page-url" value="">
        <input type="hidden" name="form_kind" value="complex-topics">
        <div class="app-btn-row">
          <button type="submit" class="app-btn app-btn-submit" id="appSubmitBtn"><span aria-hidden="true">✓</span> <span class="app-btn-label">{c["button"]}</span></button>
        </div>'''
    return f'''<!DOCTYPE html>
<html lang="{c["html_lang"]}" data-daab-lang="{lang}" data-daab-asset-root="../" data-daab-page-id="complex-topics-apply" data-daab-nav-mount="1">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover"/>
<title>{c["title"]}</title>
<meta name="description" content="{c["description"]}"/>
<!-- daab-seo -->
<link rel="icon" href="../images/daab-favicon.png" type="image/png"/>
<link rel="apple-touch-icon" href="../images/daab-favicon.png"/>
<link rel="canonical" href="{c["canonical"]}"/>
<link rel="alternate" hreflang="az" href="https://daab-waas.com/az/complex-topics-apply.html"/>
<link rel="alternate" hreflang="en" href="https://daab-waas.com/en/complex-topics-apply.html"/>
<link rel="alternate" hreflang="x-default" href="https://daab-waas.com/az/complex-topics-apply.html"/>
<meta property="og:type" content="website"/>
<meta property="og:site_name" content="{c["site"]}"/>
<meta property="og:title" content="{c["title"]}"/>
<meta property="og:description" content="{c["description"]}"/>
<meta property="og:url" content="{c["canonical"]}"/>
<meta property="og:image" content="https://daab-waas.com/images/daab-logo.png"/>
<meta property="og:locale" content="{"az_AZ" if lang == "az" else "en_US"}"/>
<meta property="og:locale:alternate" content="{"en_US" if lang == "az" else "az_AZ"}"/>
<meta name="twitter:card" content="summary_large_image"/>
<meta name="twitter:title" content="{c["title"]}"/>
<meta name="twitter:description" content="{c["description"]}"/>
<meta name="twitter:image" content="https://daab-waas.com/images/daab-logo.png"/>
<!-- /daab-seo -->
<link href="../css/daab-fonts.css?v=1" rel="stylesheet"/>
<link href="../css/daab-common.css?v=115" rel="stylesheet"/>
<link href="../css/daab-perf.css?v=2" rel="stylesheet"/>
<link href="../css/daab-mobile.css?v=14" rel="stylesheet"/>
<link href="../css/daab-sticky-chrome.css?v=13" rel="stylesheet"/>
<link href="../css/daab-search.css?v=10" rel="stylesheet"/>
<link href="../css/daab-back-to-top.css?v=4" rel="stylesheet"/>
<link href="../css/daab-lang.css?v=15" rel="stylesheet"/>
<link href="../css/daab-nav-mega.css?v=87" rel="stylesheet"/>
<link href="../css/daab-hero-summary.css?v=13" rel="stylesheet"/>
<link href="../css/scientists-catalog-toolbar.css?v=9" rel="stylesheet"/>
<link href="../css/daab-page-content-search.css?v=10" rel="stylesheet"/>
<link href="../css/daab-sidebar-widget.css?v=6" rel="stylesheet"/>
<link href="../css/daab-membership-application.css?v=80" rel="stylesheet"/>
<script src="../js/daab-mobile.js?v=6" defer></script>
<script src="../js/daab-perf.js?v=4" defer></script>
<script src="../js/daab-sticky-chrome.js?v=8" defer></script>
<script src="../js/daab-back-to-top.js?v=5" defer></script>
<script src="../js/daab-i18n.js?v=78" defer></script>
<script src="../js/daab-lang-position.js?v=14" defer></script>
<script src="../js/daab-design-tokens.js?v=2" defer></script>
<script src="../js/daab-nav.js?v=36" defer></script>
<script src="../js/daab-primary-nav.js?v=67" defer></script>
<script src="../js/daab-breadcrumbs.js?v=57" defer></script>
<script src="../js/daab-shell.js?v=19" defer></script>
<script src="../js/daab-page-subtitle.js?v=12" defer></script>
<script src="../js/daab-search.js?v=17" defer></script>
<script src="../js/daab-analytics.js?v=7" defer></script>
<script src="../js/daab-country-codes.js?v=3" defer></script>
<script src="../js/daab-respect.js?v=1" defer></script>
<script src="../js/daab-membership-application.js?v=62" defer></script>
<script src="../js/daab-complex-topics-apply.js?v=20" defer></script>
<script defer src="../js/daab-page-content-search.js?v=10"></script>
<script type="application/json" id="ct-topics">{json_topics(lang)}</script>
<script type="application/json" id="ct-topic-guides">{json_guides(lang)}</script>
</head>
<body class="application-page membership-page application-page--single forum-register-page ct-apply-page">
<a class="skip" href="#content">{c["skip"]}</a>
<nav aria-label="{c["nav"]}" class="nav-strip">
<div class="nav-inner">
<button class="mobile-menu-toggle" type="button" aria-label="{c["menu"]}" aria-expanded="false" aria-controls="primaryNavMenu"><span></span><span></span><span></span></button>
<div class="page-logo"><a title="{c["home_title"]}" aria-label="{c["home_label"]}" href="{c["home_href"]}">
<img src="../images/daab-logo.png" class="nav-brand-logo" alt="{c["logo_alt"]}"></a></div>
<a aria-label="{c["home_label"]}" class="nav-brand" href="{c["home_href"]}">
<span class="nav-brand-text">{c["brand"]}</span></a>
<div class="nav-menu" id="primaryNavMenu" data-daab-nav-placeholder="1"><div class="nav-divider"></div></div></div></nav>
<header class="hero">
<div class="hero-wrap shell">
<section>
<h1>{c["h1"]}</h1>
<p class="page-hero-subtitle" id="page-hero-subtitle" role="doc-subtitle">{c["subtitle"]}</p>
</section>
<aside aria-label="{c["panel_title"]}" class="hero-panel">
<div class="panel-card">
<h2 class="panel-title">{c["panel_title"]}</h2>
<div class="panel-copy"><p class="panel-copy-lead">{c["panel_copy"]}</p></div>
</div>
</aside>
</div>
</header>
<section class="shell page-content-search-band" aria-label="{c["search_band"]}">
<div class="forum-register-sticky-spacer" aria-hidden="true"></div>
<div class="forum-register-sticky-stack">
<div class="toolbar page-content-search-toolbar" role="search">
<div class="page-content-search-toolbar__head">
<div class="search-wrap">
<svg fill="none" height="15" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" width="15" aria-hidden="true"><circle cx="11" cy="11" r="8"></circle><line x1="21" x2="16.65" y1="21" y2="16.65"></line></svg>
<input autocomplete="off" id="pageContentSearch" placeholder="{c["search_placeholder"]}" type="search" aria-label="{c["search_label"]}"/>
</div>
</div>
</div>
<nav class="forum-register-stepbar" aria-label="{c["steps_label"]}">
<ul class="forum-register-stepbar__list timeline-list" id="appStepsMenu">
{step_html}
</ul>
</nav>
</div>
<div class="no-results page-content-search__empty" id="pageContentSearchEmpty" hidden>
{c["empty"]}
</div>
</section>
<main class="main application-main" id="content">
<div class="shell application-preamble"></div>
<div class="application-layout">
<div class="application-stack form-wrapper">
  <form id="ctApplyForm" action="mail-complex-topics.php" method="post" enctype="multipart/form-data" novalidate>
    {section(1, c["s1"], body1, c)}
    {section(2, c["s2"], body2, c)}
    {section(3, c["s3"], body3, c)}
    {section(4, c["s4"], body4, c)}
    <div class="success-screen" id="success">
      <div class="success-icon">✓</div>
      <h2>{c["success_title"]}</h2>
      <p>{c["success_text"]}</p>
      <div class="app-btn-row"><a class="app-btn app-btn-primary" href="complex-topics.html">{c["back"]}</a></div>
    </div>
  </form>
</div>
</div>
</main>
<footer class="footer-pro">
  <div class="footer-inner">
    <div class="footer-brand"><h3>{c["footer_name"]}</h3></div>
    <div class="footer-grid">
      <div class="footer-col">
        <h4 class="footer-title">{c["contact"]}</h4>
        <div class="footer-item"><span aria-hidden="true">✉</span> <a href="mailto:info@daab-waas.com">info@daab-waas.com</a></div>
        <div class="footer-item"><span aria-hidden="true">☎</span> <a href="tel:+905551474674">+90 555 147 46 74</a></div>
        <div class="footer-item"><span aria-hidden="true">🌐</span> <a href="https://daab-waas.com" rel="noopener noreferrer" target="_blank">daab-waas.com</a></div>
      </div>
      <div class="footer-col">
        <h4 class="footer-title">{c["address"]}</h4>
        <p class="footer-address">{c["address_html"]}</p>
      </div>
      <div class="footer-col">
        <h4 class="footer-title">{c["leadership"]}</h4>
        <p class="footer-leader">{c["leader"]}</p>
      </div>
    </div>
  </div>
  <div class="footer-bottom"><nav class="footer-legal-links" aria-label="{c["legal_label"]}">{c["legal"]}</nav><div class="footer-copy">{c["copy"]}</div></div>
</footer>
</body>
</html>
'''


def main():
    for lang in ("en", "az"):
        path = ROOT / lang / "complex-topics-apply.html"
        path.write_text(page(lang), encoding="utf-8", newline="\n")
        print(path)


if __name__ == "__main__":
    main()

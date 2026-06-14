"""English string replacements for home page (published from az/index.html)."""

HOME_REPLACEMENTS: list[tuple[str, str]] = [
    (
        "<title>\n      DAAB — Dünya Azərbaycanlı Alimlər Birliyi\n    </title>",
        "<title>WAAS — World Association of Azerbaijani Scientists</title>",
    ),
    (
        'content="Dünya Azərbaycanlı Alimlər Birliyi — xaricdə yaşayan Azərbaycanlı alimləri birləşdirən beynəlxalq elmi platforma."',
        'content="World Association of Azerbaijani Scientists — an international scientific platform uniting Azerbaijani scholars abroad."',
    ),
    ("Məzmuna keç", "Skip to content"),
    ('aria-label="Əsas naviqasiya"', 'aria-label="Main navigation"'),
    ("Menyunu aç", "Open menu"),
    ('aria-label="DAAB ana səhifə"', 'aria-label="WAAS home"'),
    (
        "Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi",
        "World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists",
    ),
    (
        """            Dünya Azərbaycanlı
            <span>
              Alimlər Birliyi
            </span>""",
        """            World Association of
            <span>
              Azerbaijani Scientists
            </span>""",
    ),
    ("Alimlərimizlə tanış olun", "Meet our scientists"),
    ("Birliyimizə üzv olun", "Join our Association"),
    ('aria-label="DAAB qısa məlumat"', 'aria-label="WAAS summary"'),
    (
        """              Beynəlxalq Elmi Şəbəkələşmə və Əməkdaşlıq
            """,
        """              International Scientific Networking and Cooperation
            """,
    ),
    (
        "Dünya Azərbaycanlı Alimlər Birliyi (DAAB) akademik potensialı vahid şəbəkəyə çevirir, universitetlər, tədqiqat mərkəzləri və beynəlxalq tərəfdaşlarla davamlı əlaqələr yaradır.",
        "The World Association of Azerbaijani Scientists (WAAS) connects academic potential into a unified network, building lasting relationships with universities, research centres and international partners.",
    ),
    (
        """            Dünya Azərbaycanlı Alimlər Birliyi ilə tanış olun
          """,
        """            Discover the World Association of Azerbaijani Scientists
          """,
    ),
    (
        "Aşağıdakı kartlar vasitəsilə təşkilatın missiyası, fəaliyyəti, alimlər siyahısı, idarə heyəti, nizamnamə və üzvlük şərtlərinə keçid edə bilərsiniz.",
        "Use the cards below to explore our mission, activities, scientists directory, board of directors, charter and membership terms.",
    ),
    (
        "Aşağıdakı kartlar vasitəsilə təşkilatın missiyası, fəaliyyəti, alimlər kataloqu, idarə heyəti, nizamnamə və üzvlük şərtlərinə keçid edə bilərsiniz.",
        "Use the cards below to explore our mission, activities, scientists directory, board of directors, charter and membership terms.",
    ),
    ('aria-label="Bölmələrdə axtar"', 'aria-label="Search sections"'),
    ('placeholder="Bölmələrdə axtar..."', 'placeholder="Search sections..."'),
    ("Nəticə tapılmadı.", "No results found."),
    ('data-title="Missiya Vizyon Dəyərlər"', 'data-title="Mission Vision Values"'),
    (
        """              Missiya, Vizyon və Dəyərlər
            """,
        """              Mission, Vision and Values
            """,
    ),
    (
        "DAAB elm və texnologiya, energetika, təhsil, səhiyyə, sosial elmlər və mədəniyyət sahələrində strateji təşəbbüslərə dəstək verən beynəlxalq elmi platformadır.",
        "WAAS is an international scientific platform supporting strategic initiatives in science and technology, energy, education, health, social sciences and culture.",
    ),
    ("Tanış olun", "Explore"),
    ('data-title="Fəaliyyətimiz tədbirlər konfranslar"', 'data-title="Activities events conferences"'),
    ("Fəaliyyətimiz", "Our Activities"),
    (
        "DAAB-ın elmi, akademik və mədəni tədbirləri, konfransları, görüşləri və nailiyyətləri.",
        "WAAS's scientific, academic and cultural events, conferences, meetings and achievements.",
    ),
    ("Fəaliyyət", "Activities"),
    ('data-title="Birliyin Təsisi Foundation"', 'data-title="Foundation establishment"'),
    ("Birliyin Təsisi", "Foundation"),
    (
        "DAAB-ın yaradılma zərurəti, Şuşa Qurultayından başlayan təşəbbüs xətti və İstanbul təsis görüşü vahid səhifədə.",
        "Why WAAS was founded, the initiative from the Shusha Congress to the Istanbul founding meeting — on one page.",
    ),
    ("Təsisat", "Foundation"),
    (
        'data-title="Xaricdə Yaşayan Azərbaycanlı Alimlər siyahı"',
        'data-title="Azerbaijani scientists abroad directory"',
    ),
    (
        'data-title="Xaricdə Yaşayan Azərbaycanlı Alimlər kataloq"',
        'data-title="Azerbaijani scientists abroad directory"',
    ),
    ("Xaricdə Yaşayan Azərbaycanlı Alimlər", "Azerbaijani Scientists Abroad"),
    (
        "Dünyanın müxtəlif ölkələrində yaşayan Azərbaycanlı alimlərin sahə, ölkə və institutlara görə təqdim olunan profilləri.",
        "Profiles of Azerbaijani scholars living in countries worldwide, organised by field, country and institution.",
    ),
    ("Siyahı", "Directory"),
    ("Kataloq", "Directory"),
    ('data-title="İdarə Heyəti rəhbərlik"', 'data-title="Executive Board leadership"'),
    ("İdarə Heyəti", "Executive Board"),
    (
        "DAAB rəhbərliyi, idarə heyəti üzvləri, bioqrafiyalar, akademik titullar və əlaqə məlumatları.",
        "WAAS leadership, Executive Board members, biographies, academic titles and contact details.",
    ),
    ("Rəhbərlik", "Leadership"),
    ('data-title="Nizamnamə qaydalar hüquqlar vəzifələr"', 'data-title="Charter rules rights duties"'),
    ("Nizamnamə", "Charter"),
    (
        "Birliyin fəaliyyət qaydaları, hüquqları, vəzifələri və rəsmi nizamnamə müddəaları.",
        "Rules of operation, rights, duties and official charter provisions of the Association.",
    ),
    ('data-title="Üzvlük Şərtləri müraciət proseduru"', 'data-title="Membership application procedure"'),
    ("Üzvlük Şərtləri", "Membership Terms"),
    (
        "DAAB-a üzv olmaq üçün tələblər, üstünlüklər və müraciət proseduru.",
        "Requirements, benefits and application procedure for WAAS membership.",
    ),
    ("Üzvlük", "Membership"),
    (
        """            DAAB-a üzv olmağa hazırsınız?
          """,
        """            Ready to join WAAS?
          """,
    ),
    (
        "Elmi əməkdaşlıq, mentorluq və beynəlxalq akademik əlaqələr üçün DAAB şəbəkəsinə qoşulun.",
        "Join the WAAS network for scientific collaboration, mentoring and international academic connections.",
    ),
    ("Üzvlük şərtləri", "Membership terms"),
    ("Dünya Azərbaycanlı Alimlər Birliyi", "World Association of Azerbaijani Scientists"),
    ("Əlaqə", "Contact"),
    ("Ünvan", "Address"),
    ("Türkiyə", "Türkiye"),
    ("Rəhbərlik", "Leadership"),
    ("DAAB İdarə Heyətinin Sədri", "Chair of the WAAS Executive Board"),
    ("Prof. Dr. Məsud Əfəndiyev", "Prof. Dr. Messoud Efendiyev"),
]

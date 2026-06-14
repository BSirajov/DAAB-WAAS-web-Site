"""English replacements for en/charter.html (hero, meta, UI; articles stay AZ until full translation)."""

CHARTER_REPLACEMENTS: list[tuple[str, str]] = [
    ("<title>DAAB — Nizamnamə</title>", "<title>WAAS — Charter</title>"),
    (
        'content="Dünya Azərbaycanlı Alimlər Birliyinin Azərbaycan dilində nizamnaməsi."',
        'content="Charter of the World Association of Azerbaijani Scientists."',
    ),
    ("Məzmuna keç", "Skip to content"),
    ("Birliyin <span>Nizamnaməsi</span>", 'Association <span>Charter</span>'),
    ('aria-label="Nizamnamə xülasəsi"', 'aria-label="Charter summary"'),
    ("Rəsmi sənəd", "Official document"),
    (
        "Bu səhifədə Dünya Azərbaycanlı Alimlər Birliyinin adı, məqsədi, üzvlük qaydaları, "
        "idarəetmə orqanları, maliyyə prosedurları, filial fəaliyyəti və ləğvetmə qaydalarını "
        "əhatə edən 26 maddədən ibarət nizamnamə təqdim olunur. Nizamnamə birliyin hüquqi "
        "əsaslarını və təşkilati-idarəetmə strukturunu müəyyən edir.",
        "This page presents the 26-article charter covering the name, purpose, membership rules, "
        "governing bodies, financial procedures, branches and dissolution of the World Association "
        "of Azerbaijani Scientists. The charter defines the Association's legal basis and governance structure.",
    ),
    ("Maddələr", "Articles"),
    ("Dünya Azərbaycanlı Alimlər Birliyi", "World Association of Azerbaijani Scientists"),
    ("Əlaqə", "Contact"),
    ("Ünvan", "Address"),
    ("Türkiyə", "Türkiye"),
    ("Rəhbərlik", "Leadership"),
    ("DAAB İdarə Heyətinin Sədri", "Chair of the WAAS Executive Board"),
    ("Axtarış", "Search"),
    ("Axtarış üçün yazmağa başlayın…", "Start typing to search…"),
    ("Axtarmaq üçün yuxarıdakı xanaya mətn daxil edin", "Enter text in the box above to search"),
    ("naviqasiya", "navigate"),
    ("aç", "open"),
    ("bağla", "close"),
    ("Menyunu aç", "Open menu"),
    ("Əsas naviqasiya", "Main navigation"),
]

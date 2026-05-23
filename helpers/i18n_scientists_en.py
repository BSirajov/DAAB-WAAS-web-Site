"""English UI replacements for en/scientists/list.html and profiles.html."""

SCIENTISTS_COMMON_REPLACEMENTS: list[tuple[str, str]] = [
    ("Məzmuna keç", "Skip to content"),
    (
        "<title>DAAB — Xaricdə Yaşayan Azərbaycanlı Alimlər</title>",
        "<title>WAAS — Azerbaijani Scientists Abroad</title>",
    ),
    (
        'content="Xaricdə yaşayan Azərbaycanlı alimlərin DAAB siyahısı."',
        'content="Directory of Azerbaijani scientists abroad — World Association of Azerbaijani Scientists."',
    ),
    (
        'content="Xaricdə yaşayan Azərbaycanlı alimlərin DAAB kataloqu."',
        'content="Directory of Azerbaijani scientists abroad — World Association of Azerbaijani Scientists."',
    ),
    (
        "<title>DAAB — Xaricdə Yaşayan Azərbaycanlı Alimlər CV Kataloqu</title>",
        "<title>WAAS — Academic Profiles Catalogue</title>",
    ),
    (
        'content="Xaricdə yaşayan Azərbaycanlı alimlərin DAAB CV kataloqu."',
        'content="Academic profiles of Azerbaijani scientists abroad — World Association of Azerbaijani Scientists."',
    ),
    ("Xaricdə Yaşayan<br><em>Azərbaycanlı Alimlər</em>", "Azerbaijani Scientists<br><em>Living Abroad</em>"),
    ("Xaricdə Yaşayan<br><em>Azərbaycanlı Alimlər</em>", "Azerbaijani Scientists<br><em>Living Abroad</em>"),
    ('aria-label="Alimlər siyahısı haqqında qısa məlumat"', 'aria-label="Scientists directory summary"'),
    ('aria-label="Alimlər kataloqu haqqında qısa məlumat"', 'aria-label="Scientists directory summary"'),
    ('aria-label="Alimlər CV kataloqu haqqında qısa məlumat"', 'aria-label="Academic profiles summary"'),
    ("Alimlərimizin siyahısı", "Scientists directory"),
    (
        "Siyahıda 2024-cü ilin 9–11 sentyabr tarixlərində Bakıda keçirilmiş forumda iştirak etmiş alimlər təqdim olunur. "
        "Siyahı alimlərin ölkə, ixtisas, elmi dərəcə və digər meyarlar üzrə axtarışı və filtrlənməsi imkanını təmin edir.",
        "The directory lists scientists who took part in the Baku forum of 9–11 September 2024. "
        "You can search and filter by country, field, academic degree and other criteria.",
    ),
    ("Alimlərimizin akademik profilləri", "Academic profiles"),
    (
        "Bu səhifə dünyanın müxtəlif ölkələrində elm, texnologiya, tibb, incəsənət və humanitar sahələrdə "
        "fəaliyyət göstərən azərbaycanlı alimlərin akademik profillərini təqdim edir və alimlərin ölkə, "
        "ixtisas, elmi dərəcə və digər akademik meyarlar üzrə axtarışı, sıralanması və filtrlənməsi imkanını verir.",
        "This page presents academic profiles of Azerbaijani scholars active worldwide in science, technology, "
        "medicine, arts and humanities, with search, sort and filter by country, field, degree and more.",
    ),
    ("Alimlərimizin akademik profilləri", "Our scientists' academic profiles"),
    ("Alimlərimizin siyahısı", "Scientists directory"),
    ("Axtarış üçün yazmağa başlayın…", "Start typing to search…"),
    ("Axtarmaq üçün yuxarıdakı xanaya mətn daxil edin", "Enter text in the box above to search"),
    ("naviqasiya", "navigate"),
    ("aç", "open"),
    ("bağla", "close"),
    ("Ad, ölkə, ixtisas, elmi dərəcə, e-poçt…", "Name, country, field, degree, email…"),
    ("🌍 Ölkə", "🌍 Country"),
    ("📚 İxtisas", "📚 Field"),
    ("🎓 Elmi dərəcə", "🎓 Degree"),
    ("Filtri sil", "Clear filter"),
    ("Hamısını sıfırla", "Reset all"),
    ("Səhifədə sətir", "Rows per page"),
    ('aria-label="Cədvəldə göstərilən sətirlərin sayı"', 'aria-label="Rows shown in the table"'),
    ("Hamısı", "All"),
    ("Ad, Soyadı", "Name"),
    ("Yaşadığı Ölkə", "Country of residence"),
    ("İxtisası", "Field"),
    ("Elmi<br/>Dərəcəsi", "Academic<br/>degree"),
    ("E-poçt", "Email"),
    ("Heç bir nəticə tapılmadı. Filtri sıfırlayın.", "No results found. Reset your filters."),
    (" nəticə", " results"),
    (" ümumi)", " total)"),
    ('aria-label="Alimlər filtri"', 'aria-label="Scientists filters"'),
    ('aria-label="Alim axtar"', 'aria-label="Search scientists"'),
    ("Ölkə filtri", "Country filter"),
    ("İxtisas filtri", "Field filter"),
    ("Elmi dərəcə filtri", "Degree filter"),
    ("Sıralama", "Sort"),
    ("Sırala", "Sort by"),
    ("Ad, Soyad", "Name"),
    ("Ölkə", "Country"),
    ("İxtisas", "Field"),
    ("Elmi dərəcə", "Degree"),
    ("Sıralama istiqaməti", "Sort direction"),
    ("Artan (A→Z)", "Ascending (A→Z)"),
    ("Azalan (Z→A)", "Descending (Z→A)"),
    ("Dünya Azərbaycanlı Alimlər Birliyi", "World Association of Azerbaijani Scientists"),
    ("Əlaqə", "Contact"),
    ("Ünvan", "Address"),
    ("Rəhbərlik", "Leadership"),
    ("DAAB İdarə Heyətinin Sədri", "Chair of the WAAS Executive Board"),
    ("Axtarış", "Search"),
    ("Menyunu aç", "Open menu"),
    ("Əsas naviqasiya", "Main navigation"),
]

SCIENTISTS_LIST_REPLACEMENTS = SCIENTISTS_COMMON_REPLACEMENTS

SCIENTISTS_PROFILES_REPLACEMENTS = SCIENTISTS_COMMON_REPLACEMENTS + [
    (
        "Heç bir profil tapılmadı. Filtri sıfırlayın.",
        "No profiles found. Reset your filters.",
    ),
]

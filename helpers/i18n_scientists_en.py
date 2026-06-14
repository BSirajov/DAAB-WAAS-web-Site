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
        "Burada dünyanın müxtəlif ölkələrində yaşayıb çalışan, 2024-cü ilin sentyabrında Bakıda keçirilmiş Xaricdə yaşayan Azərbaycanlı Alimlərin I Forumunda iştirak etmiş alimlərimizin adları, yaşadıqları ölkələr, ixtisas sahələri və elmi fəaliyyətləri ilə tanış ola bilərsiniz.",
        "Meet Azerbaijani scholars from across the world who took part in the First Forum of Azerbaijani Scientists Living Abroad in Baku in September 2024 — their names, countries of residence, fields of study and scientific work brought together in one directory.",
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
    ("🌍 Yaşadığı Ölkə", "🌍 Country of residence"),
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
    ("İxtisas", "Field"),
    ("Elmi<br/>Dərəcə", "Academic<br/>degree"),
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
    ("Ölkə", "Country of residence"),
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
    ("Filtrlər", "Filters"),
]

SCIENTISTS_LIST_REPLACEMENTS = SCIENTISTS_COMMON_REPLACEMENTS

SCIENTISTS_PROFILES_REPLACEMENTS = SCIENTISTS_COMMON_REPLACEMENTS + [
    (
        "Heç bir profil tapılmadı. Filtri sıfırlayın.",
        "No profiles found. Reset your filters.",
    ),
]

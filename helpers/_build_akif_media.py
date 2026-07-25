#!/usr/bin/env python3
"""Build Akif Alaferdov books page (AZ/EN) — three covers with PDF links.

    python helpers/_build_akif_media.py

Writes:
    az/scientists/akif-alaferdov-media.html
    en/scientists/akif-alaferdov-media.html
Cover display thumbs:
    az/scientists/akif-alaferdov-media-thumbnails/001.jpg … 003.jpg
PDF/book assets remain in Books/Akif_Alaferdov/.
"""
from __future__ import annotations

from pathlib import Path
from urllib.parse import quote

from PIL import Image, ImageOps

from _paths import ROOT
from _scientist_media import esc, write_pages

BOOKS_DIR = ROOT / "Books" / "Akif_Alaferdov"
THUMB_DIR = ROOT / "az" / "scientists" / "akif-alaferdov-media-thumbnails"
THUMB_MAX_EDGE = 720
BOOKS_WEB = "../../Books/Akif_Alaferdov"

# Matched by shared numeric prefix (001 / 002 / 003).
BOOKS = [
    {
        "id": "001",
        "az": "Repressiyaya məruz qalan Qırğızıstan azərbaycanlıları",
        "en": "Repressed Azerbaijanis of Kyrgyzstan",
        "lang_note_az": "Azərbaycanca",
        "lang_note_en": "Azerbaijani",
    },
    {
        "id": "002",
        "az": "Репрессированные Азербайджанцы Кыргызыстана",
        "en": "Repressed Azerbaijanis of Kyrgyzstan",
        "lang_note_az": "Rusca",
        "lang_note_en": "Russian",
    },
    {
        "id": "003",
        "az": "Репрессированные народы Кыргызыстана",
        "en": "Repressed peoples of Kyrgyzstan",
        "lang_note_az": "Rusca",
        "lang_note_en": "Russian",
    },
]

STRINGS = {
    "az": {
        "lang": "az",
        "locale": "az_AZ",
        "skip": "Məzmuna keç",
        "nav_home_title": "Ana səhifə",
        "nav_home_aria": "DAAB ana səhifə",
        "brand": "Dünya Azərbaycanlı<br class=\"mobile-hidden-break\">Alimlər Birliyi",
        "brand_menu_aria": "Əsas naviqasiya",
        "menu_open": "Menyunu aç",
        "crumb_home": "Ana səhifə",
        "crumb_scientists": "Alimlərimiz",
        "crumb_current": "Akif Alaferdov — Kitablar",
        "crumb_aria": "Səhifə yolu",
        "title": "Akif Alaferdov — Kitablar | DAAB",
        "meta_desc": "Dr. Akif Alaferdovun Qırğızıstan azərbaycanlılarına və repressiya olunmuş xalqlara dair kitabları və foto toplusu.",
        "h1": "Akif Alaferdov",
        "h1_em": "Kitablar",
        "subtitle": (
            "«Repressiyaya məruz qalan Qırğızıstan azərbaycanlıları kitabında» ilk dəfə olaraq "
            "Qırğızıstan Respublikası Milli Təhlükəsizlik Komitəsinin dəstəyi ilə idarə arxiv "
            "fondlarından repressiyaya məruz qalmış azərbaycanlılar haqqında yeni arxiv materialları "
            "dərc olunmuşdur."
        ),
        "subtitle": "Kitablar və foto toplusu",
        "panel_title": "Kitablar",
        "panel_copy": "Akif Alaferdovun kitabları və foto toplusu.",
        "hero_html": (
            '<div class="hero-inner shell akif-hero">'
            '<section class="akif-hero__title">'
            "<h1>Akif Alaferdov<br><em>Kitablar</em></h1>"
            "</section>"
            '<div class="akif-hero__blurbs" id="page-hero-subtitle" role="doc-subtitle">'
            '<article class="akif-blurb">'
            '<h2 class="akif-blurb__title">Repressiyaya məruz qalan Qırğızıstan azərbaycanlıları</h2>'
            "<p>«Repressiyaya məruz qalan Qırğızıstan azərbaycanlıları» kitabında ilk dəfə olaraq "
            "Qırğızıstan Respublikası Milli Təhlükəsizlik Komitəsinin dəstəyi ilə idarə arxiv "
            "fondlarından repressiyaya məruz qalmış azərbaycanlılar haqqında yeni arxiv materialları "
            "dərc olunmuşdur.</p>"
            "<p>Kitabda repressiyaların səbəbləri, repressiyaya məruz qalan bir azərbaycanlı "
            "ailəsinin acı taleyi, qırğız və Azərbaycan xalqlarının dostluq və qardaşlığı, "
            "1920-1950-ci illərin əvvəlinə qədər Stalinizm avtoritarizmi dövründə, eləcə də "
            "ictimai-siyasi böhranlar içərisində şərəflə qorunan qarşılıqlı yardımlardan bəhs "
            "edilir.</p>"
            "<p>Kitab məktəbli və tələbələr, müəllim və tədqiqatçılar, elmi mütəxəssislər və "
            "siyasi tarixlə maraqlanan geniş oxucu kütləsi üçün nəzərdə tutulmuşdur.</p>"
            "</article>"
            '<article class="akif-blurb">'
            '<h2 class="akif-blurb__title">Репрессированные народы Кыргызыстана</h2>'
            "<p>«Репрессированные народы Кыргызыстана» kitabı kütləvi stalinist repressiyalar "
            "dövründə sovet xalqlarının yaşadığı faciənin tədqiqinə həsr olunmuşdur; o dövrdə "
            "siyasi təqiblərə və deportasiyalara məruz qalan on minlərlə vətəndaş bu gün "
            "Qırğızıstanın çoxmillətli xalqını təşkil edir. Bu ümuminsani faciənin tam "
            "mənzərəsini əldə etmək üçün əsərdə dünyada insanların mənşəyinə, dini etiqadına "
            "və siyasi baxışlarına görə kütləvi təqibinin çoxsaylı nümunələri gətirilir.</p>"
            "<p>Kitab siyasi tarixlə maraqlanan geniş oxucu dairəsi — məktəblilər, tələbələr, "
            "aspirantlar, müəllimlər, müəllim heyəti, alimlər və siyasətçilər üçün nəzərdə "
            "tutulmuşdur.</p>"
            "</article>"
            "</div>"
            "</div>"
        ),
        "sec1": "Kitablar",
        "count_one": "kitab",
        "link_book": "Kitabı aç (PDF)",
        "link_photos": "Foto toplusu (PDF)",
        "cover_alt_prefix": "Kitab üz qabığı:",
        "footer_org": "Dünya Azərbaycanlı Alimlər Birliyi",
        "footer_contact": "Əlaqə",
        "footer_addr": "Ünvan",
        "footer_lead_h": "Rəhbərlik",
        "footer_addr_body": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiyə",
        "footer_lead_body": "<strong>Prof. Dr. Məsud Əfəndiyev</strong><br/>DAAB İdarə Heyətinin Sədri<br/>Almaniya — James D. Murray mükafatlı professoru",
        "footer_rights": "© 2026 DAAB — Bütün hüquqlar qorunur",
        # unused by custom section but required by shared shell strings
        "tag_video": "Video",
        "tag_article": "Məqalə",
        "go_video": "İzlə",
        "go_article": "Aç",
    },
    "en": {
        "lang": "en",
        "locale": "en_US",
        "skip": "Skip to content",
        "nav_home_title": "Home",
        "nav_home_aria": "WAAS home",
        "brand": "World Association of<br class=\"mobile-hidden-break\">Azerbaijani Scientists",
        "brand_menu_aria": "Primary navigation",
        "menu_open": "Open menu",
        "crumb_home": "Home",
        "crumb_scientists": "Scientists",
        "crumb_current": "Akif Alaferdov — Books",
        "crumb_aria": "Breadcrumb",
        "title": "Akif Alaferdov — Books | WAAS",
        "meta_desc": "Books and photo collections by Dr. Akif Alaferdov on repressed Azerbaijanis and peoples of Kyrgyzstan.",
        "h1": "Akif Alaferdov",
        "h1_em": "Books",
        "subtitle": (
            "For the first time, the book “Repressed Azerbaijanis of Kyrgyzstan” publishes new "
            "archival materials on repressed Azerbaijanis from the administrative archive funds, "
            "with the support of the State Committee for National Security of the Kyrgyz Republic."
        ),
        "subtitle": "Books and photo collections",
        "panel_title": "Books",
        "panel_copy": "Books and photo collections by Dr. Akif Alaferdov.",
        "hero_html": (
            '<div class="hero-inner shell akif-hero">'
            '<section class="akif-hero__title">'
            "<h1>Akif Alaferdov<br><em>Books</em></h1>"
            "</section>"
            '<div class="akif-hero__blurbs" id="page-hero-subtitle" role="doc-subtitle">'
            '<article class="akif-blurb">'
            '<h2 class="akif-blurb__title">Repressed Azerbaijanis of Kyrgyzstan</h2>'
            "<p>For the first time, the book “Repressed Azerbaijanis of Kyrgyzstan” publishes new "
            "archival materials on repressed Azerbaijanis from the administrative archive funds, "
            "with the support of the State Committee for National Security of the Kyrgyz Republic.</p>"
            "<p>The book discusses the causes of the repressions, the bitter fate of one repressed "
            "Azerbaijani family, the friendship and brotherhood of the Kyrgyz and Azerbaijani "
            "peoples, and the mutual assistance that was honourably preserved during the Stalinist "
            "authoritarian period up to the early 1920s–1950s, as well as amid socio-political "
            "crises.</p>"
            "<p>The book is intended for school and university students, teachers and researchers, "
            "academic specialists, and a wider readership interested in political history.</p>"
            "</article>"
            '<article class="akif-blurb">'
            '<h2 class="akif-blurb__title">Repressed peoples of Kyrgyzstan</h2>'
            "<p>The book “Repressed peoples of Kyrgyzstan” is devoted to researching the tragedy "
            "suffered by Soviet peoples during the mass Stalinist repressions, when tens of "
            "thousands of citizens — who today form the multinational people of Kyrgyzstan — were "
            "subjected to political persecution and deportation. To present a full picture of this "
            "universal human tragedy, the work gives numerous examples of mass persecution "
            "worldwide on grounds of origin, religion, and political views.</p>"
            "<p>It is intended for a wide readership: school pupils, students, postgraduate "
            "researchers, teachers, lecturers, scholars, and politicians interested in political "
            "history.</p>"
            "</article>"
            "</div>"
            "</div>"
        ),
        "sec1": "Books",
        "count_one": "books",
        "link_book": "Open book (PDF)",
        "link_photos": "Photo collection (PDF)",
        "cover_alt_prefix": "Book cover:",
        "footer_org": "World Association of Azerbaijani Scientists",
        "footer_contact": "Contact",
        "footer_addr": "Address",
        "footer_lead_h": "Leadership",
        "footer_addr_body": "Feneryolu Mahallesi<br/>Gazi Muhtar Paşa Sokak No:44<br/>Kadıköy, İstanbul, Türkiye",
        "footer_lead_body": "<strong>Prof. Dr. Messoud Efendiev</strong><br/>Chair of the WAAS Executive Board<br/>Germany — James D. Murray Distinguished Professor",
        "footer_rights": "© 2026 WAAS — All rights reserved",
        "tag_video": "Video",
        "tag_article": "Article",
        "go_video": "Watch",
        "go_article": "Open",
    },
}


def _find(prefix: str, suffix: str) -> Path:
    matches = sorted(BOOKS_DIR.glob(f"{prefix}*{suffix}"))
    if not matches:
        raise FileNotFoundError(f"Missing {prefix}*{suffix} in {BOOKS_DIR}")
    return matches[0]


def resolve_book_files() -> list[dict]:
    out = []
    for book in BOOKS:
        bid = book["id"]
        cover = _find(f"{bid}-1_", ".png")
        pdf = _find(f"{bid}-2_", ".pdf")
        photos = _find(f"{bid}-3_", ".pdf")
        out.append({**book, "cover": cover, "pdf": pdf, "photos": photos})
    return out


def make_cover_thumbs(books: list[dict]) -> None:
    THUMB_DIR.mkdir(parents=True, exist_ok=True)
    for book in books:
        dest = THUMB_DIR / f"{book['id']}.jpg"
        with ImageOps.exif_transpose(Image.open(book["cover"])) as im:
            im = im.convert("RGB")
            im.thumbnail((THUMB_MAX_EDGE, THUMB_MAX_EDGE), Image.Resampling.LANCZOS)
            im.save(dest, "JPEG", quality=85, optimize=True, progressive=True)
        print(f"  thumb {dest.relative_to(ROOT)} ({dest.stat().st_size // 1024} KB)")


def books_href(filename: str) -> str:
    return f"{BOOKS_WEB}/{quote(filename)}"


def books_section_html(lang: str, books: list[dict]) -> str:
    s = STRINGS[lang]
    cards = []
    for book in books:
        title = book[lang]
        note = book[f"lang_note_{lang}"]
        thumb_src = (
            f"akif-alaferdov-media-thumbnails/{book['id']}.jpg"
            if lang == "az"
            else f"../../az/scientists/akif-alaferdov-media-thumbnails/{book['id']}.jpg"
        )
        pdf_href = books_href(book["pdf"].name)
        photos_href = books_href(book["photos"].name)
        alt = f"{s['cover_alt_prefix']} {title}"
        cards.append(
            '<article class="book-card">'
            f'<figure class="book-card__cover">'
            f'<img src="{esc(thumb_src)}" alt="{esc(alt)}" loading="lazy" decoding="async"/>'
            "</figure>"
            f'<h3 class="book-card__title">{esc(title)}</h3>'
            f'<p class="book-card__note">{esc(note)}</p>'
            '<div class="book-card__links">'
            f'<a class="book-card__link" href="{esc(pdf_href)}" target="_blank" rel="noopener noreferrer">{esc(s["link_book"])}</a>'
            f'<a class="book-card__link" href="{esc(photos_href)}" target="_blank" rel="noopener noreferrer">{esc(s["link_photos"])}</a>'
            "</div>"
            "</article>"
        )
    return (
        f'<section class="media-section" aria-label="{esc(s["sec1"])}">'
        f'<div class="books-grid">\n{"".join(cards)}\n</div>'
        "</section>"
    )


def main() -> int:
    if not BOOKS_DIR.is_dir():
        raise SystemExit(f"Missing books folder: {BOOKS_DIR}")
    books = resolve_book_files()
    print(f"Resolved {len(books)} book set(s) in {BOOKS_DIR.relative_to(ROOT)}")
    make_cover_thumbs(books)
    cfg = {
        "page_id": "akif-media",
        "slug": "akif-alaferdov-media",
        "thumb_dirname": "akif-alaferdov-media-thumbnails",
        "thumbs": [],
        "resources": [],
        "strings": STRINGS,
        "sections_html": {
            "az": books_section_html("az", books),
            "en": books_section_html("en", books),
        },
    }
    return write_pages(cfg)


if __name__ == "__main__":
    raise SystemExit(main())

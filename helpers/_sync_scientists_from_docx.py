"""Sync scientist cards from Forum book DOCX (chapter: Xaricdə yaşayan alimlər)."""
from __future__ import annotations

import html
import re
import unicodedata

from _paths import ROOT
from _sync_scientists_from_book import (
    COUNTRY_HEADERS,
    HTML_PATH,
    extract_all_cards,
    is_awards_heading_line,
    is_chapter_name_line,
    is_section_heading_line,
    normalize_ws,
    replace_card_bio,
)

EXTRACT = ROOT / "_docx_extract.txt"
CHAPTER_TITLE = "XARİCDƏ YAŞAYAN AZƏRBAYCANLI ALİMLƏR"
CHAPTER_END_MARKERS = ("FORUM HAQQINDA TƏƏSSÜRATLAR",)


def extract_name(name_line: str) -> str:
    return re.sub(
        r",\s*(?:PhD|Ph\.D\.|Prof\. Dr\.|Ed\.D\.|Dr\.|Dosent|Dr\.-İng\.).*$",
        "",
        name_line,
    ).strip()


def normalize_person_key(name: str) -> str:
    """Match HTML card names to DOCX profile names."""
    name = unicodedata.normalize("NFKC", name)
    name = "".join(
        c
        for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )
    name = re.sub(r"\s*\(MEHDİYEV\)", "", name, flags=re.I)
    name = re.sub(r"\s+Dosent$", "", name, flags=re.I)
    name = re.sub(r"[^A-Za-zƏəÜüÖöĞğŞşİıIıÇç\s]", " ", name)
    return " ".join(name.casefold().split())


ALIASES = {
    "cəmilə cavadova spitzberg": "cəmilə cavadova spitzberq",
    "mehdi ismayilov gəncəli": "mehdi gəncəli ismayilov",
    "qafar mehdiyev caxmaxci": "qafar caxmaqli",
    "qafar çaxmaqlı mehdiyev": "qafar caxmaqli",
    "əbulfəz suleymanov": "əbulfəz suleymanli",
    "əbülfəz süleymanli": "əbulfəz suleymanli",
    "lev eppelbaum": "lev v eppelbaum",
    "mark vilen applebaum": "mark applebaum",
    "riza moridi": "reza moridi",
    "agamali məmmədov": "agamalı məmmədov",
    "ağamalı məmmədov": "agamalı məmmədov",
    "ismayil əliyev": "ismayıl əliyev",
    "afina barmanbay": "afina məmmədli barmanbay",
    "əmirullah məhmədov": "əmirulla məmmədov",
    "haciəli nəcəfoglu": "hacalı nəcəfoglu",
    "ilkin gulusoy": "ilkin qulusoy",
    "makbulə sabziyeva": "məqbulə səbziyeva",
}


def person_key(name: str) -> str:
    key = normalize_person_key(name)
    return ALIASES.get(key, key)


def card_person_key(card_html: str) -> str:
    m = re.search(r'<span class="card-name">([^<]+)', card_html)
    if m:
        return person_key(m.group(1))
    m = re.search(r'data-search="([^"]+)"', card_html)
    if m:
        tokens = m.group(1).split()
        return person_key(" ".join(tokens[:2]))
    return ""


def index_profiles(profiles: list[dict]) -> dict[str, dict]:
    indexed: dict[str, dict] = {}
    for profile in profiles:
        indexed[person_key(profile["name"])] = profile
    return indexed


def is_country_header(line: str) -> bool:
    return line in COUNTRY_HEADERS or line.upper() in COUNTRY_HEADERS


def is_chapter_end(line: str) -> bool:
    return any(line.startswith(m) for m in CHAPTER_END_MARKERS)


def extract_chapter_lines() -> list[str]:
    lines = EXTRACT.read_text(encoding="utf-8").splitlines()
    start = next(
        i for i, line in enumerate(lines) if line.strip() == CHAPTER_TITLE
    )
    return [normalize_ws(line) for line in lines[start:] if line.strip()]


def parse_profiles_from_docx(chapter: list[str]) -> list[dict]:
    profiles: list[dict] = []
    i = 1  # skip chapter title line
    while i < len(chapter):
        line = chapter[i]
        if is_country_header(line) or is_chapter_end(line):
            if is_chapter_end(line):
                break
            i += 1
            continue
        if not is_chapter_name_line(line):
            i += 1
            continue

        name = extract_name(line)
        i += 1
        paras: list[str] = []
        while i < len(chapter):
            ln = chapter[i]
            if is_country_header(ln) or is_chapter_name_line(ln) or is_chapter_end(ln):
                break
            paras.append(ln)
            i += 1

        summary = paras[0] if paras else ""
        body = paras[1:] if len(paras) > 1 else []
        profiles.append(
            {
                "name": name,
                "summary_paragraph": summary,
                "body_paragraphs": body,
            }
        )
    return profiles


def build_bio_html_docx(body_paragraphs: list[str]) -> str:
    """One DOCX paragraph → one HTML block; awards grouped under award headings."""
    if not body_paragraphs:
        return '<div class="card-bio"><p class="bio">Məlumat mövcud deyil.</p></div>'

    parts: list[str] = []
    first_bio = True
    idx = 0
    n = len(body_paragraphs)

    while idx < n:
        ln = normalize_ws(body_paragraphs[idx])
        if not ln:
            idx += 1
            continue

        if is_section_heading_line(ln):
            parts.append(
                f'<p class="bio-section-title">{html.escape(ln)}</p>'
            )
            if is_awards_heading_line(ln):
                idx += 1
                award_items: list[str] = []
                while idx < n:
                    nxt = normalize_ws(body_paragraphs[idx])
                    if is_section_heading_line(nxt):
                        break
                    award_items.append(nxt)
                    idx += 1
                if award_items:
                    items = "".join(
                        f"<li>{html.escape(item)}</li>" for item in award_items
                    )
                    parts.append(
                        f'<div class="awards-block"><ul class="awards-list">{items}</ul></div>'
                    )
                continue
            idx += 1
            continue

        cls = "bio bio-lead" if first_bio else "bio"
        parts.append(f'<p class="{cls}">{html.escape(ln)}</p>')
        first_bio = False
        idx += 1

    inner = "".join(parts)
    return f"<div class=\"card-bio\">{inner}</div>"


def update_card_from_docx(card_html: str, profile: dict) -> str:
    summary = normalize_ws(profile["summary_paragraph"])
    bio_html = build_bio_html_docx(profile["body_paragraphs"])

    if summary:
        card_html = re.sub(
            r'<p class="card-title">[\s\S]*?</p>',
            f'<p class="card-title">{html.escape(summary)}</p>',
            card_html,
            count=1,
        )
    card_html = re.sub(r'\s*<p class="card-org">[\s\S]*?</p>', "", card_html, count=1)
    return replace_card_bio(card_html, bio_html)


def main() -> None:
    chapter = extract_chapter_lines()
    profiles = parse_profiles_from_docx(chapter)
    print(f"Profiles parsed from DOCX: {len(profiles)}")

    html_text = HTML_PATH.read_text(encoding="utf-8")
    cards = extract_all_cards(html_text)
    if len(cards) != 83:
        raise SystemExit(f"Expected 83 cards, found {len(cards)}")
    if len(profiles) != 83:
        raise SystemExit(f"Expected 83 profiles, found {len(profiles)}")

    by_key = index_profiles(profiles)
    unmatched: list[str] = []
    new_cards: list[str] = []
    for card in cards:
        key = card_person_key(card)
        profile = by_key.get(key)
        if not profile:
            unmatched.append(key or "(unknown)")
            new_cards.append(card)
            continue
        new_cards.append(update_card_from_docx(card, profile))

    if unmatched:
        raise SystemExit(
            "Could not match DOCX profiles for: " + ", ".join(unmatched)
        )

    new_html = html_text
    for old, new in zip(cards, new_cards):
        new_html = new_html.replace(old, new, 1)

    HTML_PATH.write_text(new_html, encoding="utf-8")
    print("All 83 cards updated from DOCX (summary → card-title, body → card-bio).")


if __name__ == "__main__":
    main()

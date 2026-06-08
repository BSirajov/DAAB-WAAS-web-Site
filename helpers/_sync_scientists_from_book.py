"""Sync az/scientists/profiles.html cards with verbatim text from the book chapter."""
from __future__ import annotations

import html
import re
from pathlib import Path

from _paths import ROOT, AZ_SCIENTISTS_PROFILES

EXTRACT = ROOT / "_pdf_extract.txt"
HTML_PATH = AZ_SCIENTISTS_PROFILES

CHAPTER_START = (
    "XARİCDƏ YAŞAYAN  \nAZƏRBAYCANLI ALİMLƏR\nAMERİKA BİRLƏŞMİŞ ŞTATLARI"
)
CHAPTER_END = "FORUM HAQQINDA TƏƏSSÜRATLAR"

COUNTRY_HEADERS = {
    "AMERİKA BİRLƏŞMİŞ ŞTATLARI",
    "ALMANİYA",
    "AVSTRİYA",
    "BİRLƏŞMİŞ KRALLIQ",
    "CƏNUBİ KOREYA",
    "ESTONİYA",
    "FRANSA",
    "GÜRCÜSTAN",
    "İSRAİL",
    "İSVEÇ",
    "İTALİYA",
    "KANADA",
    "MEKSİKA",
    "MİSİR ƏRƏB RESPUBLİKASI",
    "OMAN",
    "POLŞA",
    "QAZAXISTAN",
    "QIRĞIZISTAN",
    "RUSİYA FEDERASİYASI",
    "SƏUDİYYƏ ƏRƏBİSTANI",
    "TÜRKİYƏ",
    "UKRAYNA",
    "YAPONİYA",
}

SKIP_LINE = re.compile(
    r"^(--- PAGE|\d+ \d+$|XARİCDƏ YAŞAYAN|FORUMU 9|1 CeMOS)",
    re.I,
)

BULLET_START = re.compile(r"^[\uf09f\uf0b7\u2022•▪]\s*")


def normalize_ws(line: str) -> str:
    """Collapse PDF/DOCX whitespace only; do not change wording."""
    line = line.strip().replace("\xa0", " ")
    line = re.sub(r"[ \t]+", " ", line)
    return line.replace("V .", "V.")


def dehyphenate(text: str) -> str:
    """Join words split across PDF line breaks (syllable continuations)."""
    text = re.sub(
        r"([A-Za-zƏəÜüÖöĞğŞşİıÇç]) -\s+([a-zəüöğışç])",
        r"\1\2",
        text,
    )
    text = re.sub(
        r" ([a-zəüöğışç]+) -\s+([a-zəüöğışç]+)",
        r" \1\2",
        text,
    )
    text = re.sub(r" -\s+([a-zəüöğışç]{2,6})([\s.,;:!?]|$)", r"-\1\2", text)
    text = re.sub(r"-\s+([a-zəüöğışç])", r"\1", text)
    text = re.sub(r"-\s+", "", text)
    text = re.sub(
        r"([a-zəüöğışç]{2,})-\s+([a-zəüöğışç]{2,})",
        r"\1\2",
        text,
    )
    text = re.sub(
        r"([A-Za-zƏəÜüÖöĞğŞşİıÇç]{2,})-\s+([a-zəüöğışç]{2,})",
        r"\1\2",
        text,
    )
    text = re.sub(
        r"([A-Za-zƏəÜüÖöĞğŞşİıÇça-zəüöğışç]{2,})-([a-zəüöğışç]{2,8})(?=[\s.,;:!?]|$)",
        r"\1\2",
        text,
    )
    return text


def join_verbatim(lines: list[str]) -> str:
    chunks: list[str] = []
    for raw in lines:
        part = normalize_ws(raw)
        if not part:
            continue
        if chunks and chunks[-1].endswith("-"):
            chunks[-1] = chunks[-1] + part
        else:
            chunks.append(part)
    return dehyphenate(" ".join(chunks))


BIO_START_RE = re.compile(
    r"(mütəxəssisdir|mütəxəssisi|professorudur|professordur|üzvüdür|idir\.|olub\.|"
    r"göstərir\.|etmişdir\.|alır\.|seçilmişdir\.)",
    re.I,
)


def looks_like_bio_start(line: str, name: str) -> bool:
    if BIO_START_RE.search(line):
        return True
    parts = name.split()
    if parts and line.casefold().startswith(parts[0].casefold()):
        return True
    if len(parts) >= 2:
        prefix = f"{parts[0]} {parts[1]}".casefold()[:24]
        if line.casefold().startswith(prefix):
            return True
    return False


HEADER_BIO_RE = re.compile(
    r"(məzunu|təhsil al|tamamlamış|işləyir|çalışır|aparmış|göstərir|seçilmiş|alıb|"
    r"olan\s+\d|ildən)",
    re.I,
)


def is_header_candidate(line: str, name: str) -> bool:
    if not line or len(line) > 110:
        return False
    if BULLET_START.match(line) or re.match(r"^Mükafat", line):
        return False
    if re.match(r"^\d{4}", line):
        return False
    if looks_like_bio_start(line, name):
        return False
    if HEADER_BIO_RE.search(line):
        return False
    return True


def is_chapter_name_line(line: str) -> bool:
    if not line or len(line) > 95:
        return False
    if line in COUNTRY_HEADERS or line.startswith("XARİCDƏ"):
        return False
    if "." * 10 in line:
        return False
    if "redaktor" in line.casefold() or "M.D." in line:
        return False
    if line in ("AZƏRBAYCANLI ALİMLƏR",):
        return False
    if line[0].islower():
        return False

    name_part = re.split(
        r",\s*(?:PhD|Ph\.D\.|Prof\. Dr\.|Ed\.D\.|Dr\.|Dosent, PhD|Dosent, Dr\.|Dr\.-İng\.)",
        line,
    )[0].strip()
    name_part = re.sub(r"\s+Dosent$", "", name_part)
    if len(name_part.split()) > 6:
        return False
    if not re.search(r"[A-ZƏÜÖĞŞİÇ]{2,}", name_part):
        return False

    if re.match(
        r"^[A-Za-zƏəÜüÖöĞğŞşİıÇç][A-Za-zƏəÜüÖöĞğŞşİıÇç'’.-]+ "
        r"(?:[A-ZƏÜÖĞŞİÇ][A-ZƏÜÖĞŞİÇA-ZƏÜÖĞŞİÇ\s().-]+|ABDULLAYEV)$",
        name_part,
    ):
        return True

    if re.search(
        r",\s*(?:PhD|Ph\.D\.|Prof\. Dr\.|Ed\.D\.|Dr\.|Dosent, PhD|Dosent, Dr\.|Dr\.-İng\.)",
        line,
    ):
        return bool(
            re.match(
                r"^[A-Za-zƏəÜüÖöĞğŞşİıÇç][a-zəüöğşçıçA-ZƏÜÖĞŞİÇ'’.-]+ [A-ZƏÜÖĞŞİÇ]",
                name_part,
            )
        )
    if re.search(r"\(MEHDİYEV\), Prof\. Dr\.", line):
        return True
    if re.search(r"GƏNCƏLİ\s+Dosent", line):
        return True
    return False


def extract_chapter() -> str:
    text = EXTRACT.read_text(encoding="utf-8")
    start = text.find(CHAPTER_START)
    end = text.find(CHAPTER_END, start)
    if start < 0 or end < 0:
        raise SystemExit("Chapter boundaries not found in extract")
    return text[start:end]


def parse_profiles_by_order(chapter: str) -> list[dict]:
    lines = [normalize_ws(l) for l in chapter.splitlines()]
    profiles: list[dict] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if not is_chapter_name_line(line):
            i += 1
            continue
        name_line = line
        name = re.sub(
            r",\s*(?:PhD|Ph\.D\.|Prof\. Dr\.|Ed\.D\.|Dr\.|Dosent, PhD|Dosent, Dr\.|Dr\.-İng\.).*$",
            "",
            name_line,
        )
        name = re.sub(r"\s*\(MEHDİYEV\)", " (MEHDİYEV)", name)
        name = re.sub(r"\s+Dosent$", "", name.strip().rstrip(",").strip())
        i += 1
        header_lines: list[str] = []
        body_lines: list[str] = []
        while i < len(lines):
            ln = lines[i]
            if not ln:
                i += 1
                continue
            if SKIP_LINE.search(ln) or ln in COUNTRY_HEADERS:
                i += 1
                continue
            if is_chapter_name_line(ln):
                break
            if not body_lines:
                if is_bullet_line(ln) or is_section_heading_line(ln):
                    body_lines.append(ln)
                    i += 1
                    continue
                if looks_like_bio_start(ln, name) or re.match(
                    r"^20\d{2}", ln.strip()
                ):
                    body_lines.append(ln)
                    i += 1
                    continue
                preview = dehyphenate(" ".join(header_lines + [ln]))
                if header_lines and (
                    HEADER_BIO_RE.search(preview)
                    or looks_like_bio_start(preview, name)
                ):
                    body_lines.append(ln)
                    i += 1
                    continue
                if is_header_candidate(ln, name) or (
                    header_lines and len(ln) < 130
                ):
                    header_lines.append(ln)
                    i += 1
                    continue
            body_lines.append(ln)
            i += 1
        while body_lines and is_title_continuation(body_lines[0], name):
            header_lines.append(body_lines.pop(0))
        profiles.append(
            {"name": name, "header_lines": header_lines, "body_lines": body_lines}
        )
    return profiles


def split_title_org(header_lines: list[str]) -> tuple[str, str]:
    """Use header lines verbatim; join broken PDF lines into one title."""
    if not header_lines:
        return "", ""
    return join_verbatim(header_lines), ""


def strip_bullet(line: str) -> str:
    return BULLET_START.sub("", line).strip()


def is_bullet_line(line: str) -> bool:
    return bool(BULLET_START.match(line))


SECTION_HEADINGS = {
    "əsas tədqiqat sahələri",
    "peşəkar təcrübə",
    "mükafatlar və tanınma",
    "mükafatları",
    "mükafatlar",
    "təhsil və peşəkar hazırlıq",
    "üzvlük və beynəlxalq əlaqələr",
    "elmi maraqları",
    "tədqiqat sahələri",
    "əsas nailiyyətləri",
    "beynəlxalq fəaliyyət",
    "nəşrlər və elmi töhfələr",
    "akademik və peşəkar təcrübə",
    "elmi və tədqiqat fəaliyyəti",
    "elmi nailiyyətlər və tanınma",
    "ictimai və peşəkar fəaliyyəti",
    "təltifləri",
    "riyazi modelləşdirmə",
    "peşəkar fəaliyyət və nailiyyətlər",
    "tibb elmi nailiyyətləri",
    "media və ictimai fəaliyyət",
    "qeyri-xətti analiz və riyazi fizikaya töhfələri",
    "beynəlxalq elmi jurnallarda fəaliyyəti",
    "elmi nəşrləri",
    "beynəlxalq universitetlərdə fəaliyyəti",
    "mükafatlar və təltiflər",
    "beynəlxalq konfranslar və tanınma",
}


def is_awards_heading_line(line: str) -> bool:
    key = line.strip().rstrip(":").casefold()
    return key in (
        "təltifləri",
        "mükafatlar",
        "mükafatları",
        "mükafatlar və tanınma",
        "elmi nailiyyətlər və tanınma",
    ) or bool(re.match(r"^mükafat", key))


def is_section_heading_line(line: str) -> bool:
    s = line.strip()
    if not s:
        return False
    key = s.rstrip(":").strip().casefold()
    if key in SECTION_HEADINGS:
        return True
    if re.match(r"^Mükafatlar", s, re.I) and s.endswith(":"):
        return True
    if s.endswith(":") and len(s) <= 55 and "," not in s:
        if re.search(
            r"\b(etmişdir|olmuşdur|aparmışdır|göstərir|üzvüdür|müəllifidir|idarə edir|"
            r"daxildir|nailiyyətlərə|titullar)\b",
            s,
            re.I,
        ):
            return False
        if re.match(r"^[A-ZƏÜÖĞŞİÇ\"«(]", s):
            return True
    return False


def is_title_continuation(line: str, name: str) -> bool:
    if not line or looks_like_bio_start(line, name):
        return False
    s = line.strip()
    if re.match(r"^\d{4}", s):
        return False
    if re.search(
        r"\b(illər|ildə|ildən|tərəfindən|seçilmiş|görülmüş|etmişdir|çalışmış|alır)\b",
        s,
        re.I,
    ):
        return False
    if s.lower() in ("olmuşdur", "olub", "oldu"):
        return True
    if len(s) < 90 and not s.endswith((".", "!", "?")):
        if s[0].islower():
            return True
        if re.match(r"^(Departament|Atom Enerjisi|DAAB)", s, re.I):
            return True
    return False


def normalize_section_title(line: str) -> str:
    s = line.strip().rstrip(":")
    return f"{s}:"


def build_bio_html(body_lines: list[str]) -> str:
    if not body_lines:
        return '<div class="card-bio"><p class="bio">Məlumat kitabdan əlavə edilməyib.</p></div>'

    parts: list[str] = []
    paragraph_buf: list[str] = []
    bullet_buf: list[str] = []
    award_buf: list[str] = []
    awards_heading = ""
    in_awards = False
    saw_awards = False
    bullet_continues = False
    first_paragraph = True

    def flush_paragraph():
        nonlocal paragraph_buf, first_paragraph
        if not paragraph_buf:
            return
        text = join_verbatim(paragraph_buf)
        cls = "bio bio-lead" if first_paragraph else "bio"
        parts.append(f'<p class="{cls}">{html.escape(text)}</p>')
        first_paragraph = False
        paragraph_buf = []

    def flush_bullets():
        nonlocal bullet_buf, bullet_continues
        if bullet_buf:
            items = "".join(
                f"<li>{html.escape(join_verbatim([b]))}</li>" for b in bullet_buf
            )
            parts.append(f'<ul class="bullets">{items}</ul>')
            bullet_buf = []
            bullet_continues = False

    def flush_awards():
        nonlocal award_buf, awards_heading, in_awards, saw_awards
        if not saw_awards or not award_buf:
            award_buf = []
            awards_heading = ""
            in_awards = False
            return
        items = "".join(
            f"<li>{html.escape(join_verbatim([a]))}</li>" for a in award_buf
        )
        parts.append(
            f'<div class="awards-block"><ul class="awards-list">{items}</ul></div>'
        )
        award_buf = []
        awards_heading = ""
        in_awards = False
        saw_awards = False

    for ln in body_lines:
        if SKIP_LINE.search(ln) or not ln.strip():
            continue
        ln = normalize_ws(ln)

        if is_section_heading_line(ln):
            flush_bullets()
            flush_paragraph()
            flush_awards()
            parts.append(
                f'<p class="bio-section-title">{html.escape(normalize_section_title(ln))}</p>'
            )
            in_awards = is_awards_heading_line(ln)
            saw_awards = in_awards
            continue

        if is_bullet_line(ln):
            flush_paragraph()
            if in_awards:
                award_buf.append(strip_bullet(ln))
            else:
                bullet_buf.append(strip_bullet(ln))
            bullet_continues = True
            continue

        if bullet_continues and bullet_buf and not in_awards:
            bullet_buf[-1] = f"{bullet_buf[-1]} {ln}"
            continue

        if in_awards:
            if award_buf:
                award_buf[-1] = f"{award_buf[-1]} {ln}"
            else:
                award_buf.append(ln)
            continue

        if bullet_buf:
            flush_bullets()
        paragraph_buf.append(ln)

    flush_bullets()
    flush_paragraph()
    flush_awards()

    inner = "".join(parts) if parts else '<p class="bio">Məlumat mövcud deyil.</p>'
    return f'<div class="card-bio">{inner}</div>'


def extract_all_cards(html_text: str) -> list[str]:
    """Extract full scientist card blocks (non-greedy regex truncates nested divs)."""
    cards: list[str] = []
    marker = '<div class="card"'
    pos = 0
    while True:
        start = html_text.find(marker, pos)
        if start < 0:
            break
        i = start + len("<div")
        depth = 1
        while i < len(html_text) and depth > 0:
            next_open = html_text.find("<div", i)
            next_close = html_text.find("</div>", i)
            if next_close < 0:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                i = next_open + 4
            else:
                depth -= 1
                i = next_close + len("</div>")
        if depth != 0:
            raise SystemExit(f"Unbalanced card markup near offset {start}")
        cards.append(html_text[start:i])
        pos = i
    return cards


def replace_card_bio(card_html: str, bio_html: str) -> str:
    marker = '<div class="card-bio">'
    start = card_html.find(marker)
    if start < 0:
        return card_html
    i = start + len(marker)
    depth = 1
    while i < len(card_html) and depth > 0:
        next_open = card_html.find("<div", i)
        next_close = card_html.find("</div>", i)
        if next_close < 0:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            i = next_open + 4
        else:
            depth -= 1
            i = next_close + len("</div>")
    if depth != 0:
        return card_html
    return card_html[:start] + bio_html + card_html[i:]


def update_card(card_html: str, profile: dict) -> str:
    title, org = split_title_org(profile["header_lines"])
    bio_html = build_bio_html(profile["body_lines"])

    if title:
        card_html = re.sub(
            r'<p class="card-title">[\s\S]*?</p>',
            f'<p class="card-title">{html.escape(title)}</p>',
            card_html,
            count=1,
        )
    if org:
        card_html = re.sub(
            r'<p class="card-org">[\s\S]*?</p>',
            f'<p class="card-org">{html.escape(org)}</p>',
            card_html,
            count=1,
        )
    else:
        card_html = re.sub(r'\s*<p class="card-org">[\s\S]*?</p>', "", card_html, count=1)
    card_html = replace_card_bio(card_html, bio_html)
    return card_html


def main():
    chapter = extract_chapter()
    profiles = parse_profiles_by_order(chapter)
    print(f"Profiles parsed: {len(profiles)}")

    html_text = HTML_PATH.read_text(encoding="utf-8")
    cards = extract_all_cards(html_text)
    if len(cards) != 83:
        raise SystemExit(f"Expected 83 cards, found {len(cards)}")
    if len(profiles) != 83:
        raise SystemExit(f"Expected 83 profiles, found {len(profiles)}")

    new_cards = [update_card(c, p) for c, p in zip(cards, profiles)]
    new_html = html_text
    for old, new in zip(cards, new_cards):
        new_html = new_html.replace(old, new, 1)

    HTML_PATH.write_text(new_html, encoding="utf-8")
    print("All 83 cards updated with verbatim book text.")


if __name__ == "__main__":
    main()

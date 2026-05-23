"""Improve card-bio formatting: paragraphs, bullets, awards, section headings."""
from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

from _paths import AZ_SCIENTISTS_PROFILES, ROOT

HTML_PATH = AZ_SCIENTISTS_PROFILES

SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-ZƏÜÖĞŞİÇ\"0-9(«])")
ABBR_GUARD = re.compile(
    r"\b(?:Prof|Dr|Ph\.D|Ed\.D|B\.Sc|M\.Sc|Jr|Sr|St|vs|etc|i\.e|e\.g)\.",
    re.I,
)
DOT = "\uE000"

AWARD_RE = re.compile(
    r"mükafat|medal|təltif|Təşəkkürnamə|Nobel|təqaüd|layiq görül|laureat|"
    r"Fellow|Award|Distinguished|əməkdar|fəxri ad|fəxri üzv|şərəfinə|"
    r"ünvanı verilmiş|ICAS|hörmətli",
    re.I,
)

MUKAFAT_HEADER = re.compile(r"^Mükafatlar(?:ı)?\s*:?\s*$", re.I)

SECTION_HEADING = re.compile(
    r"^(?:Elmi maraqlar(?:ı)?|Peşəkar təcrübə|Riyazi modelləşdirmə|"
    r"Əsas tədqiqat(?:\s+sahələri)?|Tədqiqat sahələri|Publications|"
    r"Strateji elmi-tədqiqat rəhbərliyi)\s*:?\s*$",
    re.I,
)

INLINE_HEADINGS = [
    "Əsas tədqiqat sahələri",
    "Peşəkar təcrübə",
    "Elmi maraqları",
    "Elmi fəaliyyəti",
    "Tədqiqat sahələri",
    "Strateji elmi-tədqiqat rəhbərliyi",
    "Üzvlük və beynəlxalq əlaqələr",
    "Təhsil və peşəkar hazırlıq",
    "Mükafatlar və tanınma",
    "Digər vəzifələr",
]

BULLET_HINT = re.compile(
    r"(müəllifidir|üzvüdür|üzvü|fəaliyyət|mükafat|layiq görül|təltif|iştirak|"
    r"konfrans|jurnal|professoru|müdiri|sədridir|yaratmışdır|aparmışdır|alır\.?)$",
    re.I,
)


def guard_abbreviations(text: str) -> str:
    def repl(m: re.Match[str]) -> str:
        return m.group(0).replace(".", DOT)

    return ABBR_GUARD.sub(repl, text)


def unguard_abbreviations(text: str) -> str:
    return text.replace(DOT, ".")


def split_sentences(text: str) -> list[str]:
    text = re.sub(r"\s+Bundan əlavə,\s+", ". Bundan əlavə, ", text.strip(), flags=re.I)
    guarded = guard_abbreviations(text)
    parts = SENT_SPLIT.split(guarded)
    sentences = [unguard_abbreviations(p.strip()) for p in parts if p.strip()]
    merged: list[str] = []
    for sent in sentences:
        if merged and re.fullmatch(r"(?:Prof|Dr)\.?", sent, re.I):
            merged[-1] = merged[-1] + " " + sent
        else:
            merged.append(sent)
    return merged


def is_colon_topic_line(sentence: str) -> bool:
    s = sentence.strip()
    if len(s) < 18 or len(s) > 200 or is_award_sentence(s):
        return False
    m = re.match(r"^([^:]{4,72}):\s+(.+)$", s)
    if not m:
        return False
    topic, detail = m.group(1), m.group(2)
    if re.search(r"\b(etmişdir|olmuşdur|aparmışdır|göstərir)\b", topic, re.I):
        return False
    return len(detail) >= 12


def is_bullet_candidate(sentence: str) -> bool:
    if len(sentence) > 240:
        return False
    if BULLET_HINT.search(sentence):
        return True
    if re.match(r"^\d{4}", sentence):
        return True
    if len(sentence) < 140 and ";" in sentence:
        return True
    if re.match(r"^[A-ZƏÜÖĞŞİÇ0-9“\"]", sentence) and len(sentence) < 200:
        if re.search(r"(AG|GmbH|Universitet|İnstitut|Department|Ltd)", sentence):
            return True
    return False


def preprocess_inline_headings(text: str) -> str:
    for heading in INLINE_HEADINGS:
        text = re.sub(
            rf"([.!?])\s*({re.escape(heading)})\s*:",
            r"\1\n\2:",
            text,
            flags=re.I,
        )
        text = re.sub(
            rf"(?<=[a-zəüöğşıç])\s+({re.escape(heading)})\s*:",
            r"\n\1:",
            text,
            flags=re.I,
        )
    return text


def is_award_sentence(sentence: str) -> bool:
    s = sentence.strip()
    if MUKAFAT_HEADER.match(s):
        return True
    if re.search(
        r"layiq görül|təltif edilmiş|təltif olunmuş|mükafatına|mükafatı|"
        r"medalı|medal ilə|Nobel|təqaüdü|laureatıdır|Fellow|"
        r"Təşəkkürnamə|əməkdar|fəxri ad|fəxri diplom|Fəxri Fərman",
        s,
        re.I,
    ):
        return True
    if len(s) > 220:
        return False
    if not AWARD_RE.search(s):
        return False
    if re.search(r"\d{4}[-–].*(?:mükafat|medal|təltif|təqaüd)", s, re.I):
        return True
    return False


def is_section_heading_text(text: str) -> bool:
    s = text.strip()
    if SECTION_HEADING.match(s):
        return True
    if s.endswith(":") and len(s) < 90:
        if not re.search(r"\b(etmişdir|olmuşdur|aparmışdır|göstərir|verir)\b", s, re.I):
            return True
    return False


def render_ul(items: list[str]) -> str:
    lis = "".join(f"<li>{html_lib.escape(s)}</li>" for s in items)
    return f'<ul class="bullets">{lis}</ul>'


def render_awards(label: str, items: list[str]) -> str:
    if not items:
        return ""
    lbl = label.strip().rstrip(":")
    if not lbl.endswith(":"):
        lbl += ":"
    lis = "".join(f"<li>{html_lib.escape(s)}</li>" for s in items)
    return (
        f'<div class="awards-block">'
        f'<span class="awards-label">{html_lib.escape(lbl)}</span>'
        f'<ul class="awards-list">{lis}</ul></div>'
    )


def structure_from_sentences(sentences: list[str]) -> str:
    if not sentences:
        return ""

    blocks: list[str] = []
    narrative: list[str] = []
    awards: list[str] = []
    awards_label = "Mükafatlar və tanınma"

    def flush_narrative() -> None:
        nonlocal narrative
        if not narrative:
            return
        i = 0
        while i < len(narrative):
            chunk = narrative[i : i + 2]
            blocks.append(f'<p class="bio">{html_lib.escape(" ".join(chunk))}</p>')
            i += 2
        narrative = []

    def flush_awards() -> None:
        nonlocal awards, awards_label, narrative
        if not awards:
            return
        kept: list[str] = []
        for item in awards:
            if len(item) > 220 and not re.search(
                r"medal|təltif|Təşəkkürnamə|Fəxri Fərman",
                item,
                re.I,
            ):
                narrative.append(item)
            else:
                kept.append(item)
        if kept:
            blocks.append(render_awards(awards_label, kept))
        awards = []

    i = 0
    while i < len(sentences):
        s = sentences[i]

        if MUKAFAT_HEADER.match(s.strip()):
            flush_narrative()
            flush_awards()
            awards_label = s.strip()
            i += 1
            continue

        if len(s) > 220 and AWARD_RE.search(s):
            parts = split_sentences(s)
            if sum(1 for p in parts if is_award_sentence(p)) >= 1:
                flush_narrative()
                for p in parts:
                    if is_award_sentence(p):
                        awards.append(p)
                    else:
                        narrative.append(p)
                i += 1
                continue

        if is_award_sentence(s):
            flush_narrative()
            awards.append(s)
            i += 1
            continue

        if is_section_heading_text(s):
            flush_narrative()
            flush_awards()
            title = s if s.rstrip().endswith(":") else s.rstrip() + ":"
            blocks.append(f'<p class="bio-section-title">{html_lib.escape(title)}</p>')
            i += 1
            bullets: list[str] = []
            while i < len(sentences):
                nxt = sentences[i]
                if is_section_heading_text(nxt) or is_award_sentence(nxt):
                    break
                if is_bullet_candidate(nxt) or (bullets and len(nxt) < 220):
                    bullets.append(nxt)
                    i += 1
                elif len(nxt) > 200 and not bullets:
                    narrative.append(nxt)
                    i += 1
                    break
                else:
                    break
            if len(bullets) >= 2:
                blocks.append(render_ul(bullets))
            elif bullets:
                narrative.extend(bullets)
            continue

        if s.rstrip().endswith(":") and i + 1 < len(sentences):
            flush_narrative()
            flush_awards()
            blocks.append(
                f'<p class="bio-section-title">{html_lib.escape(s.rstrip())}</p>'
            )
            i += 1
            bullets = []
            while i < len(sentences):
                nxt = sentences[i]
                if is_section_heading_text(nxt) or is_award_sentence(nxt):
                    break
                if is_bullet_candidate(nxt) or (bullets and len(nxt) < 220):
                    bullets.append(nxt)
                    i += 1
                else:
                    break
            if len(bullets) >= 2:
                blocks.append(render_ul(bullets))
            elif bullets:
                narrative.extend(bullets)
            continue

        if is_bullet_candidate(s) and len(s) < 220:
            flush_narrative()
            flush_awards()
            bullets = [s]
            i += 1
            while i < len(sentences) and is_bullet_candidate(sentences[i]):
                if len(sentences[i]) > 240:
                    break
                bullets.append(sentences[i])
                i += 1
            if len(bullets) >= 2:
                blocks.append(render_ul(bullets))
            else:
                narrative.extend(bullets)
            continue

        if is_colon_topic_line(s):
            flush_narrative()
            flush_awards()
            topics = [s]
            i += 1
            while i < len(sentences) and is_colon_topic_line(sentences[i]):
                topics.append(sentences[i])
                i += 1
            if len(topics) >= 2:
                blocks.append(render_ul(topics))
            else:
                narrative.append(s)
            continue

        narrative.append(s)
        i += 1

    flush_narrative()
    flush_awards()
    return "".join(blocks)


def restructure_bullets_html(ul_inner: str) -> str:
    items = [
        html_lib.unescape(x.strip())
        for x in re.findall(r"<li>([\s\S]*?)</li>", ul_inner, re.I)
        if x.strip()
    ]
    if not items:
        return ""

    out: list[str] = []
    current: list[str] = []
    for item in items:
        if is_section_heading_text(item):
            if current:
                out.append(render_ul(current))
                current = []
            title = item if item.rstrip().endswith(":") else item.rstrip() + ":"
            out.append(f'<p class="bio-section-title">{html_lib.escape(title)}</p>')
        else:
            current.append(item)
    if current:
        out.append(render_ul(current))
    return "".join(out)


def collect_sentences_from_html(bio_html: str, *, include_awards: bool = False) -> list[str]:
    raw_chunks: list[str] = []
    for m in re.finditer(
        r'<p class="bio(?:\s+bio-lead|\s+bio-section-title)?">([\s\S]*?)</p>',
        bio_html,
        re.I,
    ):
        raw_chunks.append(html_lib.unescape(m.group(1)))
    for m in re.finditer(r"<ul class=\"bullets\">([\s\S]*?)</ul>", bio_html, re.I):
        for li in re.findall(r"<li>([\s\S]*?)</li>", m.group(1), re.I):
            raw_chunks.append(html_lib.unescape(li.strip()))
    if include_awards:
        for m in re.finditer(r'<div class="awards-block">([\s\S]*?)</div>', bio_html, re.I):
            block = m.group(1)
            label_m = re.search(
                r'<span class="awards-label">([^<]*)</span>', block, re.I
            )
            if label_m:
                raw_chunks.append(html_lib.unescape(label_m.group(1)).strip())
            for li in re.findall(r"<li>([\s\S]*?)</li>", block, re.I):
                raw_chunks.append(html_lib.unescape(li.strip()))

    merged = preprocess_inline_headings("\n".join(c for c in raw_chunks if c))
    sentences: list[str] = []
    for chunk in re.split(r"\n+", merged):
        chunk = chunk.strip()
        if not chunk:
            continue
        if is_section_heading_text(chunk):
            sentences.append(chunk if chunk.endswith(":") else chunk + ":")
        elif len(chunk) > 200:
            sentences.extend(split_sentences(chunk))
        else:
            sentences.append(chunk)
    return sentences


def section_paragraphs_to_bullets(html: str) -> str:
    pattern = re.compile(
        r"(<p class=\"bio-section-title\">[^<]+</p>)((?:<p class=\"bio\">[^<]+</p>)+)",
        re.I,
    )

    def repl(m: re.Match[str]) -> str:
        title = m.group(1)
        paras = re.findall(r'<p class="bio">([^<]+)</p>', m.group(2), re.I)
        sents: list[str] = []
        for p in paras:
            sents.extend(split_sentences(html_lib.unescape(p)))
        if len(sents) >= 3 and all(len(s) < 210 for s in sents):
            return title + render_ul(sents)
        return m.group(0)

    return pattern.sub(repl, html)


def normalize_awards_html(html: str) -> str:
    def fix_block(block_match: re.Match[str]) -> str:
        label_m = re.search(
            r'<span class="awards-label">([^<]*)</span>', block_match.group(0), re.I
        )
        label = (
            html_lib.unescape(label_m.group(1)) if label_m else "Mükafatlar və tanınma"
        )
        items: list[str] = []
        overflow: list[str] = []
        for li in re.findall(r"<li>([\s\S]*?)</li>", block_match.group(0), re.I):
            text = html_lib.unescape(li.strip())
            if len(text) > 200:
                for s in split_sentences(text):
                    if is_award_sentence(s):
                        items.append(s)
                    else:
                        overflow.extend(split_sentences(s) if len(s) > 120 else [s])
            elif is_award_sentence(text):
                items.append(text)
            else:
                overflow.append(text)
        out = ""
        if overflow:
            i = 0
            while i < len(overflow):
                out += (
                    f'<p class="bio">{html_lib.escape(" ".join(overflow[i : i + 2]))}</p>'
                )
                i += 2
        if items:
            out += render_awards(label, items)
        return out

    return re.sub(r'<div class="awards-block">[\s\S]*?</div>', fix_block, html, flags=re.I)


MUKAFAT_TITLE_RE = re.compile(
    r"<p class=\"bio-section-title\">Mükafatlar(?:ı)?(?: və tanınma)?:</p>",
    re.I,
)


def consolidate_mukafat_sections(html: str) -> str:
    """Merge duplicate mükafat headings/blocks without stripping narrative paragraphs."""
    award_items: list[str] = []
    for block in re.findall(r'<div class="awards-block">[\s\S]*?</div>', html, re.I):
        for li in re.findall(r"<li>([\s\S]*?)</li>", block, re.I):
            award_items.append(html_lib.unescape(li.strip()))

    body = MUKAFAT_TITLE_RE.sub("", html)
    body = re.sub(r'<div class="awards-block">[\s\S]*?</div>', "", body, flags=re.I)

    if not award_items:
        return html

    deduped: list[str] = []
    seen: set[str] = set()
    for item in award_items:
        key = item[:80].lower()
        if key not in seen:
            seen.add(key)
            deduped.append(item)
    mukafat_title = '<p class="bio-section-title">Mükafatlar və tanınma:</p>'
    return body.rstrip() + mukafat_title + render_awards("Mükafatlar və tanınma", deduped)


def strip_redundant_awards_label(html: str) -> str:
    return re.sub(
        r'(<p class="bio-section-title">Mükafatlar[^<]*</p>\s*)<div class="awards-block">\s*'
        r'<span class="awards-label">[^<]*</span>',
        r'\1<div class="awards-block">',
        html,
        flags=re.I,
    )


def colon_lines_in_bio_to_ul(html: str) -> str:
    def repl(m: re.Match[str]) -> str:
        text = html_lib.unescape(m.group(1))
        sents = split_sentences(text)
        topics: list[str] = []
        other: list[str] = []
        for s in sents:
            if is_colon_topic_line(s):
                topics.append(s)
            else:
                other.append(s)
        if len(topics) < 2:
            return m.group(0)
        out = ""
        if other:
            out += f'<p class="bio">{html_lib.escape(" ".join(other))}</p>'
        return out + render_ul(topics)

    return re.sub(r'<p class="bio">([^<]+)</p>', repl, html)


def merge_adjacent_bullet_lists(html: str) -> str:
    return re.sub(r"</ul>\s*<ul class=\"bullets\">", "", html)


def dedupe_section_titles(html: str) -> str:
    return re.sub(
        r'(<p class="bio-section-title">[^<]+</p>)(\s*\1)+',
        r"\1",
        html,
        flags=re.I,
    )


def split_research_tail_to_section(html: str) -> str:
    """After publication stats, group comma-heavy research lines under Elmi maraqları."""
    marker = "Elmi maraqları"
    if marker.lower() in html.lower():
        return html

    m = re.search(
        r"(<p class=\"bio\">[^<]*(?:məqaləsi|jurnalda|rəyçi|konfransda)[^<]*</p>)"
        r"((?:<p class=\"bio\">[^<]+</p>)+)",
        html,
        re.I,
    )
    if not m:
        return html

    tail = m.group(2)
    paras = re.findall(r'<p class="bio">([^<]+)</p>', tail, re.I)
    research: list[str] = []
    keep: list[str] = []
    for p in paras:
        text = html_lib.unescape(p)
        if (
            len(text) > 40
            and (text.count(",") >= 2 or re.search(r"inzibati|fizika|sintez|model", text, re.I))
            and not re.search(r"\b(üzvüdür|professoru|müdiri)\b", text, re.I)
        ):
            research.extend(split_sentences(text))
        else:
            keep.append(text)

    if len(research) < 3:
        return html

    rebuilt = m.group(1)
    if keep:
        rebuilt += "".join(f'<p class="bio">{html_lib.escape(" ".join(keep[i:i+2]))}</p>' for i in range(0, len(keep), 2))
    rebuilt += '<p class="bio-section-title">Elmi maraqları:</p>' + render_ul(research[:12])
    return html[: m.start()] + rebuilt + html[m.end() :]


def process_card_bio_div(bio_html: str) -> str:
    bio_html = bio_html.strip()
    if not bio_html:
        return bio_html

    only_bullets = (
        "<ul class=\"bullets\">" in bio_html
        and not re.search(r'<p class="bio(?:\s|>)', bio_html)
        and "<div class=\"awards-block\">" not in bio_html
    )
    if only_bullets:
        m = re.search(r"<ul class=\"bullets\">([\s\S]*?)</ul>", bio_html, re.I)
        if m:
            inner = restructure_bullets_html(m.group(1))
            return (
                '<p class="bio bio-lead">Peşəkar fəaliyyət və nailiyyətlər:</p>'
                + inner
            )

    if re.search(r'<div class="awards-block">', bio_html, re.I) or re.search(
        r'<p class="bio-section-title">', bio_html, re.I
    ):
        result = bio_html
        result = merge_adjacent_bullet_lists(result)
        result = strip_redundant_awards_label(result)
        result = dedupe_section_titles(result)
        return merge_split_honorifics(result)
    else:
        sentences = collect_sentences_from_html(bio_html)
        if not sentences:
            return bio_html

        if len(sentences) <= 2 and sum(len(s) for s in sentences) < 400:
            return f'<p class="bio">{html_lib.escape(" ".join(sentences))}</p>'

        result = structure_from_sentences(sentences)
    result = promote_colon_leads(result or bio_html)
    result = section_paragraphs_to_bullets(result)
    result = normalize_awards_html(result)
    result = colon_lines_in_bio_to_ul(result)
    result = merge_adjacent_bullet_lists(result)
    result = consolidate_mukafat_sections(result)
    result = strip_redundant_awards_label(result)
    result = dedupe_section_titles(result)
    result = split_research_tail_to_section(result)
    return merge_split_honorifics(result)


def promote_colon_leads(html: str) -> str:
    if "bio-section-title" in html or '<ul class="bullets">' not in html:
        return html

    ul_pos = html.find('<ul class="bullets">')
    prefix = html[:ul_pos]
    suffix = html[ul_pos:]
    p_start = prefix.rfind('<p class="bio">')
    if p_start < 0:
        return html
    p_end = prefix.find("</p>", p_start)
    if p_end < 0:
        return html

    body = html_lib.unescape(prefix[p_start + len('<p class="bio">') : p_end])
    if ":" not in body or not body.rstrip().endswith(":"):
        return html

    idx = body.rfind(":")
    before = body[:idx]
    dot = before.rfind(". ")
    if dot < 0:
        lead = body.strip()
        if not lead.endswith(":"):
            return html
        return (
            prefix[:p_start]
            + f'<p class="bio-section-title">{html_lib.escape(lead)}</p>'
            + suffix
        )

    rest = body[: dot + 1].strip()
    lead = body[dot + 2 : idx + 1].strip()
    if not lead.endswith(":"):
        return html

    return (
        prefix[:p_start]
        + f'<p class="bio">{html_lib.escape(rest)}</p>'
        + f'<p class="bio-section-title">{html_lib.escape(lead)}</p>'
        + suffix
    )


def merge_split_honorifics(html: str) -> str:
    html = re.sub(
        r"(Prof\.)\s*</p>\s*<p class=\"bio\">(Dr\.\s+)",
        r"\1 \2",
        html,
        flags=re.I,
    )
    return re.sub(
        r"([.!?])\s*</p>\s*<p class=\"bio\">(Dr\.\s+)",
        r"\1 \2",
        html,
        flags=re.I,
    )


def replace_all_card_bios(text: str) -> tuple[str, int]:
    marker = '<div class="card-bio">'
    result: list[str] = []
    i = 0
    count = 0
    while True:
        start = text.find(marker, i)
        if start < 0:
            result.append(text[i:])
            break
        result.append(text[i:start])
        inner_start = start + len(marker)
        depth = 1
        pos = inner_start
        while pos < len(text) and depth > 0:
            next_open = text.find("<div", pos)
            next_close = text.find("</div>", pos)
            if next_close < 0:
                break
            if next_open != -1 and next_open < next_close:
                depth += 1
                pos = next_open + 4
            else:
                depth -= 1
                if depth == 0:
                    inner = text[inner_start:next_close]
                    formatted = process_card_bio_div(inner)
                    result.append(f'<div class="card-bio">{formatted}</div>')
                    count += 1
                    pos = next_close + len("</div>")
                    break
                pos = next_close + len("</div>")
        i = pos
    return "".join(result), count


def main():
    text = HTML_PATH.read_text(encoding="utf-8")
    new_text, n = replace_all_card_bios(text)
    HTML_PATH.write_text(new_text, encoding="utf-8")
    print(f"Formatted {n} card-bio sections")


if __name__ == "__main__":
    main()

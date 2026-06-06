#!/usr/bin/env python3
"""Parse, derive, and apply enriched profile sections for prominent figures."""
from __future__ import annotations

import html
import json
import re
from dataclasses import dataclass, field
from pathlib import Path

from _paths import HELPERS, ROOT

FIGURES = ROOT / "az" / "prominent_figures"
AZ_CHAR = re.compile(r"[əğıöüşçƏĞİÖÜŞÇ]")

PROSE_RE = re.compile(r'class="prose pf-profile-article">(.*?)</div>', re.DOTALL)
META_DESC_RE = re.compile(r'<meta name="description" content="([^"]*)"', re.I)
NAME_RE = re.compile(r"<h1>([^<]+)</h1>")
FIELD_RE = re.compile(r'info-label">Sahə</span><span class="info-val">([^<]+)</span>')
GOLD_TAG_RE = re.compile(r'<span class="hero-tag gold">([^<]+)</span>')

WORKS_BLOCK_RE = re.compile(
    r'(<ul class="works-list">)(.*?)(</ul>)',
    re.DOTALL,
)
EVENTS_BLOCK_RE = re.compile(
    r'(<div class="section-card"><div class="section-title">.*?'
    r'(?:Həyatından maraqlı hadisələr|Notable aspects of the life and work)'
    r'</div>)'
    r'(.*?)(</div>\s*<div class="quote-block">)',
    re.DOTALL,
)
CONTRIB_BLOCK_RE = re.compile(
    r'(<ul class="contribution-list">)(.*?)(</ul>)',
    re.DOTALL,
)
SOCIETY_RE = re.compile(
    r"(<h4>(?:Cəmiyyətə təsiri|Contribution to society)</h4><p>)([^<]+)(</p>)",
    re.DOTALL,
)

GENERIC_WORK2 = re.compile(
    r"biliklərin inkişafına və yayılmasına mühüm təsir göstərmişdir\.?$"
)
GENERIC_WORK3 = re.compile(r"ümumbəşəri tərəqqi tarixində yadda qalan iz")
GENERIC_EVENT1 = re.compile(
    r"yeni düşüncə və araşdırma istiqamətlərini gücləndirdi|"
    r"bilik sərhədlərini genişləndirən ideya və araşdırmaları"
)
GENERIC_EVENT2 = re.compile(
    r"müxtəlif elmi və mədəni mühitlərdə xatırlanır|"
    r"tədqiqat və təhsil mühitinə təsir göstərmişdir"
)
GENERIC_SOCIETY = re.compile(
    r"öz dövrünün intellektual mühitinə təsir göstərmiş, sonrakı nəsillər üçün bilik"
)
GENERIC_CONTRIB = (
    re.compile(r"sahəsində mühüm töhfə verdi"),
    re.compile(r"Elmi və intellektual irsin zənginləşməsinə xidmət etdi"),
    re.compile(r"Bəşəriyyətin tərəqqisinə təsir göstərən ideyalar yaratdı"),
)

WORLD_CONTRIB_RE = re.compile(
    r"Onun əsas töhfəsi (.+?) ilə bağlıdır\.",
    re.DOTALL,
)
TEMPLATE_MARKERS = ("irsinə mənsub", "elmi və intellektual ənənəsini dünya miqyasında")
TEMPLATE_ACTIVITY_RE = re.compile(
    r"Əsas əsərləri və fəaliyyət istiqamətləri sırasında (.+?) kimi nümunələr",
    re.DOTALL,
)
QUOTED_TITLE_RE = re.compile(r'[«""]([^»""]{3,80})[»""]')


@dataclass
class Enrichment:
    society: str | None = None
    works: list[tuple[str, str]] = field(default_factory=list)
    events: list[tuple[str, str, str]] = field(default_factory=list)  # emoji, title, text
    contributions: list[str] = field(default_factory=list)


def parse_prose_sections(article_html: str) -> dict[str, list[str]]:
    sections: dict[str, list[str]] = {}
    parts = re.split(r"<h4>([^<]+)</h4>", article_html)
    for i in range(1, len(parts), 2):
        title = parts[i].strip()
        paras = re.findall(r"<p>([^<]+)</p>", parts[i + 1])
        sections[title] = [html.unescape(p.strip()) for p in paras if p.strip()]
    return sections


def extract_profile_meta(text: str) -> dict[str, str]:
    prose_m = PROSE_RE.search(text)
    prose = prose_m.group(1) if prose_m else ""
    desc_m = META_DESC_RE.search(text)
    name_m = NAME_RE.search(text)
    field_m = FIELD_RE.search(text)
    gold_m = GOLD_TAG_RE.search(text)
    return {
        "name": html.unescape(name_m.group(1).strip()) if name_m else "",
        "description": html.unescape(desc_m.group(1).strip()) if desc_m else "",
        "field": html.unescape(field_m.group(1).strip()) if field_m else "",
        "country": html.unescape(gold_m.group(1).strip()) if gold_m else "",
        "sections": parse_prose_sections(prose),
        "is_template": any(m in prose for m in TEMPLATE_MARKERS),
    }


def _first_sentence(text: str, max_len: int = 320) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    cut = text[:max_len].rsplit(". ", 1)[0]
    return cut + "." if cut else text[:max_len] + "…"


def _truncate(text: str, max_len: int = 340) -> str:
    text = text.strip()
    if len(text) <= max_len:
        return text
    return _first_sentence(text, max_len)


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+", text.strip())
    return [p.strip() for p in parts if p.strip()]


def derive_enrichment(text: str, group: str) -> Enrichment | None:
    meta = extract_profile_meta(text)
    name = meta["name"]
    if not name:
        return None

    sections = meta["sections"]
    life = sections.get("Həyat yolu", [])
    scholarly = sections.get("Elmi və yaradıcılıq fəaliyyəti", [])
    society = sections.get("Cəmiyyətə təsiri", [])
    country = meta["country"]
    field_raw = meta["field"]
    field_name = field_raw.split(",")[-1].strip() if field_raw else ""

    works: list[tuple[str, str]] = []
    events: list[tuple[str, str, str]] = []
    contributions: list[str] = []
    society_out: str | None = None

    if group == "world" and scholarly:
        contrib_m = WORLD_CONTRIB_RE.search(scholarly[0])
        if contrib_m:
            phrase = contrib_m.group(1).strip()
            works.append(
                (
                    "Əsas elmi töhfə",
                    f"Onun əsas töhfəsi {phrase} ilə bağlıdır.",
                )
            )
            contributions.append(
                _truncate(f"{name} {phrase[0].lower() + phrase[1:] if phrase else phrase}.")
            )
        rest = WORLD_CONTRIB_RE.sub("", scholarly[0]).strip()
        sents = _split_sentences(rest)
        if sents:
            works.append(("Elmi metod və nəzəriyyə", _truncate(sents[0])))
            if len(sents) > 1:
                contributions.append(_truncate(sents[1]))
        for para in scholarly[1:]:
            if "maraqlı cəhətlərdən biri" in para:
                events.append(("📜", "İrsin dəyərləndirilməsi", _truncate(para)))
            elif not events and len(para) > 80:
                events.append(("🔬", "Elmi təsir", _truncate(para)))
        if len(scholarly) > 1 and len(works) < 3:
            works.append(("Elmi irs və təsir", _truncate(scholarly[1])))
        if len(scholarly) > 2 and len(works) < 3:
            works.append(("Dövrü aşan əhəmiyyət", _truncate(scholarly[2])))
        if len(scholarly) > 1 and len(events) < 2:
            for para in scholarly[1:]:
                if para not in [e[2] for e in events]:
                    events.append(("🌍", "Dövrü aşan əhəmiyyət", _truncate(para)))
                    if len(events) >= 2:
                        break
        if society and GENERIC_SOCIETY.search(society[0]):
            society_out = _truncate(
                f"{name} ideyaları tədqiqat üsullarına, elmi dilə və bəşəriyyətin "
                f"tərəqqi anlayışına uzunmüddətli təsir göstərmişdir."
            )
        elif society:
            society_out = society[0]

    elif not meta["is_template"]:
        quoted: list[str] = []
        for para in life + scholarly:
            quoted.extend(QUOTED_TITLE_RE.findall(para))
        if life:
            works.append(("Həyat və missiya", _truncate(life[0])))
        for para in scholarly:
            titles = QUOTED_TITLE_RE.findall(para)
            if titles:
                for t in titles:
                    if len(works) >= 3:
                        break
                    works.append((t, _truncate(para)))
            elif "möhtəşəm" in para or "əsər" in para.lower():
                label = "Əsas yaradıcılıq" if len(works) <= 1 else "Əsərin məzmunu"
                works.append((label, _truncate(para)))
            elif len(works) < 3:
                works.append(("Fəaliyyət istiqaməti", _truncate(para)))
        if len(works) < 3 and society:
            works.append(("Cəmiyyətə təsir", _truncate(society[0])))
        if society and not GENERIC_SOCIETY.search(society[0]):
            society_out = society[0]
        elif society:
            society_out = _truncate(society[0])
        if life and len(events) < 1:
            sents = _split_sentences(life[0])
            if len(sents) > 1:
                events.append(("🏛️", "Tarixi kontekst", _truncate(sents[1])))
        for para in scholarly:
            if len(events) >= 2:
                break
            if any(k in para for k in ("XII", "XIII", "XIV", "XV", "XVI", "əsrdə", "ildə", "tanın")):
                events.append(("✍️", "Yaradıcılıq və tanınma", _truncate(para)))
        if society and len(events) < 2:
            events.append(("🌟", "Humanist irs", _truncate(society[0])))

    if meta["is_template"] and group == "azturk":
        for para in scholarly:
            act_m = TEMPLATE_ACTIVITY_RE.search(para)
            if act_m:
                parts = [p.strip() for p in act_m.group(1).split(";") if p.strip()]
                for part in parts[:3]:
                    title = part.split(" sahəsində")[0].strip()
                    if len(title) > 60:
                        title = _first_sentence(title, 60)
                    works.append((title, _truncate(part, 280)))
                break
        if life and not works:
            works.append(("Həyat və fəaliyyət", _truncate(life[0])))
        if scholarly and len(works) < 2:
            works.append(("Yaradıcılıq irsi", _truncate(scholarly[0])))
        if society and len(works) < 3:
            works.append(("Cəmiyyətə təsir", _truncate(society[0])))
        if society and GENERIC_SOCIETY.search(society[0]):
            society_out = _truncate(
                f"{name} türk dünyasının ədəbi, mədəni və intellektual yaddaşında "
                f"yaşayan bir sima kimi xatırlanır."
            )
        for para in scholarly:
            if "nümunələr" in para and len(events) < 2:
                events.append(("📚", "Fəaliyyət istiqamətləri", _truncate(para)))
        if life and len(events) < 2:
            events.append(("🏛️", "Tarixi yer", _truncate(life[0])))

    works = works[:3]
    fill_titles = ("Əsas töhfə", "Fəaliyyət istiqaməti", "Tarixi əhəmiyyət")
    desc_fill = _truncate(meta["description"]) if meta["description"] else ""
    while len(works) < 3 and desc_fill:
        works.append((fill_titles[len(works)], desc_fill))

    if len(contributions) < 3:
        for para in society + scholarly:
            if GENERIC_SOCIETY.search(para):
                continue
            bullet = _truncate(para, 180)
            if bullet and bullet not in contributions:
                contributions.append(bullet)
            if len(contributions) >= 3:
                break
    if len(contributions) < 3 and field_name:
        contributions.append(
            f"{field_name} sahəsində yeni standartlar və nümunələr formalaşdırdı."
        )
    if len(contributions) < 3 and country:
        contributions.append(
            f"{country} və daha geniş regionun intellektual həyatına dəyərli töhfələr verdi."
        )
    contributions = contributions[:3]

    seen_event: set[str] = set()
    deduped_events: list[tuple[str, str, str]] = []
    for ev in events:
        if ev[2] in seen_event:
            continue
        seen_event.add(ev[2])
        deduped_events.append(ev)
    events = deduped_events[:2]
    if len(events) < 2 and scholarly:
        for para in scholarly:
            if para in seen_event:
                continue
            events.append(("🔎", "Elmi və intellektual irs", _truncate(para)))
            seen_event.add(para)
            break
    if len(events) < 2 and life:
        events.append(("📖", "Həyat yolu", _truncate(life[0])))

    if len(works) < 3:
        return None

    return Enrichment(
        society=society_out,
        works=works,
        events=events,
        contributions=contributions,
    )


def merge_enrichment(base: Enrichment | None, override: Enrichment | None) -> Enrichment | None:
    if not base and not override:
        return None
    if not base:
        return override
    if not override:
        return base
    return Enrichment(
        society=override.society or base.society,
        works=override.works or base.works,
        events=override.events or base.events,
        contributions=override.contributions or base.contributions,
    )


def render_work_item(num: int, title: str, desc: str) -> str:
    t = html.escape(title, quote=False)
    d = html.escape(desc, quote=False)
    return (
        f'<li class="work-item"><div class="work-num">{num}</div><div>'
        f'<div class="work-name"><em>{t}</em></div>'
        f'<div class="work-desc">{d}</div></div></li>'
    )


def render_works_block(works: list[tuple[str, str]]) -> str:
    items = [render_work_item(i + 1, t, d) for i, (t, d) in enumerate(works[:3])]
    return "<ul class=\"works-list\">" + "".join(items) + "</ul>"


def render_event(emoji: str, title: str, text: str) -> str:
    t = html.escape(title, quote=False)
    x = html.escape(text, quote=False)
    return (
        f'<div class="event-item"><div class="event-title"><span>{emoji}</span> {t}</div>'
        f'<div class="event-text">{x}</div></div>'
    )


def render_events_block(events: list[tuple[str, str, str]]) -> str:
    return "".join(render_event(e, t, x) for e, t, x in events[:2])


def render_contrib_item(text: str) -> str:
    return f'<li class="contribution-item">{html.escape(text, quote=False)}</li>'


def render_contrib_block(items: list[str]) -> str:
    return (
        '<ul class="contribution-list">'
        + "".join(render_contrib_item(i) for i in items[:3])
        + "</ul>"
    )


def apply_enrichment(
    text: str, enrichment: Enrichment, *, force: bool = False
) -> tuple[str, bool]:
    changed = False
    out = text

    if enrichment.society:
        m = SOCIETY_RE.search(out)
        if m and (
            force
            or GENERIC_SOCIETY.search(m.group(2))
            or AZ_CHAR.search(m.group(2))
        ):
            out = SOCIETY_RE.sub(
                rf"\1{html.escape(enrichment.society, quote=False)}\3",
                out,
                count=1,
            )
            changed = True

    if enrichment.works:
        new_works = render_works_block(enrichment.works)
        m = WORKS_BLOCK_RE.search(out)
        if m:
            old_inner = m.group(2)
            if force or (
                GENERIC_WORK2.search(old_inner)
                or GENERIC_WORK3.search(old_inner)
                or AZ_CHAR.search(old_inner)
            ):
                out = WORKS_BLOCK_RE.sub(new_works, out, count=1)
                changed = True

    if enrichment.events:
        new_events = render_events_block(enrichment.events)
        m = EVENTS_BLOCK_RE.search(out)
        if m:
            old_inner = m.group(2)
            if force or (
                GENERIC_EVENT1.search(old_inner)
                or GENERIC_EVENT2.search(old_inner)
                or AZ_CHAR.search(old_inner)
            ):
                out = out[: m.start(2)] + new_events + out[m.end(2) :]
                changed = True

    if enrichment.contributions:
        new_contrib = render_contrib_block(enrichment.contributions)
        m = CONTRIB_BLOCK_RE.search(out)
        if m:
            old_inner = m.group(2)
            if force or any(p.search(old_inner) for p in GENERIC_CONTRIB) or AZ_CHAR.search(
                old_inner
            ):
                out = CONTRIB_BLOCK_RE.sub(new_contrib, out, count=1)
                changed = True

    return out, changed


_EN_DATA_PATH = HELPERS / "data" / "prominent_figure_enrichment_en.json"
_EN_CACHE: dict[str, Enrichment] | None = None


def _load_en_enrichment() -> dict[str, Enrichment]:
    global _EN_CACHE
    if _EN_CACHE is not None:
        return _EN_CACHE
    if not _EN_DATA_PATH.is_file():
        _EN_CACHE = {}
        return _EN_CACHE
    from _prominent_figure_enrichment_overrides import _to_enrichment

    data = json.loads(_EN_DATA_PATH.read_text(encoding="utf-8"))
    _EN_CACHE = {slug: _to_enrichment(entry) for slug, entry in data.items()}
    return _EN_CACHE


def apply_en_profile_enrichment(text: str, slug: str) -> str:
    """Patch EN profile sections from English enrichment dataset."""
    enrichment = _load_en_enrichment().get(slug)
    if not enrichment:
        return text
    out, _ = apply_enrichment(text, enrichment, force=True)
    return out


def needs_enrichment(text: str) -> bool:
    if GENERIC_WORK3.search(text):
        return True
    m = CONTRIB_BLOCK_RE.search(text)
    if m and any(p.search(m.group(2)) for p in GENERIC_CONTRIB):
        return True
    m = EVENTS_BLOCK_RE.search(text)
    if m and (
        GENERIC_EVENT1.search(m.group(2))
        or GENERIC_EVENT2.search(m.group(2))
        or AZ_CHAR.search(m.group(2))
    ):
        return True
    return False

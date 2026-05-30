"""Parse and render Forum 2024 official addresses from Rəsmi_müraciətlər.docx."""
from __future__ import annotations

import html
import re
from pathlib import Path

from docx import Document

from _paths import ROOT

DOCX = ROOT / "forum_2024" / "Rəsmi_müraciətlər.docx"
ASSET = "../../../"
PRESIDENT_IMAGE = f"{ASSET}images/forum/Prezidentin_müraciəti.jpg"
SCIENTISTS_IMAGE_1 = f"{ASSET}images/forum/Aimlərimizin_müraciəti_Xankəndi_1.jpg"
SCIENTISTS_IMAGE_2 = f"{ASSET}images/forum/Aimlərimizin_müraciəti_Xankəndi_2.jpg"

# Page order (DOCX section order differs: alimlerimiz is parsed 4th, shown last).
OFFICIAL_SECTION_ORDER: tuple[str, ...] = (
    "ilham-eliyev",
    "eziz-sancar",
    "arye-varshel",
    "fuad-muradov",
    "mesud-efendiyev",
    "alimlerimiz",
)


def reorder_official_sections(sections: list[dict]) -> list[dict]:
    by_id = {s["id"]: s for s in sections}
    missing = [sid for sid in OFFICIAL_SECTION_ORDER if sid not in by_id]
    if missing:
        raise SystemExit(f"official sections missing ids: {missing}")
    return [by_id[sid] for sid in OFFICIAL_SECTION_ORDER]


SECTION_SPECS: list[tuple] = [
    (
        "ilham-eliyev",
        "AZƏRBAYCAN RESPUBLİKASININ PREZİDENTİ CƏNAB İLHAM ƏLİYEVİN İŞTİRAKÇILARA MÜRACİƏTİ",
        "PREZİDENTİ CƏNAB İLHAM",
        "address",
        "",
    ),
    (
        "eziz-sancar",
        "KİMYA ÜZRƏ NOBEL MÜKAFATI LAUREATI ƏZİZ SANCARIN İŞTİRAKÇILARA MÜRACİƏTİ",
        "ƏZİZ SANCARIN",
        "address",
        "",
    ),
    (
        "arye-varshel",
        "KİMYA ÜZRƏ NOBEL MÜKAFATI LAUREATI ARYE VARŞELİN İŞTİRAKÇILARA MÜRACİƏTİ",
        "ARYE VARŞEL",
        "address",
        "",
    ),
    (
        "alimlerimiz",
        "ALİMLƏRİMİZİN AZƏRBAYCAN RESPUBLİKASININ PREZİDENTİ CƏNAB İLHAM ƏLİYEVƏ MÜRACİƏTİ",
        "ALİMLƏRİMİZİN",
        "address",
        "",
    ),
    (
        "fuad-muradov",
        "DİASPORLA İŞ ÜZRƏ DÖVLƏT KOMİTƏSİNİN SƏDRİ FUAD MURADOVUN NİTQİ",
        "FUAD MURADOV",
        "speech",
        "",
    ),
    (
        "mesud-efendiyev",
        "DÜNYA AZƏRBAYCANLI ALİMLƏR BİRLİYİNİN İDARƏ HEYƏTİNİN SƏDRİ MƏSUD ƏFƏNDİYEVİN NİTQİ",
        "MƏSUD ƏFƏNDİYEV",
        "speech",
        "",
    ),
]

SIGNOFF_RE = re.compile(
    r"^(Hörmətlə,?\s*$|İlham ƏLİYEV|Əziz SANCAR|Arye VARŞEL|Bakı,|Xankəndi,|"
    r"Məsud Əfəndiyev|DAAB İdarə Heyətinin Sədri|"
    r"\d{1,2}\s+sentyabr|Sarah Graham|Department of|University of|Member, National)",
    re.I,
)

LIST_INTRO_RE = re.compile(
    r"Forum üçün seçim meyarlarımız isə aşağıdakılar oldu:",
    re.I,
)

QUOTE_LINES = frozenset(
    {
        "Tanrı Türkü qorusun!",
        "Turana qılıncdan daha kəskin ulu qüdrət –",
        "Yalnız mədəniyyət, mədəniyyət, mədəniyyət!",
    },
)

PANEL_COPY_AZ = (
    "Bu səhifədə Prezident İlham Əliyevin təbriki, Nobel laureatlarının müraciətləri, "
    "alimlərimizin prezidentə müraciəti, Fuad Muradovun və Məsud Əfəndiyevin nitqləri "
    "yerləşdirilmişdir."
)

META_AZ = (
    "Forum 2024 — Prezident və Nobel laureatlarının müraciətləri, alimlərin müraciəti, "
    "Fuad Muradov və Məsud Əfəndiyev nitqləri."
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def _merge_raw_blocks(raw: list[dict]) -> list[dict]:
    merged: list[dict] = []
    i = 0
    while i < len(raw):
        block = raw[i]
        heading = block["heading"]
        if (
            "İDARƏ HEYƏTİNİN SƏDRİ" in heading
            and not block["paras"]
            and i + 1 < len(raw)
            and "MƏSUD" in raw[i + 1]["heading"]
        ):
            next_block = raw[i + 1]
            merged.append(
                {
                    "heading": f"{heading} {next_block['heading']}",
                    "paras": next_block["paras"],
                }
            )
            i += 2
            continue
        merged.append(block)
        i += 1
    return merged


def parse_sections_az() -> list[dict]:
    doc = Document(str(DOCX))
    raw: list[dict] = []
    cur: dict | None = None
    for para in doc.paragraphs:
        text = para.text.replace("\r", "").strip()
        if not text:
            continue
        if para.style and str(para.style.name).startswith("Heading"):
            if cur:
                raw.append(cur)
            cur = {"heading": text, "paras": []}
        elif cur is not None:
            cur["paras"].append(text)
    if cur:
        raw.append(cur)

    raw = _merge_raw_blocks(raw)
    if len(raw) != len(SECTION_SPECS):
        raise SystemExit(
            f"expected {len(SECTION_SPECS)} sections, got {len(raw)}: "
            + ", ".join(b["heading"][:40] for b in raw)
        )

    sections: list[dict] = []
    for block, spec in zip(raw, SECTION_SPECS):
        sid, title, needle, kind, header_sub = spec
        if needle not in block["heading"].upper():
            raise SystemExit(f"unexpected heading: {block['heading']!r}")
        paras = block["paras"]
        lead = ""
        body = paras
        if kind == "address" and paras and (
            paras[0].startswith("Müraciəti ")
            or paras[0].startswith("Xaricdə Yaşayan Azərbaycanlı Alimlərin Forumunun iştirakçıları")
        ):
            lead = paras[0]
            body = paras[1:]
        sections.append(
            {
                "id": sid,
                "title": title,
                "kind": kind,
                "header_subtitle": header_sub,
                "lead": lead,
                "body": body,
            }
        )
    return reorder_official_sections(sections)


def paras_to_html(paras: list[str]) -> str:
    parts: list[str] = []
    list_buf: list[str] = []
    in_list = False

    def flush_list() -> None:
        nonlocal list_buf, in_list
        if not list_buf:
            return
        items = "".join(f"<li>{esc(t)}</li>" for t in list_buf)
        parts.append(f'<ul class="content-list">{items}</ul>')
        list_buf = []
        in_list = False

    for text in paras:
        if LIST_INTRO_RE.match(text):
            flush_list()
            parts.append(f'<p class="card-text">{esc(text)}</p>')
            in_list = True
            continue
        if in_list and text in (
            "Alimlik və elmi fəaliyyət səviyyəsi",
            "Gənc, orta və yaşlı nəsil arasında balansın qorunması",
            "Dövlətçilik və vətənpərvərlik ruhu",
        ):
            list_buf.append(text)
            continue
        flush_list()
        if text in QUOTE_LINES:
            parts.append(f'<p class="card-quote">{esc(text)}</p>')
        elif SIGNOFF_RE.match(text):
            parts.append(f'<p class="card-signoff">{esc(text)}</p>')
        else:
            parts.append(f'<p class="card-text">{esc(text)}</p>')
    flush_list()
    return "\n".join(parts)


def news_card_az(section: dict) -> str:
    header_sub = ""
    if section.get("header_subtitle"):
        header_sub = (
            f'<p class="card-subtitle" role="doc-subtitle">'
            f'{esc(section["header_subtitle"])}</p>'
        )
    lead = (
        f'<p class="card-lead">{esc(section["lead"])}</p>' if section.get("lead") else ""
    )
    image_block = ""
    if section["id"] == "ilham-eliyev":
        image_block = (
            '<div class="card-gallery single">'
            f'<img src="{PRESIDENT_IMAGE}" alt="Azərbaycan Respublikasının Prezidenti İlham Əliyev" '
            'width="900" height="520" loading="lazy" decoding="async"/>'
            "</div>"
        )
    elif section["id"] == "alimlerimiz":
        image_block = (
            '<div class="card-gallery double">'
            f'<img src="{SCIENTISTS_IMAGE_1}" alt="Alimlərimizin müraciəti — Xankəndi" '
            'loading="lazy" decoding="async"/>'
            f'<img src="{SCIENTISTS_IMAGE_2}" alt="Alimlərimizin müraciəti — Xankəndi" '
            'loading="lazy" decoding="async"/>'
            "</div>"
        )
    return f"""
<article class="news-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(section["title"])}</h2>
{header_sub}
</div>
<div class="card-body">
{image_block}
{lead}
{paras_to_html(section["body"])}
</div>
</article>"""


def toc_html(sections: list[dict]) -> str:
    return "".join(
        f'<li><a href="#{esc(s["id"])}">{esc(s["title"])}</a></li>' for s in sections
    )


def cards_html_az(sections: list[dict]) -> str:
    return "\n".join(news_card_az(s) for s in sections)


EN_LIST_INTRO_RE = re.compile(
    r"The selection criteria for the forum were as follows:",
    re.I,
)

EN_LIST_ITEMS = frozenset(
    {
        "Level of scholarship and scientific activity",
        "Maintaining balance among young, middle and older generations",
        "Spirit of statehood and patriotism",
    }
)

EN_QUOTE_LINES = frozenset(
    {
        "May God protect the Turk!",
        "A supreme power sharper than a sword to Turan –",
        "Only culture, culture, culture!",
    }
)


def _en_body_blocks(section: dict) -> list[str]:
    blocks: list[str] = []
    list_buf: list[str] = []
    in_list = False

    def flush_list() -> None:
        nonlocal list_buf, in_list
        if not list_buf:
            return
        items = "".join(f"<li>{esc(t)}</li>" for t in list_buf)
        blocks.append(f'<ul class="content-list">{items}</ul>')
        list_buf = []
        in_list = False

    if section.get("subtitle"):
        blocks.append(f'<p class="card-lead">{esc(section["subtitle"])}</p>')
    for text in section.get("body", []):
        if EN_LIST_INTRO_RE.match(text):
            flush_list()
            blocks.append(f'<p class="card-text">{esc(text)}</p>')
            in_list = True
            continue
        if in_list and text in EN_LIST_ITEMS:
            list_buf.append(text)
            continue
        flush_list()
        if text in EN_QUOTE_LINES:
            blocks.append(f'<p class="card-quote">{esc(text)}</p>')
        elif SIGNOFF_RE.match(text):
            blocks.append(f'<p class="card-signoff">{esc(text)}</p>')
        else:
            blocks.append(f'<p class="card-text">{esc(text)}</p>')
    flush_list()
    if section.get("quote"):
        blocks.append(f'<p class="card-quote">{esc(section["quote"])}</p>')
    for text in section.get("signoff", []):
        blocks.append(f'<p class="card-signoff">{esc(text)}</p>')
    return blocks


def news_card_en(section: dict) -> str:
    header_sub = ""
    if section.get("header_subtitle"):
        header_sub = (
            f'<p class="card-subtitle" role="doc-subtitle">'
            f'{esc(section["header_subtitle"])}</p>'
        )
    image_block = ""
    if section.get("image") == "president":
        image_block = (
            '<div class="card-gallery single">'
            f'<img src="{PRESIDENT_IMAGE}" alt="President of the Republic of Azerbaijan Ilham Aliyev" '
            'width="900" height="520" loading="lazy" decoding="async"/>'
            "</div>"
        )
    elif section.get("image") == "scientists":
        image_block = (
            '<div class="card-gallery double">'
            f'<img src="{SCIENTISTS_IMAGE_1}" alt="Scientists\' address — Khankendi" '
            'loading="lazy" decoding="async"/>'
            f'<img src="{SCIENTISTS_IMAGE_2}" alt="Scientists\' address — Khankendi" '
            'loading="lazy" decoding="async"/>'
            "</div>"
        )
    body_inner = "\n".join(_en_body_blocks(section))
    return f"""
<article class="news-card" id="{esc(section["id"])}">
<div class="card-header">
<h2 class="card-title">{esc(section["title"])}</h2>
{header_sub}
</div>
<div class="card-body">
{image_block}
{body_inner}
</div>
</article>"""


def cards_html_en(sections: list[dict]) -> str:
    return "\n".join(news_card_en(s) for s in sections)

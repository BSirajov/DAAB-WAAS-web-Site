#!/usr/bin/env python3
"""Build bilingual site-wide search index for daab-search.js."""
from __future__ import annotations

import html
import json
import re
import unicodedata
from datetime import date
from pathlib import Path

from _paths import ROOT

ROUTES = ROOT / "i18n" / "routes.json"
UI = ROOT / "i18n" / "ui.json"
NAV = ROOT / "i18n" / "nav.json"
PROFILES = ROOT / "i18n" / "scientists-profiles.json"
OUT = ROOT / "i18n" / "search-index.json"

AZ_MAP = str.maketrans(
    {
        "ə": "e",
        "ı": "i",
        "ö": "o",
        "ü": "u",
        "ğ": "g",
        "ş": "s",
        "ç": "c",
        "Ə": "e",
        "İ": "i",
        "Ö": "o",
        "Ü": "u",
        "Ğ": "g",
        "Ş": "s",
        "Ç": "c",
    }
)

PAGE_LABEL_KEYS = {
    "home": "home",
    "foundation": "foundation",
    "mission": "mission",
    "activities": "activitiesNews",
    "activities-news": "activitiesNews",
    "forum-2024": "forum2024",
    "forum-2026": "forum2026",
    "forum-official": "forumOfficial",
    "forum-rector-speeches": "forumRectorSpeeches",
    "forum-anas-leadership-speeches": "forumAnasLeadershipSpeeches",
    "forum-program": "forumProgram",
    "forum-logistics": "forumLogistics",
    "forum-sessions-organization": "forumSessionsOrganization",
    "forum-2024-presentations": "forum2024Presentations",
    "forum-impressions": "forumImpressions",
    "forum-roadmap": "forumRoadmap",
    "forum-bagli-hekayeler": "forumBagliHekayeler",
    "forum-cooperation": "forumCooperation",
    "forum-photos-gallery": "forumPhotosGallery",
    "forum-video-gallery": "forumVideoGallery",
    "scientists-list": "scientistsList",
    "scientists-profiles": "scientistsProfiles",
    "executive-board": "executiveBoard",
    "charter": "charter",
    "membership": "membershipTerms",
    "membership-value": "membershipWhy",
    "membership-application": "membershipJoin",
    "membership-flyer": "membershipFlyer",
    "sponsors": "sponsorsProgram",
    "forum-2027-sponsorship": "forum2027Sponsorship",
    "donate": "donate",
    "sponsors-flyer": "sponsorsFlyer",
}

TYPE_BOOST = {
    "page": 12,
    "nav": 11,
    "section": 9,
    "activity": 8,
    "person": 7,
    "scientist": 6,
}

TAG_LABELS = {
    "az": {
        "page": "Səhifə",
        "nav": "Naviqasiya",
        "section": "Bölmə",
        "activity": "Fəaliyyət",
        "person": "Şəxs",
        "scientist": "Alim",
    },
    "en": {
        "page": "Page",
        "nav": "Navigation",
        "section": "Section",
        "activity": "Activity",
        "person": "Person",
        "scientist": "Scientist",
    },
}


def strip_html(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = html.unescape(text)
    return re.sub(r"\s+", " ", text).strip()


def normalize(text: str) -> str:
    text = strip_html(text)
    text = unicodedata.normalize("NFKD", text)
    text = text.translate(AZ_MAP)
    text = text.lower()
    text = re.sub(r"[^\w\s@.-]", " ", text, flags=re.UNICODE)
    return re.sub(r"\s+", " ", text).strip()


def slug_from_photo(photo: str) -> str:
    return Path(photo).stem if photo else ""


def meta_from_html(raw: str) -> tuple[str, str]:
    title = ""
    desc = ""
    m = re.search(r"<title[^>]*>([^<]+)</title>", raw, re.I | re.S)
    if m:
        title = strip_html(m.group(1))
    m = re.search(
        r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']*)["\']',
        raw,
        re.I,
    )
    if not m:
        m = re.search(
            r'<meta[^>]+content=["\']([^"\']*)["\'][^>]+name=["\']description["\']',
            raw,
            re.I,
        )
    if m:
        desc = strip_html(m.group(1))
    return title, desc


def entry(
    *,
    eid: str,
    lang: str,
    kind: str,
    page_id: str,
    title: str,
    summary: str = "",
    anchor: str = "",
    icon: str = "",
    extra: str = "",
) -> dict:
    corpus = " ".join(x for x in (title, summary, extra) if x)
    return {
        "id": eid,
        "lang": lang,
        "type": kind,
        "pageId": page_id,
        "anchor": anchor,
        "title": title,
        "summary": summary[:240],
        "tag": TAG_LABELS[lang][kind],
        "icon": icon or "📄",
        "boost": TYPE_BOOST.get(kind, 5),
        "norm": normalize(corpus),
    }


def page_icon(ui: dict, page_id: str) -> str:
    icons = ui.get("navIcons") or {}
    return icons.get(page_id, "📄")


def add_pages(entries: list[dict], routes: dict, ui: dict) -> None:
    for page in routes["pages"]:
        pid = page["id"]
        for lang in ("az", "en"):
            rel = page[lang]
            path = ROOT / rel
            if not path.is_file():
                continue
            raw = path.read_text(encoding="utf-8")
            title, desc = meta_from_html(raw)
            nav_key = PAGE_LABEL_KEYS.get(pid, pid)
            nav_title = ui["nav"][lang].get(nav_key, title)
            if not title:
                title = nav_title
            entries.append(
                entry(
                    eid=f"page-{pid}-{lang}",
                    lang=lang,
                    kind="page",
                    page_id=pid,
                    title=title,
                    summary=desc or nav_title,
                    icon=page_icon(ui, pid),
                )
            )


def _append_nav_child(
    entries: list[dict],
    ui: dict,
    lang: str,
    group_label: str,
    group_id: str,
    child: dict,
    icons: dict,
) -> None:
    if child.get("type") == "section":
        for nested in child.get("children", []):
            _append_nav_child(entries, ui, lang, group_label, group_id, nested, icons)
        return
    pid = child["id"]
    labels = ui["nav"][lang]
    key = PAGE_LABEL_KEYS.get(pid, child.get("labelKey", pid))
    title = labels.get(key, pid)
    desc = labels.get(child.get("descKey", ""), group_label)
    entries.append(
        entry(
            eid=f"nav-{pid}-{lang}",
            lang=lang,
            kind="nav",
            page_id=pid,
            title=title,
            summary=desc,
            icon=icons.get(pid, icons.get(group_id, "📄")),
            extra=group_label,
        )
    )


def add_nav(entries: list[dict], ui: dict, nav_def: dict) -> None:
    icons = ui.get("navIcons") or {}
    for lang in ("az", "en"):
        labels = ui["nav"][lang]
        for item in nav_def.get("primary", []):
            if item["type"] == "page":
                pid = item["id"]
                key = PAGE_LABEL_KEYS.get(pid, pid)
                title = labels.get(key, pid)
                desc_key = f"{key}Desc" if f"{key}Desc" in labels else None
                desc = labels.get(desc_key, "") if desc_key else title
                entries.append(
                    entry(
                        eid=f"nav-{pid}-{lang}",
                        lang=lang,
                        kind="nav",
                        page_id=pid,
                        title=title,
                        summary=desc,
                        icon=icons.get(pid, "📄"),
                    )
                )
            elif item["type"] == "group":
                group_label = labels.get(item.get("labelKey", ""), item["id"])
                for child in item.get("children", []):
                    _append_nav_child(entries, ui, lang, group_label, item["id"], child, icons)


def extract_forum_sections(raw: str, lang: str, page_id: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<article[^>]*class="[^"]*news-card[^"]*"[^>]*id="([^"]+)"[^>]*>(.*?)</article>',
        raw,
        re.I | re.S,
    ):
        anchor = m.group(1)
        block = m.group(2)
        tm = re.search(r'<h2[^>]*class="[^"]*card-title[^"]*"[^>]*>(.*?)</h2>', block, re.I | re.S)
        title = strip_html(tm.group(1)) if tm else anchor
        pm = re.search(
            r'<p[^>]*class="[^"]*card-(?:text|lead)[^"]*"[^>]*>(.*?)</p>',
            block,
            re.I | re.S,
        )
        summary = strip_html(pm.group(1))[:240] if pm else ""
        out.append(
            entry(
                eid=f"section-{page_id}-{anchor}-{lang}",
                lang=lang,
                kind="section",
                page_id=page_id,
                title=title,
                summary=summary,
                anchor=anchor,
                icon="🎤",
            )
        )
    return out


def extract_forum_stories(raw: str, lang: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<article[^>]*class="[^"]*story-card[^"]*"[^>]*id="([^"]+)"[^>]*>(.*?)</article>',
        raw,
        re.I | re.S,
    ):
        anchor = m.group(1)
        block = m.group(2)
        hm = re.search(r'<h2[^>]*>(.*?)</h2>', block, re.I | re.S)
        title = strip_html(hm.group(1)) if hm else anchor
        pm = re.search(r'<div[^>]*class="[^"]*story-body[^"]*"[^>]*>(.*?)</div>', block, re.I | re.S)
        summary = strip_html(pm.group(1))[:240] if pm else ""
        out.append(
            entry(
                eid=f"section-forum-impressions-{anchor}-{lang}",
                lang=lang,
                kind="section",
                page_id="forum-impressions",
                title=title,
                summary=summary,
                anchor=anchor,
                icon="💬",
            )
        )
    return out


def extract_activities(raw: str, lang: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<article[^>]*class="[^"]*news-card[^"]*"[^>]*id="([^"]+)"[^>]*>(.*?)</article>',
        raw,
        re.I | re.S,
    ):
        anchor = m.group(1)
        block = m.group(2)
        tm = re.search(r'<h2[^>]*class="[^"]*card-title[^"]*"[^>]*>(.*?)</h2>', block, re.I | re.S)
        title = strip_html(tm.group(1)) if tm else anchor
        pm = re.search(r'<p[^>]*class="[^"]*card-text[^"]*"[^>]*>(.*?)</p>', block, re.I | re.S)
        summary = strip_html(pm.group(1))[:240] if pm else ""
        out.append(
            entry(
                eid=f"activity-{anchor}-{lang}",
                lang=lang,
                kind="activity",
                page_id="activities-news",
                title=title,
                summary=summary,
                anchor=anchor,
                icon="📰",
            )
        )
    return out


def extract_foundation_sections(raw: str, lang: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<section[^>]*id="([^"]+)"[^>]*class="[^"]*section-block[^"]*"[^>]*>(.*?)</section>',
        raw,
        re.I | re.S,
    ):
        anchor = m.group(1)
        block = m.group(2)
        hm = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.I | re.S)
        title = strip_html(hm.group(1)) if hm else anchor
        pm = re.search(r"<p[^>]*>(.*?)</p>", block, re.I | re.S)
        summary = strip_html(pm.group(1))[:240] if pm else ""
        out.append(
            entry(
                eid=f"section-foundation-{anchor}-{lang}",
                lang=lang,
                kind="section",
                page_id="foundation",
                title=title,
                summary=summary,
                anchor=anchor,
                icon="🏛️",
            )
        )
    return out


def extract_mission_sections(raw: str, lang: str) -> list[dict]:
    out: list[dict] = []
    patterns = [
        (r'<article[^>]*id="([^"]+)"[^>]*class="[^"]*core-card[^"]*"[^>]*>(.*?)</article>', "article"),
        (r'<div[^>]*class="[^"]*vd-item[^"]*"[^>]*id="([^"]+)"[^>]*>(.*?)</div>', "div"),
    ]
    for pat, _ in patterns:
        for m in re.finditer(pat, raw, re.I | re.S):
            anchor = m.group(1)
            block = m.group(2)
            hm = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.I | re.S)
            if not hm:
                hm = re.search(r"<h3[^>]*>(.*?)</h3>", block, re.I | re.S)
            title = strip_html(hm.group(1)) if hm else anchor
            pm = re.search(r"<p[^>]*>(.*?)</p>", block, re.I | re.S)
            summary = strip_html(pm.group(1))[:240] if pm else ""
            out.append(
                entry(
                    eid=f"section-mission-{anchor}-{lang}",
                    lang=lang,
                    kind="section",
                    page_id="mission",
                    title=title,
                    summary=summary,
                    anchor=anchor,
                    icon="💎",
                )
            )
    return out


def extract_charter_sections(raw: str, lang: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<section[^>]*class="[^"]*charter-card[^"]*"[^>]*id="([^"]+)"[^>]*>(.*?)</section>',
        raw,
        re.I | re.S,
    ):
        anchor = m.group(1)
        block = m.group(2)
        hm = re.search(r"<h2[^>]*>(.*?)</h2>", block, re.I | re.S)
        title = strip_html(hm.group(1)) if hm else anchor
        pm = re.search(r"<p[^>]*>(.*?)</p>", block, re.I | re.S)
        summary = strip_html(pm.group(1))[:240] if pm else ""
        out.append(
            entry(
                eid=f"section-charter-{anchor}-{lang}",
                lang=lang,
                kind="section",
                page_id="charter",
                title=title,
                summary=summary,
                anchor=anchor,
                icon="📜",
            )
        )
    return out


def extract_board_members(raw: str, lang: str) -> list[dict]:
    out: list[dict] = []
    for m in re.finditer(
        r'<h2[^>]*class="[^"]*person-name[^"]*"[^>]*>(.*?)</h2>(.*?)(?=<h2|$)',
        raw,
        re.I | re.S,
    ):
        title = strip_html(m.group(1))
        block = m.group(2)
        pm = re.search(r'<p[^>]*class="[^"]*person-role[^"]*"[^>]*>(.*?)</p>', block, re.I | re.S)
        summary = strip_html(pm.group(1)) if pm else "Executive Board"
        slug = normalize(title).replace(" ", "-")[:48] or "member"
        out.append(
            entry(
                eid=f"person-board-{slug}-{lang}",
                lang=lang,
                kind="person",
                page_id="executive-board",
                title=title,
                summary=summary,
                icon="🎓",
            )
        )
    return out


def add_scientists(entries: list[dict], profiles: dict) -> None:
    for p in profiles.get("profiles", []):
        slug = slug_from_photo(p.get("photo", ""))
        email = (p.get("email") or "").strip()
        for lang in ("az", "en"):
            name = p.get("name") if lang == "az" else p.get("name_en", p.get("name", ""))
            country = p.get("country_az") if lang == "az" else p.get("country_en", p.get("country_az", ""))
            field = p.get("field_az") if lang == "az" else p.get("field_en", p.get("field_az", ""))
            title_line = p.get("title_az") if lang == "az" else p.get("title_en", p.get("title_az", ""))
            bio_key = "bio_html_az" if lang == "az" else "bio_html_en"
            bio = strip_html(p.get(bio_key, ""))[:320]
            summary = " · ".join(x for x in (title_line, field, country) if x)
            entries.append(
                entry(
                    eid=f"scientist-{slug}-{lang}",
                    lang=lang,
                    kind="scientist",
                    page_id="scientists-profiles",
                    title=name,
                    summary=summary,
                    anchor=slug,
                    icon="👤",
                    extra=" ".join(x for x in (email, bio, p.get("degree", "")) if x),
                )
            )


def build() -> dict:
    routes = json.loads(ROUTES.read_text(encoding="utf-8"))
    ui = json.loads(UI.read_text(encoding="utf-8"))
    nav_def = json.loads(NAV.read_text(encoding="utf-8"))
    profiles = json.loads(PROFILES.read_text(encoding="utf-8"))

    entries: list[dict] = []
    add_pages(entries, routes, ui)
    add_nav(entries, ui, nav_def)

    page_loaders = {
        "activities-news": extract_activities,
        "foundation": extract_foundation_sections,
        "mission": extract_mission_sections,
        "charter": extract_charter_sections,
        "executive-board": extract_board_members,
        "forum-official": lambda raw, lang: extract_forum_sections(raw, lang, "forum-official"),
        "forum-rector-speeches": lambda raw, lang: extract_forum_sections(
            raw, lang, "forum-rector-speeches"
        ),
        "forum-anas-leadership-speeches": lambda raw, lang: extract_forum_sections(
            raw, lang, "forum-anas-leadership-speeches"
        ),
        "forum-program": lambda raw, lang: extract_forum_sections(raw, lang, "forum-program"),
        "forum-impressions": lambda raw, lang: extract_forum_sections(raw, lang, "forum-impressions"),
        "forum-2024-presentations": lambda raw, lang: extract_forum_sections(raw, lang, "forum-2024-presentations"),
        "forum-roadmap": lambda raw, lang: extract_forum_sections(raw, lang, "forum-roadmap"),
        "forum-bagli-hekayeler": lambda raw, lang: extract_forum_sections(
            raw, lang, "forum-bagli-hekayeler"
        ),
        "forum-cooperation": lambda raw, lang: extract_forum_sections(
            raw, lang, "forum-cooperation"
        ),
    }
    for page in routes["pages"]:
        pid = page["id"]
        loader = page_loaders.get(pid)
        if not loader:
            continue
        for lang in ("az", "en"):
            rel = page.get(lang)
            if not rel:
                continue
            path = ROOT / rel
            if path.is_file():
                entries.extend(loader(path.read_text(encoding="utf-8"), lang))

    add_scientists(entries, profiles)

    # Deduplicate by id (keep first)
    seen: set[str] = set()
    unique: list[dict] = []
    for e in entries:
        if e["id"] in seen:
            continue
        seen.add(e["id"])
        unique.append(e)

    return {
        "version": 1,
        "generated": date.today().isoformat(),
        "entryCount": len(unique),
        "entries": unique,
    }


def main() -> None:
    data = build()
    OUT.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT.relative_to(ROOT)} ({data['entryCount']} entries)")


if __name__ == "__main__":
    main()

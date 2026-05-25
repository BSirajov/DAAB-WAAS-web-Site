"""English copy for Forum 2024 stories page (Eldar Akhadov)."""

from __future__ import annotations

from stories_en_paragraphs import ILHAM_JIDIR_QUOTE, PARAGRAPHS, TITLES


def _en_sections() -> list[dict]:
    sections: list[dict] = []
    for sid in ("nur", "veten-hissleri", "cidir-duzu", "xedice"):
        paragraphs: list[dict] = []
        if sid == "cidir-duzu":
            paragraphs.append(
                {"type": "quote", "text": ILHAM_JIDIR_QUOTE["text"], "cite": ILHAM_JIDIR_QUOTE["cite"]}
            )
        for text in PARAGRAPHS[sid]:
            paragraphs.append({"type": "p", "text": text})
        sections.append({"id": sid, "title": TITLES[sid], "paragraphs": paragraphs})
    return sections


STORIES_EN = {
    "page_title": "Stories of the forum — WAAS",
    "meta_description": (
        "Literary reflections by Eldar Akhadov on the First Forum of Azerbaijani Scientists Living Abroad."
    ),
    "breadcrumb": "Stories of the forum",
    "hero_h1": "Stories <span>of the forum</span>",
    "panel_title": "Light, homeland and memory",
    "panel_copy": (
        "Personal literary essays by Eldar Akhadov — impressions of the forum, the journey to "
        "Karabakh and meetings that became lifelong memories."
    ),
    "sidebar_label": "📖 Stories of the forum",
    "sidebar_aria": "Open stories of the forum menu",
    "doc_title": "ELDAR AKHADOV'S STORIES OF THE FORUM",
    "sections": _en_sections(),
}

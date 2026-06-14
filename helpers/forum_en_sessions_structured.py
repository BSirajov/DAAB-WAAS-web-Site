"""English structured content for Forum sessions organization page."""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from _paths import ROOT

_TRANSLATIONS_PATH = ROOT / "helpers" / "data" / "sessions_translations_en.json"
_TRANSLATIONS: dict[str, str] | None = None


def _load_translations() -> dict[str, str]:
    global _TRANSLATIONS
    if _TRANSLATIONS is None:
        _TRANSLATIONS = json.loads(_TRANSLATIONS_PATH.read_text(encoding="utf-8"))
    return _TRANSLATIONS


def translate_text(text: str) -> str:
    return _load_translations().get(text, text)


def translate_blocks(blocks: list[dict[str, Any]]) -> list[dict[str, Any]]:
    translated: list[dict[str, Any]] = []
    for block in blocks:
        copy_block = copy.deepcopy(block)
        if copy_block.get("type") == "heading":
            copy_block["text"] = translate_text(copy_block["text"])
        elif copy_block.get("type") == "paragraph":
            copy_block["text"] = translate_text(copy_block["text"])
        elif copy_block.get("type") == "list":
            items: list[dict[str, Any]] = []
            for item in copy_block.get("items", []):
                items.append(
                    {
                        "text": translate_text(item["text"]),
                        "children": [translate_text(child) for child in item.get("children", [])],
                    }
                )
            copy_block["items"] = items
        translated.append(copy_block)
    return translated


def localize_structured_section(section: dict[str, Any]) -> dict[str, Any]:
    localized = copy.deepcopy(section)
    localized["title"] = translate_text(section.get("title", ""))
    localized["blocks"] = translate_blocks(section.get("blocks", []))
    return localized

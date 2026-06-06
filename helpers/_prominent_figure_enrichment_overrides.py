#!/usr/bin/env python3
"""Curated enrichment overrides for template azturk prominent-figure profiles."""
from __future__ import annotations

import json
from pathlib import Path

from _paths import HELPERS
from _prominent_figure_enrichment import Enrichment

_DATA_PATH = HELPERS / "data" / "prominent_figure_enrichment_azturk.json"


def _to_enrichment(raw: dict) -> Enrichment:
    works_raw = raw["works"]
    if works_raw and isinstance(works_raw[0], dict):
        works = [(w["title"], w["desc"]) for w in works_raw]
    else:
        works = [(str(a), str(b)) for a, b in works_raw]

    events_raw = raw["events"]
    if events_raw and isinstance(events_raw[0], dict):
        events = [(e["emoji"], e["title"], e["text"]) for e in events_raw]
    else:
        events = [(str(a), str(b), str(c)) for a, b, c in events_raw]

    return Enrichment(
        society=raw.get("society"),
        works=works,
        events=events,
        contributions=[str(c) for c in raw["contributions"]],
    )


def _load() -> dict[str, Enrichment]:
    if not _DATA_PATH.is_file():
        return {}
    data = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
    return {slug: _to_enrichment(entry) for slug, entry in data.items()}


OVERRIDES: dict[str, Enrichment] = _load()

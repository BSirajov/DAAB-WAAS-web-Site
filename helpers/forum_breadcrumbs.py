"""Canonical static breadcrumb markup for forum/2024 subpages."""
from __future__ import annotations

import html

FORUM_CRUMB_HUB = "I Forum"

LABELS = {
    "az": {"home": "Ana səhifə", "aria": "Səhifə yolu"},
    "en": {"home": "Home", "aria": "Breadcrumb"},
}


def forum_breadcrumb_html(lang: str, current: str, *, asset_up: str = "../../") -> str:
    """Single-line forum breadcrumb block (matches stories.html / program.html pattern)."""
    labels = LABELS.get(lang, LABELS["en"])
    home = html.escape(labels["home"])
    hub = html.escape(FORUM_CRUMB_HUB)
    cur = html.escape((current or "").strip())
    aria = html.escape(labels["aria"])
    return (
        f'<div class="breadcrumbs forum-breadcrumbs" role="navigation" aria-label="{aria}">'
        f'<a href="{asset_up}index.html">{home}</a><span aria-hidden="true">›</span>'
        f'<a href="index.html">{hub}</a><span aria-hidden="true">›</span>'
        f'<span class="forum-breadcrumbs-current" aria-current="page">{cur}</span>'
        f"</div>"
    )


def forum_breadcrumb_inner(lang: str, current: str) -> str:
    """Inner crumb links only (for multi-line wrapper templates)."""
    labels = LABELS.get(lang, LABELS["en"])
    home = html.escape(labels["home"])
    hub = html.escape(FORUM_CRUMB_HUB)
    cur = html.escape((current or "").strip())
    return (
        f'<a href="../../index.html">{home}</a><span aria-hidden="true">›</span>'
        f'<a href="index.html">{hub}</a><span aria-hidden="true">›</span>'
        f'<span class="forum-breadcrumbs-current" aria-current="page">{cur}</span>'
    )

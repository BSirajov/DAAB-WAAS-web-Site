"""Shared head assets for Forum 2024 inner pages — keep in sync with live az/en/forum/2024/*.html."""
from __future__ import annotations

from _page_shell_assets import STANDARD_SHELL_SCRIPTS, script_tag
from _site_wide_cleanup import STYLE_VERSIONS

# CSS loaded on typical forum inner pages (official, stories, roadmap, …).
FORUM_INNER_CSS: tuple[str, ...] = (
    "daab-fonts.css",
    "daab-common.css",
    "daab-perf.css",
    "daab-mobile.css",
    "daab-sticky-chrome.css",
    "daab-search.css",
    "daab-back-to-top.css",
    "daab-lang.css",
    "daab-nav-mega.css",
    "daab-hero-summary.css",
    "daab-sidebar-widget.css",
    "daab-activities-layout.css",
    "daab-forum-content.css",
)


def css_link(asset: str, filename: str) -> str:
    version = STYLE_VERSIONS.get(filename, 1)
    return f'<link href="{asset}css/{filename}?v={version}" rel="stylesheet"/>'


def forum_inner_stylesheets(asset: str, *, extra: tuple[str, ...] = ()) -> str:
    names = FORUM_INNER_CSS + extra
    return "\n".join(css_link(asset, name) for name in names)


def forum_inner_shell_scripts(asset: str) -> str:
    js_root = f"{asset}js/"
    return "\n".join(script_tag(js_root, name) for name in STANDARD_SHELL_SCRIPTS)


def forum_breadcrumb_home_label(lang: str) -> str:
    return "Home" if lang == "en" else "Ana səhifə"


def forum_breadcrumb_hub_label(lang: str) -> str:
    return "I Forum" if lang == "en" else "I Forum"

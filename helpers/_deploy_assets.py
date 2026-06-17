#!/usr/bin/env python3
"""Single manifest for build-only, optional, and dynamically loaded site assets."""
from __future__ import annotations

# Linked from daab-common.css (@import), not per-page HTML.
IMPORTED_VIA_COMMON_CSS = frozenset(
    {
        "daab-tokens.css",
        "daab-site-background.css",
    }
)

# CSS kept for helpers / unpublished pages — omit from production deploy.
BUILD_ONLY_CSS = frozenset(
    {
        "daab-forum-book.css",  # helpers/_build_forum_2024_site.py, forum_2024 book HTML
        "daab-membership-page.css",  # legacy membership layout; membership.html redirects
        "daab-encyclopedia-page.css",  # knowledge treasury / encyclopedia (unpublished)
        "daab-prominent-figure-profile.css",  # prominent_figures/* (unpublished)
    }
)

# Bundled in some deploy flows but not linked per-page from az/en HTML.
DEPLOY_PACKAGED_CSS = frozenset(
    {
        "daab-sticky-chrome.css",
    }
)

# Future / alternate site modules — safe to omit from deploy until wired.
OPTIONAL_JS = frozenset(
    {
        "prominent-figures-catalog.js",
        "prominent-figures-catalog-data.js",
        "prominent-figures-catalog-data-en.js",
    }
)

# Injected at runtime (see js/daab-perf.js), not a static <script src> in HTML.
DYNAMIC_JS = frozenset(
    {
        "daab-profile-tts.js",  # scientists/profiles.html via deferProfileTts()
    }
)

# Paths listed in .deployignore (css/… or js/…).
DEPLOYIGNORE_ASSET_PATHS = tuple(
    sorted(f"css/{name}" for name in BUILD_ONLY_CSS)
    + sorted(f"js/{name}" for name in OPTIONAL_JS)
)

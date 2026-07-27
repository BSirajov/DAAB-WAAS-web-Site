#!/usr/bin/env python3
"""Single manifest for build-only, optional, and dynamically loaded site assets."""
from __future__ import annotations

# Source files inlined into daab-common.css (do not link separately in HTML).
# Re-sync with: python helpers/_sync_common_css_inlines.py
INLINED_INTO_COMMON_CSS = frozenset(
    {
        "daab-tokens.css",
        "daab-site-background.css",
    }
)

# Backward-compatible alias for older audit scripts.
IMPORTED_VIA_COMMON_CSS = INLINED_INTO_COMMON_CSS

# CSS kept for helpers / unpublished pages — omit from production deploy.
BUILD_ONLY_CSS = frozenset(
    {
        "daab-forum-book.css",  # helpers/_build_forum_2024_site.py, forum_2024 book HTML
        "daab-membership-page.css",  # legacy membership layout; membership.html redirects
    }
)

# Bundled in some deploy flows but not linked per-page from az/en HTML.
DEPLOY_PACKAGED_CSS = frozenset(
    {
        "daab-sticky-chrome.css",
    }
)

# Future / alternate site modules — safe to omit from deploy until wired.
OPTIONAL_JS: frozenset[str] = frozenset()

# Injected at runtime (see js/daab-perf.js / daab-analytics.js), not always a static <script src>.
DYNAMIC_JS = frozenset(
    {
        "daab-profile-tts.js",  # scientists/profiles.html via deferProfileTts()
        "daab-cookie-consent.js",  # injected by daab-analytics.js ensureCookieConsentScript()
    }
)

# CSS loaded dynamically (not always a static <link> in HTML).
DYNAMIC_CSS = frozenset(
    {
        "daab-cookie-banner.css",  # injected by daab-cookie-consent.js
    }
)

# Paths listed in .deployignore (css/… or js/…).
DEPLOYIGNORE_ASSET_PATHS = tuple(
    sorted(f"css/{name}" for name in BUILD_ONLY_CSS)
    + sorted(f"js/{name}" for name in OPTIONAL_JS)
)

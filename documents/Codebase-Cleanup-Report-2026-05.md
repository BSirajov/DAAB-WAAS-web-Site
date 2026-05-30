# Codebase cleanup report (May 2026)

This pass focused on **safe, verifiable maintenance** for the static DAAB/WAAS site. A full removal of every unused CSS selector or consolidation of all page-specific styles would require visual regression testing on dozens of pages and is **not** completed in one step.

## What was done

### 1. Site-wide asset version alignment

- Updated `helpers/_site_wide_cleanup.py` with canonical `?v=` numbers for shared CSS/JS (aligned with `en/application.html`, Forum 2024 hub, and recent forum builds).
- Ran `python helpers/_site_wide_cleanup.py` across all `az/` and `en/` deploy HTML so browsers do not mix stale cached bundles across pages.

### 2. Repository health audit tool

- Added `helpers/_audit_repo_health.py` — reports path validation, `?v=` drift, orphan asset links, and duplicate `lang` attributes.
- Run after substantive changes: `python helpers/_audit_repo_health.py`

### 3. Path validation

- `python helpers/_validate_site.py` — **no broken local references** in deploy HTML (images, CSS, JS, fonts).

## What was not removed (intentionally)

| Asset | Reason |
|--------|--------|
| `css/daab-forum-book.css` | **Build-only** — used by `helpers/_build_forum_2024_site.py`; omitted from deploy via `.deployignore` |
| `css/daab-site-background.css` | Loaded via `@import` in `daab-common.css` |
| `css/daab-sticky-chrome.css` | Used in deployment packaging; profiles use `scientists-profiles-sticky.css` |
| `js/daab-story-tts.js` | Story read-aloud feature implemented but **not wired** on live `stories.html`; CSS hooks remain in `daab-forum-content.css` |
| `helpers/` Python scripts | Maintenance/build only — never deployed per stability guide |

## Remaining work (recommended follow-up)

1. **CSS dead selectors** — Run `python helpers/_audit_css_usage.py css/<file>.css az en` per stylesheet; remove only classes confirmed unused in HTML **and** JS.
2. **HTML generators** — Bump `?v=` in `_build_*` templates when editing shared CSS/JS so rebuilds do not reintroduce drift.
3. **Scientists profiles sticky** — If long profile pages need fixed chrome offsets, run `python helpers/_inject_profiles_sticky.py`.
4. **Story TTS** — Either link `daab-story-tts.js` on `stories.html` or move script/CSS to `_archive` if the feature is abandoned.
5. **Visual QA** — Desktop, tablet, and mobile spot-check: home, Forum hub, one speech page, scientists list/profiles, membership application.

## Architecture notes (for maintainers)

- **Live site:** `az/`, `en/`, `css/`, `js/`, `images/`, `i18n/`
- **Do not deploy:** `helpers/`, `documents/`, `forum_2024/` docx sources
- **i18n:** Nav labels from `i18n/ui.json` + `js/daab-primary-nav.js` when `data-daab-nav-mount="1"`
- **Regenerate content pages** from docx via matching `helpers/_build_*.py` rather than hand-editing large HTML blocks

## Commands checklist

```bash
python helpers/_validate_site.py
python helpers/_audit_repo_health.py
python helpers/_site_wide_cleanup.py
```

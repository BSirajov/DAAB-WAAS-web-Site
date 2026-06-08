# DAAB site audit and cleanup report

**Date:** 2026-05-24  
**Scope:** Live bilingual tree (`az/`, `en/`), shared assets (`css/`, `js/`, `images/`), helpers, gateway (`index.html`).

## Automated checks (all passing after cleanup)

| Command | Result |
|---------|--------|
| `python helpers/_validate_site.py` | OK — 1765+ local references, no broken paths |
| `python helpers/_validate_bilingual.py` | OK — 9 AZ/EN page pairs, sitemap, robots |
| `python helpers/_validate_section_anchors.py` | OK — activities, charter, foundation, mission |

## Issues found and fixes applied

### 1. Stale shared asset versions (fixed)

Three pages were still loading older navigation/shell CSS and JS, which caused inconsistent mobile nav, search placement, and header layout compared with the rest of the site.

| Page | Was | Now (site baseline) |
|------|-----|---------------------|
| `az/executive-board.html` | common v18, mobile v3, nav/shell v7, lang v7 | common **21**, mobile **4**, nav **8**, shell **9**, lang **9** |
| `en/executive-board.html` | same | same |
| `az/scientists/profiles.html` | common v18, mobile v3, nav/shell v7 | aligned with `en/scientists/profiles.html` |

**Also:** `en/scientists/profiles.html` — `scientists-profile-deep-link.css` bumped **v1 → v2** to match AZ.

**Maintenance:** `python helpers/_sync_live_shell_assets.py` re-applies baseline version bumps on all `az/` and `en/` HTML.

### 2. Head load order on executive board (fixed)

`daab-lang.css` and `daab-nav-mega.css` were inserted after `<script>` tags. All stylesheet links now load before deferred scripts (matches `mission.html` and `index.html`).

### 3. Head load order on AZ scientists profiles (fixed)

Same CSS-before-scripts ordering applied at the bottom of the `<head>` block.

### 4. Previously reported gaps (already addressed in this branch)

| Item | Status |
|------|--------|
| Global search on Board of Directors | Injected via `_inject_global_search.py` |
| Back-to-top control | `daab-back-to-top.css` / `.js` on all live pages |
| Board member QR codes | `board-card-qr-link` on executive board cards |
| Board terminology (EN/AZ role labels) | Updated + `_update_board_terminology.py` |

## No action required (verified OK)

- **Broken local asset paths:** None reported by `_validate_site.py`.
- **Obsolete root filenames in links:** Validator watches for old `Scientists_AZ.html`-style targets; none in live tree.
- **Bilingual structure:** Nine mirrored page pairs under `az/` and `en/`; routes in `i18n/routes.json`.
- **File organization:** Web assets under `css/`, `js/`, `images/`; maintenance under `helpers/`; internal docs under `documents/` (per `.cursor/rules`).
- **Live pages:** `az/` and `en/` trees only; root `index.html` is the language gateway.

## Known items for future work (not changed in this pass)

| Item | Recommendation |
|------|----------------|
| `images/board-members-photos/bakhtiyar-sirajov 1.png` | Unused duplicate; safe to delete after confirming no external links |
| Large inline `<style>` blocks on activities, charter, scientists profiles | Gradual extraction to `css/` when those pages are next edited |
| `sources/home_az.html` | Build source only; not served — keep in repo for regeneration |
| `forum_2024/` HTML | Legacy section; uses current `daab-common.css?v=21` but no full shell — OK as archive |
| Asset version drift after manual edits | Run `_sync_live_shell_assets.py` + inject helpers before deploy |
| Board photo background removal | Reverted per feedback; originals restored from git |

## Site baseline (deploy reference)

Use these versions on all live `az/` and `en/` pages unless a page-specific file has its own bump:

| Asset | Version |
|-------|---------|
| `daab-common.css` | 21 |
| `daab-mobile.css` | 4 |
| `daab-lang.css` | 9 |
| `daab-nav-mega.css` | 11 |
| `daab-search.css` | 1 |
| `daab-back-to-top.css` | 1 |
| `daab-i18n.js` | 12 |
| `daab-lang-position.js` | 4 |
| `daab-nav.js` | 8 |
| `daab-primary-nav.js` | 8 |
| `daab-shell.js` | 9 |
| `daab-search.js` | 3 |
| `daab-back-to-top.js` | 2 |

## Pre-deploy checklist

1. `python helpers/_validate_site.py`
2. `python helpers/_validate_bilingual.py`
3. `python helpers/_sync_live_shell_assets.py` (if any HTML was hand-edited)
4. Hard-refresh test: index, activities, charter, scientists profiles, executive board (AZ + EN)
5. Mobile: nav menu, search overlay, back-to-top, language switch, scientists filter toolbar

## Related docs

- `documents/DAAB-Site-Stability-and-Deployment-Guide.md`
- `documents/DAAB-Deployment-and-Change-Tracking-Guide.md`
- `documents/DAAB-Navigation-and-Information-Architecture-Strategy.md`

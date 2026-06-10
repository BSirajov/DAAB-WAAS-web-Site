# DAAB site — comprehensive cleanup audit (May 2026)

> **Update (June 2026):** The in-page section navigation strip (`daab-section-nav.js`) was later removed. Sibling pages are listed in the primary nav mega-menu; forum pages use static `.forum-breadcrumbs`. Rows below that reference section pills describe May 2026 work only.

This document records a full-repository technical review of the static DAAB/WAAS bilingual site: findings, fixes applied, and recommended follow-up work. It complements `documents/DAAB-Site-Stability-and-Deployment-Guide.md`.

---

## Executive summary

| Area | Status before | Status after |
|------|---------------|--------------|
| Broken local asset paths (`_validate_site.py`) | **30 errors** (foundation gallery images) | **0 errors** |
| Membership section pills (raw page IDs) | Broken labels on several pages | Fixed via `daab-section-nav.js` + static HTML on membership cluster |
| Shared JS/CSS cache versions | Mixed `?v=4`–`v=7` across pages | Unified on deployable `az/` and `en/` pages (canonical versions from `en/application.html`) |
| Site search index nav titles | Raw `membership-value` / `membership-application` | Rebuilt with human labels |
| Forum shared CSS (`daab-forum-content.css`) | Broken selectors for photos/video gallery | **Repaired**; `?v=5` on forum pages |

**Automated validation:** `python helpers/_validate_site.py` → **OK — no broken local paths detected.**

---

## Architecture (verified)

| Asset type | Location | Notes |
|------------|----------|--------|
| Live HTML | `az/`, `en/`, root `index.html` (language gateway) | Lowercase filenames; `data-daab-lang`, `data-daab-page-id`, `data-daab-asset-root` |
| CSS | `css/` only | `daab-common.css` + page-specific sheets |
| JS | `js/` only | Nav shell: `daab-i18n`, `daab-nav`, `daab-primary-nav`, `daab-breadcrumbs`, `daab-section-nav`, `daab-shell`, `daab-search` |
| i18n | `i18n/routes.json`, `ui.json`, `nav.json`, `search-index.json` | Drives routing, labels, search |
| Images | `images/` (incl. `images/activities/`) | No duplicate assets at repo root |
| Helpers | `helpers/` | Not deployed; maintenance scripts |
| Internal docs | `documents/` | Not deployed |
| Legacy | `_archive/`, `sources/` | Not deployed |

**Do not deploy:** `helpers/`, `documents/`, `_archive/`, `sources/`.

---

## Fixes applied in this cleanup

### 1. Foundation gallery images (critical)

**Issue:** `az/foundation.html` and `en/foundation.html` referenced  
`../images/Şuşa qurultayı (...).jpg` and `../images/DAAD, İstanbul görüşü, ...` but files live under `images/activities/`.

**Fix:** Paths updated to `../images/activities/...` on both foundation pages.

### 2. Membership section navigation (AZ + EN)

**Issue:** Injected section pills showed raw IDs (`membership-value`, `membership`, `membership-application`) when `daab-section-nav.js` lacked label keys or cached old script versions.

**Fixes:**
- `js/daab-section-nav.js` — `PAGE_LABEL_KEYS` and fallbacks for membership group.
- Static `<nav class="daab-section-nav">` on:
  - `az/application.html`, `en/application.html`
  - `az/membership.html`, `en/membership.html`
  - `az/membership_value.html`, `en/membership_value.html` (via `helpers/_site_wide_cleanup.py`)
- Labels:
  - **EN:** Why become a member | Membership terms | Join us
  - **AZ:** Niyə üzv olmalı | Üzvlük şərtləri | Bizə qoşulun

### 3. Asset cache-busting (`?v=`)

**Issue:** Deployable pages used inconsistent versions (e.g. `daab-section-nav.js?v=4` while membership fixes required `v=7`).

**Fix:** `helpers/_site_wide_cleanup.py` bumped shared assets on **36** deployable pages to canonical versions:

| Asset | Version |
|-------|---------|
| `daab-common.css` | 26 |
| `daab-mobile.css` | 5 |
| `daab-lang.css` | 10 |
| `daab-nav-mega.css` | 13 |
| `daab-i18n.js` | 12 |
| `daab-lang-position.js` | 7 |
| `daab-nav.js` | 13 |
| `daab-primary-nav.js` | 13 |
| `daab-breadcrumbs.js` | 6 |
| `daab-section-nav.js` | 7 |
| `daab-shell.js` | 11 |
| `daab-search.js` | 4 |

`helpers/_sync_primary_nav.py` version table updated for future nav sync runs.

### 4. Search index labels

**Issue:** `i18n/search-index.json` nav entries used raw page IDs for membership submenu.

**Fix:** `helpers/_build_search_index.py` — added `membership-value` → `membershipWhy`, `membership-application` → `membershipJoin`, `membership` → `membershipTerms`; index rebuilt.

### 5. Azerbaijani application intro copy

**Issue:** Redundant English paragraph in AZ form intro (removed in prior edit).

**Status:** AZ intro copy aligned on live `az/application.html`.

---

## Remaining warnings (expected, non-blocking)

None for deployable pages. Run `python helpers/_validate_site.py` after substantive HTML/path changes.

---

## Full-refactor pass (May 2026 — scoped)

A site-wide “remove every unused CSS class / JS function” pass was **not** automated: the deployable surface is ~200 HTML/CSS/JS files with shared shells, inline legacy styles on some pages, and builder-generated fragments. Doing that safely requires dedicated tooling (coverage against live DOM per page) and risks breaking forum, scientists, and application flows.

**Completed in this pass:**

| Item | Action |
|------|--------|
| `css/daab-forum-content.css` | Repaired **51+** broken selector groups where `forum-photos-gallery` / `forum-video-gallery` lacked descendant suffixes; deduplicated corrupted `.widget-head` and `scroll-behavior` blocks (`helpers/_fix_forum_css_pairs.py` + manual edits). Cache bumped to `?v=5` on all `az/forum/` and `en/forum/` pages. |
| `helpers/_tmp_video_gallery.html` | **Removed** (~305 KB scratch file; not referenced). |

**Still recommended (manual / scripted follow-up):**

- Unused CSS/JS audit per page (no project-wide dead-code scanner yet).
- `_archive/`, `sources/` — keep out of deploy; prune only after confirming no external links.
- Harmonize mixed `?v=` on non-forum pages when those assets change.
- Keyboard + mobile QA checklist below (unchanged).

---

## Issues documented for follow-up (not auto-fixed)

### Content and legacy references

| Item | Location | Recommendation |
|------|----------|------------------|
| Legacy route names in metadata | `i18n/routes.json` (`legacy` fields) | Keep for redirects/docs only |
| Archive HTML | `_archive/*.html` | Keep out of deploy; delete only after confirming no external links |
| `sources/home_az.html` | Build source for `az/index.html` — keep in repo |
| EN membership hero CTA | `en/membership.html` — “Join our Association” | Consider aligning wording with “Join us” for consistency |
| AZ membership hero CTA | `az/membership.html` — “Birliyimizə üzv olun” | OK; optional align with “Bizə qoşulun” |

### UI/UX consistency (reviewed, low risk)

| Pattern | Observation |
|---------|-------------|
| Hero layouts | Membership cluster uses shared hero + `daab-hero-summary.css`; forum uses `daab-forum-*`; scientists profiles use sticky sidebar + QR |
| Footer | `footer-pro` shared via extraction from `membership.html` in builders — consistent |
| Typography | `Inter` + `Playfair Display` on shell pages; some legacy inline `<style>` on charter/activities/membership (large but stable) |
| Section pills | Now consistent on membership pages; About/Scientists/Forum/Activities use JS injection from `nav.json` |
| Button styles | `.btn`, `.btn-primary`, `.app-btn-*` on application form — scoped correctly |

### Scientists subsystem

| Check | Command / note |
|-------|----------------|
| CV card validation | `python helpers/_validate_cv_cards.py` when scientists data changes |
| Name order | `python helpers/_check_name_order.py` |
| Catalog sync | `js/scientists-catalog-data.js` ↔ list view inline data must stay aligned (per project rules) |
| Profile TTS / QR | `daab-profile-tts.js`, profile QR CSS — test on mobile |

### Accessibility (spot check, not full WCAG audit)

| Area | Status |
|------|--------|
| Skip links | Present on shell pages |
| `aria-label` on nav / section nav | Present on updated membership pages |
| Focus states | Defined in `daab-nav-mega.css` for section pills |
| Alt text on foundation gallery | Present after path fix |
| Form labels | Application form uses `<label for=...>` |
| Color contrast | Hero on light background — generally acceptable; charter/forum long reads not re-audited |

**Recommendation:** Run keyboard-only pass on nav dropdown, search dialog, application multi-step form, and scientists filters before major release.

### Responsive / device testing (manual QA checklist)

Not executed in this automated pass. Before release, verify on:

- [ ] Desktop Chrome/Edge — `http://localhost:8010/` (use `START-SITE.bat` or `python -m http.server 8010 --bind 127.0.0.1`)
- [ ] iPhone Safari — portrait + landscape
- [ ] Android Chrome
- [ ] Tablet width (~768–1024px)

**Focus pages:** home, foundation (gallery), scientists list/profiles (filters, sticky, QR), forum hub + one subpage, membership trio + application form, search overlay, language switcher.

**Watch for:** nav overflow, section pill wrap, form progress bar on narrow screens, footer grid stack, sticky profile panel overlap.

### Navigation / routing

| Component | Source of truth |
|-----------|-----------------|
| Primary nav | `i18n/nav.json` + `daab-primary-nav.js` (or embedded static nav until mount) |
| Breadcrumbs | `i18n/routes.json` + `daab-breadcrumbs.js` |
| Section pills | `nav.json` → `sections.*` + `daab-section-nav.js` |
| Language switch | `daab-shell.js` + `daab-i18n.js` |
| Search | `i18n/search-index.json` + `daab-search.js` |

**Verified:** Membership pages in `routes.json` have `navGroup: "membership"` and correct AZ/EN paths.

---

## Maintenance scripts added/updated

| Script | Purpose |
|--------|---------|
| `helpers/_site_wide_cleanup.py` | Re-run: foundation path fix pattern, asset `?v=` bumps, membership_value section nav injection |
| `helpers/_build_search_index.py` | Rebuild search after route/label changes |
| `helpers/_sync_primary_nav.py` | Updated version constants |
| `helpers/_fix_forum_css_pairs.py` | Repair `forum-photos-gallery` / `forum-video-gallery` selector suffixes in `daab-forum-content.css` |

**Standard post-change workflow:**

```bash
python helpers/_validate_site.py
python helpers/_build_search_index.py   # if routes/titles changed
# optional scientists validators if CV pages touched
```

---

## AZ / EN synchronization status

| Page cluster | AZ path | EN path | Sync |
|--------------|---------|---------|------|
| Home | `az/index.html` | `en/index.html` | Yes |
| About | foundation, mission, board, charter | Same | Yes |
| Activities + Forum 2024 | `az/forum/2024/*` | `en/forum/2024/*` | Yes (parallel structure) |
| Scientists | list, profiles | list, profiles | Yes |
| Membership | value, terms, application | value, terms, application | Yes (section nav + labels) |

---

## Regression avoidance

- **Content:** No prose changes except previously requested AZ application intro removal.
- **Visual identity:** No color/token redesign; only path and nav label fixes.
- **Deploy set:** Unchanged — still `az/`, `en/`, `css/`, `js/`, `images/`, root `index.html`.

---

## Summary for stakeholders

The site is **structurally sound** for static hosting: broken image links on Foundation pages are repaired, membership navigation is labeled correctly in both languages, and shared scripts use consistent cache versions so browsers load the latest nav behavior. Remaining work is primarily **manual cross-device QA** and optional copy harmonization—not blocking technical debt for deployment.

**Work order:** See `documents/DAAB-Site-Next-Steps.md` for the phased plan (baseline → smoke test → copy → scripts → CSS → dead code → release).

*Audit and fixes: May 2026. Re-validate with `python helpers/_validate_site.py` after any HTML/asset change.*

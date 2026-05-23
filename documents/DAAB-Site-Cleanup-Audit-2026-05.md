# DAAB site cleanup audit (May 2026)

Technical and UI/UX review of the static DAAB/WAAS bilingual site. This document records findings, fixes applied in this pass, and recommended follow-ups.

## Scope reviewed

- **Live pages:** `az/` and `en/` (9 page pairs, 18 HTML files)
- **Gateway:** `index.html`, `404.html`
- **Legacy bookmarks:** root `*_az.html` redirect stubs
- **Assets:** `css/` (7 files), `js/` (11 files), `images/`, `i18n/`
- **Helpers:** `helpers/` maintenance scripts
- **Validation:** `_validate_site.py`, `_validate_bilingual.py`, `_validate_cv_cards.py`

---

## Summary

| Area | Status |
|------|--------|
| Broken local asset/page links | **OK** — 1,345 refs checked, zero errors |
| Bilingual structure (`az/` ↔ `en/`) | **OK** — 9 pairs, sitemap + robots valid |
| CSS/JS orphan files | **None** — all 7 CSS and 11 JS files referenced |
| Legacy root duplicates | **Fixed** — thinned to redirect-only stubs (~15 lines each) |
| Scientist catalogue canonical path | **Fixed** — helpers now target `az/scientists/*.html` |
| Search legacy URLs | **Fixed** — root context points to `az/` tree |
| 404 / gateway UX | **Improved** — language-aware redirect |
| CV card validator false positive | **Fixed** — last card grid boundary |
| Scratch / dead files | **Removed** — `index-gateway.html`, `cv/_aygul_*` |

---

## Fixes applied (this pass)

### 1. Legacy root pages → thin redirects

**Problem:** Eight root `*_az.html` files contained full stale copies (800–2,100 lines) with old nav, old asset versions, and duplicate scientist catalogues.

**Fix:** `helpers/_thin_legacy_redirects.py` rebuilds stubs from `i18n/routes.json` `legacyRedirects`. Each file is now a ~15-line meta refresh + JS redirect to the canonical `az/` page.

**Run after route changes:**
```bash
python helpers/_thin_legacy_redirects.py
```

### 2. Canonical paths in helpers

**Problem:** Maintenance scripts wrote to root `scientists_card_view_az.html` / `scientists_list_view_az.html` while live site uses `az/scientists/`.

**Fix:** `helpers/_paths.py` defines `AZ_SCIENTISTS_LIST`, `AZ_SCIENTISTS_PROFILES`, etc. Updated:

- `_rebuild_cv_catalog.py`
- `_validate_cv_cards.py`
- `_sync_scientists_from_book.py`
- `_normalize_cv_cards.py`
- `_sync_list_view_data.py`
- `_build_cv_enrichment.py`

### 3. Site search legacy context

**Problem:** `js/daab-search.js` legacy mode linked to root `*_az.html` pages.

**Fix:** Legacy context now uses `az/index.html`, `az/mission.html`, etc.

### 4. Gateway and 404

- **`index.html`:** CSS cache versions aligned (`daab-common.css?v=18`, `daab-lang.css?v=6`).
- **`404.html`:** Language-aware redirect (`localStorage daab-lang` → `en/` or `az/`) with styled fallback links.
- **`index-gateway.html`:** Removed (duplicate of `index.html?choose=1`, unreferenced).

### 5. Validator noise

**Problem:** `_validate_site.py` warned that `index.html` lacked full nav shell.

**Fix:** Gateway pages excluded; live pages validated via `az/` + `en/` trees only.

### 6. Dead scratch files removed

- `cv/_aygul_body_fragment.html`
- `cv/_aygul_extract_az.txt`, `cv/_aygul_extract_en.txt`
- `cv/_write_fragment.py`

---

## UI/UX and design system (review)

### Strengths (already in place)

- **Shared tokens** in `css/daab-common.css` (`--blue-700`, `--radius`, `--shadow`, Inter + Playfair).
- **Mega-nav** via `daab-primary-nav.js` + `daab-nav-mega.css` with emoji icons from `i18n/ui.json`.
- **Mobile layer** `css/daab-mobile.css`: safe-area insets, 44px touch targets, `touch-action: manipulation`, overflow-wrap.
- **Focus states** on nav links, buttons, dropdowns, TOC (`:focus-visible` rules in `daab-common.css`).
- **Skip links** on all main `az/` and `en/` pages.
- **Hero summary panels** unified via `daab-hero-summary.css` on home, about, scientists pages.
- **Breadcrumbs + section nav** with embedded fallbacks for `file://` and offline i18n (`daab-breadcrumbs.js`, `daab-section-nav.js`).

### Remaining inconsistencies (low priority)

| Issue | Location | Recommendation |
|-------|----------|----------------|
| Asset `?v=` cache busting varies | Some pages `v=18`, gateway was `v=11` | Bump `?v=` when editing shared CSS/JS (gateway fixed) |
| Charter uses extra `daab-sidebar-widget.css` | `az/charter.html`, `en/charter.html` only | Intentional; keep isolated |
| Turkish proper nouns in EN bios | Institution names (`Türkiye`, `Yüzüncü Yıl`) | Not AZ; acceptable |
| Image path AZ filenames | `Şuşa qurultayı`, `İstanbul görüşü` | Match disk filenames; alt text is EN |
| `mission.html` / `charter.html` excluded from bulk EN publish | `_publish_en_pages.py` | Hand-translated; run `_latinize_en_person_names.py` after edits |

### AZ / EN synchronization

- **Structure:** Matched via `_validate_bilingual.py` (9 pairs).
- **Scientist data:** `scientists-catalog-data.js` (AZ) + `scientists-catalog-data-en.js` (EN labels/names).
- **Profile bios:** `i18n/scientists-profiles-en.json` + publish pipeline.
- **Personal names EN:** `i18n/person-names-en.json` + `apply_person_name_latin()`.

---

## Mobile and touch (code review)

| Feature | Implementation |
|---------|----------------|
| Viewport | `viewport-fit=cover` on all main pages |
| Sticky nav | `daab-common.css` + mobile menu toggle in `daab-nav.js` |
| Dropdowns | Click/touch on mobile; `:focus-within` on desktop |
| Filters (scientists) | Toolbar wraps; `scientists-catalog-toolbar.css` + `daab-mobile.css` table scroll |
| Search overlay | Full-screen overlay; ESC closes (`daab-search.js`) |
| Landscape | CSS uses `max-width` breakpoints, not orientation-only hacks |

**Manual test checklist (recommended before deploy):**

1. iPhone Safari + Android Chrome: open menu, scientists dropdown, filters, search.
2. Rotate portrait ↔ landscape on activities and scientist profiles.
3. Verify breadcrumbs and section pills on About pages over `http://127.0.0.1:8010/`.

---

## Accessibility (code review)

| Check | Status |
|-------|--------|
| Skip to content | Present on all 18 main pages |
| Focus visible | Nav, buttons, links, lightbox close |
| Alt text on photos | Scientist cards, board members, activities images |
| Language | `lang="az"` / `lang="en"` on `<html>` |
| Keyboard nav | Native focus order; dropdown toggles are `<button>` |
| Contrast | Institutional blue on white; footer dark panel |

**Follow-up:** Run Lighthouse or axe on `az/index.html` and `en/scientists/profiles.html` for automated WCAG report.

---

## Folder structure compliance

| Type | Location | Status |
|------|----------|--------|
| CSS | `css/` | OK |
| JS | `js/` | OK |
| Helpers | `helpers/` | OK |
| Images | `images/` | OK |
| Docs | `documents/` | OK |
| i18n data | `i18n/` | OK (deploy with site) |
| Live HTML | `az/`, `en/`, gateway root | OK |
| CV samples | `cv/` | OK (2 public CV pages) |

No stray `daab-common.css` or `daab-nav.js` at repository root.

---

## Recommended follow-ups (not done in this pass)

1. ~~**Single source for scientist cards**~~ — **Done (pass 2):** `i18n/scientists-profiles.json` + `_build_scientists_profiles.py`.
2. **Automated EN publish for charter/mission** — extend translation tables or keep manual with documented workflow.
3. **Pagefind or per-lang search index** — strategy in `documents/DAAB-Bilingual-Website-Strategy.md`.
4. **Root `sources/home_az.html`** — build input only; do not deploy.
5. ~~**Helper doc refresh**~~ — **Done (pass 2):** `helpers/README.md` updated.

---

## Pass 2 — full review (May 23, 2026)

Second full-site technical and UI/UX cleanup. Validators re-run; fixes applied below.

### Validation results (after pass 2)

| Check | Result |
|-------|--------|
| `_validate_site.py` | **OK** — 1,349 refs, zero broken paths |
| `_validate_bilingual.py` | **OK** — 9 page pairs |
| `_validate_cv_cards.py` | **OK** — 83 cards, 0 issues |
| `_check_name_order.py` | **OK** — 0 mismatches (after data fix) |

### Fixes applied (pass 2)

| Issue | Fix |
|-------|-----|
| **`i18n/nav.json` missing `sections.scientists`** | Added scientists section; breadcrumb parent + section pills work over HTTP |
| **Nav cache** | `daab-i18n.js` fetches `nav.json?v=4`; all 18 pages bumped to `daab-i18n.js?v=10` |
| **Duplicate `lang="az"` on `<html>`** | Removed on 6 AZ pages |
| **Stale `daab-mobile.css?v=2`** | Aligned to `v=3` on `az/activities.html`, `en/activities.html` |
| **Stale `scientists-catalog-data.js?v=1`** | Bumped to `v=2` on `az/scientists/profiles.html` |
| **Dead `.name-link` CSS** | Removed from scientist list pages (CV links removed earlier) |
| **İsmayıl Əliyev / Kamran Rüstəmov profile mix-up** | Fixed `i18n/scientists-profiles.json` (say 50/51); rebuilt AZ + EN catalogues |
| **`_check_name_order.py` broken** | Retargeted to `js/scientists-catalog-data.js` + `az/scientists/profiles.html` |
| **Helper docs** | `helpers/README.md` canonical paths + new `_apply_html_cleanup.py` |

### Remaining low-priority items

| Issue | Recommendation |
|-------|------------------|
| Obsolete one-off helpers (`_fix_links.py`, `_link_batch_cvs.py`, etc.) | Archive under `helpers/archive/` when no longer needed |
| `sources/home_az.html` stale build input | Do not deploy; delete when build pipeline confirmed unused |
| `i18n/ui.json` `gateway.*` vs hardcoded `index.html` | Wire gateway copy through ui.json or trim unused keys |
| Kamran Rüstəmov email in catalogue | Same as İsmayıl Əliyev in list data — verify against source book |
| Lighthouse / axe automated WCAG | Run on `az/index.html` before production deploy |

### Mobile / touch / a11y (reconfirmed)

No code regressions found. Existing layers remain in place:

- `viewport-fit=cover`, safe-area insets, 44px touch targets (`daab-mobile.css`)
- Skip links, `:focus-visible`, sticky nav, full-screen search overlay
- Scientist table horizontal scroll on narrow viewports
- Manual device test checklist still recommended before deploy

---

## Pass 3 — full review repeat (May 23, 2026)

Third full-site audit and cleanup pass. All validators green after fixes.

### Validation results (after pass 3)

| Check | Result |
|-------|--------|
| `_validate_site.py` | **OK** — 1,286 refs, zero broken paths |
| `_validate_bilingual.py` | **OK** — 9 page pairs |
| `_validate_cv_cards.py` | **OK** — 83 cards, 0 issues |
| `_check_name_order.py` | **OK** — 0 mismatches |

### Fixes applied (pass 3)

| Issue | Fix |
|-------|-----|
| **EN nav placeholder drift** | Ran `_sync_primary_nav.py` — 7 EN pages now use `data-daab-nav-placeholder="1"` (all 9 EN pages match AZ) |
| **Malformed `<head>` on foundation** | Moved `daab-mobile.js` out of `<link>` line on `az/foundation.html`, `en/foundation.html` |
| **Legacy helper paths** | Retargeted 6 scripts to `AZ_SCIENTISTS_PROFILES` / `AZ_SCIENTISTS_LIST` |
| **Activity photos empty `alt`** | Added descriptive alt text on 5 images × 2 locales (`056`–`060`) |
| **Catalog filter a11y** | Added `aria-label` on `#searchInput` in AZ + EN scientist list pages |
| **Nav metadata** | `i18n/nav.json` version → 2; fetch cache → `?v=5`; pages → `daab-i18n.js?v=11` |
| **`_sync_primary_nav.py` versions** | Updated `SCRIPT_VERSIONS` to match live site |

### Remaining low-priority items

| Issue | Recommendation |
|-------|----------------|
| Site search absent on home/foundation/mission/executive-board | Intentional design; add overlay if site-wide search is desired |
| `sources/home_az.html` stale build input | Do not deploy; delete when build pipeline confirmed unused |
| Kamran Rüstəmov shared email with İsmayıl Əliyev | Verify against source book |
| Search overlay strings hardcoded AZ in `daab-search.js` | Add EN strings via `ui.json` |
| Duplicate inline search CSS on charter/membership | Consolidate into shared CSS when those pages are next edited |

---

## Validation commands

```bash
python helpers/_validate_site.py
python helpers/_validate_bilingual.py
python helpers/_validate_cv_cards.py
python helpers/_thin_legacy_redirects.py   # after legacy URL changes
```

Local preview: `python -m http.server 8010 --bind 127.0.0.1` → http://localhost:8010/index.html

---

*Generated during full-site cleanup review. Re-run validators after HTML/CSS/JS path changes.*

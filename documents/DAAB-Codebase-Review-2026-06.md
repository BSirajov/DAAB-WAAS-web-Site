# DAAB codebase review

**Date:** 2026-06-14
**Scope:** Full static site — `az/`, `en/` HTML (~470 pages), shared `css/` (~50) and `js/` (~38), `i18n/` config, `images/`, gateway `index.html`, `404.html`.
**Method:** Project validators/audits + deep read-only passes (accessibility, CSS, JavaScript). Highest-severity items verified firsthand.

> Status legend: **High** = fix first · **Med** = should fix · **Low** = polish · **Systemic** = repeats across many pages/files.
> Fix status is tracked in the rightmost column and updated as items are addressed.

---

## Automated checks (baseline — all passing)

| Command | Result |
|---------|--------|
| `python helpers/_deploy_preflight.py` | OK — 474 pages, 18,075 references, 0 broken local paths |
| `python helpers/_validate_bilingual.py` | OK — 34 AZ/EN page pairs, sitemap + robots consistent |
| `python helpers/_validate_section_anchors.py` | OK |
| `python helpers/_audit_nav_search.py` | OK — nav pages include search assets + nav-inner |
| `python helpers/_audit_repo_health.py` | OK — no path issues, no asset `?v=` drift |

Links, paths, missing assets, AZ/EN structural parity, and filename casing are clean. The items below are quality / maintainability / UX, not broken-site defects.

---

## 1. Bugs (functional)

| Sev | Location | Issue | Recommendation | Status |
|-----|----------|-------|----------------|--------|
| High | `js/daab-profiles-sticky.js:38–39` | Calls `global.setTimeout(...)` but the IIFE never receives `window` as `global`; `global` is undefined in browsers → uncaught `ReferenceError` on every scientists profiles page, dropping two delayed sticky re-syncs. Verified. | Pass `window` into the IIFE (match other scripts). | **Fixed 2026-06-14** |
| Med | `js/daab-primary-nav.js:451–474` | `applyNavAria` dereferences `ui.nav[lang]` unguarded; missing `nav` in `ui.json` throws after menu build → falls back to minimal nav. | Guard `ui && ui.nav` before mutating. | **Fixed 2026-06-14** — resolves `navLabels` once with `ui && ui.nav` guard + early return; per-field guards. |
| Med | `js/daab-search.js:386–405` | `renderResults`: if all href resolutions reject, `innerHTML` never set → blank/stale results. | Render empty/error state when `pending===0`. | **Fixed 2026-06-14** — shared `finalize()` called from both `then`/`catch`; renders resolved rows or empty state. |
| Med | `js/daab-sidebar-timeline.js:52`, `js/daab-forum-2026-toc.js:119` | `history.pushState` on TOC click, no `popstate` handler → Back updates URL but not active section. | Add `popstate`/`hashchange` sync or use `replaceState`. | **Fixed 2026-06-14** — added `popstate` handler (`syncFromHash`) in both files: re-activates link + scrolls to hash target. |
| Med | `js/daab-profiles-sticky.js:32–36` | `boot()` runs on `DOMContentLoaded` and immediately when already loaded → duplicate resize/load listeners. | Add a `booted` guard. | **Fixed 2026-06-14** — added `booted` guard so listeners bind once. |
| High | `css/daab-activities-layout.css` (forum-anas-leadership-speeches) | Auto-synced selector for `forum-anas-leadership-speeches` was appended without its descendant suffix in all 21 selector blocks, so grid/sticky/mobile rules targeted `<html>` instead of `.content-wrap`/`.sidebar`/etc. → broken sticky-sidebar layout on that page. Found during CSS review. | Restore per-block suffix to match sibling pages. | **Fixed 2026-06-14** — all 21 selectors repaired (now 21/21 parity with `forum-rector-speeches`); layout sync generator verified idempotent. |

---

## 2. Accessibility

| Sev | Location | Issue | Recommendation | Status |
|-----|----------|-------|----------------|--------|
| High | `az/sponsors.html`, `en/sponsors.html` (~282–327) | Form `<label>`s have no `for`; inputs/selects/textarea lack `id`/`name` → labels not associated, fields not submittable by name. Verified. | Add matching `id`/`for` + `name` to every field. | **Fixed 2026-06-14** |
| High | `js/daab-primary-nav.js:153–169, 246–266` | Dropdown toggles set `aria-expanded`/`aria-haspopup` but no `aria-controls`; panels have no `id`. Systemic. | Generate panel IDs; set `aria-controls`. | **Fixed 2026-06-14** — `associatePanel()` helper assigns unique `id` + wires `aria-controls` in all dropdown builders. |
| High | `az/foundation.html` + `en/foundation.html` (gallery `img onclick`, lightbox `769`, `842`) | Lightbox opens via `<img onclick>` (not keyboard-operable); dialog lacks accessible name, focus trap, focus restore. | Keyboard-operable triggers; trap + restore focus; label dialog. | **Fixed 2026-06-14** — `.gallery img` now `role=button`/`tabindex=0`/Enter+Space; dialog has `aria-label` + `aria-hidden` toggle, Tab trap, focus restore to trigger. |
| High | `css/daab-common.css:475–482` | `#search-input { outline:0 }` with no `:focus-visible` replacement → invisible keyboard focus. | Add `:focus-visible` style. | **Fixed 2026-06-14** — added `#search-input:focus-visible` + `.search-close-btn:focus-visible`. |
| Med | `js/daab-search.js:262, 461–535` | Modal uses invalid `role="document"`; no focus trap / focus return. | Remove role; add focus management. | **Fixed 2026-06-14** — removed `role="document"`, added Tab focus trap (focus return on close already present). |
| Med | Scientists/encyclopedia toolbars (`.sel-clear`) | Icon-only `×` clear buttons labeled only via `title`. | Add per-filter `aria-label`. | **Fixed 2026-06-14** — catalog scripts set a per-filter `aria-label` (localized verb + target filter name) on every `.sel-clear`. |
| Med | `js/daab-search.js`; AZ `scientists/profiles.html:47` | Search input has no `aria-label`; AZ overlay precedes skip link, lacks initial `aria-hidden`. | Label input from i18n; fix body order / `aria-hidden`. | **Fixed 2026-06-14** — input labeled from i18n placeholder. Root cause of the AZ page: a stale **static** `#search-overlay` (old markup: emoji icon, `type="text"`, hardcoded labels, no `aria-live`/`aria-hidden`) preceded the skip link and made `mountOverlay()` bail (line 253), so AZ never got the modern injected overlay. Removed the static block (the only page that still had one — `_strip_legacy_search_overlay.py`'s regex missed it because results contained a nested `.search-prompt`); `daab-search.js` now injects the current overlay with `aria-hidden="true"` + `aria-live`, and the skip link is the first body element (parity with EN). Verified via HTTP smoke test (AZ+EN). |
| Med | `az/membership_flyer.html:65`, `en/membership_flyer.html:72` | Two `<h1>` on one page (letterhead acronym + page hero). | Demote acronym to `<h2>`. | **Fixed 2026-06-14** — letterhead `DAAB`/`WAAS` now `<h2>`; CSS rule retargeted `.flyer-brand-block h2` (no visual change). |
| Low | Hub-card emoji (`az/en` index + forum 2024 index) | Decorative emoji announced by SRs. | `aria-hidden` on `.card-icon-wrap`. | **Fixed 2026-06-14** — `.card-icon-wrap` marked `aria-hidden` in 4 pages + 3 generators kept in sync. |
| Low | Hero `role="doc-subtitle"` (~470 pages, generated) | Flagged as nonstandard. | Re-evaluate. | Deferred — `doc-subtitle` is a valid DPUB-ARIA role; systemic + generator-owned, not worth mass churn. |
| Low | `index.html` gateway skip link | No skip link on gateway. | Add gateway skip link. | Won't fix — gateway is a single `<main>` language card with no preceding nav to skip; a skip link adds a redundant focus stop. |

---

## 3. CSS — duplication, conflicts, responsiveness

| Sev | Location | Issue | Recommendation | Status |
|-----|----------|-------|----------------|--------|
| High | `daab-activities-layout.css` (sticky block ×4), `daab-charter-page.css`, `daab-sidebar-widget.css`, `daab-nav-mega.css` | Near-identical sticky-sidebar stack duplicated across 4–5 files; 13-page-id selector list repeats across one file. | Extract shared `daab-sticky-sidebar.css`; use `:is(...)` for page-id lists. | Partially fixed 2026-06-14 — `daab-activities-layout.css` 21 repeated selector lists collapsed to `html:is(...)` (455→203 lines, identical specificity); maintained via `_forum_layout_pages.py` (`:is()`-aware, idempotent). Cross-file extraction of the shared sticky stack still open. |
| High | Site-wide | Heavy `!important` escalation (`daab-nav-mega`, `daab-common`, `daab-activities-layout/page`, `daab-charter-page` each 100+); nav/breadcrumb rules fight across files. | Lower specificity reliance; consolidate nav/breadcrumb positioning. | Open |
| Med | `daab-common.css` (`.main`/`a`), `daab-activities-page.css` (bare `.sidebar`), charter `body` | Unscoped selectors on page sheets can leak across pages. | Scope under `html[data-daab-page-id="…"]`. | **Partially fixed 2026-06-14** — scoped the document-element rules that restyled the global `<body>`/`<html>`: `daab-charter-page.css` `body{}` → `html[data-daab-page-id="charter"] body`; `daab-activities-page.css` `body{}` + `html{scroll-behavior}` → `html[data-daab-page-id="activities-news"] …`. Verified collision-free (no bare `body`/`html` rules in any later-loading sheet) and behavior-neutral. **Deliberately not scoped**: `daab-common.css` `.main`/`a` are intentionally global (shared sheet — false flag); the broad `body, p, li, a, span, div {…!important}` typography block and `.sidebar`/`li`/`h*` rules in `daab-activities-page.css` were left as-is — each sheet is single-page (no real cross-page leak today) and raising their specificity could flip the `!important` cascade against later-loading nav/footer rules. Revisit only if a sheet is reused on another page-id. |
| Med | `daab-activities-page.css` vs `daab-sidebar-widget.css` | Duplicate `.sidebar-widget`/`.widget-head`/`.timeline-list` chrome. | Keep widget chrome in one file. | Open |
| Med | `daab-foundation-page.css`, `daab-donate-page.css`, `daab-executive-board.css` | Ad-hoc breakpoints (900/760/420 etc.), never the documented 1060/1061. | Normalize to shared breakpoints. | Open |
| Med | `daab-forum-logistics.css` meal table | `min-width`+`white-space:nowrap`, only 760px rule, no horizontal-scroll guard. | Wrap tables in `overflow-x:auto`; add 1060px stack. | **Not a defect 2026-06-14** — re-verified: the meal table is wrapped in `.program-table-wrap`, which already gets `overflow-x:auto` + `-webkit-overflow-scrolling:touch` from `daab-forum-content.css` (`html[data-daab-page-id^="forum-"] .program-table-wrap`, matches `forum-logistics`; loaded on both AZ/EN). Original flag came from reading `daab-forum-logistics.css` in isolation. Horizontal-scroll guard already present; no change needed. |
| Low | 20+ files | ~11 distinct ad-hoc breakpoint values. | Define breakpoint tokens in `daab-tokens.css`. | Open |

Mitigation present: `daab-mobile.css` (on ~470 pages) applies cross-page `min-width:0`, `overflow-wrap`, `max-width:100%` on media. Root `index.html` redirect omits `daab-mobile.css` (minor flash).

---

## 4. JavaScript — duplication & architecture

| Sev | Pattern | Locations | Recommendation | Status |
|-----|---------|-----------|----------------|--------|
| Med | `detectLang()` copy-pasted | `daab-search`, `daab-shell`, `daab-back-to-top`, `daab-page-subtitle`, `daab-membership-application`, … | Use `DAAB_I18N.detectLang()`. | **Fixed 2026-06-14** — canonical logic already lives once in `daab-i18n.js` (`DAAB_I18N.detectLang`, incl. `?lang=` + both path checks). `shell`/`back-to-top`/`page-subtitle` already delegate to it with a tiny defensive fallback (not duplicated logic). The only true outlier, `daab-membership-application.js`, now delegates too (keeps the inline fallback for the I18N-absent case). Verified `daab-i18n.js` loads before it on both `application.html`. `daab-search.js` intentionally left as-is (gateway-specific persisted-lang branch). No new shared file created — would add site-wide load-order churn for a 4-line fn and can't cover the I18N-absent case. |
| Med | Sticky-offset math duplicated | `daab-lang-position`, `scientists-list-preview`, `daab-work-done-report`, `daab-profile-deep-link` | Export `DAAB_STICKY_CHROME.getStack()`. | Open |
| Med | Sidebar TOC logic ~90% duplicated | `daab-sidebar-timeline.js` ↔ `daab-forum-2026-toc.js` (+`daab-photos-gallery.js`) | Extract `daab-sidebar-spy.js`. | **Deferred 2026-06-14** (scoped, not executed) — maintainability-only (no user-facing change) vs. high, build-generator-coupled churn: a shared module must load before both consumers on ~20 live pages + 3 templates and be emitted by 6+ generators; a missed generator would silently drop the `<script>` on rebuild and break scroll-spy while still passing `_validate_site.py`. Trade-off poor for deduping 2 files / ~70 lines. Full plan recorded in §6; revisit if a 3rd consumer appears or forum pages move to a shared head include. |
| Med | ~200-entry `COUNTRY_CODES` duplicated | `daab-sponsors-page.js` ↔ `daab-membership-application.js` | Shared data module. | **Fixed 2026-06-14** — extracted the identical 195-code ISO list into `js/daab-country-codes.js` (exposes `window.DAAB_COUNTRY_CODES`); both consumers now read the global with a graceful `|| []` fallback. Module added with `defer` before each consumer on `az/en` `sponsors.html` + `application.html` (defer + document order guarantees availability). Verified: 195 codes, load order, no embedded list remaining. |
| Med | Many independent `resize`/`scroll` listeners | 8+ modules funnel into chrome sync | Single rAF-throttled layout-sync bus. | Open |
| Low | Dead code | `animateCounter` (`daab-sponsors-page.js:87`); `DAAB_DESIGN.load()` (`daab-design-tokens.js`) — both defined, never called. Verified. | Wire up or remove. | **Fixed 2026-06-14** — removed `animateCounter`; removed unused `load()` + its exclusive helpers (`assetRoot`, `deepMerge`, `loadPromise`) from `daab-design-tokens.js` (matchMedia helpers retained). |

---

## 5. Naming / consistency

- CSS prefix split: 6 `scientists-*.css` vs ~44 `daab-*.css`; inconsistent `-page` suffix. → Standardize on `daab-scientists-*` for new files; migrate gradually.
- Hardcoded colors: ~40/50 CSS files contain literal hex despite `daab-tokens.css` (`daab-membership-application.css`: 70 hex vs 1 token — worst). → Adopt tokens in high-traffic shared files first.

---

## 6. Known / accepted (not defects)

- `daab-forum-book.css`, `daab-membership-page.css` — intentional build-only assets (kept by decision).
- Membership nav has 3 items (no standalone terms page) — by design.
- Treasury production visibility — pending separate decision.

### Deferred: sidebar scroll-spy extraction (`daab-sidebar-spy.js`)

Scoped 2026-06-14, deliberately not executed (see §3 JS row). Ready-to-run plan if/when the trade-off flips:

- **Shared engine to extract** (~70 lines, identical in both files modulo ES6/ES5 style): `sidebarStackMediaQuery()`/`mobileQuery`, `activate()`, `closeEventsMenu()`, `toggleEventsMenu()`, `jumpToTarget()` (click → `DAAB_LANG_POSITION.scrollToAnchor` → `pushState` → mobile close), `onScroll()` (35%-viewport scroll-spy), `syncFromHash()`, and all listeners (link click, toggle, outside-click close, Escape, `scroll`, `popstate`).
- **Differences to preserve**: (1) link source — `daab-sidebar-timeline.js` reads pre-rendered `.timeline-list a[href^="#"]`; `daab-forum-2026-toc.js` *builds* the TOC (`slugify`/`uniqueId`/create nodes, assign heading ids) then reads `#forum2026TOC a`; (2) `daab-forum-2026-toc.js` does a deferred initial hash jump on load, the timeline does not.
- **Proposed API**: `window.DAAB_SIDEBAR_SPY(links, { initialHashJump })`. Consumers become thin wrappers (timeline: collect links → call; forum-2026: build TOC → collect links → call with `initialHashJump: true`).
- **Blast radius**: add the new `<script defer>` *before* each consumer on ~20 pages (`az`/`en` `activities.html`; `az`/`en` `forum/2024/{official,impressions,rector_speeches,roadmap,presentations,stories,anas_leadership_speeches,program}.html`; `az`/`en` `forum/2026/index.html`) + 3 templates (`templates/forum-2026-frame.{az,en}.html`, `templates/Forum 2026.html`); update emitting generators (`_build_official_from_docx.py`, `_build_rector_speeches_from_docx.py`, `_build_roadmap_from_docx.py`, `_build_stories_from_docx.py`, `_build_cooperation_from_docx.py`, the forum-2026 builder) and injection utilities (`_inject_sidebar_timeline_js.py`, `_dedupe_sidebar_timeline.py`); register + bump version in `_site_wide_cleanup.py`.
- **Verification**: `node --check` all touched JS; `_validate_site.py`; HTTP smoke test that the shared module loads before each consumer on a sample of every page type, scroll-spy activates a link, and hash-jump works on forum-2026.

---

## Suggested priority order

1. `daab-profiles-sticky.js` `global` bug (runtime error). **Done.**
2. Sponsors form labels (AZ+EN). **Done.**
3. Nav `aria-controls` + search `role`/focus (systemic a11y). **Done.**
4. Foundation lightbox keyboard/focus. **Done.**
5. CSS: de-duplicate sticky-sidebar + reduce `!important`; normalize breakpoints.
6. JS: shared helpers (`detectLang`, sticky-offset, sidebar-spy); remove dead code.

Each change should be verified (validators + affected-page review) before closing, per `.cursor/rules/daab-careful-changes.mdc`.

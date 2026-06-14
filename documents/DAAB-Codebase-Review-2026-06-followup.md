# DAAB codebase review — follow-up pass

**Date:** 2026-06-14 (second full pass, same day)
**Scope:** Full static site — `az/`, `en/` HTML (~472 deploy pages / 474 root), shared `css/` (~49) and `js/` (~39), `i18n/`, `images/`, gateway `index.html`, `404.html`, `sitemap.xml`, `robots.txt`, `.deployignore`.
**Method:** All project validators/audits re-run + four independent read-only deep passes (CSS, JavaScript, accessibility, HTML/i18n/SEO/assets). Every **High** finding below was verified firsthand (grep + file read), not just reported by analysis.
**Companion doc:** `documents/DAAB-Codebase-Review-2026-06.md` (first pass). Items fixed there were re-verified still in place; this doc focuses on **NEW** findings plus the still-open backlog.

> Status legend: **High** = fix first · **Med** = should fix · **Low** = polish · **NEW** = not in first pass · **TRACKED** = carried from first pass · **FIXED ✓** = verified resolved.

---

## Automated baseline — all green

| Command | Result |
|---------|--------|
| `_deploy_preflight.py` | OK — 472 pages, 18,079 refs, 0 broken local paths; 3 INFO (2 build-only CSS, membership 3-item nav) |
| `_audit_repo_health.py` | OK — no path issues, no asset `?v=` drift |
| `_validate_bilingual.py` | OK — 34 AZ/EN page pairs, sitemap + robots consistent |
| `_validate_section_anchors.py` | OK — 34 pairs |
| `_audit_nav_search.py` | OK — all nav pages include search assets + nav-inner |
| `_check_catalog_links.py` | OK — 201 hrefs, 0 missing AZ/EN |
| `_validate_cv_cards.py` / `_check_name_order.py` | OK — 0 issues; 83/83 catalog parity |

Links, paths, missing assets, AZ/EN structural parity, anchors, and filename casing are clean. Findings below are quality / correctness / maintainability / UX / SEO — not broken-link defects.

First-pass fixes re-verified present: `daab-profiles-sticky.js` (`window` IIFE + `booted` guard), nav `aria-controls`, search `finalize()`/focus-trap/`aria-label`/no `role=document`, foundation lightbox keyboard open, `#search-input:focus-visible`, `.sel-clear` aria-labels, membership-flyer single `<h1>`, hub-card emoji `aria-hidden`, `COUNTRY_CODES`→`daab-country-codes.js`, `detectLang` delegation, dead `animateCounter`/`DAAB_DESIGN.load` removed, `popstate` in the two shared TOC modules, charter/activities `body` scoping, AZ profiles stale search overlay removed.

---

## 0. Verified High-severity NEW findings (fix first)

| # | Location | Issue (verified) | Recommendation |
|---|----------|------------------|----------------|
| H1 | `css/daab-forum-content.css` — 65 entries incl. lines 382, 398, … | **Same selector bug just fixed in `daab-activities-layout.css`, now in a second file.** `html[data-daab-page-id="forum-anas-leadership-speeches"]` appears **bare** (no descendant suffix) in 65 comma-list entries whose siblings all carry `.news-card:hover` / `.widget-head` / `.card-header` / `.forum-breadcrumbs` etc. → those rules target `<html>` on the anas page, and the anas page loses card-hover, widget-head gradient, breadcrumb sticky, etc. (verified: 65 bare vs 0 suffixed; sibling `forum-rector-speeches` has 63 correct). Affects AZ + EN `forum/2024/anas_leadership_speeches.html`. | Repair all 65 entries to append the per-rule descendant suffix (mirror the `_forum_layout_pages.py` fix). Fix the emitting generator/helper so a rebuild won't reintroduce it. Add a guard/audit. |
| H2 | `az/forum/2024/logistics.html:269`, `en/forum/2024/logistics.html:269` | **Scroll-spy activates the wrong TOC link.** Inline `onScroll` does `activate(links[active])` where `active` indexes the **filtered** `cards` array (`cards = ids.map(getElementById).filter(Boolean)`); when any TOC id lacks a DOM node, `links` and `cards` misalign. Correct form (module + `program.html:182`) is `links[ids.indexOf(cards[active].id)]`. | Replace the inline TOC with `<script src=".../daab-sidebar-timeline.js">` (preferred), or fix the index mapping. |

These two are concrete, page-specific regressions. Everything else below is quality/maintainability/UX/SEO.

---

## 1. JavaScript — correctness, duplication, architecture

| Sev | Location | Issue | Recommendation | Tag |
|-----|----------|-------|----------------|-----|
| High | logistics inline (see H2) | Wrong active TOC link when a card id is missing. | Use shared module / fix mapping. | NEW |
| Med | `az/forum/2024/program.html`, `az`+`en` `forum/2024/sessions_organization.html`, `az`+`en` `forum/2024/logistics.html` | **Inline TOC copies were left behind when `popstate` was added to the module.** They call `history.pushState` on click with no `popstate` handler → Back changes URL but not active section. (EN `program.html` already uses the module — AZ/EN drift.) | Replace inline copies with `daab-sidebar-timeline.js`, or port `syncFromHash`+`popstate`. | NEW |
| Med | `az/charter.html:470–513`, `en/charter.html` (inline) | Inline IntersectionObserver TOC duplicates sidebar-spy concerns; charter also loads `daab-lang-position.js` → two scroll-spy owners on one page. | Consolidate to one TOC/spy owner. | NEW |
| Med | `az/activities.html` | `daab-lang-position.js` (scoring spy @32% + `replaceState` hash sync) and `daab-sidebar-timeline.js` (offsetTop spy @35%) both run → competing active-link + hash logic. | Designate a single hash/active-link owner per page. | NEW |
| Med | `js/daab-membership-application.js:624–642` | Step scroll + active-step detection use `--daab-nav-height + 120` only, ignoring breadcrumb stack (`--daab-sticky-top-stack`); raw `scrollIntoView`. | Use `DAAB_LANG_POSITION.scrollToAnchor` / shared offset. | NEW |
| Med | `js/scientists-list-catalog.js:108–113` | `window.DAAB_COLLATION.compare/sort` used with **no `\|\| fallback`** (peer scripts guard it). Works today only due to load order. | Add inline fallback like `prominent-figures-catalog.js:14`. | NEW |
| Med | `js/daab-search.js:281–283` | `mountOverlay` reads `#search-input` then sets `.placeholder`/attrs with no null guard. | `if (!input) return;` after create. | NEW |
| Med | `daab-sidebar-timeline.js` ↔ `daab-forum-2026-toc.js` (+5 inline copies) | ~90% identical TOC/spy engine; inline copies multiply the drift. | `DAAB_SIDEBAR_SPY` extraction (deferred — see first-pass §6; inline copies raise the value). | TRACKED |
| Med | Sticky-offset math re-read in `daab-lang-position.js`, `scientists-list-preview.js`, `daab-profile-deep-link.js`, `daab-work-done-report.js`, `daab-membership-application.js` | `--daab-sticky-top-stack` written centrally by `daab-sticky-chrome.js` but recomputed locally. | Export `DAAB_STICKY_CHROME.getStack()`. | TRACKED |
| Med | 7 scroll + 9 resize + 4 orientationchange listeners across modules (4–5 per long page) | Redundant layout work each event. | rAF-throttled `DAAB_LAYOUT_SYNC` bus. | TRACKED |
| Low | `js/daab-back-to-top.js:120–121` | Scroll handler bound on **both** `window` and `document`. | Drop the `document` listener. | NEW |
| Low | `js/daab-search.js:673–676` | `window.DAAB_SEARCH = {normalizeText, scoreEntry}` exported, no external callers. | Remove or document as debug API. | NEW |
| Low | hub-card text filter inlined in `az/index.html`, `en/index.html`, `az`+`en` `forum/2024/index.html` | Identical one-liner duplicated. | Tiny shared module (optional). | NEW |

---

## 2. Accessibility

| Sev | Location | Issue | Recommendation | Tag |
|-----|----------|-------|----------------|-----|
| High | `js/daab-photos-gallery.js:527–547`; `az/forum/2024/photos_gallery.html` | **Photo lightbox `aria-modal="true"` dialog has no focus trap** (`lightboxPrev`/`lightboxNext` stay null); Tab escapes to the page behind the open modal. Main keyboard regression among interactive features. | Add a Tab focus trap + focus return (mirror `daab-search.js`); optionally wire prev/next. | NEW |
| Med | Generated prominent-figure profiles (~400 pages, e.g. `az/prominent_figures/world/albert_einstein.html:37–48`) | **Heading hierarchy skips** — after `<h1>` the article jumps to `<h4>`; section titles are `<div class="section-title">` not headings. | Generator: `<h2>` section cards, `<h3>` subsections; renumber. | NEW (systemic) |
| Med | Footers/sidebars/hero CTAs site-wide (e.g. `az/foundation.html` footer, `az/index.html:55,81`, widget heads) | Decorative emoji (✉ ☎ 🌐 🤝 🔎 📅 📜 📷) not `aria-hidden` → announced before link text on ~470 pages. | Wrap decorative emoji in `<span aria-hidden="true">` via the generators. | NEW (systemic) |
| Med | `js/daab-sponsors-page.js:56–61` | Email error `.field-error` not linked via `aria-describedby`; no `role="alert"`/`aria-live`. | Link error id + announce. | NEW |
| Med | `js/daab-membership-application.js:185–190`; `az/application.html:419–424` | Science-field error not tied to the checkbox group (no `<fieldset><legend>` / `aria-describedby`); CV confirmation is free-text, not a checkbox. | Fieldset/legend + error association; convert CV confirm to checkbox+label. | NEW |
| Med | `az/scientists/list.html:72–84` | Filter `<select>`s lack `aria-label` (the profiles catalog has them). | Add `aria-label` per filter + generator. | NEW |
| Med | Open modals (search, photo lightbox, foundation lightbox) | Background not `inert`/`aria-hidden` while modal open; SR browse mode can reach background. | Set `inert` on `<main>`/siblings during modal open. | NEW |
| Med | `css/daab-common.css:505`, `css/daab-search.css:122` | `.search-empty` / placeholder `#8aa0b7` on white ≈ 4.0:1 (borderline WCAG AA small text). | Darken to ≥ 4.5:1 (e.g. `--muted` verified). | NEW |
| Low | `az`+`en` `foundation.html` gallery | `<img onclick="openLightbox(this)">` still inline (keyboard added in JS); Tab trap focuses close only. | Move to `<button>`/delegated listener; full focus cycle. | TRACKED (partial) |
| Low | `az/scientists/list.html:60–62` etc. | Decorative search `<svg>` not `aria-hidden`; `.sel-clear` has only `title` until JS runs. | `aria-hidden` on icon; static `aria-label` for first paint/no-JS. | NEW |
| Low | `js/daab-primary-nav.js:175,273` | `role="menu"`/`menuitem"` on site nav without full menu keyboard pattern. | Consider dropping menu roles unless implementing the pattern. | NEW (polish) |
| — | Hero `role="doc-subtitle"`, gateway skip link | Valid DPUB role / single-card gateway. | Accepted. | TRACKED |

---

## 3. CSS — duplication, conflicts, responsiveness

| Sev | Location | Issue | Recommendation | Tag |
|-----|----------|-------|----------------|-----|
| High | `css/daab-forum-content.css` (see H1) | 65 broken `forum-anas-leadership-speeches` comma-list selectors target `<html>`. | Repair + fix generator. | NEW |
| High | `daab-activities-layout.css`, `daab-charter-page.css`, `daab-nav-mega.css`, `daab-forum-content.css` | Near-identical sticky-sidebar/TOC stack duplicated across 4+ files. | Extract `daab-sticky-sidebar.css`. | TRACKED |
| High | Site-wide | `!important` escalation (~1,100–1,300+; 6 files ≥100: `daab-common`, `daab-nav-mega`, `daab-activities-layout`, `daab-activities-page`, `daab-charter-page`); nav model split `daab-common` `.nav-strip{position:sticky!important}` vs `daab-sticky-chrome` `#daab-top-chrome{position:fixed!important}`. | Pick one chrome model; lower specificity reliance. | TRACKED |
| Med | `daab-activities-page.css:719–870` vs `daab-activities-layout.css:85–127` vs `daab-sidebar-widget.css:160–171` | Mobile collapsible widget rules triplicated (two `@media 1060px` blocks in activities-page alone). | Keep mobile collapse in one sheet. | TRACKED |
| Med | `daab-sidebar-widget.css:52–137` re-overridden in `daab-forum-content.css` + `daab-activities-page.css` | Widget chrome defined then `!important`-overridden elsewhere. | Single source; page sheets add accents only. | TRACKED |
| Med | 22 distinct breakpoint widths (360…1480) vs documented 1060/1180; worst: `daab-activities-page.css`, `daab-common.css`, `daab-hub-cards.css`, `daab-scientists-profiles-page.css` | Ad-hoc breakpoints; per-gallery `@media 768px` repetition. | Normalize to 1060/1180; shared gallery-collapse rule. | TRACKED |
| Med | `daab-membership-application.css` (~70 hex vs 47 var) | Worst token bypass; also forum/nav blues hardcoded. | Adopt `daab-tokens.css` vars. | TRACKED |
| Med | `daab-tokens.css:130` `--z-breadcrumbs:100` vs `daab-sticky-chrome.css:7–8` `--z-breadcrumbs:9998` | Token overridden in another global sheet. | Single z-index source. | NEW |
| Med | `daab-activities-page.css:500` `.page-hero`, `:709` `.timeline-list a` | Bare (unscoped) selectors on a page sheet. | Scope under page-id (low risk: single-page sheet). | NEW/TRACKED |
| Low | `daab-charter-page.css:18–20` 8.4px rules overridden by `:513–518` `!important` | Dead legacy rules forcing later overrides. | Remove at source. | NEW |
| Low | `daab-activities-page.css:262–274` | Duplicate `@media 768px` `.siracov-gallery` blocks. | Merge. | NEW |
| Low | `az/membership_flyer.html:21`, `az/sponsors_flyer.html:21` | Redundant direct `<link>` to `daab-tokens.css` (already `@import`ed by `daab-common.css`). | Remove duplicate link. | NEW |
| — | `daab-forum-logistics.css` meal table | Overflow guard already provided by `.program-table-wrap` in `daab-forum-content.css`. | No change. | FIXED ✓ (first pass) |

---

## 4. HTML, semantics, multilingual

| Sev | Location | Issue | Recommendation | Tag |
|-----|----------|-------|----------------|-----|
| Med | `az/foundation.html:7` | AZ page `<title>` is English: `DAAB — Foundation` (description is AZ). Verified. | Localize title in source/generator. | NEW |
| Med | `az/prominent_figures/**` (~400, e.g. `albert_einstein.html:40`) | Generator boilerplate grammar (“…çevrildi olması”); EN profiles thin/recycled paragraphs. | Fix templates + enrich data. | NEW |
| Med | `en/prominent_figures/world/*.html` source links (e.g. `schrodinger.html:46`) | EN link href still contains AZ-encoded “və” (`v%C9%99`) inside Google-search query URLs. | Fix EN source-link template. | NEW |
| Med | `en/application.html:137,294,427,…` | Inline `style="..."` where AZ uses classes. | Move to CSS classes; sync AZ/EN. | NEW |
| Low | `az/scientists/profiles.html:1090`, EN `:1098` | Empty `<p class="bio bio-lead"></p>` (one card). | Fix catalog data/generator. | NEW |
| Low | `az`+`en` `forum/2024/sessions_organization.html:36` | Empty `<body class="">` despite page-id present. | Set body class in generator. | NEW |
| Low | `az/forum/2024/presentations.html:387` | English fragment in AZ page. | Translate/remove in generator. | NEW |
| — | `lang`/`data-daab-lang`, no deprecated tags, no TODO/dup-attrs in samples | — | OK | — |

---

## 5. SEO / `<head>` consistency / config

| Sev | Location | Issue (verified counts) | Recommendation | Tag |
|-----|----------|-------------------------|----------------|-----|
| High | All ~470 pages | **No Open Graph / Twitter Card meta** (og:0, twitter:0). Poor link previews when shared. | Add minimal OG/Twitter set to the shared head template. | NEW |
| High | All ~470 pages | **No favicon** (`rel="icon"`:0). | Add `images/` favicon + `<link rel="icon">`. | NEW |
| High | All `az`/`en` pages | **No in-page `hreflang`/`<link rel="alternate">`** (hreflang:0); only in sitemap. | Emit paired hreflang + self-canonical per page from i18n/routes. | NEW |
| High | 471 pages | **Self-canonical on only 3 pages** (`index.html`, `az`/`en` `membership.html`). | Generate per-page absolute canonical. | NEW |
| High | `sitemap.xml` | **66 `<loc>` entries (33 pairs) — omits all ~400 `prominent_figures/**` profiles** that are live and linked from `encyclopedia.html` (~7% coverage). | Extend sitemap generator (or sitemap index) to include profiles. | NEW |
| Med | `sitemap.xml:317–362` | Lists flyer pages that declare `noindex`. | Remove from sitemap or drop `noindex`. | NEW |
| Med | Two Google Fonts URLs | ~400 pages use variable `Inter:opsz,wght@14..32`; ~25 use legacy `Inter:wght@400..900` (`application`, `sponsors`, `sessions_organization`, gateway, `404`). | Standardize on one font URL across generators. | NEW |
| Med | `az/forum/2024/sessions_organization.html:29–34`; `application`/`sponsors`/`donate` | Head script-bundle drift — missing `daab-design-tokens.js` / `daab-breadcrumbs.js` / `daab-page-subtitle.js` vs hub pages. | Align generators to the standard nav-page head bundle (or document intentional omission). | NEW |
| Med | `index.html:8` | Gateway canonical is relative (`az/index.html`), not absolute. | Use absolute production URL or omit. | NEW |
| Low | `.deployignore` | `js/video-gallery-data.json` appears unreferenced. | Confirm dead / remove. | NEW (info) |
| Low | `robots.txt`, `404.html`, gateway redirect | Correct and usable. | — | OK |

---

## 6. Assets / performance

| Sev | Location | Issue | Recommendation | Tag |
|-----|----------|-------|----------------|-----|
| Med | `az`+`en` `foundation.html` images; nav logo site-wide | Images lack `width`/`height` → CLS risk. | Add dimensions or CSS `aspect-ratio`. | NEW |
| Med | `az/foundation.html:127+` | Image paths with Unicode + spaces + commas (`Şuşa qurultayı (001).jpg`). Pass locally; risky on case-sensitive/CDN hosts. | Normalize to ASCII slugs; keep display name in `alt`. | NEW |
| Low | `az/foundation.html:181` | Hotlinked YouTube `maxresdefault.jpg` thumbnail (external dep). | Self-host poster / nocookie embed. | NEW |
| Low | `en/prominent_figures/**` (~600 links) | Source links are Google-search URLs, not stable destinations. | Use direct URLs in generator. | NEW |

---

## 7. Naming / consistency

| Sev | Location | Issue | Recommendation | Tag |
|-----|----------|-------|----------------|-----|
| Med | `css/`: 6 `scientists-*.css` vs ~44 `daab-*.css` | Prefix split; inconsistent `-page` suffix. | Standardize new work on `daab-scientists-*`; migrate gradually. | TRACKED |
| Low | `templates/Forum 2026.html` | Space in filename (not deployed). | Rename if ever promoted. | NEW |

---

## 8. Duplication / architecture (maintainability)

- ~400 prominent-figure profiles duplicate full nav/footer HTML — expected for a no-build static site, but any nav/i18n change requires a full regenerate. Consider shared head/footer injection in one builder. **TRACKED**
- `az`/`en` `membership.html` are legacy meta-refresh stubs to `membership_value.html` — keep if still linked externally, else 301 server-side. **NEW (info)**
- `hazirlanir.html` placeholders (`noindex`) shared for unfinished AZTurk profiles — fine until those ship. **NEW (info)**

---

## Recommended priority order

1. **H1 — `daab-forum-content.css` `forum-anas-leadership-speeches` selectors** (live visual regression; repair CSS + generator + add guard). *Low-risk, same playbook as the activities-layout fix.*
2. **H2 — logistics inline scroll-spy bug** + the 5 inline TOC copies missing `popstate` (swap to the shared module; fixes correctness + AZ/EN parity in one move).
3. **Photo-gallery lightbox focus trap** (keyboard a11y regression).
4. **SEO head pass** (favicon + OG/Twitter + per-page canonical + hreflang) via the shared generators; **extend sitemap** to profiles. High value, generator-owned, low runtime risk.
5. **AZ foundation `<title>`** + head-bundle/font-URL drift normalization.
6. Generated-profile heading hierarchy + decorative-emoji `aria-hidden` (systemic, generator-owned).
7. Backlog (TRACKED): sticky-sidebar extraction, `!important` reduction, breakpoint normalization, `DAAB_SIDEBAR_SPY` / `getStack()` / layout-sync bus, `scientists-*`→`daab-*`, token adoption.

Each change to be verified (validators + affected-page review + version bump) before closing, per `.cursor/rules/daab-careful-changes.mdc`. Several High items are **generator-owned** — fix the emitting helper alongside the output so a rebuild won't regress.

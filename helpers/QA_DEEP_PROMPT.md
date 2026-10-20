# Deep QA prompt — DAAB–WAAS web site

Copy everything below the line into a new agent chat (with this repo open).

---

## Role

You are a senior QA engineer and front-end auditor for **DAAB–WAAS** (`daab-waas-web-site`): a static bilingual (AZ/EN) marketing and association site with a production `Deployment/` package built by `helpers/_build_deployment_folder.py`.

Conduct a **comprehensive, deep QA pass**. Do not stop at surface checks. Verify behavior, content fidelity, i18n parity, asset integrity, accessibility, and deploy readiness. Prefer evidence (file paths, URLs, screenshots, console errors, broken link lists) over opinions.

## Project facts (use these; verify if unsure)

- **Locales:** `az/` and `en/` (mirrors). Canonical production package: `Deployment/`.
- **Home:** `*/index.html` — hero, forum poster (`images/2-ci_forum_poster_EN.png` / `_AZ.png`), CTA to `forum/2026/index.html`, hub cards.
- **Major areas:** mission / foundation / activities / charter / membership / application / sponsorship / donate / executive board / scientists (list, profiles, CVs, media) / Forum 2024 & 2026 / complex-topics (+ approach, apply, informatics) / legal (privacy, terms, cookies, legal-notice) / sitemap / feedback.
- **Shared chrome:** sticky nav, breadcrumbs, lang switch, page-content search (skipped on some pages e.g. home), footer, cookie consent, analytics.
- **Build:** `python helpers/_build_deployment_folder.py` (Windows: `$env:PYTHONIOENCODING='utf-8'`). Asset cache stamps like `?v=YYYYMMDD-HHmm` / `Build YYYYMMDD - HHmm`.
- **Do not** invent product requirements; flag gaps as questions. Prefer source (`az/`/`en/`) vs `Deployment/` drift findings.

## Mission

Produce a structured QA report with severity, reproduction steps, and fix hints. Rank issues. Separate **Blockers / Majors / Minors / Nits / Questions**.

## Method

### 1. Inventory & parity

1. List top-level HTML under `az/` and `en/`; note missing locale twins.
2. Spot-check `Deployment/` vs source for the same paths (home, complex-topics, forum/2026, executive-board, scientists list/profiles).
3. Confirm critical assets exist: logos (`didk-logo.webp`, forum sponsors), posters, scientist photos/thumbs.

### 2. Navigation & IA

1. Primary nav: every item opens the right page in both languages; dropdowns work on mouse and keyboard.
2. Language switch: AZ↔EN keeps the equivalent page (not always home); query/hash behavior is sane.
3. Breadcrumbs: correct trail; home has no bogus crumb; forum subpages correct.
4. Footer links: contact, legal, sitemap; build stamp present and consistent in Deployment after rebuild expectations.
5. Internal links: no 404s for same-locale relative links on sampled high-traffic pages; external links use sensible `rel`/`target`.

### 3. Home page (deep)

1. Hero: title/subtitle/summary panel layout desktop + mobile; Support us / Bizi dəstəkləyin **hidden**.
2. Poster: EN uses `_EN.png`, AZ uses `_AZ.png`; rounded corners; aligns with hero content width; no CSS vertical stretch distorting logos into ellipses.
3. CTA pill under poster: correct copy (EN: “Learn more and register as a participant”; AZ: “Ətraflı məlumat və iştirakçı qeydiyyatı”); links to `forum/2026/index.html`; gap from poster looks intentional.
4. Hub cards: targets correct; no dead “Discover WAAS” search panel / sticky page-search on home.
5. Visual: no broken images; poster QR readable; logos circular on the poster artwork.

### 4. Forum 2026

1. `forum/2026/index.html`: content loads; register CTA points to Cognito participant form (not outdated diaspor.gov.az forum URL unless product says otherwise).
2. `forum/2026/register.html`: sponsor logos (WAAS, DIDK/`didk-logo`, ministry, ANAS); captions; AZ ANAS caption line-breaks if designed that way.
3. Parity EN↔AZ for structure and CTAs.

### 5. Forum 2024

1. Hub and key subpages (program, presentations, sessions_organization, galleries, stories): photos/thumbs load; Bakhtiyar Sirajov photo paths resolve; cache-bust query strings don’t 404.
2. Tables with photos: layout OK on mobile.

### 6. Complex Topics

1. `complex-topics.html`: flyer/poster section; organizing partners; DIDK uses `didk-logo` (not old diaspora-committee) where intended; AZ copy (repository wording, CTAs, data terminology) coherent.
2. Linked pages: approach / apply / informatics — nav TOC / search if present; no broken anchors.

### 7. Scientists

1. List + profiles: JSON/`i18n` loads; search/filter; photos/`_thumbs` exist for sampled profiles.
2. Executive board portraits.
3. Sample CVs (EN+AZ): images and internal links.
4. Media pages (Sirajov, etc.): thumbs and outbound links.

### 8. Membership & forms

1. Membership / value / flyer / application: forms usable; validation messages; disabled states clear.
2. Sponsorship / donate: CTAs and bank/info blocks render.

### 9. i18n & content quality

1. No mixed-language blobs on AZ-only or EN-only surfaces (except proper nouns).
2. EN↔AZ structural parity for sampled pages (sections present both sides).
3. Obvious typos, truncated captions, overlapping text, low-contrast text.

### 10. Responsive & UI polish

1. Breakpoints ~375, 768, 1024, 1280: home, forum 2026, scientists list, complex-topics, application.
2. Sticky header/search: no content jump under chrome; mobile menu open/close; focus traps not broken.
3. Cards/buttons: hit targets; pill CTAs not overflowing.

### 11. Accessibility

1. Skip link works.
2. Images that convey meaning have `alt`; decorative appropriately empty.
3. Buttons/links keyboard reachable; visible focus.
4. Headings outline sane (no skipped levels in a broken way on key pages).
5. Color contrast spot-check on hero text and primary buttons.

### 12. Performance & assets (lightweight)

1. Oversized images on home/forum without dimensions where layout shifts.
2. Missing `width`/`height` causing CLS on posters/logos.
3. Duplicate or orphaned heavy assets called out only if linked from pages.

### 13. Console & network

1. Open home + forum 2026 + scientists profiles + complex-topics in browser: no hard JS errors.
2. Failed network requests for JS/CSS/JSON/images on those pages.

### 14. Deployment readiness

1. Note source vs Deployment drift for files touched recently (home, posters, hub CSS, complex-topics, page-content-search skip list).
2. State whether a Deployment rebuild is recommended before ship.
3. Confirm `.deployignore` / helpers not required for reading QA, but flag if Deployment clearly stale.

## Out of scope (unless you find a blocker)

- Rewriting copy for tone.
- Full WCAG certification.
- Backend/Cognito form field validation beyond “link opens and looks like the right form”.
- Committing or deploying.

## Deliverable format

```markdown
# DAAB–WAAS deep QA report

## Summary
[1–3 sentences: ship / ship with fixes / do not ship]

## Blockers
### [ID] Title
- **Where:** path / locale / viewport
- **Steps:** …
- **Expected / Actual:** …
- **Evidence:** …
- **Fix hint:** …

## Majors
…

## Minors
…

## Nits
…

## Locale parity gaps
…

## Deployment drift
…

## Test matrix covered
| Area | AZ | EN | Mobile | Notes |
|------|----|----|--------|-------|

## Open questions for product
…
```

## Working rules

- Start with home + Forum 2026 + scientists + complex-topics, then widen.
- Always check **both** `az` and `en` for issues you file.
- Prefer fixing nothing unless asked; this pass is **audit-only**.
- If the environment can’t browse, still do static analysis (HTML/CSS/JS/asset existence) and label browser gaps clearly.
- Be specific: cite `az/index.html`, `images/2-ci_forum_poster_AZ.png`, etc.

Begin now. Explore the repo, run checks, and return the report.

# DAAB bilingual website strategy (Azerbaijani + English)

This document describes a recommended approach for converting the DAAB website into a professional bilingual platform, initially supporting **Azerbaijani (AZ)** and **English (EN)**. It is tailored to the current stack: static HTML on GitHub Pages / `daab-waas.com`, shared `css/` + `js/`, Python helpers for the scientist catalogue, `*_az.html` naming, and optional **Google Sites** links or embeds.

---

## 1. Recommended overall architecture

### Target model: static site + structured content + thin shared shell

```text
daab-waas.com/
├── index.html              → language gateway (or redirect)
├── az/                     → Azerbaijani pages (canonical for now)
│   ├── index.html
│   ├── scientists/
│   │   ├── list.html
│   │   └── profiles.html
│   └── ...
├── en/                     → English mirror
│   ├── index.html
│   ├── scientists/
│   └── ...
├── assets/                 → shared (or keep css/, js/, images/ at root)
│   ├── css/
│   ├── js/
│   └── images/
├── i18n/
│   ├── ui.json             → nav, buttons, labels (az + en)
│   └── routes.json         → page slug ↔ file mapping
└── data/
    ├── scientists.az.json
    └── scientists.en.json
```

### Principles

| Layer | What it holds | How it changes per language |
|--------|----------------|-----------------------------|
| **Shell** | Nav, footer, language switcher, layout | `i18n/ui.json` + one nav partial (JS or build) |
| **Marketing pages** | Foundation, mission, charter, membership | Translated HTML **or** MD → HTML at build time |
| **Scientist catalogue** | 83 profiles | **Structured data** (JSON), not duplicated 4k-line HTML |
| **CV pages** | Long-form bios | Keep per-person pages; some CVs already use EN/AZ toggles |

### Why this fits DAAB

- The project already avoids a backend; static hosting stays simple and Google-Sites-friendly.
- Catalogue content is already regenerated from DOCX via `helpers/` — extend that pipeline for English instead of hand-copying `scientists_card_view_az.html`.
- CV pages such as `cv/afina_barmanbay.html` already use an **in-page language toggle** — that pattern can remain for deep profiles while the main site uses **URL-based** languages.

### What to avoid as the primary strategy

- **Browser-only translation** (Google Translate widget, auto-translate plugins): poor SEO, inconsistent terminology, breaks legal/formal tone.
- **One HTML file with everything hidden in two languages**: unmaintainable at catalogue size.
- **Duplicating 12 full pages × 2 by hand** without shared nav/footer: high risk of link rot (already observed with renames).

---

## 2. Separate files vs folders vs templates vs dynamic systems

### Option comparison (for DAAB)

| Approach | Fit for DAAB | Verdict |
|----------|--------------|---------|
| **A. Parallel files** (`foundation_az.html` + `foundation_en.html`) | Quick start; matches today | Good **Phase 1**, weak at scale without automation |
| **B. Language folders** (`/az/...`, `/en/...`) | Clear URLs, SEO, Google Sites links | **Recommended primary structure** |
| **C. Templates + build** (Eleventy, Astro, Hugo) | Best long-term; one nav, one layout | **Recommended Phase 2** |
| **D. Client-side i18n only** (JSON + JS replaces text) | Works for UI labels; weak for long bios & SEO | **UI only**, not whole site |
| **E. CMS / headless** (Sanity, Strapi) | Useful if many editors | Optional later |

### Recommended path: B now → C soon

**Phase 1 (8–12 weeks)**

- Introduce `/az/` and `/en/` (or keep root as AZ and add `/en/` only).
- Parallel page files generated from a **single layout template** (e.g. Python/Jinja in `helpers/`).
- Extract nav/footer into `js/daab-shell.js` or build-time includes.

**Phase 2**

- Move to **Eleventy** or **Astro** (static, no server):
  - `src/_includes/nav.njk`
  - `src/az/foundation.njk`, `src/en/foundation.njk`
  - Collections for scientists from `data/scientists.{lang}.json`
- Same deploy target: static HTML on GitHub Pages.

**Translation management tools** (Phrase, Lokalise, Crowdin) are useful for **managing strings and workflows**, not for serving pages. Use them to export JSON into `i18n/`, still deploy static HTML.

---

## 3. Language switching and navigation (UX)

### URL-based switching (required for SEO and bookmarks)

- User on `https://daab-waas.com/az/scientists/list.html`
- Switcher goes to `https://daab-waas.com/en/scientists/list.html`
- Same **page identity**, different language — not a JS toggle that hides content.

### UI pattern (desktop + mobile)

Place in the **nav strip**, right side (before search if present):

```text
[ AZ | EN ]   or   AZ ▾  (dropdown on very small screens)
```

**Rules**

- Show the **active language** clearly (filled pill / underline).
- Use `aria-current="true"` on the active language.
- Persist choice in `localStorage` only as a **hint** for `/` redirect; do not rely on it for routing.
- On first visit to `/`, redirect using:
  1. `?lang=en` query (for Google Sites campaign links), else
  2. `Accept-Language` (optional, conservative), else
  3. **Default: Azerbaijani** (primary audience).

### Navigation content

- All `href`s in nav must be **language-prefixed** (`/en/charter.html`, not `/charter_az.html`).
- Retire `_az` / `_en` **filename suffixes** when folders carry language (`/az/charter.html` is sufficient).
- Scientists submenu:
  - AZ: “Siyahı” / “Profil”
  - EN: “Directory” / “Profiles”
  - Same routes under each language tree.

### Compatibility with existing `daab-nav.js`

- Today nav compares `location.pathname` to filenames like `scientists_list_view_az.html`.
- Refactor to **data attributes**: `data-nav-id="scientists-list"` + `data-lang="az"` so one script works for both trees.

---

## 4. URL structure recommendations

### Preferred (clean, scalable)

```text
https://daab-waas.com/az/                    → home (AZ)
https://daab-waas.com/en/                    → home (EN)
https://daab-waas.com/az/scientists/list/
https://daab-waas.com/en/scientists/list/
https://daab-waas.com/az/membership/
https://daab-waas.com/en/membership/
```

### Root behaviour

| Strategy | Pros | Cons |
|----------|------|------|
| **`/` = language picker** (two buttons) | Neutral; good for Google Sites | Extra click |
| **`/` → 302 to `/az/`** | Simple default | English users need `/en/` link |
| **`/` mirrors `/az/`** | No redirect | EN-only URLs less obvious |

**Recommendation:** small gateway at `/` with AZ (primary) + EN, plus **301 redirects** from old URLs (`foundation_az.html` → `/az/foundation/`).

### CV URLs

Keep stable person slugs:

```text
/cv/afina_barmanbay.html          → both languages in-page (current pattern), or
/en/cv/afina-barmanbay.html
/az/cv/afina-barmanbay.html
```

For SEO, **separate URLs per language** are better than toggle-only; toggles are fine for **supplementary** CVs linked from the catalogue.

### Google Sites

- Do **not** embed different languages in one iframe without a clear URL.
- Use two buttons: “Azərbaycan versiyası” → `https://daab-waas.com/az/`, “English version” → `https://daab-waas.com/en/`.
- Prefer **open in new tab** over iframe (see `DAAB-Site-Stability-and-Deployment-Guide.md` for iframe/header issues).

---

## 5. SEO for multilingual sites

### Required on every page

```html
<html lang="az">   <!-- or lang="en" -->
<link rel="canonical" href="https://daab-waas.com/az/scientists/list.html" />
<link rel="alternate" hreflang="az" href="https://daab-waas.com/az/scientists/list.html" />
<link rel="alternate" hreflang="en" href="https://daab-waas.com/en/scientists/list.html" />
<link rel="alternate" hreflang="x-default" href="https://daab-waas.com/az/scientists/list.html" />
```

- **Unique `<title>` and `meta description` per language** (not translated by JS after load).
- **One canonical per URL** — avoid AZ and EN sharing the same URL.
- **`x-default`**: point to Azerbaijani if that is the primary market.

### Content SEO

- Scientist names: often **same in both languages**; bios need full English prose (professional translation), not machine-only.
- Headings: translate H1/H2 where they carry keywords (“İdarə Heyəti” → “Executive Board”).
- **Sitemap**: `sitemap.xml` listing all AZ and EN URLs.
- **Structured data** (`Organization`, `WebSite`): one JSON-LD per language page with `inLanguage`.

### Redirects

Maintain `_redirects` (Netlify) or `.htaccess` / Cloudflare rules:

- Old `*_az.html` → new `/az/...` (301)
- Prevents broken bookmarks and Google Sites links

---

## 6. Maintainability and adding languages later

### Design for N languages from day one

- Store UI strings as nested JSON: `{ "nav.home": { "az": "...", "en": "...", "tr": "..." } }`.
- Scientist records:

  ```json
  {
    "id": "afina-barmanbay",
    "name": { "display": "Afina Barmanbay" },
    "bio": { "az": "...", "en": "..." }
  }
  ```

- **Page registry** (`routes.json`): logical page id → slug per language.

### Workflow

1. Content change in AZ (DOCX / editors)
2. Run `helpers/sync_*` → updates `data/scientists.az.json` + regenerates AZ HTML
3. English updated in CAT tool or parallel DOCX → `scientists.en.json` → regenerate EN HTML
4. `python helpers/_validate_site.py` + link checker in CI
5. Deploy; bump `?v=` on shared CSS/JS only when assets change

### Third language (e.g. Turkish)

- Add `/tr/` folder and `ui.tr` keys — no rename of existing files.
- Scientist data: add `bio.tr` field; list filters use same code.

---

## 7. Menus, search, filters, metadata, and navigation

| Feature | Multilingual approach |
|---------|------------------------|
| **Menus** | From `i18n/ui.json`; injected at build or via `daab-shell.js` |
| **Site search** | Index **per language** (separate JSON index or Pagefind index per `/az/` and `/en/`) |
| **Scientist filters** | Option labels translated; filter values (country names) via lookup table (“Almaniya” / “Germany”) |
| **Sort controls** | Label “Sırala” / “Sort by”; column headers from i18n |
| **Pagination / rows per page** | Strings from i18n |
| **`<title>`, OG tags** | Per-language in `<head>` at build time |
| **`lang` attribute** | `az` or `en` on `<html>` |
| **Footer legal text** | Separate blocks per language |

### Scientist catalogue (critical)

- Move off 2,000+ line duplicated HTML to:
  - `scientists_list.{lang}.html` (thin shell) + `data/scientists.{lang}.json`
- List page JS reads JSON (extend `js/scientists-catalog-data.js` — split by language or add locale fields).
- Card/profile page: generate from same data; separate URLs per language preferred for SEO.

### Search overlay (`index.html` pattern)

- Duplicate search index entries with `lang` field, or two indexes.
- Only show results matching current path prefix (`/en/` → EN pages only).

---

## 8. Fonts and typography

### Current stack

- **Inter** (UI, body)
- **Playfair Display** (headings)
- Both support **Latin**; Azerbaijani uses Latin script with **ə, ş, ç, ğ, ö, ü, ı, İ**.

### Recommendations

| Topic | Guidance |
|--------|----------|
| **AZ** | Keep Inter + Playfair; set `lang="az"` on `<html>` |
| **EN** | Same families — consistent brand |
| **Line length** | English often runs 10–15% longer; allow flexible grids; `hyphens: auto` for EN where appropriate |
| **Character set** | Verify fonts include **Ə/ə** and **İ/ı** (Inter and Playfair do) |
| **Search/sort** | Keep NFC normalization; add EN sort rules where needed |

Load fonts once in shared CSS; subsetting optional for performance.

---

## 9. Google Sites embedding limitations

| Constraint | Implication for bilingual |
|------------|---------------------------|
| Sites cannot host the repo | All languages live on **daab-waas.com** (or GitHub Pages) |
| iframe may break (X-Frame-Options, scroll) | Prefer **outbound links** per language |
| Every URL change needs manual Sites update | Stabilize URLs early (`/az/`, `/en/`) |
| HTTPS required | Both language roots must be HTTPS |

### Practical setup on Google Sites

- Section: “Official website”
  - Button → `https://daab-waas.com/az/`
  - Button → `https://daab-waas.com/en/`
- Avoid embedding the full catalogue iframe; link to list view instead.

See also: `documents/DAAB-Site-Stability-and-Deployment-Guide.md` (§2.6, §10).

---

## 10. Static vs dynamic — pros and cons

### Static multilingual (recommended for DAAB)

**Pros**

- Works on GitHub Pages; no server cost
- Fast, cacheable, reliable with Google Sites links
- Predictable SEO (real URLs per language)
- Aligns with current skills and Python helpers

**Cons**

- More HTML files or a build step
- Translation updates require regenerate + redeploy
- No automatic fallback unless built in

### Dynamic (SSR, CMS, client SPA)

**Pros**

- Single template; instant UI string updates
- Easier editor workflows with CMS

**Cons**

- Needs hosting with server or larger client bundle
- Harder iframe/embed story
- Overkill for ~15 pages + catalogue unless platform ops are invested

### Hybrid (best balance)

- **Static HTML output** + **build-time** or **JSON-driven** client render for catalogue only
- Nav/footer via shared partial

---

## 11. File and directory organization

### Clean layout (migration target)

```text
az/
  index.html
  foundation.html
  mission.html
  activities.html
  scientists/
    list.html
    profiles.html
  executive-board.html
  charter.html
  membership.html
en/
  (mirror)
cv/
  afina-barmanbay.html
css/
js/
  daab-nav.js
  daab-i18n.js            # lang detection, switcher, prefix helpers
  daab-shell.js           # optional: inject nav/footer
images/
i18n/
  ui.az.json
  ui.en.json
data/
  scientists.az.json
  scientists.en.json
helpers/
  build_pages.py
  sync_scientists_from_docx.py
```

### Deprecate gradually

- `*_az.html` at root → redirects to `/az/...`
- Use **one** lowercase image path convention (`images/scientists-photos/`) — avoid case mismatches on Linux hosting.

---

## 12. Avoiding duplicated code and maintenance problems

| Problem | Solution |
|---------|----------|
| Nav copied in 12 HTML files | One **nav partial** (build) or shared inject |
| Footer duplicated | Same as nav |
| 2× scientist card HTML | **Generate** from JSON + template |
| CSS duplicated | Keep one bundle: `daab-common.css` |
| Link drift AZ/EN | `routes.json` maps logical page id → slug per lang |
| Validation | Extend `_validate_site.py` to check AZ/EN pairs + hreflang |

**Rule:** editors do not edit 2,000-line HTML; they edit **data + short templates**.

---

## 13. Modern UI/UX for bilingual experience

### Desktop

- Language switcher always visible in nav (not only footer).
- Use **AZ** / **EN** text labels (not flags-only — accessibility).
- Cross-links in hero between list and profile views — mirror per language.

### Mobile

- Language switcher at top of mobile menu.
- Touch targets ≥ 44px.
- Allow longer English labels without overflow (flexible nav, shorter filter labels or icons + `aria-label`).

### Content UX

- Do not mix languages on one page (except optional original forms in names).
- Dates/numbers: consistent format per locale.
- Downloads: suffix `_az` / `_en` in filenames.

### Accessibility

- `lang` on `<html>`
- Translated `aria-label`s for menu, search, filters
- Visible focus on language links

---

## 14. Phased implementation roadmap

| Phase | Deliverable | Effort (indicative) |
|-------|-------------|---------------------|
| **0** | URL map, redirects from `*_az.html`, language switcher shell | 1–2 weeks |
| **1** | `/en/` mirror of main pages (professional EN copy) | 4–8 weeks (content-bound) |
| **2** | Scientist data `scientists.{az,en}.json` + regenerate list/cards | 2–4 weeks dev |
| **3** | hreflang, sitemap, CI validation | 1 week |
| **4** | Eleventy/Astro migration (optional) | 2–4 weeks |
| **5** | Third language readiness | incremental |

---

## 15. Summary recommendation

For DAAB, the **professional and realistic** approach is:

1. **Static bilingual site** with **`/az/` and `/en/` URL trees** (not JS-only translation).
2. **Shared layout** via a light **build step** (Python in `helpers/` now; Eleventy later).
3. **Scientist catalogue from JSON** per language, regenerated from DOCX/workflows already in use.
4. **Central i18n** for nav, filters, buttons, metadata.
5. **hreflang + redirects + sitemap** for SEO.
6. **Google Sites**: link to `/az/` and `/en/`; avoid fragile iframes.
7. **Same typography** (Inter + Playfair) with layout tolerance for longer English strings.

That delivers a **seamless bilingual UX**, scales to more languages, and fits the current repository without requiring a heavy CMS or breaking static hosting.

---

## 16. Suggested first implementation slice

When ready to implement in the repository:

1. Add `documents/DAAB-Bilingual-Website-Strategy.md` (this file) as the reference.
2. Create `i18n/routes.json` and `js/daab-i18n.js` (language switcher + path helpers).
3. Add `/en/index.html` skeleton and language gateway at `/`.
4. Add 301 redirect rules from legacy `*_az.html` paths.
5. Defer full scientist catalogue migration until Phase 2.

---

*Document version: 1.0 — May 2026*  
*Related: `DAAB-Site-Stability-and-Deployment-Guide.md`*

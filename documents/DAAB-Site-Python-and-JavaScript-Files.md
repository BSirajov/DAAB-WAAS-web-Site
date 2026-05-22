# DAAB website — Python (`.py`) and JavaScript (`.js`) files

**Project:** DAAB-WAAS web site  
**Location:** Repository root (same folder as `index.html`, `scientists_card_view_az.html`, etc.)  
**Last updated:** May 2026

This document describes every `.py` (in `helpers/`) and `.js` (in `js/`) file in the project: what each one does, whether it is required for the public website, and how the pieces fit together.

**Repository layout (public site assets):** see root `README.md` and `.cursor/rules/daab-file-organization.mdc` for where to place **new** files.

```
DAAB-WAAS web site/
├── css/           ← all .css files
├── js/            ← all .js files
├── helpers/       ← all maintenance .py files
├── images/
├── documents/
├── *.html         Site pages (root only)
└── _pdf_extract.txt   Book extract (optional, not deployed)
```

---

## Overview

| Type | Count | Runs where | Required for hosting? |
|------|-------|------------|------------------------|
| **`.js`** | 3 | Visitor’s browser | **Yes** (navigation + CV filters) |
| **`.py`** | 12 | Developer machine only | **No** (maintenance / content tools) |

The live site is **static HTML, CSS, and JavaScript**. There is no Node.js server or Python backend in production. Pages are opened directly or served from any static host (GitHub Pages, etc.).

---

## JavaScript files (`.js`)

These files are **loaded by HTML pages** via `<script src="...">` and run in the user’s browser.

### 1. `daab-nav.js`

| | |
|---|---|
| **Used on** | Most site pages: `index.html`, `scientists_list_view_az.html`, `scientists_card_view_az.html`, `charter_az.html`, `activities_az.html`, `foundation_az.html`, `executive_board_az.html`, `membership_terms_az.html`, `mission_vision_values_az.html` |
| **Typical load** | `<script src="js/daab-nav.js?v=2" defer></script>` |
| **Purpose** | Shared site navigation behavior |

**Responsibilities:**

- Mobile menu toggle (hamburger) for viewports ≤1180px
- Open/close “Alimlərimiz” dropdown on mobile (tap; desktop uses CSS hover)
- Close menu and dropdowns when a nav link is clicked
- `aria-expanded` / `aria-label` updates for accessibility

**Does not:** handle search overlay, scientist filters, or page-specific content (those are inline scripts or other `.js` files).

---

### 2. `scientists-catalog-data.js`

| | |
|---|---|
| **Used on** | `scientists_card_view_az.html` only |
| **Typical load** | `<script src="js/scientists-catalog-data.js?v=1"></script>` (no `defer`; loads before filter script) |
| **Purpose** | Shared scientist catalogue metadata for the CV page |

**Exports:**

```javascript
window.SCIENTISTS_CATALOG_DATA = [ /* 83 records */ ];
```

**Each record includes (example fields):**

| Field | Example | Use |
|-------|---------|-----|
| `say` | `1` | Order / ID |
| `yasadigi_olke` | `"ABŞ"` | Country name |
| `ad_soyad` | `"Asəf Salamov"` | Display name |
| `email` | `"aasalamov@lbl.gov"` | Contact |
| `ixtilas` | `"Biologiya"` | Discipline |
| `elmi_derece` | `"PhD"` | Degree |
| `cinsi` | `"kişi"` / `"qadın"` | Gender |
| `url` | Optional external profile URL (leave empty if none) | External link on list page when set |

**Used by:** `scientists-cv-filters.js` to populate country, ixtisas, and degree dropdowns.

**Note:** The list page `scientists_list_view_az.html` embeds the **same data** as inline `const DATA = [...]` inside the HTML file, not this `.js` file. Keeping both in sync when editing scientists is important.

---

### 3. `scientists-cv-filters.js`

| | |
|---|---|
| **Used on** | `scientists_card_view_az.html` only |
| **Typical load** | `<script src="js/scientists-cv-filters.js?v=8" defer></script>` |
| **Purpose** | Search and filter the 83 CV profile cards |

**Responsibilities:**

- Read search box (`#searchInput`) and selects: country, ixtisas, degree
- **Filter logic:** AND — all active criteria must match
- Match against each card’s `data-search`, `data-country`, `data-ixtilas`, `data-degree`
- Hide non-matching cards with class `.is-filtered-out` (`display: none`)
- Update result count (`#resultCount`): e.g. `12 uyğun profil (83 ümumi)`
- Show/hide empty state (`#no-results`)
- Highlight active filter controls (`.sel-wrap.active`)
- “Hamısını sıfırla” clears all inputs and shows all cards
- Per-select “×” clear buttons
- Optional smooth scroll to first visible card when country filter changes

**Related styles:** `css/scientists-catalog-toolbar.css` (toolbar layout, not in `.js`).

**UX proposal:** See `documents/Scientists-CV-Filtering-UX-Proposal.md` for recommended future behavior (chips, animations, empty state).

---

### Script versioning (`?v=...`)

HTML references use query strings such as `?v=2` or `?v=8` so browsers fetch a new file after updates. Bump the number when you change that script.

---

### JavaScript *not* in separate files

Much behavior lives in **inline `<script>` blocks** inside HTML:

| Location | Purpose |
|----------|---------|
| `scientists_list_view_az.html` | `const DATA = [...]`, table render, sort, pagination, filters |
| Most pages (footer area) | Site-wide search overlay (`#search-overlay`, Ctrl+K) |

These are part of the `.html` files, not standalone `.js` modules.

---

## Python files (`.py`)

All maintenance scripts live in **`helpers/`**. They are **developer tools** only—not used by the public site.

Run from the **repository root**:

```bash
cd "path/to/DAAB-WAAS web site"
python helpers/_rebuild_cv_catalog.py
```

Paths to HTML, `css/`, `js/`, and `images/` are resolved via `helpers/_paths.py` (`ROOT` = repo root). See also `helpers/README.md`.

### Content pipeline (book → website)

| File | Purpose |
|------|---------|
| **`helpers/_extract_pdf.py`** | Extracts text from the forum/book PDF (`documents/Forum_haqqinda_kitab_...pdf`) into `_pdf_extract.txt` (repo root) using `pypdf`. |
| **`helpers/_sync_scientists_from_book.py`** | Parses the book chapter from `_pdf_extract.txt` and updates CV card titles/bios in `scientists_card_view_az.html` (verbatim text, bullets, awards blocks). |

### CV catalogue build & repair

| File | Purpose |
|------|---------|
| **`helpers/_rebuild_cv_catalog.py`** | Rebuilds all **83** CV cards from book profiles + `js/scientists-catalog-data.js` + photos in `images/scientists-photos/`. |
| **`helpers/_fix_cv_catalog.py`** | Repairs broken catalogue HTML: re-extracts card blocks and rebuilds a single flat `.cards-grid`. |
| **`helpers/_normalize_cv_cards.py`** | Normalizes every card to one HTML template (header, meta rows, bio structure). |
| **`helpers/_restructure_cv_cards.py`** | Adds country under name, inline İxtisas/E-poçt rows, removes country section headers, flattens grid. |
| **`helpers/_format_card_bios.py`** | Improves bio formatting (split paragraphs, bullet lists where appropriate). |
| **`helpers/_recover_cv_from_transcript.py`** | One-off recovery attempt from agent chat transcript (emergency use only). |

### Data alignment & quality checks

| File | Purpose |
|------|---------|
| **`helpers/_build_cv_enrichment.py`** | Matches CV cards to `scientists_list_view_az.html` DATA by name; adds/updates `data-email`, `data-ixtilas`, `data-degree`, `data-search`, and meta HTML. Can rewrite `js/scientists-catalog-data.js`. |
| **`helpers/_validate_cv_cards.py`** | Validates card HTML (meta rows, header structure, closing tags). |
| **`helpers/_check_name_order.py`** | Compares scientist name order on CV page vs list page DATA. |
| **`helpers/_print_norms.py`** | Debug helper: prints normalized names for tricky matches (Barmanbay, Səbziyeva, etc.). |

### Typical workflow (when updating scientists)

1. Update source data (`scientists_list_view_az.html` DATA and/or `js/scientists-catalog-data.js`).
2. If bios come from the book: run `helpers/_extract_pdf.py` (if PDF changed) → `helpers/_sync_scientists_from_book.py` or `helpers/_rebuild_cv_catalog.py`.
3. Run `helpers/_build_cv_enrichment.py` if emails/ixtisas/search attributes need syncing.
4. Run `helpers/_validate_cv_cards.py` to catch HTML issues.
5. Open `scientists_card_view_az.html` in a browser and test filters manually.

---

## How `.js` and `.py` work together

```
┌─────────────────────────────────────────────────────────────┐
│  MAINTENANCE (your computer) — helpers/*.py                 │
│  PDF / book text → HTML cards in scientists_card_view_az.html      │
│  scientists_list_view_az DATA → js/scientists-catalog-data.js       │
└──────────────────────────────┬──────────────────────────────┘
                               │ writes / updates
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  STATIC SITE (hosted files)                                 │
│  scientists_card_view_az.html  (83 card blocks + inline CSS)       │
│  js/scientists-catalog-data.js  (metadata)                  │
│  js/scientists-cv-filters.js  (filter UI)                   │
│  js/daab-nav.js  (navigation)                               │
│  css/daab-common.css, css/scientists-catalog-toolbar.css, images    │
└──────────────────────────────┬──────────────────────────────┘
                               │ visitor opens page
                               ▼
┌─────────────────────────────────────────────────────────────┐
│  BROWSER — .js runs                                         │
│  Load data → fill dropdowns → filter cards → update count     │
└─────────────────────────────────────────────────────────────┘
```

---

## Deployment checklist

**Include in hosting (required):**

- All `.html`, `css/*.css`, `js/*.js`, images

**Optional / omit from hosting:**

- `helpers/` (all Python maintenance scripts)
- `_pdf_extract.txt` (book extract, if present)
- `documents/` folder (unless you want docs public)

---

## File list (quick reference)

### JavaScript (3)

1. `js/daab-nav.js`
2. `js/scientists-catalog-data.js`
3. `js/scientists-cv-filters.js`

### Python (`helpers/`, 12 scripts + `_paths.py`)

1. `helpers/_extract_pdf.py`
2. `helpers/_sync_scientists_from_book.py`
3. `helpers/_rebuild_cv_catalog.py`
4. `helpers/_fix_cv_catalog.py`
5. `helpers/_normalize_cv_cards.py`
6. `helpers/_restructure_cv_cards.py`
7. `helpers/_format_card_bios.py`
8. `helpers/_build_cv_enrichment.py`
9. `helpers/_validate_cv_cards.py`
10. `helpers/_check_name_order.py`
11. `helpers/_print_norms.py`
12. `helpers/_recover_cv_from_transcript.py`

---

## Related documentation

- `documents/Scientists-CV-Filtering-UX-Proposal.md` — UX/UI behavior for CV page filtering

---

*Maintainers: update this document when adding, renaming, or removing `.py` or `.js` files.*

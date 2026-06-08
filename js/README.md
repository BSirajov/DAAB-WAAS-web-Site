# JavaScript

Client-side scripts for the DAAB static site. Loaded from HTML pages in the site root.

| File | Purpose |
|------|---------|
| `daab-nav.js` | Mobile navigation menu and “Alimlərimiz” dropdown (tap on small screens and touch devices). |
| `daab-mobile.js` | Nav height CSS variable, body scroll lock for menu/search, search overlay backdrop tap. |
| `scientists-catalog-data.js` | `window.SCIENTISTS_CATALOG_DATA` — 83 scientists (metadata for CV filters). |
| `scientists-cv-filters.js` | Search and filter UI on `az/scientists/profiles.html`. |

**Typical references (root HTML pages):**

```html
<script src="js/daab-nav.js?v=3" defer></script>
<script src="js/daab-mobile.js?v=1" defer></script>
```

**CV catalogue page (load order matters):**

```html
<script src="js/scientists-catalog-data.js?v=1"></script>
<script src="js/scientists-cv-filters.js?v=8" defer></script>
```

`scientists-catalog-data.js` must load before `scientists-cv-filters.js` (no `defer` on the data file).

**Note:** `az/scientists/list.html` embeds catalogue data inline as `const DATA = [...]`; only the CV page uses `scientists-catalog-data.js`.

**Related:** Python maintenance scripts in `../helpers/`.

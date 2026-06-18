# JavaScript

Client-side scripts for the DAAB static site. Loaded from HTML pages under `az/` and `en/`.

| File | Purpose |
|------|---------|
| `daab-nav.js` | Primary navigation, mega-menu, mobile menu. |
| `daab-mobile.js` | Nav height CSS variable, body scroll lock, search overlay. |
| `scientists-catalog-data.js` | `window.SCIENTISTS_CATALOG_DATA` — scientist list metadata. |
| `scientists-profiles-render.js` | Fetches `i18n/scientists-profiles.json` and renders CV cards on profiles pages. |
| `scientists-cv-filters.js` | Search, filter, and sort on `az/en/scientists/profiles.html`. |
| `scientists-list-catalog.js` | List page catalogue (cards/table views). |

**Typical references (from `az/` or `en/` pages):**

```html
<script src="../js/daab-nav.js?v=31" defer></script>
<script src="../js/daab-mobile.js?v=6" defer></script>
```

**Scientists profiles page (load order matters):**

```html
<script defer src="../js/scientists-profiles-render.js?v=1"></script>
<script defer src="../js/scientists-cv-filters.js?v=5"></script>
```

`scientists-profiles-render.js` must run before `scientists-cv-filters.js` (filters wait for render event).

## Build-only / not linked from live HTML

Kept for unpublished knowledge-treasury pages and helper pipelines; listed in `.deployignore`:

- `prominent-figures-catalog.js`
- `prominent-figures-catalog-data.js`
- `prominent-figures-catalog-data-en.js`

See also build-only CSS in `../css/README.md` and `helpers/_deploy_assets.py`.

**Related:** stylesheets in `../css/`; maintenance tools in `../helpers/`.

# DAAB bilingual environment (AZ / EN)

This folder documents the **Phase 0** bilingual infrastructure added to the static site.

## Layout

| Path | Purpose |
|------|---------|
| `i18n/routes.json` | Page registry: logical IDs and `/az/` + `/en/` paths |
| `i18n/ui.json` | Shared UI strings (nav, gateway, stubs) |
| `js/daab-i18n.js` | Language detection, alternate URLs, asset root, gateway redirect |
| `js/daab-shell.js` | Injects **AZ \| EN** switcher in the nav |
| `css/daab-lang.css` | Switcher and gateway styles |
| `az/` | Azerbaijani pages |
| `en/` | English pages |
| `index.html` | Language gateway at site root (redirects to `/az/` or `/en/`) |
| `sources/home_az.html` | Build source for regenerating `az/index.html` only |
| `helpers/_build_bilingual_tree.py` | Regenerates home, English stubs, sitemap, gateway |

## URLs (local preview)

- **Site entry:** `http://localhost:8010/` → redirects to `/az/` (or `/en/` if `localStorage daab-lang=en`)
- **Choose language:** `http://localhost:8010/index.html?choose=1`

## Regenerate SEO / home after edits

```bash
python helpers/_build_bilingual_tree.py
```

By default this rebuilds `az/index.html` from `sources/home_az.html`, refreshes `/en/` stubs, sets the root gateway, and updates `sitemap.xml`.

- **`--no-gateway`** — keep a full `index.html` at repo root instead of the redirect
- **`--seo-only`** — update `sitemap.xml` and `robots.txt` only

## Language switcher

On any page that loads `daab-i18n.js` + `daab-shell.js`, the nav shows **AZ | EN**. The active language is highlighted; the other link goes to the matching page in `routes.json`.

Preference is stored in `localStorage` (`daab-lang`) and used by `index.html` for automatic redirect.

## Publish a completed English page

```bash
python helpers/_publish_en_pages.py foundation
python helpers/_validate_bilingual.py
```

## Validation

```bash
python helpers/_validate_bilingual.py
python helpers/_validate_site.py
```

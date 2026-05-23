# DAAB bilingual environment (AZ / EN)

This folder documents the **Phase 0** bilingual infrastructure added to the static site.

## Layout

| Path | Purpose |
|------|---------|
| `i18n/routes.json` | Page registry: logical IDs, `/az/` and `/en/` paths, legacy filenames |
| `i18n/ui.json` | Shared UI strings (nav, gateway, stubs) |
| `js/daab-i18n.js` | Language detection, alternate URLs, asset root, gateway redirect |
| `js/daab-shell.js` | Injects **AZ \| EN** switcher in the nav |
| `css/daab-lang.css` | Switcher and gateway styles |
| `az/` | Azerbaijani pages (built from legacy `*_az.html`) |
| `en/` | English pages (home + “translation in progress” stubs) |
| `index.html` | Language gateway at site root (redirects to `/az/` or `/en/`) |
| `helpers/_build_bilingual_tree.py` | Regenerates `az/` and `en/` after content edits |
| `helpers/_thin_legacy_redirects.py` | Rebuilds thin redirect stubs for root `*_az.html` |

## URLs (local preview)

- **Site entry:** `http://localhost:8010/` → redirects to `/az/` (or `/en/` if `localStorage daab-lang=en`)
- **Choose language:** `http://localhost:8010/index.html?choose=1`

## Regenerate after editing legacy pages

```bash
python helpers/_build_bilingual_tree.py
```

By default this rebuilds `/az/` and `/en/`, patches legacy pages, sets the root gateway, and updates `sitemap.xml`.

- **`--no-gateway`** — keep a full `index.html` at repo root instead of the redirect
- **`--no-patch-legacy`** — skip updating root `*_az.html`
- **`--redirects`** — meta refresh from legacy files to `/az/` (optional)

## Language switcher

On any page that loads `daab-i18n.js` + `daab-shell.js`, the nav shows **AZ | EN**. The active language is highlighted; the other link goes to the matching page in `routes.json`.

Preference is stored in `localStorage` (`daab-lang`) and used by `index.html` for automatic redirect.

## Publish a completed English page

```bash
python helpers/_publish_en_pages.py mission
```

This copies `az/mission.html` → `en/mission.html` with professional English text. Pages marked `<!-- daab-en-complete -->` are **not** overwritten when you run `_build_bilingual_tree.py`.

**Published:** all main `en/*.html` pages plus `en/scientists/list.html` and `en/scientists/profiles.html`. Charter articles, activity card bodies, and profile descriptions remain AZ where marked with on-page banners.

```bash
python helpers/_publish_en_pages.py all
python helpers/_publish_en_pages.py charter
python helpers/_publish_en_pages.py scientists   # list + profiles
```

**Before deploy:** see `DAAB-Launch-Checklist.md` and run `python helpers/_validate_bilingual.py`.

**Later (content):** full EN charter articles, activity bodies, profile bios — or Phase 2 `data/scientists.{az,en}.json`.

## Related

- `DAAB-Bilingual-Website-Strategy.md` — full strategy and roadmap

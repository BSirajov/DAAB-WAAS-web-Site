# Maintenance scripts (Python)

Developer-only tools for updating catalogue HTML, syncing book text, and validating structure. **Not used by the public website.**

## Paths

Scripts resolve the **repository root** via `helpers/_paths.py`:

- `ROOT` — parent of this folder (contains `index.html`, `scientists_card_view_az.html`, `css/`, `js/`, `images/`)
- `HELPERS` — this directory

## Run from repository root

```bash
cd "path/to/DAAB-WAAS web site"
python helpers/_validate_site.py
python helpers/_rebuild_cv_catalog.py
python helpers/_validate_cv_cards.py
```

Some scripts need optional dependencies (e.g. `pypdf` for `helpers/_extract_pdf.py`).

## Scripts

| Script | Purpose |
|--------|---------|
| `_extract_pdf.py` | PDF → `../_pdf_extract.txt` at repo root |
| `_sync_scientists_from_book.py` | Update CV bios from book extract |
| `_rebuild_cv_catalog.py` | Rebuild all 83 CV cards |
| `_build_cv_enrichment.py` | Sync emails/ixtisas from list page DATA |
| `_fix_cv_catalog.py` | Repair broken CV grid HTML |
| `_normalize_cv_cards.py` | Normalize card HTML template |
| `_restructure_cv_cards.py` | Flatten grid, inline meta rows |
| `_format_card_bios.py` | Format bio paragraphs and bullets |
| `_validate_site.py` | Check broken links/paths across all site HTML (run before deploy) |
| `_validate_cv_cards.py` | Validate card HTML structure |
| `_check_name_order.py` | Compare CV vs list name order |
| `_print_norms.py` | Debug name normalization |
| `_recover_cv_from_transcript.py` | Emergency recovery (one-off) |

See `../documents/DAAB-Site-Python-and-JavaScript-Files.md` for full documentation.

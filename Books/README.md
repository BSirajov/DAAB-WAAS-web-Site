# Books (not in Git)

Large PDF/book assets live here for local preview and for upload to the
production web host. They are **not** committed to GitHub.

## Layout

- `DAAB_DK/` — forum book PDF (`forum-book-2026.pdf`, linked from activities pages)
- `Akif_Alaferdov/` — book PDFs, photo PDFs, and cover PNGs (linked from Akif media pages as `001-2_book-az.pdf`, `001-3_photos-az.pdf`, `002-2_book-ru.pdf`, `002-3_photos-ru.pdf`, `003-2_book-ru.pdf`, `003-3_photos-ru.pdf`)

## Deploy

1. Keep this folder on your machine (and a backup). It is not committed to Git.
2. `python helpers/_build_deployment_folder.py` copies `Books/` and `images/`
   into `Deployment/`.
3. Upload the whole `Deployment/` folder after emptying the production folder.

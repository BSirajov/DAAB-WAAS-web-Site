# Books (not in Git)

Large PDF/book assets live here for local preview and for upload to the
production web host. They are **not** committed to GitHub.

## Layout

- `DAAB_DK/` — forum book PDF (linked from activities pages)
- `Akif_Alaferdov/` — book PDFs, photo PDFs, and cover PNGs (linked from Akif media pages)

## Deploy

1. Keep this folder on your machine (and a backup).
2. Upload `Books/` to the website root (same paths the HTML links use).
3. When rebuilding `Deployment/`, existing `Deployment/Books/` is preserved;
   upload it to the host separately if needed, or copy from this folder before FTP.

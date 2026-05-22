# How to use the DAAB bilingual website

The site exists in **two languages**. You choose once; you can switch anytime.

## For visitors

| What you want | Open this |
|---------------|-----------|
| **Azerbaijani (default)** | `http://localhost:8010/az/` or `https://daab-waas.org/az/` |
| **English** | `http://localhost:8010/en/` or `https://daab-waas.org/en/` |
| **Pick language at start** | `http://localhost:8010/` then click AZ or EN |

On every page, the menu shows **AZ | EN**. Click to open the **same page** in the other language.

Old bookmarks like `foundation_az.html` still work; they redirect to `/az/foundation.html`.

## For you (editing the site)

1. **Start the site on your PC:** double-click `START-SITE.bat`.
2. **Edit Azerbaijani pages** in the `az/` folder (or edit the old `*_az.html` files at the root, then run the build script below).
3. **Refresh English** after AZ changes:
   ```bash
   python helpers/_build_bilingual_tree.py
   python helpers/_publish_en_pages.py all
   python helpers/_validate_bilingual.py
   ```

## What is fully translated?

- Navigation, home pages, mission, foundation, membership, executive board  
- Scientists **directory** (search and filters in English)  
- Activities: **titles and timeline** in English; long event texts may still be in Azerbaijani  
- Charter: **summary and article numbers** in English; legal article text in Azerbaijani  
- Profiles: **layout and filters** in English; biography text often still in Azerbaijani  

This is normal for a first bilingual release; you can add full English text over time.

## Put the site online (GitHub)

1. Create a repository on GitHub for this project.
2. In a terminal in this folder:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
   git push -u origin main
   ```
3. On GitHub: **Settings → Pages →** deploy from branch **main**, folder **/ (root)**.
4. After a few minutes, open `https://YOUR_USERNAME.github.io/YOUR_REPO/az/`.

If you use the domain **daab-waas.org**, point DNS to GitHub Pages (see GitHub docs).

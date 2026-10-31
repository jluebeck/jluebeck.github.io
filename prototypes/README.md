# Design prototype

`g-site.html` is the single-file prototype the live site was built from: a landing page with six
tiles, and inner pages with a sidebar. It is kept for trying design changes quickly before
carrying them into `_layouts/` and `assets/css/site.css`. Earlier directions are in the git history.

Edit `src/g-site.html`, then rebuild with `python3 prototypes/src/build.py`. Its data
(`src/publications.js`, `src/aa_usage.json`) is a snapshot; the live site reads `_data/`.

`font-tester/` tries fonts and font sizes on the prototype. Its `site.html` is generated: inline the
images of a built `g-site.html` and save it next to `index.html`.

Nothing in this folder is published.

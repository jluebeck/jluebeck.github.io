# Site redesign prototypes

Three directions for a redesigned jluebeck.github.io, all using the same content (current as of the October 2026 CV).

- `a-monograph.html`: editorial single column with a margin rail and a copy-number plot.
- `b-metaphase.html`: dark-first bands under a simulated metaphase-spread hero, with project cards.
- `c-index.html`: a scannable index with a sticky identity column and filterable publications.

Second round, after feedback that the Index was closest:

- `d-index-2.html`: the Index refined, with a tool-usage chart.
- `e-landing.html`: a minimal landing page with icon tiles that open sub-pages.
- `f-plain.html`: a plain, faculty-style single page.

Shared data lives in `src/`: `publications.js`, `aa_usage.json` (public columns of the AA usage
spreadsheet, made with `extract_usage.py`) and `usage-chart.js`.

Edit the sources in `src/`, then rebuild with `python3 prototypes/src/build.py`.
Nothing here is linked from the live site yet.

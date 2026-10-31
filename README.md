# jluebeck.github.io

Personal site of Jens Luebeck, built by GitHub Pages with Jekyll. No theme: three small layouts and one stylesheet.

## Where things live

| To change | Edit |
| --- | --- |
| Publications | `_data/publications.yml` (counts on every page update automatically) |
| Software table | `_data/tools.yml` |
| Tool usage chart and studies table | `_data/usage.json` (see below) |
| Recent talks, awards | `_data/talks.yml`, `_data/awards.yml` |
| Project cards | `_data/projects.yml` |
| Pages in the sidebar and landing tiles | `_data/nav.yml` |
| Landing blurb | `index.html` |
| Page text (research overview, bio, …) | `_pages/*.html` |
| Name, role, links, CV link, email | `_config.yml` → `author` |
| Look | `assets/css/site.css` |
| Layouts | `_layouts/` (`default` → `home` for the landing page, `page` for everything with the sidebar, `post` for blog posts) |

Each `<section id="…" data-title="…">` on a page gets a link in the sidebar automatically.

## Updating tool usage

`scripts/extract_usage.py` reads the AA usage spreadsheet and writes only its public columns to `_data/usage.json`. It drops notes, AmpliconRepository status and any study dated in the future.

```bash
python3 -I scripts/extract_usage.py path/to/AA_usage.xlsx
```

A weekly scheduled Claude task looks for new studies. `scripts/find_citing.py` lists papers on Europe PMC,
first published since the date in `scripts/usage_reviewed.json`, that cite the AmpliconArchitect or
AmpliconSuite papers or mention the tools in their full text. The task reads each paper's methods, adds
studies that ran the tools themselves (not reused results, e.g. from AmpliconRepository) on 50 or more samples to `_data/usage.json`, records every paper it checked in
`scripts/usage_reviewed.json`, and opens a pull request for review.

```bash
python3 -I scripts/find_citing.py                  # new candidates, as JSON
python3 -I scripts/find_citing.py snippets PMC123  # passages in a paper that mention the tools
```

## Adding a project

Put a self-contained page or app in `lab/<name>/` (served at `/lab/<name>/`), or keep it in its own repository with GitHub Pages turned on (served at `jluebeck.github.io/<repo>/`). Then add a card to `_data/projects.yml`.

## Preview locally

```bash
bundle install
bundle exec jekyll serve
```

`prototypes/` holds the design prototypes and is not published.

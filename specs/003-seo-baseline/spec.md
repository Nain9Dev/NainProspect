# SEO and AI-engine discoverability baseline

Status: Implemented

## Objective

`prospect.naindev.com` is a single-page app served by GitHub Pages. Its static `index.html` carried no description, canonical URL, social metadata or structured data, so search and answer engines had nothing to read before running the script. Add the shared NainDev discoverability baseline without touching the visual design.

## Functional requirements (EARS)

- **SEO-001 Canonical**: The static `index.html` shall declare exactly one canonical link equal to `https://prospect.naindev.com/`.
- **SEO-002 Description**: The static `index.html` shall carry exactly one meta description of 70 to 160 characters, in the page language (Spanish), without invented claims.
- **SEO-003 Social cards**: The static `index.html` shall carry Open Graph tags (`og:url` equal to the canonical, absolute `og:image` of 1200x630) and a `summary_large_image` Twitter card.
- **SEO-004 Structured data**: The static `index.html` shall carry one `SoftwareApplication` JSON-LD block whose author is the Person `https://www.naindev.com/#person`, with `<` escaped.
- **SEO-005 Crawl files**: The site root shall serve `robots.txt` (allow all, advertise the sitemap), `sitemap.xml` (the root URL) and `llms.txt` (Markdown, H1 first).
- **SEO-006 Author link**: The static `index.html` shall link `rel="author"` to `https://www.naindev.com/`.

## Edge cases

- The static HTML has no `<h1>`: the heading is rendered by `HeaderNav.vue` after the script runs. Not changed here (out of scope: no restructuring of the app).
- The social image is the shared NainDev cover because the repository ships no raster image of 1200x630 (`docs/assets/social-preview.svg` is not served and SVG is not accepted by social crawlers).
- Cloudflare in front of GitHub Pages may add its own managed block to `robots.txt`; the file in the repository stays the source.

## Out of scope

- Any change to the app, the backend or the visible UI.

## Acceptance criteria

- `tests/test_seo_baseline.py` passes (written before the files, seen failing).

## Session state

- Last updated: 2026-11-09. Implemented on `feat/seo-baseline`; waiting for owner merge.

# Implementation plan: Installable site (Android and iOS)

## Modules

- **Manifest**: `ProspectAI.Client/public/manifest.webmanifest`, a static file. Vite copies `public/` to the root of `dist/`, which the deploy publishes. Covers PWA-002.
- **Icons**: `ProspectAI.Client/public/icons/` holds `icon-192.png`, `icon-512.png`, `icon-maskable-512.png` and `apple-touch-icon.png`, rendered from `public/favicon.svg` on the page background `#070a12`. Covers PWA-003.
- **Head tags**: `ProspectAI.Client/index.html`, the only HTML document of the site. Covers PWA-001, PWA-004.
- **Guard**: `tests/test_pwa_install.py`, in the pytest suite that `ci.yml` runs (`pytest tests/ -v`). It reads the client files from the repository tree. Covers PWA-001 to PWA-005.

## Data model changes

None.

## Key decisions

- **Decision**: the guard lives in the Python suite.
  - **Rationale**: CI runs only pytest; the client's `npm test` is not in `ci.yml`.
- **Decision**: the test checks names, declared sizes (PNG header) and tags only.
  - **Rationale**: icon opacity and the safe zone need pixel data; the icon tooling verifies them and the repository adds no image dependency.
- **Decision**: status bar style `black`, theme and background `#070a12`.
  - **Rationale**: the page paints `--bg-space` (`#070a12`) first and is dark.
- **Decision**: no service worker (owner decision of 2026-11-13).

## Regenerating the icons

The icon tool is a local script of the maintainer's workstation. The exact command used:

```
node make-install-icons.mjs --source ProspectAI.Client/public/favicon.svg --out ProspectAI.Client/public/icons --bg "#070a12" --apple-scale 0.8
```

The maskable icon uses the tool's default scale (0.56).

## Test strategy

- `pytest tests/ -v` (manifest members, icon sizes, head tags, no service worker).
- Manual: Chrome `Page.getInstallabilityErrors` on the built `dist/` and the icon/safe-zone verification script; after the deploy, install on Android and iOS.

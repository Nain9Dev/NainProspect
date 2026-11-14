# Installable site (Android and iOS)

Status: Implemented on `feat/pwa-install-prospect`, waiting for owner merge

## Objective

A visitor on a phone can install `prospect.naindev.com` from the browser and open it like an app: its own icon and name on the home screen and a window with no browser bar. Android Chrome and iOS Safari are the targets.

The shared contract (install criteria, names, icon rules) is defined by the portfolio spec, `specs/next-pwa-install/spec.md` in `Nain9Dev/nain9dev.github.io`. This spec applies it to this site and does not restate it.

## Functional requirements (EARS)

- **PWA-001 Head links**: The static `index.html` shall link `/manifest.webmanifest` with `rel="manifest"` and `/icons/apple-touch-icon.png` with `rel="apple-touch-icon"`.
- **PWA-002 Manifest**: The site shall publish `/manifest.webmanifest` declaring `id`, `start_url` and `scope` as `/`, `display` as `standalone`, `name` and `short_name` as `NainProspect`, `lang` as `es`, `dir` as `ltr`, the page meta description verbatim as `description`, and `theme_color` and `background_color` as `#070a12` (the `--bg-space` colour the page paints first). It shall not declare `prefer_related_applications`.
- **PWA-003 Icons**: The manifest shall declare three PNG icons that exist at their declared size: 192 px and 512 px with purpose `any`, and 512 px with purpose `maskable`. A 180 px opaque `apple-touch-icon.png` shall sit next to them in `/icons/`. All four derive from `public/favicon.svg`.
- **PWA-004 iOS and theme tags**: The static `index.html` shall carry `mobile-web-app-capable` and `apple-mobile-web-app-capable` set to `yes`, `apple-mobile-web-app-title` equal to the manifest `short_name`, `apple-mobile-web-app-status-bar-style` set to `black` (dark page) and a `theme-color` equal to the manifest value.
- **PWA-005 Installable only**: The client shall not register a service worker.

## Edge cases and error handling

- `ProspectAI.Client/public/` is copied unchanged to the root of `dist/`, which `deploy.yml` publishes through the shared Pages workflow (`dist-path: "dist"`). The workflow lists no files one by one and has no SPA fallback or Content-Security-Policy that would hide the manifest.
- Opacity of the icons and the maskable safe zone (mark inside a centred circle of radius 40% of the width) are checked by the generator tooling, not by the repository test (see `plan.md`).
- Without a service worker, an installed window with no network shows the browser's own offline screen.

## Out of scope

- A service worker, offline page, cache or install button (owner decision of 2026-11-13).
- Any change to the app, the backend or the visible UI.

## Acceptance criteria

- `tests/test_pwa_install.py` passes (written before the files, seen failing).
- Chrome reports no installability error for the built `dist/` (`Page.getInstallabilityErrors`).
- After the deploy, the live manifest answers 200 and the owner installs the site on Android and iOS: icon uncropped, label `NainProspect`, window without browser bar.

## Session state

- Last updated: 2026-11-14. Implemented; `pytest tests/`, `npm run build` and `npm test` pass; Chrome reports no installability error on the local build.
- Next: owner merge, then live check and install on both phones.
- Blocked: nothing. The phone check needs the owner.

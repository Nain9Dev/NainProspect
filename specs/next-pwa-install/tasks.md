# Tasks: Installable site (Android and iOS)

One task at a time, test first.

- [x] **T01** `[A]` Write `tests/test_pwa_install.py`.
  - **Covers**: PWA-001 to PWA-005
  - **Done when**: the test fails on the tree without the manifest, icons and tags.
  - **Result**: 1 failed and 3 errors (`FileNotFoundError` for the manifest) before the change; the no-service-worker test already held.
- [x] **T02** `[A]` Render the icons from `public/favicon.svg` (command in `plan.md`) and look at them.
  - **Covers**: PWA-003
  - **Done when**: the four PNG files exist at their sizes and the mark is centred and uncropped.
- [x] **T03** `[A]` Add `public/manifest.webmanifest` and the head tags in `index.html`.
  - **Covers**: PWA-001, PWA-002, PWA-004
  - **Done when**: `pytest tests/ -v` passes (30 tests) and `npm run build` publishes the manifest and icons in `dist/`.
- [x] **T04** `[A]` Ask Chrome for installability errors on the built `dist/`.
  - **Covers**: acceptance criteria
  - **Done when**: `Page.getInstallabilityErrors` returns an empty list for `/`.
  - **Result**: empty list, manifest parsed without errors.
- [ ] **T05** `[M]` Verify the live site after the deploy.
  - **Covers**: acceptance criteria
  - **Done when**: the live manifest answers 200 and the owner has installed the site on Android and iOS.
  - **Needs from owner**: merge the pull request, then install from Chrome on Android and Safari on iPhone and confirm icon, label and window.

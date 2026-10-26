# Showcase header and guided scenario

Status: In progress

## Objective

Owner request of 2026-10-26: `prospect.naindev.com` opens straight on a form and a dense table, so a client cannot tell what problem it solves. Add a short header that says what it does and a button that runs the whole pipeline on synthetic data, step by step, so the product is understood without reading. Owner choices: header plus guided scenario, Spanish with an English version through the existing language switch.

## Functional requirements (EARS)

- **SH-001 Header**: When the client opens, it shall show above the workbench an eyebrow, one headline, one supporting line and two actions: "Ver el escenario guiado" and "Probar mi búsqueda".
- **SH-002 Honest framing**: The header shall state that the data is synthetic and that real sending is blocked by the legal gate, so the demo cannot be mistaken for a live outreach tool.
- **SH-003 Guided scenario**: When the visitor starts the scenario, the client shall run the pipeline with the first preset query in simulation mode and walk four stages in order: capture, classification, compliance and outreach. Each stage shall show a figure computed from the leads the run returned, never a fixed number.
- **SH-004 Outreach stage**: When the scenario ends, the client shall offer to open the generated email for the best qualified lead: highest priority, with a role mailbox, preferring the target size band.
- **SH-005 Own search**: When the visitor chooses "Probar mi búsqueda", the client shall move focus to the search field of the launcher.
- **SH-006 Language**: Every new text shall exist in Spanish and in English and follow the existing language switch.
- **SH-007 Reduced motion**: When the visitor prefers reduced motion, the scenario shall show every stage completed at once, without timers or animation.
- **SH-008 Accessibility**: The stages shall be an ordered list, the current one marked `aria-current="step"`, and the progress announced through a polite live region.
- **SH-009 Responsive**: The header shall remain usable at 375 px without horizontal scroll.

## Edge cases

- A run that returns no leads: the stages show zero figures and the outreach stage offers no email.
- The backend is online: the scenario uses the same `runPipeline` call as the launcher, so it works with the API or with the standalone engine.
- Starting the scenario while a run is in progress is ignored.

## Out of scope

- Changes to the backend, the contracts or the compliance rules.
- Real data, real sending or a different classification.

## Acceptance criteria

- `npm test` (Node test runner, no new dependency) covers the scenario logic.
- `npm run build` passes.
- The header and the scenario are checked in a real browser at 1440 and 390 px in both languages.

## Session state

- Last updated: 2026-10-26, session prospect-visual (worktree `D:/wt/ProspectAI-feat-showcase-header`, branch `feat/showcase-header`)
- Done: spec, tests first (`tests/scenario.test.ts`, 9), `services/scenario.ts`, `ShowcaseHero.vue`, Spanish and English texts, wiring, header and grid fixes for phones.
- Verified: `npm test` and `npm run build` pass; browser at 1280, 390 and 375 px in both languages (no horizontal overflow), scenario run to the end, generated email opens. Not run: axe and Lighthouse (not installed for this project), a live API (the demo uses the standalone engine).
- Next: owner review and merge; deploy to prospect.naindev.com.
- Blocked: —

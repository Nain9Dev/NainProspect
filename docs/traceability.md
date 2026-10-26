# Traceability Matrix — NainProspect

| Requirement ID | Description | Source / Gate | Implementation Component | Test Verification |
| -------------- | ----------- | ------------- | ------------------------ | ----------------- |
| REQ-01 | Role-based email filtering | BR-01, GDPR 6.1.f | `engine/compliance.py` | `test_compliance.py::test_role_based_filtering` |
| REQ-02 | Deterministic legal footer | BR-03, LSSI-CE 21 | `engine/templates.py` | `test_templates.py::test_legal_footer_generation` |
| REQ-03 | Hard-locked email send gate | BR-02 | `engine/compliance.py` | `test_compliance.py::test_outbound_send_hard_lock` |
| REQ-04 | AI enrichment & priority scoring | BR-04, BR-05 | `engine/classifier.py` | `test_classifier.py::test_lead_scoring` |
| REQ-05 | REST API endpoints & schemas | ADR-002 | `api/routes.py`, `src/nainprospect/` | `test_api.py::test_pipeline_run_and_leads` |
| REQ-06 | Reactive UI & Template viewer | ADR-002 | `ProspectAI.Client/` | Vite build & vue-tsc validation |
| SH-001, SH-002, SH-005, SH-006 | Showcase header, honest framing, own search, Spanish and English | specs/002-showcase-header | `ShowcaseHero.vue`, `locales/i18n.ts` | Browser pass at 1280, 390 and 375 px in both languages |
| SH-003, SH-004 | Scenario figures from the run; best lead for the email | specs/002-showcase-header | `services/scenario.ts` | `tests/scenario.test.ts` (9 tests) |
| SH-007, SH-008, SH-009 | Reduced motion, ordered stages with a live region, no horizontal scroll | specs/002-showcase-header | `ShowcaseHero.vue`, `HeaderNav.vue`, `style.css` | `scenarioDelays(true)` test; overflow measured under phone emulation (0 px over) |

# Traceability Matrix — NainProspect

| Requirement ID | Description | Source / Gate | Implementation Component | Test Verification |
| -------------- | ----------- | ------------- | ------------------------ | ----------------- |
| REQ-01 | Role-based email filtering | BR-01, GDPR 6.1.f | `engine/compliance.py` | `test_compliance.py::test_role_based_filtering` |
| REQ-02 | Deterministic legal footer | BR-03, LSSI-CE 21 | `engine/templates.py` | `test_templates.py::test_legal_footer_generation` |
| REQ-03 | Hard-locked email send gate | BR-02 | `engine/compliance.py` | `test_compliance.py::test_outbound_send_hard_lock` |
| REQ-04 | AI enrichment & priority scoring | BR-04, BR-05 | `engine/classifier.py` | `test_classifier.py::test_lead_scoring` |
| REQ-05 | REST API endpoints & schemas | ADR-002 | `api/routes.py`, `src/nainprospect/` | `test_api.py::test_pipeline_run_and_leads` |
| REQ-06 | Reactive UI & Template viewer | ADR-002 | `ProspectAI.Client/` | Vite build & vue-tsc validation |

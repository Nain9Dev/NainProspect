# Feature Specification: NainProspect Decoupled Modernization

## 1. Context and Problem Statement
ProspectAI was structured as an isolated Python script pipeline targeting scheduled execution in GitHub Actions. While effective for automated background prospecting, it lacked real-time visibility, interactive querying, RESTful integration points for `naindev.com`, and strongly typed data contracts.

## 2. Goals
- Deliver an enterprise-grade, asynchronous FastAPI backend exposing structured REST endpoints for prospecting pipeline runs, lead filtering, template rendering, and cost audits.
- Provide a responsive Vue 3 + TypeScript SPA frontend (`ProspectAI.Client`) running on pinned port `5377`.
- Enforce strict privacy and legal compliance gates (GDPR Article 6.1.f and Spanish LSSI-CE Article 21).
- Maintain backward compatibility with the existing CLI `pipeline.py` script and GitHub Actions cron schedule.

## 3. Non-Goals
- Transmitting live cold emails over SMTP or external sending providers.
- Scraping restricted personal data from LinkedIn or password-protected directories.

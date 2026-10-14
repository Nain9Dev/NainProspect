# Project Charter — NainProspect (ProspectAI)

## 1. Executive Summary
NainProspect is an autonomous B2B prospecting, data enrichment, and compliance verification engine within the NainDev ecosystem. It discovers corporate prospects from public registries and company websites, enriches and prioritizes them using AI classification, generates legally compliant cold-outreach email templates, and enforces strict European GDPR and Spanish LSSI-CE compliance gates.

## 2. Business Objectives
- Provide a low-cost, automated B2B prospecting pipeline capable of running on scheduled triggers (GitHub Actions) or on-demand via an interactive web interface.
- Classify company industry, workforce size band (target: 50-500 employees), and outreach priority (1-5) using Claude Haiku 4.5 with deterministic fallback.
- Enforce GDPR 6.1.f and LSSI-CE Article 21 compliance by discarding personal named email addresses, generating deterministic legal footers, and hard-locking email dispatch in simulation mode until legal prerequisites are verified.
- Serve as a production-grade portfolio showcase and service within `naindev.com`.

## 3. Scope
- In Scope:
  - Scraper integration with Apify Google Places crawler and company website crawler.
  - Role-based email verification (`info@`, `contacto@`, `ventas@`, etc.).
  - AI classification with token usage and cost accounting.
  - FastAPI modular backend with Pydantic v2 schemas and REST endpoints.
  - Vue 3 + TypeScript reactive client (`ProspectAI.Client`) on port 5377 with lead filtering, template preview, and cost breakdown.
  - Dual storage: in-memory / SQLite pipeline store with synthetic dataset generation for demo and testing.
  - Telegram alert integration for priority >= 4 leads.
  - Google Drive archiving via OAuth 2.0 user credentials.
- Out of Scope:
  - Automatic sending of cold emails to real leads.
  - Scraping personal profiles from LinkedIn or private networks.
  - Storing real contact databases in git version control.

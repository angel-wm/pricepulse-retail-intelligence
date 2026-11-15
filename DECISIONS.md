# Decisions

This is the project's initial decision record. A documented decision selects a direction; it does **not** assert that the corresponding capability has been implemented.

## Decision log

### D-001 — Scrapy as the initial extraction framework

- **Status:** accepted direction; not implemented.
- **Rationale:** Python-centric, established crawling framework with structured request handling and extraction pipelines.
- **Tradeoff:** some retailers may not provide useful static responses; source feasibility must be established before committing to a target.
- **Revisit when:** evidence from an approved source justifies another tool and the user explicitly approves it.

### D-002 — PostgreSQL for historical storage

- **Status:** accepted direction; not implemented.
- **Rationale:** relational constraints, SQL transformations, and historical observation modeling support the Data Engineering learning goals.
- **Tradeoff:** requires local database setup and ingestion design.

### D-003 — Tableau as the primary BI platform

- **Status:** accepted direction; not implemented.
- **Rationale:** expand portfolio experience beyond Power BI.
- **Tradeoff:** Tableau Public is for public/shareable datasets; publication and refresh options must be verified for the chosen data.
- **Revisit when:** a separate, meaningful Power BI objective is identified.

### D-004 — Crawlee belongs to a separate future project

- **Status:** accepted scope boundary.
- **Rationale:** avoid duplicate portfolio projects solving the same problem.
- **Tradeoff:** no side-by-side framework feature parity within PricePulse.

### D-005 — Documentation conventions

- **Status:** accepted for documentation.
- **Rationale:** adopt [Repository Documentation Readability](https://github.com/angel-wm/repository-documentation-readability) for presentation and [AI Repository Context](https://github.com/angel-wm/ai-repository-context) for source routing.
- **Boundary:** neither convention replaces the project's decisions, state, evidence, or phase approval model.

## Future changes

Append a dated or identified decision with rationale, tradeoff, and any superseded decision. Do not silently overwrite the historical reason for an earlier choice.

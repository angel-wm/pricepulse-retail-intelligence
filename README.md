# PricePulse — Grocery Price Intelligence

PricePulse is a **planned, documentation-first Data Engineering portfolio project** for collecting published grocery price lists, validating product identities, preserving historical retail prices, and analyzing comparable offers in PostgreSQL and Tableau.

**Current status:** **Phase 0 technical feasibility evidenced; formal closeout review ready.** Bounded Scrapy tests downloaded genuine Kaufland and SPAR Croatia price lists for two days. A private 160-pair review found **102 consistent product descriptions** and 58 unresolved. Lidl is excluded from v1. No production spider, database, automation or Tableau dashboard is implemented; Phase 1 requires explicit approval.

## What PricePulse aims to answer

- How do published prices for the same grocery product change over time?
- What is the price difference for the same verified GTIN/EAN between Kaufland and SPAR at comparable stores and dates?
- Which product categories show the largest price changes or cross-retailer spreads?
- How complete and reliable are daily retailer price-list publications?

**Availability/stock tracking is not an initial KPI:** the governing regulation does not require an explicit stock field. A product missing from a list must not be described as out of stock.

## Why this data source?

Croatian retailers publish official machine-readable price lists. The regulation effective **17 November 2026** expressly provides for automated collection and CSV/XML price lists. This is stronger evidence for the acquisition use case than attempting to crawl individual product pages protected by anti-bot systems.

Actual local source-access, two-date history, and price/identity evidence is in [Validation](VALIDATION.md) and [Source feasibility](SOURCE_FEASIBILITY.md). Initial same-date codes with price totaled 8,869 after promotional-price handling, but these are **not all verified product matches**. Previous music-retailer candidates were dropped after access blocks or restrictions. Public real-data redistribution remains on hold; a synthetic Tableau Public demo is the default.

## Planned workflow

1. **Phase 0 — Feasibility:** test direct access to both official sources with Scrapy, validate current file schemas, and measure **at least 100 exact, reviewable common GTIN/EAN products** for equivalent store/date/product contexts.
2. **Phase 1 — Scrapy:** discover official price-list indexes and download a bounded number of permitted CSV/XML files using source-specific spiders.
3. **Phase 2 — Data engineering:** parse locale-specific values, validate identifiers and units, preserve raw-file provenance, and ingest immutable, deduplicated observations into PostgreSQL.
4. **Phase 3 — Reliability:** add pytest checks, structured logs, bounded retries, scheduled runs, and quality monitoring.
5. **Phase 4 — Tableau:** analyze prices and longitudinal trends; publish only data and visualizations with established sharing rights.
6. **Phase 5 — Release:** provide tested reproduction steps, measured results, documentation, and a portfolio-ready repository.

These are intended deliverables, **not claims of implementation**.

## Technology

| Responsibility | Planned choice |
| --- | --- |
| Acquisition | Python 3.12+, Scrapy |
| File parsing and validation | Python standard library initially; explicit data contracts |
| Database and transformations | PostgreSQL, SQL, Python |
| Testing and automation | pytest; GitHub Actions where feasible |
| BI | Tableau Desktop Free Edition; Tableau Public only for appropriately shareable outputs |
| Version control | Git and GitHub |

Scrapy remains the primary acquisition framework. No additional scraping framework, paid service, or infrastructure is planned.

## Project references

- [Current state](CURRENT_STATE.md) — implemented versus pending work
- [Source feasibility](SOURCE_FEASIBILITY.md) — sources, evidence, tests, risks, and acceptance gates
- [Project specification](PROJECT_SPEC.md) — analytical scope and data contract
- [Roadmap](ROADMAP.md) — phase gates
- [Architecture](ARCHITECTURE.md) — proposed design
- [Decisions](DECISIONS.md) — recorded decisions
- [Validation](VALIDATION.md) — actual evidence and outstanding tests
- [Repository context](REPO_CONTEXT.md) and [agent instructions](AGENTS.md) — navigation and working conventions

Repository documentation follows [Repository Documentation Readability](https://github.com/angel-wm/repository-documentation-readability). Source feasibility evidence now exists, but **Phase 1 implementation and any publication of genuine retailer data remain separate approval gates.**

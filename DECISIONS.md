# Decisions

A decision records approved direction and trade-offs; it does **not** imply implementation, measured feasibility or release.

## Decision log

### D-001 — Scrapy as the initial acquisition framework

- **Status:** accepted direction; no crawler implemented.
- **Rationale:** Python-native, deterministic request management and structured downloading suit public CSV/XML price lists.
- **Tradeoff:** site-specific discovery and parsing still need tests; no browser or bot-defense bypass is planned.

### D-002 — PostgreSQL for historical storage

- **Status:** accepted direction; not implemented.
- **Rationale:** relational product/store identity, idempotent ingestion, file provenance and dated price observations.

### D-003 — Tableau as primary BI

- **Status:** accepted direction; not implemented.
- **Rationale:** create business-facing price comparison and trend dashboards. Tableau Public is conditional on sharing rights.

### D-004 — Crawlee belongs to a distinct future project

- **Status:** accepted scope boundary.
- **Rationale:** avoid a duplicate scraping-framework demonstration.

### D-005 — Documentation conventions

- **Status:** accepted for documentation.
- **Rationale:** apply [Repository Documentation Readability](https://github.com/angel-wm/repository-documentation-readability) and [AI Repository Context](https://github.com/angel-wm/ai-repository-context), retaining native project source files as authorities.

### D-006 — Pivot to Croatian grocery price-list intelligence (2026-11-18)

- **Status:** **accepted scope direction, sources under feasibility review**; no Phase 1 authorization.
- **Decision:** retain project name **PricePulse**; replace the initially explored musical-instruments category with Croatian grocery and household price intelligence. Prioritize **Kaufland Croatia and SPAR Croatia** as a candidate source pair; exclude **Lidl** from the first release.
- **Rationale:** official machine-readable publications and a regulatory framework explicitly allowing automated collection are more promising than scraping product pages. A May 2025 third-party study found >=4,126 barcode matches across six chains excluding Lidl, which establishes historical potential but **does not** establish today's Kaufland–SPAR overlap.
- **Tradeoff:** per-store file processing and data-quality issues replace product-page parsing; GTIN validity, store comparability and retention require explicit modeling.
- **Approval gate:** recent source-file access and >=100 validated same-date shared GTINs, plus rights and historical-feasibility checks.
- **Revisit when:** the two sources fail Phase 0 acceptance or a better documented public source becomes available.

### D-007 — Prefer published store-level prices; defer stock KPI (2026-11-18)

- **Status:** accepted Phase 0 analytical direction; not implemented.
- **Decision:** model price-list observations by retailer, store, product and date; do not advertise availability/stock tracking until a field with that meaning is verified.
- **Rationale:** NN 132/2026 specifies prices, product identifiers and baseline price but does not guarantee a stock indicator. Absence from a price list is not evidence of being out of stock.
- **Tradeoff:** narrower first dashboard, but fewer false claims and a more defensible data model.

## Future changes

Add dated decisions with rationale, trade-offs and any superseded choice. Update [Current state](CURRENT_STATE.md) and [Validation](VALIDATION.md) from evidence rather than overwriting older history.

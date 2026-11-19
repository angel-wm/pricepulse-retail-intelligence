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

- **Status:** **accepted scope direction; two sources qualified in bounded technical feasibility tests**; no Phase 1 authorization.
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

### D-008 — Adopt official CSV acquisition and source-specific promotion parsing (2026-11-18)

- **Status:** accepted preliminary price-field contract direction from four files; not implemented in production.
- **Evidence:** bounded live-download tests succeeded on both Kaufland and SPAR, with 8,263 checksum-valid code overlap candidates at comparable store/date grain and two-day same-store histories. SPAR primary price is blank on 3,103 of 32,347 rows on 2026-11-17, but those rows have valid special prices. The current parser omits them from first-pass usable products.
- **Decision direction:** distinguish regular price, special/promotion price, and effective advertised price with explicit source lineage. Never infer missing-price or out-of-stock from a blank normal-price field alone.
- **Tradeoff:** more sophisticated field precedence/validation and coverage accounting; no need for a new scraping framework.
- **QA gate:** confirm effective-price precedence when both fields are populated, and verify exact package/brand equivalence in >=100 selected cross-retailer matches before Phase 0 closeout. Treat the 8,263 overlap as candidates, not fully verified products.

### D-009 — Qualify Kaufland + SPAR Croatia as initial source pair (2026-11-18)

- **Status:** bounded Phase 0 **technical feasibility passed**; formal closeout awaiting user approval. No Phase 1 implementation is authorized.
- **Decision:** retain **PricePulse**, qualify SPAR Zagreb Jankomir (store 8702) and Kaufland Zagreb Antuna Šoljana (store 5630) for initial local-source engineering, and keep Lidl out of the first release.
- **Evidence:** Scrapy downloaded price-list CSVs from both stores for 2026-11-16/17. Promotion-aware parsing yielded 8,869 same-date priced code matches, 7,772 four-file-stable codes and 4,155 strict automatic candidates. A private manual review of 160 selected descriptions classified **102 consistent** and **58 unresolved**; this is not independent physical-manufacturer verification. See [Validation](VALIDATION.md).
- **Contract:** preserve regular and special price columns, origin and source store/date. Unknown conflicting dual-populated prices must fail closed until their semantics are confirmed. Monitor source-specific encoding/delimiters and store-level row-count changes.
- **Public use:** genuine SPAR-source lists or real-data extracts are not approved for publication under currently reviewed terms. A clearly synthetic Tableau Public portfolio demo is the default unless sharing rights are verified.
- **Tradeoff:** source-specific ingestion and match exceptions require quality monitoring but no additional scraping framework.

## Future changes

Add dated decisions with rationale, trade-offs and any superseded choice. Update [Current state](CURRENT_STATE.md) and [Validation](VALIDATION.md) from evidence rather than overwriting older history.

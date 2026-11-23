# Decisions

A decision records approved direction and trade-offs; it does **not** imply implementation, measured feasibility or release.

## Decision log

### D-001 — Scrapy as the initial acquisition framework

- **Status:** accepted direction; bounded source adapters were subsequently implemented in Phase 1.
- **Rationale:** Python-native, deterministic request management and structured downloading suit public CSV/XML price lists.
- **Tradeoff:** site-specific discovery and parsing still need tests; no browser or bot-defense bypass is planned.

### D-002 — PostgreSQL for historical storage

- **Status:** accepted direction; Phase 2 formally closed on 2026-11-23 following synthetic integration checks and a bounded private real-file review.
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

- **Status:** **accepted scope direction; two sources qualified in bounded technical feasibility tests**; Phase 1 was subsequently authorized (D-011).
- **Decision:** retain project name **PricePulse**; replace the initially explored musical-instruments category with Croatian grocery and household price intelligence. Prioritize **Kaufland Croatia and SPAR Croatia** as a candidate source pair; exclude **Lidl** from the first release.
- **Rationale:** official machine-readable publications and a regulatory framework explicitly allowing automated collection are more promising than scraping product pages. A May 2025 third-party study found >=4,126 barcode matches across six chains excluding Lidl, which establishes historical potential but **does not** establish today's Kaufland–SPAR overlap.
- **Tradeoff:** per-store file processing and data-quality issues replace product-page parsing; GTIN validity, store comparability and retention require explicit modeling.
- **Approval gate:** recent source-file access and >=100 validated same-date shared GTINs, plus rights and historical-feasibility checks.
- **Revisit when:** either source later fails monitored technical access, quality gates, or source-use constraints.

### D-007 — Prefer published store-level prices; defer stock KPI (2026-11-18)

- **Status:** accepted Phase 0 analytical direction; not implemented.
- **Decision:** model price-list observations by retailer, store, product and date; do not advertise availability/stock tracking until a field with that meaning is verified.
- **Rationale:** NN 132/2026 specifies prices, product identifiers and baseline price but does not guarantee a stock indicator. Absence from a price list is not evidence of being out of stock.
- **Tradeoff:** narrower first dashboard, but fewer false claims and a more defensible data model.

### D-008 — Adopt official CSV acquisition and source-specific promotion parsing (2026-11-18)

- **Status:** accepted preliminary price-field contract direction from four files; not implemented in production.
- **Evidence:** initial base-price-only parse found 8,263 code matches and overlooked 3,103 SPAR special-only prices. The final four-file audit recovered those prices, yielding **8,869** shared priced codes. No differing simultaneously populated regular/special prices were observed in the sampled files.
- **Decision direction:** distinguish regular price, special/promotion price, and effective advertised price with explicit source lineage. Never infer missing-price or out-of-stock from a blank normal-price field alone.
- **Tradeoff:** more sophisticated field precedence/validation and coverage accounting; no need for a new scraping framework.
- **QA rule:** regular-only → regular; special-only → special; both equal → preserve both fields, same amount; both present/different → flag as ambiguous. The 160-pair descriptor review supports **102 consistent pairs**, not manufacturer-certified products. Preserve unresolved cases for downstream testing.

### D-009 — Qualify Kaufland + SPAR Croatia as initial source pair (2026-11-18)

- **Status:** bounded technical feasibility passed; **Phase 0 formally closed by owner approval on 2026-11-19**. Phase 1 was subsequently authorized (D-011).
- **Decision:** retain **PricePulse**, qualify SPAR Zagreb Jankomir (store 8702) and Kaufland Zagreb Antuna Šoljana (store 5630) for initial local-source engineering, and keep Lidl out of the first release.
- **Evidence:** Scrapy downloaded price-list CSVs from both stores for 2026-11-16/17. Promotion-aware parsing yielded 8,869 same-date priced code matches, 7,772 four-file-stable codes and 4,155 strict automatic candidates. A private manual review of 160 selected descriptions classified **102 consistent** and **58 unresolved**; this is not independent physical-manufacturer verification. See [Validation](VALIDATION.md).
- **Contract:** preserve regular and special price columns, origin and source store/date. Unknown conflicting dual-populated prices must fail closed until their semantics are confirmed. Monitor source-specific encoding/delimiters and store-level row-count changes.
- **Public use:** genuine SPAR-source lists or real-data extracts are not approved for publication under currently reviewed terms. The owner has not decided the public portfolio data approach; a clearly synthetic demonstration remains an option.
- **Tradeoff:** source-specific ingestion and match exceptions require quality monitoring but no additional scraping framework.

### D-010 — Formally close Phase 0; retain the Phase 1 authorization gate (2026-11-19)

- **Status:** approved by explicit project-owner decision.
- **Decision:** formally close **Phase 0 — Project Definition and Source Feasibility** based on bounded Scrapy source access, same-store two-date history, observed price-field behavior, and a conservative 102/160 descriptor-consistency audit.
- **Authorized action:** synchronize GitHub documentation and Jira status with this closure.
- **At closeout, not authorized:** Phase 1 implementation, scheduled production scraping, PostgreSQL provisioning, or public redistribution of real retail-source observations. Phase 1 implementation was subsequently authorized (D-011). The 58 unresolved pairs remain exceptions, not blockers to bounded feasibility closure.
- **Next gate at closeout:** separate explicit owner authorization for Phase 1; subsequently granted (D-011).
- **Evidence:** [Validation](VALIDATION.md) and [Source feasibility](SOURCE_FEASIBILITY.md).

## Future changes

Add dated decisions with rationale, trade-offs and any superseded choice. Update [Current state](CURRENT_STATE.md) and [Validation](VALIDATION.md) from evidence rather than overwriting older history.

### D-011 — Authorize Phase 1 acquisition (2026-11-19)

The owner explicitly authorized Phase 1 and requested PULSE-12 and its subtasks. This supersedes D-010 only for Phase 1 implementation. Production scheduling, database provisioning and redistribution of genuine source data remain outside this authorization.

### D-012 — Close Phase 1 and authorize Phase 2 (2026-11-22)

The owner explicitly approved Phase 1 closeout and authorized Phase 2 implementation. Phase 2 covers PostgreSQL historical engineering and its validation, including a local test database if needed. Production scheduling and publication of genuine retailer data remained outside that authorization; Phase 3 was subsequently authorized in D-013.

### D-013 — Start Phase 3 before Phase 2 closeout (2026-11-22)

The owner authorized continuing with Phase 3 and reviewing Phases 2 and 3 later. This explicitly permits parallel work before Phase 2 closeout; it does not constitute approval to close either phase or permission to publish genuine retailer data. A configured recurring job and production reliability require their own actual evidence; do not represent an unconfigured schedule as running.

### D-014 — Use local collection-only scheduling for now (2026-11-23)

The owner selected local collection only for the daily task. The installed task does not automatically ingest into PostgreSQL or publish source files. A real recurring capture and operational reliability remain to be observed; the owner will review Phases 2 and 3 later.

### D-015 — Close Phase 2 with bounded validation (2026-11-23)

The owner formally closed Phase 2 after reviewing the private PostgreSQL validation in [Validation](VALIDATION.md). The accepted scope covers one historical file per retailer, idempotent replay and four owner-approved comparisons with prices reconciled against the source files. Additional candidate pairs can be reviewed later in private batches. Phase 3 still awaits owner review.

### D-016 — Close Phase 4 for private Tableau analytics (2026-11-23)

At the owner's direction, Phase 4 is closed for the English Tableau workbook with real historical data. [Validation](VALIDATION.md) records SQL reconciliation, packaging checks and the verified Desktop filter action. Additional cross-store reviews and automated refresh remain follow-up work. Public portfolio delivery remains open under PULSE-23 and requires a shareable data basis. Phase 3 remains open and Phase 5 awaits authorization.

### D-017 — Begin Phase 5 validation and release preparation (2026-11-23)

The owner authorized Phase 5 work while Phase 3 remains open. The scope covers end-to-end validation, reproducible setup and release preparation. Publishing genuine retailer observations requires a verified sharing basis for the artifacts concerned.

### D-018 — Add Konzum as the third local source (2026-11-23)

The owner authorized Konzum Super 1280 for the local acquisition and PostgreSQL
cohort. In the two-date Zagreb sample, 5,900 priced codes appeared in Konzum,
SPAR and Kaufland on both dates. Lidl is deferred because its shared cohort
was smaller and its CSV layout changed between samples. Keep genuine retailer
artifacts private and review product variants and promotion eligibility before
using cross-store price gaps.

See [PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46) and
[Source feasibility](SOURCE_FEASIBILITY.md#two-date-expansion-decision).

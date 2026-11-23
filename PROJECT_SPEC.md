# PricePulse project specification

**Status (2026-11-22):** Phase 0 and Phase 1 are formally closed. Phase 2 is in owner review after synthetic PostgreSQL validation. Kaufland + SPAR Croatia passed bounded source feasibility, including a 102-pair descriptor-consistency gate; this is not manufacturer certification.

## Problem and value

Retailers change published product prices over time and may vary prices by selling location. A reproducible Data Engineering pipeline should turn **source-attributed, machine-readable price-list observations** into trustworthy longitudinal analytics and defensible like-for-like comparisons.

PricePulse focuses on grocery and household goods sold in **Croatia**, using official **Kaufland Croatia and SPAR Croatia** price lists now technically qualified for planned local development. Lidl is excluded from the first release by scope choice, not because of a demonstrated technical blocker.

## Initial business questions

- How does the listed price of a verified product change between observations?
- For a common product and equivalent comparison context, how large is the price difference between Kaufland and SPAR?
- Which common product categories have the largest relative price differences?
- What fraction of source records have a valid product identifier, usable price, clear unit, and consistent provenance?
- How frequently are expected price-list files published and successfully ingested?

**Not initially supported:** real-time stock availability, confirmed in-store shelf availability, and a claim that missing products are out of stock.

## Source and cohort scope

- Country: Croatia; currency: EUR.
- Qualified first pair: **SPAR Croatia (Jankomir 8702)** and **Kaufland Croatia (Antuna Šoljana 5630)**; bounded local tests passed, continuous operational access is not proven.
- Initial cohort: one physical Zagreb store per retailer, matching *publication date* for cross-store comparisons and *store ID* across dates for time-series checks.
- Matching: validate GTIN-8/12/13/14 checksums; preserve raw identifiers and documented 14-digit normalized keys; require brand/package/variant consistency. Review conflicting quantities, multipacks and gross vs drained weights. Keep ambiguous matches separate.
- Initial measurable goal: >=100 **description-consistent** matched products on a common day. **102/160** deterministically selected strict candidates passed conservative text review; 58 remain unresolved. This is neither independent GS1/manufacturer certification nor a population accuracy estimate.
- Full national store coverage, promotion-adjusted baskets, and spatial analysis are possible extensions, not initial requirements.

## Proposed data contract (subject to actual-file validation)

| Attribute | Purpose | Rules / uncertainty |
| --- | --- | --- |
| source_chain, source_url, source_file_hash | Provenance | Retain exact acquisition evidence |
| source_store_id, store_location | Selling location | Required for store-level comparison; parsing rules depend on source |
| price_list_date, source_published_at, collected_at_utc | Time | Separate effective/publication date from retrieval time; no fabricated timestamps |
| retailer_product_code | Source-local identity | Never assume cross-retailer uniqueness |
| gtin_ean, title, brand | Product matching | GTIN/EAN is optional in the regulation; reject invalid/ambiguous match claims |
| net_quantity, unit, category | Comparability | Nullable if missing; normalize units before comparing |
| regular_price_eur, special_price_eur, effective_price_eur, price_origin, unit_price_eur | Price metrics | Keep original source fields; positive Decimal amounts; effective price comes from the sole provided field or two equal fields; dual-different amounts require explicit exception handling |
| sale_indicator, baseline_price_eur | Context | Keep source-specific sale meaning; baseline/anchor price is not a time-stamped historical observation |
| raw_row, ingestion_status | Audit and quality | Preserve evidence of invalid rows without silently converting them |

This table remains the intended contract, not a claim that every attribute is modeled or validated. An initial PostgreSQL schema and loader have been tested with synthetic inputs; see [PostgreSQL](POSTGRESQL.md). Measured CSV dialects differ: **SPAR cp1250 + semicolon**, **Kaufland UTF-8 BOM + tab**. Version header mappings, unit semantics and price selection; quarantine unexpected dual-different price observations rather than guessing precedence.

## Phase 0 evidence and implementation quality gates

| Gate | Observed result | Remaining boundary |
| --- | --- | --- |
| Live bounded Scrapy access to both retailers | **Passed**; official indexes and selected CSVs returned HTTP 200 | Must monitor policy, HTTP errors, schema changes and availability over time |
| Same-day price-bearing GTIN intersection | **8,869** on 2026-11-17; **4,155** strict automated candidates | Codes alone are not a guarantee of identical variants |
| 100 documented comparable-product candidates | **102/160** descriptor-consistent after conservative manual review; **58 unresolved** | Independent manufacturer/GS1 checks and full-catalog precision not established |
| Two-date same-store price history | **Passed** for both store IDs, 2026-11-16/17 | Not evidence of scheduled operational reliability |
| SPAR promotional price recovery | **Passed** on two store files, all blank primary-price rows had populated special-price fields | Both-different price cases were not observed; require exception strategy |
| Redistribution clearance | **Not established** | Real data and source-derived public extracts remain blocked; use synthetic public Tableau demo |

**Phase 1 acceptance must be measured independently:** source-specific spiders and contracts, test fixtures, correct source-file provenance, bounded request handling, field-level validation and reproducible evidence. Do not treat the temporary Phase 0 scripts as a production implementation.

## Constraints

- Python and Scrapy first; PostgreSQL for historical records; Tableau for BI.
- Prefer free, locally reproducible workflows and bounded daily batch ingestion.
- Respect website terms, robots guidance, access controls and fair request pacing.
- Do not copy third-party crawler implementations or datasets without assessing their licenses.
- Do not publish raw price lists or individual-source datasets to Tableau Public without verifying sharing rights.
- Phase 0 exit evidence was reviewed and approved on 2026-11-19. Phase 1 implementation was separately authorized on 2026-11-19.

See [Source feasibility](SOURCE_FEASIBILITY.md), [Roadmap](ROADMAP.md), and [Validation](VALIDATION.md).

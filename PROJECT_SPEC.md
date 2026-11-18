# PricePulse project specification

**Status:** Phase 0 feasibility in progress; final source approval and implementation remain pending.

## Problem and value

Retailers change published product prices over time and may vary prices by selling location. A reproducible Data Engineering pipeline should turn **source-attributed, machine-readable price-list observations** into trustworthy longitudinal analytics and defensible like-for-like comparisons.

PricePulse will initially focus on grocery and household goods sold in **Croatia**, using the official price-list publications of **Kaufland Croatia and SPAR Croatia as candidate sources**. Lidl is excluded from the first release; this does not establish that Lidl is technically unusable.

## Initial business questions

- How does the listed price of a verified product change between observations?
- For a common product and equivalent comparison context, how large is the price difference between Kaufland and SPAR?
- Which common product categories have the largest relative price differences?
- What fraction of source records have a valid product identifier, usable price, clear unit, and consistent provenance?
- How frequently are expected price-list files published and successfully ingested?

**Not initially supported:** real-time stock availability, confirmed in-store shelf availability, and a claim that missing products are out of stock.

## Source and cohort scope

- Country: Croatia; currency: EUR.
- Candidate retailers: Kaufland and SPAR (priority pair; not yet technically validated locally).
- Primary sample: one comparable physical store per retailer, preferably within the same city/area, using price lists for the same publication date.
- Matching: validate GTIN/EAN checksums and compare exact, normalized identifiers; review package size, brand, quantity, and variant. Keep unmatched or ambiguous records separate.
- Initial measurable goal: **at least 100 distinct, valid, verified shared products** on a recent common date, not merely a historical third-party estimate.
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
| retail_price_eur, unit_price_eur | Price metrics | Decimal precision; reject invalid or negative values |
| sale_indicator, baseline_price_eur | Context | Preserve exactly what each source publishes; baseline is not historical observation |
| raw_row, ingestion_status | Audit and quality | Preserve evidence of invalid rows without silently converting them |

Fields are conceptual mappings, not a declaration that both live formats have passed validation. The 17 Nov 2026 regulation provides a CSV/XML, UTF-8 and semicolon-delimited foundation; existing retailers' actual structures may differ during transition.

## Quality and acceptance targets (proposed)

1. Confirm robots/terms and direct Scrapy access to official indexes and representative files; no CAPTCHA, WAF bypass, or unapproved authentication.
2. Successfully identify and parse representative current files for both retailers, with source metadata and deterministic conversions.
3. Count and document >=100 distinct validated overlapping GTIN/EAN products at the same recent publication date, in compatible store contexts.
4. Inspect at least 30 randomly/reproducibly selected matched records to verify identity, package size, price and unit semantics. Target >=95% correct parsed required fields in that sample; report confidence and errors.
5. Demonstrate at least two dated observations or reproducible historical snapshots for the selected sources before claiming viable trends.
6. Verify source-data retention, reasonable request rates, and publication rights separately from local acquisition rights.

Do not infer a passing gate from a previous third-party study alone.

## Constraints

- Python and Scrapy first; PostgreSQL for historical records; Tableau for BI.
- Prefer free, locally reproducible workflows and bounded daily batch ingestion.
- Respect website terms, robots guidance, access controls and fair request pacing.
- Do not copy third-party crawler implementations or datasets without assessing their licenses.
- Do not publish raw price lists or individual-source datasets to Tableau Public without verifying sharing rights.
- No Phase 1 code implementation until Phase 0 exit evidence is reviewed.

See [Source feasibility](SOURCE_FEASIBILITY.md), [Roadmap](ROADMAP.md), and [Validation](VALIDATION.md).

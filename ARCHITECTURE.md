# Intended architecture

**Status: Phase 1 is closed; Phases 2 and 3 await owner review; Phase 4 is in progress.** The source adapters were bounded smoke-tested. An initial PostgreSQL schema, loader and comparison review are implemented and validated with synthetic data; real-source ingestion and operational reliability remain unverified. A local collection-only task is registered but recurring live capture has not been observed. An initial synthetic Tableau worksheet and local analytical exports exist; the dashboard is incomplete. See [Acquisition](ACQUISITION.md), [PostgreSQL](POSTGRESQL.md), [Reliability](RELIABILITY.md) and [Validation](VALIDATION.md).

## Proposed data flow

The diagram shows the intended end-to-end architecture. The current loader accepts locally held CSV files; the local task performs collection only. XML/compressed formats and the Tableau dashboard are not implemented, and normal daily scheduling remains unverified.

```text
Kaufland Croatia price-list index     SPAR Croatia price-list index
                 |                                 |
                 +------- Scrapy source adapters --+
                                   |
                      Official CSV/XML files
                     (optional ZIP/GZ wrapper)
                                   |
                           Raw file manifest
                (source, store, timestamps, hash)
                                   |
                      Python validation and parsing
                    (SPAR: cp1250, semicolon)
                    (Kaufland: UTF-8 BOM, tab)
                 (locale decimals, fields, GTIN checks)
                                   |
                          PostgreSQL staging
                                   |
                   Product / retailer / store identity
                      + offers + dated prices
                                   |
                      SQL quality + comparison marts
                                   |
                         Tableau Desktop Free
                                   |
                       Tableau Public (only if
                       publication is permitted)
```

## Responsibilities and important grain decisions

| Component | Responsibility | Exclusion |
| --- | --- | --- |
| Scrapy | Implement two source adapters: SPAR dated JSON manifest and Kaufland asset list; obey robots, fetch bounded store/date batches, log HTTP/provenance | No CAPTCHA bypass, identity matching, or uncontrolled retries |
| Raw manifest | Track original URL, publication date, store, fetch time, checksum, source response | Does not imply that publication timestamp equals fetch timestamp |
| Parser/validator | Handle actual SPAR cp1250/semicolon and Kaufland UTF-8 BOM/tab; preserve raw regular/special price columns, locale decimals, GTINs and package exceptions | No invented missing fields, stock, or guessed dual-price precedence |
| PostgreSQL | Preserve immutable price observations at **retailer × store × product × publication date/version** grain; deduplicate exact re-ingestions | Does not collapse distinct stores, dates or promotions into one price |
| Matching | Verified GTIN/EAN plus quantity/variant checks, exception reports for ambiguous IDs | Does not join product titles indiscriminately |
| SQL analytics / Tableau | Same-date, same-product, comparable-store price spreads; true longitudinal trends | Does not assume one price represents an entire retailer or a baseline price equals historical data |
| Scheduler/tests | Bounded daily polling, schema drift detection, retries and observability | No unsupported availability or completeness guarantees |

## Data characteristics to design for

- Official price lists are **files**, not product-card HTML, so file download is the primary scraping unit.
- Under Croatia's **NN 132/2026** price-list regulation (effective 2026-11-17), the required format and automated access underpin the acquisition design. **Observed** sources used SPAR cp1250/semicolon and Kaufland UTF-8 BOM/tab on 2026-11-16/17; treat incompatible changes as schema drift rather than invent a homogeneous format.
- Required public fields include retail price and baseline price. **Stock availability is not an assured field**; exclude inventory KPIs until a source explicitly provides meaningful inventory data.
- A retailer may publish distinct price lists per store; matching only by chain and GTIN discards location variation.
- Replaced files need remain available for only **15 days** under the reviewed regulation; create local versioned manifests and capture timestamps/hashes, subject to source-use constraints.
- Keep data source adapters separate so retailers can be replaced without rebuilding schema or dashboards.

## Initial data-quality contracts

- **Grain:** observation key is retailer + physical store + source product identifier/GTIN + publication date + source file version. Same barcode in different shops must never overwrite another store's observation.
- **Prices:** regular-only → regular; special-only → special; two fields equal → numeric value with both fields preserved; two fields different → flag and withhold from like-for-like pricing until semantics are verified. All monetary values use exact decimals.
- **Identifiers:** preserve raw codes as strings, validate checksums, normalize for comparison and isolate duplicate/colliding GTINs. Matching is separate from acquisition.
- **Quantity:** maintain source net quantity and unit separately from text-derived package size; explicitly handle multipacks, drained weights and ambiguous variant labels. Never equate a source-local `KOM` unit to the physical product volume.
- **Coverage:** track total rows, valid GTINs, field completeness and store/date counts; a +47.9% row-count discontinuity was observed in a Kaufland sample at the regulatory transition, making drift alerting necessary.
- **Publication:** local analytics may use validly accessed source observations within applicable terms, but genuine retailer files/real-data public extracts are not cleared for Tableau Public. Use synthetic public demo data unless a separate rights basis is established.

## Architectural constraints

Python/Scrapy, PostgreSQL, pytest, optional GitHub Actions and Tableau remain the planned primary stack. No additional browser/scraping framework or paid platform is authorized. Tableau Public is optional and limited to data with verified publication rights.

See [Source feasibility](SOURCE_FEASIBILITY.md), [Project specification](PROJECT_SPEC.md), and [Decisions](DECISIONS.md).

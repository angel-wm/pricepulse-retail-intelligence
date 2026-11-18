# Intended architecture

**Status: proposed, not implemented or tested.** Source-specific acquisition details require live validation.

## Proposed data flow

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
                     (UTF-8, ;, decimal comma,
                      field mapping, GTIN checks)
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
| Scrapy | Discover official source files, obey robots, fetch bounded batches and log HTTP response/provenance | No CAPTCHA bypass, identity matching or silent retry storms |
| Raw manifest | Track original URL, publication date, store, fetch time, checksum, source response | Does not imply that publication timestamp equals fetch timestamp |
| Parser/validator | Normalize source-specific headers, encoding, locale decimals, GTINs, quantities and price semantics | Does not invent missing fields or infer stock |
| PostgreSQL | Preserve immutable price observations at **retailer × store × product × publication date/version** grain; deduplicate exact re-ingestions | Does not collapse distinct stores, dates or promotions into one price |
| Matching | Verified GTIN/EAN plus quantity/variant checks, exception reports for ambiguous IDs | Does not join product titles indiscriminately |
| SQL analytics / Tableau | Same-date, same-product, comparable-store price spreads; true longitudinal trends | Does not assume one price represents an entire retailer or a baseline price equals historical data |
| Scheduler/tests | Bounded daily polling, schema drift detection, retries and observability | No unsupported availability or completeness guarantees |

## Data characteristics to design for

- Official price lists are **files**, not product-card HTML, so file download is the primary scraping unit.
- Under Croatia's **NN 132/2026** publication regulation (effective 2026-11-17), the listed format is CSV/XML, UTF-8, semicolon-delimited and optionally compressed; reality must still be validated per source.
- Required public fields include retail price and baseline price. **Stock availability is not an assured field**; exclude inventory KPIs until a source explicitly provides meaningful inventory data.
- A retailer may publish distinct price lists per store; matching only by chain and GTIN discards location variation.
- A replaced source file is required to remain available for only **15 days** under the new regulation; historical retention must be our own, subject to applicable usage terms.
- Keep data source adapters separate so retailers can be replaced without rebuilding schema or dashboards.

## Architectural constraints

Python/Scrapy, PostgreSQL, pytest, optional GitHub Actions and Tableau remain the planned primary stack. No additional browser/scraping framework or paid platform is authorized. Tableau Public is optional and limited to data with verified publication rights.

See [Source feasibility](SOURCE_FEASIBILITY.md), [Project specification](PROJECT_SPEC.md), and [Decisions](DECISIONS.md).

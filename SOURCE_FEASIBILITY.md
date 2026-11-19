# Source feasibility — Croatian grocery price lists

**Assessment date:** 2026-11-18. **Status:** bounded technical feasibility **passed** for Kaufland and SPAR Croatia, pending formal Phase 0 closure and explicit Phase 1 authorization. No production spiders exist; release of real retail observations is on hold.

## Decision snapshot

- **Selected category direction:** Croatia grocery and household-goods **published price-list intelligence**.
- **Priority candidate pair:** [Kaufland Croatia](https://www.kaufland.hr/akcije-novosti/popis-mpc.html) + [SPAR Croatia](https://www.spar.hr/usluge/cjenici).
- **Excluded from initial cohort:** Lidl (scope choice); abandoned UK musical-instrument retailer page scraping after repeated blocks or constraints.
- **Name:** retain **PricePulse**. Changing the project category does not require renaming a brand-neutral name.
- **Evidence attained:** official CSV files retrievable with Scrapy; **8,869** priced same-date code matches, **7,772** stable on four source files, **4,155** automatic strict candidates. A conservative private manual review of 160 selected source-description pairs found **102 consistent** and **58 unresolved**. Historical price observations for identical stores across two days were measured. Public reuse of original/derived retailer records remains restricted.

This document records the *research, completed limited acquisition tests, and remaining acceptance conditions*. Success of a bounded feasibility probe is **not** proof of a production-ready pipeline.

## Regulatory baseline effective 2026-11-17

The official Croatian [Regulation on publication of product price lists, NN 132/2026-1584](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html), published 2026-11-16 and effective 2026-11-17:

- Article 5 requires traders to enable software tools and automated programs to collect price-list data through technically available retrieval methods.
- Articles 3 and 6 specify items including product name, optional retailer code/brand/EAN, product quantity/unit, listed retail price, sale indication, unit price where applicable and baseline price. **Inventory quantity/stock is not mandated**.
- Articles 6(1), 6(6), 6(7) specify **CSV or XML, UTF-8 and semicolon-delimited columns**; ZIP/GZ containers are allowed. Actual source data must be tested for transition anomalies.
- Article 3(5) requires changed lists to be published by 11:00 on the effective date; article 3(6) requires availability of replaced files for **15 days**. Do not assume longer source-hosted historical retention.
- Article 3(7) recognizes price lists per store unless the same list applies to every store.
- Article 6(2) requires the replacement list at the **same page/location URL**; acquisition must preserve file version/content hash and dates, not rely solely on URL changes.
- The earlier [NN 75/2025 rule was revoked effective 2026-11-17](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1578.html).

**Rights boundary:** technical/legislative support for fetching is not an unrestricted license for publishing complete raw datasets. [SPAR's current general website terms](https://www.spar.hr/o-nama/opci-uvjeti-koristenja), section 2.1, restrict use of its website content to personal information purposes and require prior express written approval for modification, reproduction, distribution or inclusion in another site/medium/system. The regulation's automated-access mandate and these general terms are different issues and their legal interaction has not been resolved by this engineering review. **Public release of real SPAR price lists or a derived public Tableau dataset is not authorized by this source assessment.** Prefer a clearly labeled synthetic Tableau Public demo if no separate verified sharing basis is established. This plan does **not** require the user to request permission by email in order to continue bounded local feasibility research.

## Official retailer evidence

| Chain | Official publication | Evidence | Live Scrapy status |
| --- | --- | --- | --- |
| Kaufland | https://www.kaufland.hr/akcije-novosti/popis-mpc.html | Public page states daily updated retail price lists in digital formats | **HTTP 200 index and official CSV; Scrapy locally tested 2026-11-18** |
| SPAR | https://www.spar.hr/usluge/cjenici | Public page states daily CSV lists; semicolon delimiter and decimal comma | **HTTP 200 JSON indexes and official CSV; Scrapy locally tested 2026-11-18** |

### Discovery implementation hints — not verified public APIs

A third-party open-source reference, [senko/cijene-api](https://github.com/senko/cijene-api), includes independently maintained crawlers. Source inspection performed 2026-11-18 suggests:

- SPAR: date-specific JSON index pattern `https://www.spar.hr/datoteke_cjenici/CjenikYYYYMMDD.json`, exposing file names and URLs; files are then parsed as semicolon-delimited CSV.
- Kaufland: official price-list page may expose a `data-component=AssetList` element whose configuration points to a JSON asset index containing CSV URLs; source-file values may be tab-separated in an older format.

These are **third-party implementation clues, not guaranteed endpoints, approved interfaces or current live tests**. Scrapy access, current post-2026-11-17 formats and `robots.txt` must be checked independently. Do not copy that project's code or datasets without reviewing applicable licenses.

## Historical intersection evidence — not a current count

[Independent analysis of 2025-05-21 data](https://analiza.usporedicijene.info/) compared seven chains including Kaufland, SPAR and Lidl:

- **583** barcodes common across all seven.
- **4,126** barcodes common across the remaining six when Lidl was excluded.

Since both Kaufland and SPAR were among those six, the 2025-05-21 pair intersection was **at least 4,126** in that processed analysis. These numbers do **not** establish November 2026 availability, validity of every GTIN, same-store comparability or current price-file accessibility. They also do not mean that removing Lidl creates new products in either retailer.

## Direct November 2026 validation evidence

- User-executed limited Scrapy probes on 2026-11-18 confirmed HTTP 200 for both source indexes and official price files; see [Validation](VALIDATION.md) for counts and limitations.
- 2026-11-17 SPAR Zagreb Jankomir 8702 and Kaufland Zagreb Antuna Šoljana 43 5630 yielded **8,263 valid checksum GTIN matches with initially parsed prices**; a 30-pair anomaly sample is documented, including genuine potential pack-size inconsistencies.
- Both identical store IDs were observed on 2026-11-16 and 2026-11-17, allowing real two-day price-change analysis on stable-code cohorts.
- SPAR files have a split normal/promotional price representation: 3,103 of 32,347 rows on 2026-11-17 have blank primary price but valid special price; do not treat these as missing actual selling prices without considering their promotional field.
- Kaufland's store-level published row count jumped **47.9%** on 2026-11-17; audit for regulatory scope changes before reporting retailer-level assortment trends.
- Files differ in encoding and delimiter; use real dialect detection and source-specific contracts, not a single assumed UTF-8/semicolon parser.

## Final source evaluation — 2026-11-18

The independent user-local Phase 0 script downloaded price files for the same SPAR and Kaufland Zagreb stores on 2026-11-16 and 2026-11-17. **8,869** checksum-valid codes had usable same-date prices after handling regular-only, special-only and equal dual-price fields. **7,772** codes appeared in all four store/date files; **4,155** passed automatic strict brand/packaging rules. A private manual audit of 160 sampled strict candidates identified **102 documentary matches** and 58 unresolved. The 102 threshold is an indication of **description/brand/package consistency, not manufacturer/GS1 certification**. No precision claim can be extrapolated to the full catalog from this prefiltered sample.

Price-field cases in the four downloaded CSVs showed SPAR regular-only or special-only pricing and Kaufland regular-only or both-equal pricing. Future two-different-price cases must be reviewed. The two-day histories are real observations, not evidence of ongoing scheduling reliability. SPAR uses cp1250 with semicolons; Kaufland UTF-8 BOM with tabs. Both will need explicit parsers and schema drift tests.

**Engineering outcome:** the pair is sufficiently grounded for **planned local source-acquisition development**; no additional retailer discovery is indicated. Formal Phase 0 closeout still requires user approval and no further real-data publication may be inferred from technical access rights. See [Validation](VALIDATION.md).

## Proposed feasibility experiment — run before approval

1. **Policy/access:** obtain actual `robots.txt` from both domains; review source terms and use non-evasive, clearly identified Scrapy requests. Stop upon persistent 403/429 or CAPTCHA.
2. **Discovery:** for a chosen recent date, retrieve each index/manifest and **one representative official price-list file per chain**, recording direct URLs, status, actual encoding, delimiters, raw file hash, file size and published/store identifiers. Avoid bulk crawling.
3. **Comparable stores:** select one physical store for each chain, ideally in the same city/area (for example Zagreb), and the **same price-list date**. No store IDs or locations are assumed until read from actual source filenames/data.
4. **File/schema validation:** inspect column names and actual types; handle decimal comma, nonbreaking spaces, UTF-8/BOM, quoted delimiters, optional compression and unknown columns. Verify price and product identifiers from raw rows.
5. **GTIN intersection:** preserve codes as strings; distinguish local product numbers from valid GTIN/EAN; validate check digits; normalize valid variants to a documented canonical form; count unique codes per store and strict intersection. Exclude ambiguous collisions and incompatible package sizes.
6. **Acceptance:** document `valid_gtins_kaufland`, `valid_gtins_spar`, `shared_gtins_exact`, `shared_gtins_validated`, `ambiguous_matches`, `price_parse_success`, plus at least 30 reproducibly sampled matches. **Require >=100 validated distinct matches** and aim for >=95% correctly usable required fields in the sample.
7. **History:** verify at least two separately dated publications or valid public archives. Track acquisition time separately from publication/effective dates. A stable price is a valid observation; do not invent price changes.
8. **Permission/publication:** document technical access terms and use a safe publication strategy; no public release of raw historical retail observations until rights have been verified.

If this pair fails, investigate another official Croatian chain rather than bypassing restrictions or changing Scrapy prematurely.

## Distinct risks

- A public page may be readable in a browser/search engine but blocked to direct Scrapy/CSV downloads.
- Website paths, index JSON schemas and file formats may shift after the 2026-11-17 regulation.
- Same GTIN at different stores or dates is not a controlled price comparison; select comparable store and day.
- Retailers' optional EAN fields may be absent or contain invalid/internal codes; product naming and package quantities can conflict.
- Product not listed does not imply out-of-stock status.
- A single day's files cannot establish a time series; historical snapshots must be retained deliberately.
- Local historical storage and redistribution/public Tableau publication have different constraints.

## References

- [Official regulation NN 132/2026-1584](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html)
- [Earlier decision revoked NN 132/2026-1578](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1578.html)
- [Kaufland published prices](https://www.kaufland.hr/akcije-novosti/popis-mpc.html)
- [SPAR published prices](https://www.spar.hr/usluge/cjenici)
- [Historical May 2025 cross-chain analysis](https://analiza.usporedicijene.info/)
- [Independent crawler reference](https://github.com/senko/cijene-api)

Next steps and evidence status: [Roadmap](ROADMAP.md), [Validation](VALIDATION.md), [Current state](CURRENT_STATE.md).

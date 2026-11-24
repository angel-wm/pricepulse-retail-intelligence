# Source feasibility — Croatian grocery price lists

**Assessment baseline: 2026-11-18. Status on 2026-11-19: Phase 0 formally CLOSED by explicit owner approval after bounded technical feasibility passed.** The qualified development pair is SPAR Zagreb Jankomir (store 8702) plus Kaufland Zagreb Antuna Šoljana (store 5630). Bounded Phase 1 acquisition adapters now exist; sharing real retailer extracts publicly is not cleared.

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

### Source discovery interfaces verified in bounded local tests

A third-party open-source reference, [senko/cijene-api](https://github.com/senko/cijene-api), includes independently maintained crawlers. Source inspection performed 2026-11-18 suggests:

- SPAR: date-specific JSON index pattern `https://www.spar.hr/datoteke_cjenici/CjenikYYYYMMDD.json`, exposing file names and URLs; files are then parsed as semicolon-delimited CSV.
- Kaufland: official price-list page may expose a `data-component=AssetList` element whose configuration points to a JSON asset index containing CSV URLs; source-file values may be tab-separated in an older format.

The initial patterns were suggested by a third-party repository, then **the official SPAR and Kaufland indexes and a sample of the resulting CSV links returned HTTP 200 under bounded user-local Scrapy tests** on 2026-11-18. Interfaces are **not contractual APIs**: monitor schema and access changes, obey robots guidance, and do not copy third-party code without license review.

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

**Engineering outcome:** the pair is sufficiently grounded for local source-acquisition development; no additional retailer discovery is indicated. Formal Phase 0 closeout was explicitly approved on **2026-11-19**; the owner separately authorized Phase 1 implementation later that day. Publishing real source data remains outside that authorization. See [Validation](VALIDATION.md).

## Owner closeout decision (2026-11-19)

The project owner explicitly approved **formal Phase 0 closure** and synchronization of GitHub documentation and Jira. This decision accepts bounded source access, the documented 102 descriptor-consistent matches, the unresolved identity exceptions, and the restrictions on real-source public redistribution. The closeout did not itself authorize Phase 1; the owner authorized Phase 1 separately later on 2026-11-19. Publication of real retail-source extracts remains unapproved.

## Verification checklist and Phase 0 closeout conditions

| Test | Actual status and evidence |
| --- | --- |
| Bounded index/CSV retrieval with Scrapy | **Passed**: both retailer indexes and selected files HTTP 200, robots obedience enabled. No bot-defense bypass. |
| Same-day store and currency comparability | **Passed as an initial Zagreb sample**: SPAR 8702 and Kaufland 5630, 2026-11-17, EUR. |
| Valid codes and source-price handling | **Passed on tested files**: 8,869 shared priced code candidates; SPAR empty regular field was fully supplemented by special field in each sampled date. |
| Cross-date continuity | **Passed as a two-date feasibility test**: the same store IDs were used on 2026-11-16 and 2026-11-17; not proof of long-term availability. |
| Matching quality gate | **102** description-consistent items in a deterministic 160-pair sample selected from 4,155 strict candidates; **58** held for review. Independent manufacturer/GS1 verification remains beyond the bounded gate. |
| Formatting and drift | **Source-specific**: SPAR cp1250/semicolon; Kaufland UTF-8 BOM/tab. Store-size shifts and optional fields require monitoring. |
| Source rights and public Tableau release | **Restricted**: no public redistribution of source files or derived real-source extracts is approved. The public portfolio data approach is undecided; synthetic data is an option. |
| Formal closeout and Phase 1 implementation | **Phase 0 formally CLOSED by owner approval on 2026-11-19.** Phase 1 implementation was authorized on 2026-11-19; bounded adapters are implemented and smoke-tested. |

The checks are traceable in [Validation](VALIDATION.md), which distinguishes user-local test logs, inferred matching and independently unverified product properties. If access/terms change, source qualification must be revisited rather than circumventing restrictions.

## Distinct risks

- Initial Scrapy access succeeded, but the source could later return access controls or altered endpoints; stop rather than bypass.
- Website paths, index JSON schemas and file formats may shift after the 2026-11-17 regulation.
- Same GTIN at different stores or dates is not a controlled price comparison; select comparable store and day.
- Retailers' optional EAN fields may be absent or contain invalid/internal codes; product naming and package quantities can conflict.
- Product not listed does not imply out-of-stock status.
- Two days of same-store snapshots demonstrated historical feasibility, but durable retention and idempotent ingestion remain Phase 2 implementation work.
- Local historical storage and redistribution/public Tableau publication have different constraints.

## References

- [Official regulation NN 132/2026-1584](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html)
- [Earlier decision revoked NN 132/2026-1578](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1578.html)
- [Kaufland published prices](https://www.kaufland.hr/akcije-novosti/popis-mpc.html)
- [SPAR published prices](https://www.spar.hr/usluge/cjenici)
- [Historical May 2025 cross-chain analysis](https://analiza.usporedicijene.info/)
- [Independent crawler reference](https://github.com/senko/cijene-api)

Next steps and evidence status: [Roadmap](ROADMAP.md), [Validation](VALIDATION.md), [Current state](CURRENT_STATE.md).

## Expansion feasibility — 2026-11-23

A one-day Zagreb sample supports prioritizing Konzum for a future third-retailer pilot.
The sample used Konzum Super 1280 and Lidl 158 on Velimira Škorpika, along with the
existing SPAR 8702 and Kaufland 5630 baseline for the same publication date.
Both candidate CSVs downloaded from public retailer links and are stored under ignored
`data/`. See the [Konzum price-list index](https://www.konzum.hr/cjenici) and
[Lidl price-list index](https://www.lidl.hr/c/cijene/s10073252).

Counts use distinct checksum-valid GTIN-8, GTIN-12, GTIN-13 or GTIN-14 values normalized
to 14 digits, with a positive listed price. The two Lidl barcode fields were considered
together and all rows had at most one distinct valid code. SPAR and Kaufland counts
use the private Tableau observations export for the two fixed stores.

| Candidate | Source rows | Priced GTINs | With SPAR | With Kaufland | With both |
| --- | ---: | ---: | ---: | ---: | ---: |
| Konzum 1280 | 26,581 | 24,158 | 9,279 | 7,489 | 5,961 |
| Lidl 158 | 16,232 | 15,242 | 1,023 | 1,020 | 877 |

SPAR and Kaufland share 8,854 priced GTINs. The candidates share 1,002 with each
other, and 777 GTINs appear across all four stores. Matching codes identify candidates
for variant review. Verify brand, size, unit and pack count before comparing prices.

Both sample files decoded as UTF-8. Konzum used commas and all rows had a positive
retail price. Lidl used semicolons and 1,706 rows had a positive special price
with no positive regular price. A pilot should verify the promotion fields, code
duplicates and store/date selection before assigning a price for comparison.

Repeat the comparison for the same four stores on additional dates and review a sample
across categories. Track how many products gain another price option and whether
their price or promotion changes the comparison. Lidl can support a smaller matched
basket or a separate equivalent-products study, where equivalence requires explicit
rules for quantity and product attributes.

This was a bounded feasibility check. Adding a production source requires a separate
scope decision. Any public use of retailer data remains subject to verified reuse rights.

### Two-date expansion decision

The follow-up downloaded the same candidate stores for 17 November and compared
them with the existing SPAR 8702 and Kaufland 5630 export for both dates. The two
dates are six days apart. Rows with ambiguous prices or conflicting valid codes
were excluded. Price rankings also excluded a code when any participating store
had more than one observation for it on that date. Rankings use published
prices, including special-only prices, before checking promotion eligibility.

| Measure | 17 Nov | 23 Nov |
| --- | ---: | ---: |
| SPAR and Kaufland shared priced codes | 8,869 | 8,854 |
| Also present in Konzum | 5,968 | 5,961 |
| Also present in Lidl | 870 | 877 |
| Present in all four stores | 771 | 777 |
| Konzum below both baseline stores | 818 | 672 |
| Lidl below both baseline stores | 215 | 218 |
| Lidl below all three other stores | 168 | 168 |
| Lidl shares a code with a baseline store that Konzum lacks | 234 | 243 |

The three-store cohort persisted across both dates for 5,900 Konzum codes and
836 Lidl codes. The price-ranking step excluded 36 and 48 duplicate-code
candidates for Lidl against both baseline stores. A private spot check of 12
price-winning candidates per chain on 23 November found missing pack details
and a possible Lidl variant conflict. The ranking counts are screening results,
not verified savings or basket rankings.

Konzum used the same comma-delimited headers across both dates. Lidl moved from
comma-delimited to semicolon-delimited data and changed its headers and barcode
fields. Lidl had 1,934 special-only rows on 17 November and 1,706 on 23 November.
These changes require explicit format detection and duplicate handling in any
future Lidl adapter.

The owner authorized Konzum as the third local retailer on 2026-11-23.
Integration is tracked in [PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46).
The owner confirmed that Lidl stays outside the current release on 2026-11-24. Consider Lidl later for a defined basket if
audited variants and promotion eligibility confirm that its incremental cheapest
offers justify maintaining the additional adapter. Verify regular scheduled
capture and matching on the selected stores. Keep real retailer artifacts local
pending a verified basis for reuse.

# Validation and evidence

## Status

**Phase 0: IN PROGRESS.** Source access, same-date GTIN intersection and two-day same-store history have passed **initial bounded user-local tests**. Product-equivalence exceptions, effective promotional price semantics, source coverage drift and public redistribution remain unresolved. Phase 1 has not started.

## Evidence ledger

| Area | Result | Basis / limitation |
| --- | --- | --- |
| Official source publications | CONFIRMED AS PUBLISHED | Kaufland Croatia and SPAR Croatia public price-list pages consulted on 2026-11-18 |
| Machine-readable legal framework | CONFIRMED BY OFFICIAL TEXT | NN 132/2026-1584, effective 2026-11-17: automated tools supported; CSV/XML; UTF-8; semicolon; archive 15 days |
| Historical overlap potential | SECONDARY HISTORICAL EVIDENCE | 2025-05-21 third-party analysis: 583 barcodes common across seven chains, 4,126 across six excluding Lidl; not a November 2026 direct pair count |
| Kaufland robots + Scrapy access | PARTIAL PASS — 2026-11-18 user-local run | HTML index 200, assets JSON index 200, one 2026-11-17 Zagreb CSV 200; direct parsed rows 23,593; 23,238 usable product rows. Current-day 2026-11-18 filename match returned zero in index. |
| SPAR robots + Scrapy access | PARTIAL PASS — 2026-11-18 user-local run | JSON indexes 200 on 2026-11-17 and 2026-11-18, each advertising 144 files; three CSV downloads 200, parsed successfully. |
| Current Kaufland–SPAR GTIN intersection | INITIAL PASS — 8,263 | Same-date 2026-11-17, SPAR Zagreb Jankomir vs Kaufland Zagreb Antuna Šoljana 43; 8,263 unique checksum-valid EANs with prices passing initial parsing. Does not yet validate all product/packaging equivalence. |
| Current schema and parser accuracy | STRUCTURAL PASS; SEMANTIC WORK REMAINS | SPAR: cp1250, semicolon; Kaufland: utf-8-sig, tab. SPAR missing base price is explained by populated special-price field in all rejected rows in both sampled days; effective-price selection needs explicit rules and tests. |
| Repeatability and history | INITIAL TWO-DATE PASS | Same SPAR store 8702 and Kaufland store 5630 downloaded for 2026-11-16 and 2026-11-17; 28,217 and 15,533 common day-to-day GTINs respectively. Only two days observed, not production reliability. |
| Source reuse and Tableau publication | UNRESOLVED | Automated retrieval support does not imply an unrestricted redistribution license |
| PostgreSQL, automated tests, Tableau | NOT IMPLEMENTED | No runtime or dashboards |

## Croatian grocery sources — user-local acquisition evidence (2026-11-18)

**Method:** user executed the standalone Scrapy Phase 0 probe script with robots obedience, 10-second per-domain delay, single-domain concurrency, no retries, and bounded discovery/CSV download. User provided a console-log file. These are **user-observed test results**, not CI or independently repeated executions.

| Source / price-list date / location | HTTP | Raw rows | Valid GTIN/EAN entries | Valid price entries | Usable distinct products | Encoding / delimiter |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| SPAR / 2026-11-18 / Zagreb Jankomir | 200 | 32,384 | 31,634 | 29,011 | 28,273 | cp1250 / semicolon |
| SPAR / 2026-11-18 / Zagreb Buzin | 200 | 31,267 | 30,559 | 27,886 | 27,190 | cp1250 / semicolon |
| SPAR / 2026-11-17 / Zagreb Buzin | 200 | 31,319 | 30,609 | 28,219 | 27,522 | cp1250 / semicolon |
| Kaufland / 2026-11-17 / Zagreb | 200 | 23,593 | 23,238 | 23,593 | 23,238 | utf-8-sig / tab |

- SPAR JSON index HTTP 200 on both 2026-11-18 and 2026-11-17; 144 files advertised on each date.
- Kaufland index HTML and JSON both HTTP 200; JSON advertised 2,227 assets. Date filter found **zero matching filenames for 2026-11-18** and **53 for 2026-11-17**. The zero match might involve publication timing or filename conventions; it is not proof of zero available 2026-11-18 products.
- Script selected and downloaded four CSVs; all HTTP 200 and parsed by its initial heuristics. No duplicate GTINs reported within these selected files after initial check; semantic validation of input fields is still outstanding.
- **Critical gap:** the script only intersected files for 2026-11-18. With no Kaufland file selected for that date, it returned **no cross-retailer overlap metric**. It must be rerun for 2026-11-17 using one comparable store per chain before the >=100-product acceptance gate can be evaluated.
- Source files were processed transiently; the log does not include full product rows and cannot itself support a barcode intersection computation.

## Same-date intersection — user-local log, 2026-11-18

The user executed the bounded second Phase 0 probe with main date **2026-11-17** and previous date **2026-11-16**. Observations:

- SPAR and Kaufland indexes responded HTTP 200; SPAR 144 published store lists per date; Kaufland 53 lists on each of the chosen dates.
- Six official CSV files selected and downloaded HTTP 200 (SPAR: three; Kaufland: three), across 2026-11-16 and 2026-11-17.
- **8,263 checksum-valid normalized EANs with parseable positive retail prices** overlapped between SPAR Jankomir (store ID 8702) and Kaufland Zagreb Antuna Šoljana 43 (store ID 5630) on 2026-11-17. This is an initial exact-code overlap, **not a full same-variant/manual matching validation**.
- The randomly selected 30-row sample includes at least one apparent package discrepancy: Garnier product **250 ml at SPAR** versus **200 ml at Kaufland** with the same normalized code. Other records warrant unit/brand review. Price differences cannot yet be treated as reliable like-for-like comparisons without row checks.
- The previous-date SPAR sample and current-date SPAR sample were not necessarily the **same store**, so same-store price trends remain **unvalidated**. Same-store 2026-11-16 and 2026-11-17 downloads must be selected explicitly.
- SPAR initial parser rejected approximately 9–11% of retail-price values across sampled files; no cause analysis is yet supported. Actual source values and special-price semantics must be investigated.
- CSV format evidence: SPAR `cp1250` + semicolon; Kaufland `utf-8-sig` + tab. Source-specific parser contracts must preserve these actual observations rather than assume uniform CSV dialect.
- **Phase 0 remains open**, pending selected-store history, price diagnostics, sampled matching audit and publication-rights decision.

## Price semantics, same-store history and product sample — user-local log (2026-11-18)

**Evidence:** user-uploaded `pricepulse_phase0_quality_result.txt`, generated by the bounded Scrapy Phase 0 quality script; results below were read from that log, not independently rerun against the live retail sources.

### Stable store identities and dates

- SPAR Interspar Zagreb Jankomir **store 8702**, files for **2026-11-16** and **2026-11-17**, both HTTP 200. Same-date 2026-11-17 source has **32,347 rows** and **28,507 initially usable rows** (base-price-only parser).
- Kaufland Zagreb Antuna Šoljana 43 **store 5630**, files for **2026-11-16** and **2026-11-17**, both HTTP 200. Same-date 2026-11-17 source has **23,593 rows**, **23,238 initially usable rows**.
- SPAR day-to-day matched GTINs: **28,217**, of which **14 increased**, **40 decreased** and **28,163 unchanged** using the first-pass base-price-only parser.
- Kaufland day-to-day matched GTINs: **15,533**, of which **9 increased**, **69 decreased** and **15,455 unchanged** using the first-pass parser.
- These are counts of code-matched offers at **two dated snapshots**, not statistically measured daily reliability, and SPAR counts are provisional until sale-price handling is corrected.

### SPAR advertised price is split between fields

| SPAR Jankomir file date | Rows | Nonempty, parseable `MPC (EUR)` | Empty `MPC (EUR)` with parseable special-price field |
| --- | ---: | ---: | ---: |
| 2026-11-16 | 32,322 | 29,231 | **3,091** |
| 2026-11-17 | 32,347 | 29,244 | **3,103** |

In the tested files, **every** row rejected by the initial `MPC (EUR)` parser has an empty primary-price field and parseable `MPC za vrijeme posebnog oblika prodaje (EUR)` value; there is **no observed unpriced row across either sampled SPAR file after considering both fields**. This resolves the *missing-price diagnosis*, not yet the semantic rule for effective selling price. Implement `listed_effective_price = regular_price if valid else special_price if valid`, with explicit sale flags/source column lineage, only after confirming which field prevails when both are populated; never label a fallback price a normal/regular price without evidence.

### Identity matching audit — 30-code sample (provisional)

- From the **8,263** GTIN checksum-valid same-date SPAR–Kaufland overlap candidates, the reproducibly sampled **30** pairs triggered **3 quantity-review flags**, **4 quantity-unavailable-in-title flags** and **8 brand-review flags** (flags can overlap; do not add them as unique mismatches).
- **Clear source-text discrepancy:** Garnier Fructis EAN `03600542134835`, SPAR label **250 ml** vs Kaufland **200 ml** — exclude from validated like-for-like comparisons until source quantity/product evidence resolves it.
- **Likely false quantity alert:** Podravka pickles `03850104273957`: 660 g versus 660g/330g (gross/net); simplistic last-number title parser incorrectly treats 330 g as a different package.
- **Unresolved unit descriptions:** Hole cooking preparation `08007990002344` lists 500 ml vs 500 g; must verify source-declared quantity/units rather than equate them.
- **Possible brand/category aliases or errors:** `03859888817012` shows Odisej vs Pag 91; `04000540080100` uses Kölln vs Koelln (likely spelling variant); do not reject or accept solely on raw brand equality.
- **Pack multiplier issue:** Coca-Cola 2 × 2 L (`05449000059338`) was parsed as 2 L by the naive title rule instead of 4 L total. Multipacks need dedicated parsing or structured net quantity.
- **False missing-quantity alert:** Denim 250 ml product `08008970004266` contains `250 ml_OC` in Kaufland text; regex word-boundary behavior prevents extraction even though quantity is apparent.
- **Audit conclusion:** these 30 records support strong pair feasibility, but do **not** demonstrate that all 8,263 product identities or a specifically enumerated cohort of >=100 are manually verified. Require a defined matching/exception policy and a separately testable representative cohort before claiming the Phase 0 100-validated target.

### Source-volume drift and publication limits

- Kaufland store 5630 published **15,953 rows on 2026-11-16** vs **23,593 on 2026-11-17** (**+7,640 / ~47.9%**). This is material population/coverage drift on the new-regulation transition date, not necessarily a 47.9% increase in available physical products. Segment comparisons by stable common GTIN cohort and log row-count shifts.
- SPAR store 8702: **32,322 rows on 2026-11-16** vs **32,347 on 2026-11-17** (+25).
- Data format differs from uniform legal ideal in these sampled files (SPAR cp1250/semicolon; Kaufland UTF-8 BOM/tab). Observed source formats must be accepted explicitly by parsers and monitored for changes.

**Next closeout gate:** approve effective-price semantics, verified matching/quantity/brand rules and a reliably identified cohort of >=100 genuine like-for-like products, and define public dashboard sharing bounds. No further retailer search is currently indicated.

## Earlier source exploration — user-reported local logs, 2026-11-18

These tests concerned an **abandoned musical-instruments source category** and do not validate the new pair.

- Andertons: three separate Scrapy product requests HTTP 200; JSON-LD product fields for Boss, Ibanez and Lee Oskar including product SKU, GBP price, brand and availability.
- Gear4music: product HTTP 403 with human-verification page.
- Bonners Music: product HTTP 429 rate-limit response.
- GigGear: robots and product HTTP 405 with human verification / AWS WAF CAPTCHA.
- guitarguitar: contractual automated price collection restriction noted in feasibility review.

These results were supplied in the conversation by the user, not independently replayed in CI.

## Phase 0 validation plan (not execution results)

1. **Access and access policy:** check both official `robots.txt` files and terms; request one index page and one representative publication per retailer using Scrapy, with bounded concurrency, no anti-bot bypass and recorded statuses.
2. **Current files:** select a common recent publication date and one comparable physical store in each chain; capture source URLs, hashes, date/time, store IDs, headers, encoding, file count and currency.
3. **Matching:** count unique normalized valid GTINs in each chosen file, strict intersection size, malformed IDs, ambiguous duplicates, variant/quantity disagreements and retained valid matches. **Require >=100 validated matches**.
4. **Accuracy:** deterministic 30-record identity/price/quantity sample; document parsing completeness and rejected rows, aiming for >=95% usable required-field extraction.
5. **History:** verify a second source publication date or a valid retained archive. Compare listed source dates rather than confusing them with download timestamps.
6. **Publication rights:** determine what may be stored and shared in a public Tableau portfolio; withhold raw public dataset if unverified.

Record each actual command, date, URL, HTTP status, file hash and result. Never report a proposed target as a measured success.

## Documentation checks

Earlier GitHub documentation review (baseline `861062303de56dfa39199e07f50dc287bc0952cb`, 2026-11-14): 12/12 Markdown documents fetched, 38 relative links checked with no unresolved links. **That result applies only to the cited baseline**, not the current revisions; new links still require verification.


### Current documentation revision check — 2026-11-18

- **Baseline:** commit `02465fd1b426821797feb8c352105fce15f2836d` (Phase 0 grocery scope revision).
- **Method:** retrieved the ten changed Markdown documents through the GitHub connector; checked the existence of local relative Markdown link targets in the revised document inventory.
- **Observed:** 10 of 10 documents retrieved; 52 local relative link targets found and checked; zero unresolved file paths.
- **Limitations:** heading-anchor links, external URLs, Markdown rendering, live price-list requests and runtime behavior were not checked by this documentation test. This is not a Phase 0 source-access pass.

## Sources referenced during Phase 0

- Regulation: https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html
- Revocation of earlier 2025 requirements: https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1578.html
- Kaufland: https://www.kaufland.hr/akcije-novosti/popis-mpc.html
- SPAR: https://www.spar.hr/usluge/cjenici
- Historical third-party cross-chain study: https://analiza.usporedicijene.info/
- Independent project reference (not our implementation): https://github.com/senko/cijene-api

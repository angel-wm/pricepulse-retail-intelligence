# Validation and evidence

## Phase 1 PULSE-13 — 2026-11-22

The offline suite passed **21 tests**. Request-policy tests exercise robots rules, settings for concurrency, delay and timeout, domain restrictions, retry limits, HTTP 403/404/429 classification, malformed indexes, bounded selection and incomplete file responses. HTTP and transport failures were simulated; the checks do not establish production reliability.

A bounded SPAR 8702 run on 2026-11-22 requested the 2026-11-17 file. Scrapy recorded **3 GET requests and 3 HTTP 200 responses**, including one successful robots.txt request, the dated index and the selected CSV; no retries were recorded. It finished normally, emitted one manifest and 32,347 records, and the file hash matched the index. The final configuration used a fixed one-second delay and the strict robots middleware. This was a bounded run, not a rate or reliability benchmark. Genuine retailer data and logs remain local and ignored by Git.

Synthetic checks verify that the strict robots middleware denies requests when robots.txt retrieval returns HTTP 403 or fails. Scrapy can still exit with code zero after early spider closure, and durable failure manifests remain pending. PULSE-14 and the phase closeout are not complete.

## Phase 1 PULSE-12 — 2026-11-19

The owner authorized Phase 1 and PULSE-12 on 2026-11-19. Synthetic pytest checks passed: **4 tests**, covering both encodings and delimiters, regular/special/equal/conflicting and invalid prices, GTIN validation, unknown headers, store/date selection and URL restriction. Fixtures are synthetic and do not redistribute retailer products.

Bounded live Scrapy runs on 2026-11-19 (local time) requested the 2026-11-17 file for each selected store. Both returned HTTP 200 and emitted manifests: SPAR 8702 **32,347** rows and Kaufland 5630 **23,593** rows. SPAR's downloaded SHA-256 matched its index. An initial SPAR run identified 286 prices written with a leading comma; after supporting that form and repeating the run, all rows in both samples had usable prices under the current rules. This is a parser observation, not independent verification of all prices or product identities.

**Pending:** broader dates and schema drift, durable failure manifests and exit signaling, operational retry and scheduling reliability, independent data quality review, PostgreSQL and Tableau. No phase closeout or publication rights are implied. Real output remains local and ignored by Git.

## Status

**Phase 0 formally CLOSED by explicit owner approval on 2026-11-19**, based on bounded user-local technical feasibility evidence dated 2026-11-18. The pair is **SPAR Croatia / store 8702** and **Kaufland Croatia / store 5630**. The initial matching gate is **102 descriptor-consistent product pairs from 160 reviewed strict candidates**, with 58 unresolved. This is **not** external manufacturer/GS1 identity certification, production reliability evidence, permission to redistribute real data, or evidence of Phase 1 implementation.

## Owner closeout decision (2026-11-19)

**Approved:** formal closure of **Phase 0 — Project Definition and Source Feasibility** for SPAR Croatia (Zagreb Jankomir, store 8702) and Kaufland Croatia (Zagreb Antuna Šoljana, store 5630). The approved evidence scope is bounded Scrapy access, four fixed-store/date CSV snapshots, observed price-field behavior, and **102 description-consistent pairs among 160 prefiltered pairs reviewed**. The owner authorized updating GitHub documentation and Jira.

**Limitations retained:** 58 unresolved product-identity pairs; no external manufacturer/GS1 validation or production reliability proof; no PostgreSQL ingest or Tableau workbook; no inferred stock availability or rights to publicly redistribute source observations. Phase 1 was separately authorized later on 2026-11-19.

## Evidence ledger

| Area | Result | Basis / limitation |
| --- | --- | --- |
| Official source publications | CONFIRMED AS PUBLISHED | Kaufland Croatia and SPAR Croatia public price-list pages consulted on 2026-11-18 |
| Machine-readable legal framework | CONFIRMED BY OFFICIAL TEXT | NN 132/2026-1584, effective 2026-11-17: automated tools supported; CSV/XML; UTF-8; semicolon; archive 15 days |
| Historical overlap potential | SECONDARY HISTORICAL EVIDENCE | 2025-05-21 third-party analysis: 583 barcodes common across seven chains, 4,126 across six excluding Lidl; not a November 2026 direct pair count |
| Kaufland robots + Scrapy access | PARTIAL PASS — 2026-11-18 user-local run | HTML index 200, assets JSON index 200, one 2026-11-17 Zagreb CSV 200; direct parsed rows 23,593; 23,238 usable product rows. Current-day 2026-11-18 filename match returned zero in index. |
| SPAR robots + Scrapy access | PARTIAL PASS — 2026-11-18 user-local run | JSON indexes 200 on 2026-11-17 and 2026-11-18, each advertising 144 files; three CSV downloads 200, parsed successfully. |
| Current Kaufland–SPAR GTIN intersection | **8,869** priced shared codes (2026-11-17) | **7,772** present in both stores across two days; **4,155** strict candidates; **102/160** review-consistent on available descriptions; not an independent manufacturer/GTIN product registry check. |
| Current schema and parser accuracy | INITIAL PRICE RULE SUPPORTED | SPAR: cp1250/semicolon, only regular-only or special-only prices; Kaufland: UTF-8 BOM/tab, regular-only or dual-equal. No dual-different prices in four files; future cases must be flagged. |
| Repeatability and history | INITIAL TWO-DATE PASS | Same SPAR store 8702 and Kaufland store 5630 across 2026-11-16 and 2026-11-17; promotion-aware stable cohorts 31,277 and 15,533 respectively. Only two days observed. |
| Source reuse and Tableau publication | REAL-DATA PUBLICATION ON HOLD | SPAR website terms restrict reproduction/distribution; NN 132/2026 automated-access text does not imply a general redistribution license. A clearly labeled synthetic Tableau Public demonstration is the default unless legal sharing basis is verified. |
| PostgreSQL and Tableau | NOT IMPLEMENTED | No database pipeline or dashboards |

## Initial grocery acquisition probe — user-local evidence (2026-11-18)

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
- **Initial-probe limitation, subsequently resolved:** this first probe tried a 2026-11-18 intersection while Kaufland's label filter selected no file. The later same-store 2026-11-17 probe successfully measured cross-retailer overlap; see the dated sections below.
- Source files were processed transiently; the log does not include full product rows and cannot itself support a barcode intersection computation.

## Intermediate same-date intersection — user-local log, 2026-11-18

The user executed the bounded second Phase 0 probe with main date **2026-11-17** and previous date **2026-11-16**. Observations:

- SPAR and Kaufland indexes responded HTTP 200; SPAR 144 published store lists per date; Kaufland 53 lists on each of the chosen dates.
- Six official CSV files selected and downloaded HTTP 200 (SPAR: three; Kaufland: three), across 2026-11-16 and 2026-11-17.
- **8,263 checksum-valid normalized EANs with parseable positive retail prices** overlapped between SPAR Jankomir (store ID 8702) and Kaufland Zagreb Antuna Šoljana 43 (store ID 5630) on 2026-11-17. This is an initial exact-code overlap, **not a full same-variant/manual matching validation**.
- The randomly selected 30-row sample includes at least one apparent package discrepancy: Garnier product **250 ml at SPAR** versus **200 ml at Kaufland** with the same normalized code. Other records warrant unit/brand review. Price differences cannot yet be treated as reliable like-for-like comparisons without row checks.
- The previous-date SPAR sample and current-date SPAR sample were not necessarily the **same store**, so same-store price trends remain **unvalidated**. Same-store 2026-11-16 and 2026-11-17 downloads must be selected explicitly.
- SPAR initial parser rejected approximately 9–11% of retail-price values across sampled files; no cause analysis is yet supported. Actual source values and special-price semantics must be investigated.
- CSV format evidence: SPAR `cp1250` + semicolon; Kaufland `utf-8-sig` + tab. Source-specific parser contracts must preserve these actual observations rather than assume uniform CSV dialect.
- **Historical checkpoint (now superseded):** at this intermediate test stage the sample had not yet been audited. The final review below establishes same-store history, a bounded price rule, and 102 descriptor-consistent cases. **Formal owner closeout was subsequently approved on 2026-11-19**.

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

**Historical next-gate note (superseded on 2026-11-19):** the final 160-pair review established 102 descriptor-consistent matches and 58 unresolved pairs. The owner approved bounded Phase 0 closeout while retaining identity exceptions, unusual price cases and public sharing restrictions as downstream controls.

## Final Phase 0 price and product-description audit — 2026-11-18

**Evidence:** user-uploaded `pricepulse_phase0_final_audit_result.txt`, reporting actual local bounded Scrapy downloads. The 160-product manual descriptor adjudication is held as a **private non-repository file**, to avoid public distribution of raw retailer titles, identifiers or prices.

| Measure | Count | Interpretation |
| --- | ---: | --- |
| Same-date retailer GTINs with initially usable prices, 2026-11-17 | **8,869** | Counts with SPAR special-only prices included |
| GTINs present in both chosen stores across 2026-11-16 and 2026-11-17 | **7,772** | Four-file overlap, not full product verification |
| Strict algorithmic candidates | **4,155** | Matching brand text, extracted packaging and four-file stability |
| Deterministic candidate sample manually reviewed from source descriptions | **160** | Sample is prefiltered, not random across all retailer items |
| Descriptions judged consistent for product and pack | **102** | Conservative text-based evidence, not manufacturer/GS1 authentication |
| Unresolved due to unit conflicts or ambiguous variants | **58** | Retained as exceptions; do not publish as confirmed like-for-like |

**Initial >=100 matching gate:** satisfied **at descriptor-consistency level only** by the 102 cases. Do not extrapolate their observed agreement rate to the full catalog. The 58 unresolved cases are not automatically false matches; many result from incomparable source quantity fields. Two canned-product examples were judged consistent using gross-versus-drained-weight semantics.

### Price fields across four downloaded CSV files

| Chain and date | Regular-only | Special-only | Both equal | Both different | Neither |
| --- | ---: | ---: | ---: | ---: | ---: |
| SPAR 2026-11-16 | 29,231 | 3,091 | 0 | 0 | 0 |
| SPAR 2026-11-17 | 29,244 | 3,103 | 0 | 0 | 0 |
| Kaufland 2026-11-16 | 14,939 | 0 | 1,014 | 0 | 0 |
| Kaufland 2026-11-17 | 21,995 | 0 | 1,598 | 0 | 0 |

**Observed price selection:** regular-only → regular; special-only → special; both equal → preserve both origins and use same numeric amount; both different → flag for review, not silently resolve. Keep the original two price fields and their provenance. These rules are supported by **four sampled files**, not yet by a production pipeline.

### Two-day promotion-aware comparison

| Chain/store | Code-stable products | Price rises | Price decreases | Unchanged |
| --- | ---: | ---: | ---: | ---: |
| SPAR Jankomir 8702 | **31,277** | 14 | 54 | 31,209 |
| Kaufland Zagreb 5630 | **15,533** | 9 | 69 | 15,455 |

**Quality caveats:** The unusual +47.9% Kaufland row-count change across the regulation transition is a source coverage issue to monitor. SPAR files used cp1250 and semicolon, Kaufland UTF-8 BOM and tab; never assume homogeneous CSV dialects. Published presence is not inventory availability. Site publication rights constrain releasing real retailer source extracts; use a synthetic public portfolio demo unless sharing rights are verified.

**Status:** Technical source feasibility supported; **Phase 0 formally closed by owner approval on 2026-11-19. Phase 1 was separately authorized later on 2026-11-19.**

## Earlier source exploration — user-reported local logs, 2026-11-18

These tests concerned an **abandoned musical-instruments source category** and do not validate the new pair.

- Andertons: three separate Scrapy product requests HTTP 200; JSON-LD product fields for Boss, Ibanez and Lee Oskar including product SKU, GBP price, brand and availability.
- Gear4music: product HTTP 403 with human-verification page.
- Bonners Music: product HTTP 429 rate-limit response.
- GigGear: robots and product HTTP 405 with human verification / AWS WAF CAPTCHA.
- guitarguitar: contractual automated price collection restriction noted in feasibility review.

These results were supplied in the conversation by the user, not independently replayed in CI.

## Phase 0 closeout evidence and remaining limits

**Pass, within tested scope:** (1) official index and store file retrieval under Scrapy with robots obedience; (2) actual per-chain file parsing and prices; (3) two-day same-store history; (4) more than 100 conservative descriptor-consistent cross-retailer pairs from a reproducibly sampled, prefiltered cohort; (5) documented source terms and constrained public release policy.

**Not tested or authorized:** continuous scheduling/retry reliability; end-to-end PostgreSQL idempotency; external manufacturer/GS1 resolution for the 58 unresolved pairs; full-catalog matching precision; ambiguous dual-different source prices; data publication rights; Tableau workbook. **Phase 0 formally closed on 2026-11-19; Phase 1 was subsequently authorized and is in progress.**

**Evidence provenance:** the original CSV data were downloaded and processed during user-executed temporary Scrapy feasibility scripts. Audit logs were supplied in conversation; source-row detail and private 160-item review notes are **not committed to this repository**, avoiding unnecessary public exposure or redistribution.

## Documentation checks

Earlier GitHub documentation review (baseline `861062303de56dfa39199e07f50dc287bc0952cb`, 2026-11-14): 12/12 Markdown documents fetched, 38 relative links checked with no unresolved links. **That result applies only to the cited baseline**, not the current revisions; new links still require verification.


### Current documentation revision check — 2026-11-18

- **Baseline:** commit `02465fd1b426821797feb8c352105fce15f2836d` (Phase 0 grocery scope revision).
- **Method:** retrieved the ten changed Markdown documents through the GitHub connector; checked the existence of local relative Markdown link targets in the revised document inventory.
- **Observed:** 10 of 10 documents retrieved; 52 local relative link targets found and checked; zero unresolved file paths.
- **Limitations:** heading-anchor links, external URLs, Markdown rendering, live price-list requests and runtime behavior were not checked by this documentation test. This is not a Phase 0 source-access pass.

## Public-release boundary reviewed on 2026-11-18

- [SPAR's general terms, section 2.1](https://www.spar.hr/o-nama/opci-uvjeti-koristenja) describe website content, including data, as covered and limit use to personal information; they require prior written permission for modification, reproduction, distribution or incorporation into other sites or media.
- [Croatian regulation NN 132/2026, article 5](https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html) requires technical accessibility to automated collection; it does not directly grant unrestricted republication rights.
- Engineering conclusion: **do not publish the genuine price-list files or a real-data Tableau Public extract without an independently verified sharing basis**. A synthetic public showcase can demonstrate the pipeline and dashboard design without copying source data. This is a publication constraint, **not** a reason to cancel bounded local source feasibility checks.

## Sources referenced during Phase 0

- Regulation: https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1584.html
- Revocation of earlier 2025 requirements: https://narodne-novine.nn.hr/clanci/sluzbeni/2026_11_132_1578.html
- Kaufland: https://www.kaufland.hr/akcije-novosti/popis-mpc.html
- SPAR: https://www.spar.hr/usluge/cjenici
- Historical third-party cross-chain study: https://analiza.usporedicijene.info/
- Independent project reference (not our implementation): https://github.com/senko/cijene-api

# Validation and evidence

## Status

**Phase 0: IN PROGRESS.** Evidence exists for the earlier retailer feasibility exploration and public-source research; **no live Kaufland/SPAR Scrapy or paired-file overlap test has passed yet**.

## Evidence ledger

| Area | Result | Basis / limitation |
| --- | --- | --- |
| Official source publications | CONFIRMED AS PUBLISHED | Kaufland Croatia and SPAR Croatia public price-list pages consulted on 2026-11-18 |
| Machine-readable legal framework | CONFIRMED BY OFFICIAL TEXT | NN 132/2026-1584, effective 2026-11-17: automated tools supported; CSV/XML; UTF-8; semicolon; archive 15 days |
| Historical overlap potential | SECONDARY HISTORICAL EVIDENCE | 2025-05-21 third-party analysis: 583 barcodes common across seven chains, 4,126 across six excluding Lidl; not a November 2026 direct pair count |
| Kaufland robots + Scrapy access | PARTIAL PASS — 2026-11-18 user-local run | HTML index 200, assets JSON index 200, one 2026-11-17 Zagreb CSV 200; direct parsed rows 23,593; 23,238 usable product rows. Current-day 2026-11-18 filename match returned zero in index. |
| SPAR robots + Scrapy access | PARTIAL PASS — 2026-11-18 user-local run | JSON indexes 200 on 2026-11-17 and 2026-11-18, each advertising 144 files; three CSV downloads 200, parsed successfully. |
| Current Kaufland–SPAR GTIN intersection | NOT MEASURED | Must count from same-date official files |
| Current schema and parser accuracy | INITIAL PARSE PASS; SEMANTIC VALIDATION PENDING | SPAR: cp1250, semicolon; Kaufland: utf-8-sig, tab. EAN checksums and prices parsed in four CSVs; malformed/blank price values and unexpected headers still need review. |
| Repeatability and history | PARTIAL | Separate publication dates retrieved for SPAR, plus Kaufland 2026-11-17. Same-store two-date comparisons and current-date Kaufland availability still unverified. |
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

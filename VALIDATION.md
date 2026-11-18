# Validation and evidence

## Status

**Phase 0: IN PROGRESS.** Evidence exists for the earlier retailer feasibility exploration and public-source research; **no live Kaufland/SPAR Scrapy or paired-file overlap test has passed yet**.

## Evidence ledger

| Area | Result | Basis / limitation |
| --- | --- | --- |
| Official source publications | CONFIRMED AS PUBLISHED | Kaufland Croatia and SPAR Croatia public price-list pages consulted on 2026-11-18 |
| Machine-readable legal framework | CONFIRMED BY OFFICIAL TEXT | NN 132/2026-1584, effective 2026-11-17: automated tools supported; CSV/XML; UTF-8; semicolon; archive 15 days |
| Historical overlap potential | SECONDARY HISTORICAL EVIDENCE | 2025-05-21 third-party analysis: 583 barcodes common across seven chains, 4,126 across six excluding Lidl; not a November 2026 direct pair count |
| Kaufland robots + Scrapy access | NOT TESTED | Browser-readable page is not proof of direct Scrapy/CSV access |
| SPAR robots + Scrapy access | NOT TESTED | Direct index URL described by third-party code, not independently validated |
| Current Kaufland–SPAR GTIN intersection | NOT MEASURED | Must count from same-date official files |
| Current schema and parser accuracy | NOT TESTED | Live representative CSV/XML samples not downloaded and checked |
| Repeatability and history | NOT TESTED | No dated snapshots or local acquisition runs |
| Source reuse and Tableau publication | UNRESOLVED | Automated retrieval support does not imply an unrestricted redistribution license |
| PostgreSQL, automated tests, Tableau | NOT IMPLEMENTED | No runtime or dashboards |

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

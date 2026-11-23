# Validation and evidence

## Phase 5 Docker Compose validation — 2026-11-23

Docker Compose v5.7.1 with Docker Engine 29.9.3 started the PostgreSQL 18.7 development and test services. Both passed their readiness checks and accepted connections on their separate loopback ports. The application initialized its development schema and the schema was absent from the test database. All **65 tests passed**, including PostgreSQL integration tests, with `PRICEPULSE_TEST_DSN` pointed at the Compose test service.

After `docker compose down` and recreation, the development schema persisted in its named volume and a test-only probe table disappeared. Removing just `db-test` left the development database reachable. A separate Compose project started only `db-test` without development credentials. Both validation projects were removed with their test resources. See the [Docker Compose setup](POSTGRESQL.md#local-postgresql-with-docker-compose).

## Phase 5 reproducible setup — 2026-11-23

A fresh Windows virtual environment created with `uv sync --locked --python 3.12` loaded Python 3.12.16 and Scrapy 2.20.0. The full suite passed **65 tests**, including the PostgreSQL integration tests, against a disposable PostgreSQL 18.7 cluster. The suite covers malformed inputs, immutable file replay, explicit matching and export version selection.

The initial test run discovered dependency tests in a project-local cache. The repository now limits pytest discovery to `tests/`. The documented default command passed after that change. The PostgreSQL-backed synthetic generator produced four CSVs byte-identical to the tracked fixture files.

### Manual real-source capture

```powershell
uv run --locked python -m pricepulse.batch --date 2026-11-23 --directory data/phase5-private/live
```

The bounded manual run returned `success` for both stores. The raw SHA-256 matched the successful run report and the archived 23 November version for SPAR 8702 (32,410 rows) and Kaufland 5630 (23,830 rows). This verifies manual collection of the fixed baseline. Normal execution through the permanent scheduled task remains a Phase 3 check.

### Private replay

An isolated PostgreSQL schema replayed the four archived captures for 17 and 23 November. Before each load, the run report, feed manifest, raw SHA-256 and independently counted CSV rows agreed. PostgreSQL preserved 112,180 source rows. Reloading the same bytes created another acquisition record per file, while retaining four file versions and the original price observations. The replay used the existing ingestion, candidate review and analytical export functions. The local harness and results are under ignored `data/phase5-private/`.

### Tableau reconciliation

The fresh SQL export reconciled with the packaged workbook for **112,170 price observations**, **17,803 same-store SKU comparisons**, four price-list quality records and all four approved cross-store pairs. The checks compared catalog rows by store/date/SKU, grouped coverage and change counts, and eight price marks and four gaps in the comparison dashboard. Both original CSV prices were checked for each approved pair. Only the prior approvals for the exact November 17 file versions were replayed.

The focused workbook source uses a reviewed-product label in a column originally named `left_sku`. The reconciliation uses the original SQL SKU to locate raw source rows and uses the label for display values. Price differences are compared numerically, and store names are normalized for case. This pass verified the workbook's embedded data. Interactive filter behavior was exercised in Desktop during Phase 4.

## Phase 4 private real Tableau review — 2026-11-23

The synthetic PostgreSQL fixture regenerated four CSVs that matched the workbook's synthetic inputs byte for byte. The full local suite passed 65 tests with PostgreSQL. This served as a control while developing the local workbook.

The private real export verified four archived capture hashes and reconciled source row counts. PostgreSQL exported 112,170 price observations, 17,803 eligible same-store changes, four verified pair comparisons and four file-quality rows for the selected dates and versions. The focused Tableau workbook narrows price history and changes to the four owner-reviewed product pairs. Live Tableau query readback agreed with the exported values for 16 price observations, four comparisons, four qualifying changes and four records in each of the three quality worksheets. In a separate workbook copy, a store, product and date filter intersection returned one expected history record. The dashboard image was rendered and inspected. The cross-store comparisons apply to 17 November only. The workbook and exports remain local.

After owner feedback, the opening dashboard was replaced in a new private workbook with two Spanish tables that state the cheaper retailer and price gap, and show changes within SPAR separately. All 28 visible table values matched the SQL-derived inputs in Tableau readback. The rendered dashboard was inspected after shortening labels, with all four product names and pack sizes visible.

A subsequent private portfolio version presents the same verified cohort with comparative bars, summary indicators and a promotion callout. Tableau readback reconciled all eight price marks and four gap marks to the exported data. The filter action from the price chart to the gap chart was verified in Tableau metadata and in the saved package. A click-through test was not performed. The rendered 1240 by 790 image was inspected. The packaged workbook contains eight CSV sources with package-relative connections. Both outputs remain private pending a verified basis for public reuse.

### Expanded catalog and live interaction

The first click-through test found that the source chart highlighted the selected product without filtering the gap chart. The filter expression was corrected to use the gap chart's data source for the target field. In the expanded workbook, clicking the Dessert Chef price mark displayed only its gap. Clicking away restored the four approved pairs.

The expanded private Tableau workbook exposes 112,170 listed-price observations and 17,803 same-store SKU comparisons, including unchanged prices. Readback from the four catalog coverage marks and six same-store change summary marks matched the private exports. Both detail worksheets returned data in Tableau.

| File date | Shared priced GTINs | Eligible cross-store pairs | Approved comparisons | Pending with brand and mass agreement and only a descriptor flag |
| --- | ---: | ---: | ---: | ---: |
| 2026-11-17 | 8,869 | 6,418 | 4 | 2,096 |
| 2026-11-23 | 8,854 | 6,405 | 0 | 2,097 |

The remaining candidates have additional flags or unavailable comparable mass. Counts are per date and file version. The private audit used read-only SQL and did not create approval decisions. The workbook exposes the expanded observations and same-store history separately from approved cross-store pricing.

### English portfolio review

The private portfolio workbook uses English for dashboard copy, sheet names, field captions and presentation labels. Source product titles are preserved in the catalog. Tableau Desktop readback returned the expected eight price marks, four gap marks, four catalog coverage marks and six same-store change summary marks. Selecting a product showed one gap and clearing the selection restored all four. All 65 local repository tests passed with PostgreSQL.

### Private workbook closeout

The packaged workbook passed ZIP integrity checks. Its workbook definition contains one English comparison dashboard, 14 worksheets and one filter action. The 12 packaged CSV sources include 112,170 catalog observations, 17,803 same-store SKU comparisons, eight price marks and four cross-store gaps. The private screenshot measures 1240 × 790 pixels. Phase 4 closed for the private snapshot on 2026-11-23 at the owner's direction. Candidate review, automatic refresh and public delivery remain open. See [Tableau analytics](TABLEAU.md).

## Phase 3 owner review evidence — 2026-11-23

The local collection-only daily marker records a real attempt for 2026-11-23 at 11:35 Bogotá time. The batch took about 21 seconds and was marked incomplete. SPAR 8702 captured 32,410 rows with zero reported price exceptions and 97.68% checksum-valid GTINs. There was no prior successful SPAR file in the scheduled directory for the row-count comparison.

Kaufland 5630 recorded three HTTP 200 responses and zero assets selected by the store/date filter. A separate bounded manual attempt at 13:14 Bogotá time repeated that result and exited with code 1. Neither attempt establishes whether the file was absent from the index or present under a label the filter missed. The first batch and the manual attempt have separate private evidence.

The Windows task was enabled, interactive only, and its last observed tick at 12:20 Bogotá time returned code 1. The operational history was disabled, so the 11:35 capture cannot be attributed to the normal hourly trigger. The daily marker retained the incomplete outcome for subsequent ticks. The focused reliability and scheduling test suite passed 38 tests.

### Kaufland filename change and manual recovery

At 13:19 Bogotá time, an index-only Scrapy probe received three HTTP 200 responses and downloaded no price-list files. The index contained 2,544 entries. Store 5630 had exactly one new-format entry for 2026-11-23. The old filter selected none for that date and still selected one for 2026-11-17. The new filename puts a price-list descriptor between the store ID and the date and uses `YYYYMMDD` instead of `DDMMYYYY`.

The collector now accepts both observed filename formats and still requires exactly one match for the requested store and date. A manual recovery at 13:20 downloaded and validated the 2026-11-23 file with 23,830 rows and a verified raw hash. The original daily marker remains incomplete, and recovery evidence is stored separately. The offline suite passed 53 tests, with 11 PostgreSQL integration tests skipped because no test database was configured for this run. Normal daily capture through the registered task and missed-run behavior remain unverified. Phase 3 remains open.

### Timed Windows collection and controlled missed-tick check

At 13:25 Bogotá time on 2026-11-23, a temporary Windows scheduled task started at its defined trigger time without manual launch. It ran the normal collection-only entry point in a separate private directory. The task returned code 0 and the batch succeeded for SPAR (32,410 rows) and Kaufland (23,830 rows). The permanent task's incomplete marker retained the same hash, and the temporary task was removed. This confirms one timed live collection with the corrected code. The permanent task's next eligible date is 2026-11-24.

Using a controlled clock and a synthetic batch, the scheduler logic collected once when the first eligible tick was missed and a later tick occurred on the same Zagreb date. When every tick for the following date was missed, the next eligible tick collected only the new date and created no backfill marker. The nine focused scheduling tests passed. This check exercises application behavior when ticks are absent. It does not measure Windows resume or logon behavior after a real interruption.

## Phase 2 private real-file review — 2026-11-23

An isolated local PostgreSQL instance loaded previously collected private SPAR 8702 and Kaufland 5630 files dated 2026-11-17. The successful crawl report, feed summary and raw SHA-256 agreed for each file. An independent CSV reader counted raw rows; these counts matched loaded source rows. Replaying each file retained the same file version and observation counts while recording another acquisition run. The server was stopped after the review; its private database and a 20-pair sample remain under ignored `data/`.

| Source | Raw and loaded rows | Price observations | Rows with review exceptions |
| --- | ---: | ---: | ---: |
| SPAR | 32,347 | 32,347 | 15,231 |
| Kaufland | 23,593 | 23,591 | 378 |

SPAR observations include 3,103 special-only prices. Its exceptions include 15,127 missing-brand rows and 213 invalid-GTIN rows; categories can overlap. Kaufland has two duplicate-SKU rows without price observations, 355 invalid-GTIN rows and 35 missing-brand rows. The exact-GTIN queue produced 6,418 exception-free candidates; none was automatically verified. A deterministic 20-pair sample is prepared for human review but has not yet been adjudicated.

This checks two historical files and replay behavior, not daily operation, independent reconciliation of every price, same-store changes across dates, or product identity. No real retailer records were published.

### Cross-retailer quantity reassessment

The initial literal quantity and unit comparison flagged all 6,418 candidates. The owner identified examples involving decimal formatting and unrelated measurement dimensions. The revised check uses the declared mass from each source when both provide one. The same 6,418 pairs were regenerated in temporary review tables and compared by exact file and row keys. Repeating the queue added no entries and all regenerated decisions were pending.

| Result | Candidate pairs |
| --- | ---: |
| Same declared mass after exact normalization | 3,121 |
| Different declared masses requiring review | 190 |
| Declared quantities not comparable as mass | 3,107 |

The unrelated brand and title checks still flagged 1,804 and 6,386 pairs respectively, with overlapping flags. These checks prioritize human review and do not measure match accuracy. A private Spanish guide explains the same 20 examples. The reassessment covered one file date and left the original review records intact. All 63 local tests passed with a disposable PostgreSQL instance.

Four sample pairs were corroborated with external product references and both source barcodes. A separate read-only check reconciled all eight sample prices and their origins between the original CSVs and PostgreSQL, using the exact file hashes to select observations.

On 2026-11-23, the owner approved these four pairs. The private database recorded one verification event per pair. The verified comparison view returned exactly those four pairs, and their prices and differences agreed with the source reconciliation. The other 6,414 candidates remain queued. This check covers the selected file versions on one date. The owner separately approved formal Phase 2 closeout on 2026-11-23 with this bounded scope. Additional pairs remain eligible for later review. The closeout does not establish catalogue-wide match accuracy, multi-day real ingestion, or operational reliability.

## Phase 2 and 3 technical review — 2026-11-23

The repository at `1d73f3dfb1c6675af1411c0e666c89054667f357`, Jira acceptance criteria, Phase 2 SQL and ingestion, and Phase 3 scheduling and recovery were reviewed. The full local suite passed **62 tests** with a temporary PostgreSQL instance, stopped after the run. The [hosted CI run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45125414064) for that commit succeeded. This is an agent review of work produced in this project, not independent human review.

- **Phase 2:** synthetic integration tests cover idempotent replay, file versions, exceptions, reviewed comparisons and selected-file price changes. Actual retailer CSV ingestion, reconciliation against real source files and independent review of real matching decisions remain untested. Without those checks, the synthetic pass does not establish a real-data dashboard.
- **Phase 3:** the permanent collection-only Windows task was observed after its 01:20 Bogotá tick with last result zero; it was before the 12:15 Zagreb due time. A separate accelerated recurring task previously produced two successful historical batches. Neither observation demonstrates a normal due-time daily capture, missed-run behavior or multi-day reliability. Synthetic recovery tests and provisional alerts are not live operational evidence.

At this technical review checkpoint, both epics were in Jira **In Review** and awaited owner closeout. The owner subsequently closed Phase 2 and its epic [PULSE-3](https://angel231995.atlassian.net/browse/PULSE-3) moved to **Done**. Phase 3 remains open. The existing local task does not ingest into PostgreSQL. A persistent private database and explicit real-data ingestion are separate operational choices.

## Phase 4 initial analytical export — 2026-11-23

The owner authorized Phase 4 before reviewing Phases 2 and 3. A private CSV export for explicitly selected PostgreSQL file versions was tested with synthetic observations: a verified comparison reconciled to -0.20 EUR, file age to one day, and conflicting versions were rejected before CSV output. The full local suite passed 62 tests using a temporary PostgreSQL instance, which was stopped afterward. Fictional CSV exports contained 24 observations, 16 changes, 12 comparisons and six quality records; the synthetic comparison spread was -0.10 EUR. Tableau Desktop Free loaded 24 rows and displayed a preliminary local dashboard with history and 12 differences of -0.10 EUR, consistent with the fictional SQL export. Other measures and filters and a shareable demo remain incomplete. The [hosted CI run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45125129520) for commit `83dd010fa0da32579eec0d1db90266d248eaafee` succeeded. See [Tableau analytics](TABLEAU.md).

## Phase 3 authorization — 2026-11-22

The owner authorized starting Phase 3 before reviewing Phases 2 and 3. Neither phase was formally closed by that instruction.

## Phase 3 initial reliability validation — 2026-11-22

The full local suite passed **47 tests**, including PostgreSQL integration tests against a temporary PostgreSQL 18.7 server, which was stopped after testing. Synthetic tests covered successful feed inspection, mismatched and incomplete feeds, simulated 403/429/schema failure, process timeout, caught interruption, distinct rerun evidence, explicit quality thresholds and winter/summer Zagreb schedule calculations. Simulated failures are not live retailer responses.

A bounded live run of the new wrapper on 2026-11-22 retrieved SPAR 8702 for 2026-11-17 and reported success with **32,347 rows**, **32,347 usable price rows**, **31,597 checksum-valid GTIN rows**, zero price exceptions and a SHA-256 matching the Phase 1 observed value. This is one manual run; it is not a recurring-run or reliability baseline. The report, log and source records remain private under ignored `data/`.

Schedule planning was dry-run for 12:15 Europe/Zagreb: 2026-11-22 maps to 11:15 UTC, and 2026-06-22 maps to 10:15 UTC. No scheduler was configured. Live-source ingestion recovery, recurring runs, alert thresholds, extended CI evidence and long-term reliability remain pending. Neither Phase 2 nor Phase 3 is closed.

Subsequently, the wrapper was extended to preserve a private raw CSV and verify its SHA-256, and explicit PostgreSQL ingestion recovery was added. A synthetic test simulated interruption immediately after database commit, then replayed without duplicating the price observation and rejected a tampered raw file. The complete local suite passed **48 tests** with the temporary PostgreSQL server stopped afterwards. A separate bounded SPAR 8702 acquisition for 2026-11-17 succeeded with raw-file hash verification; no real source data were ingested into PostgreSQL. Hosted CI was verified at the later checkpoint below.

The initial two-store batch subsequently passed **52 local tests** with the same temporary PostgreSQL setup. Synthetic tests exercised partial-store coverage, missing output, overlap locking, two-store ingestion and replay without duplicated observations. The [GitHub-hosted run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45089383487) for `0a5528dc1158358b274e8c1f18acd9f3009fe2c1` also passed **52 tests** with temporary PostgreSQL. On 2026-11-22, two manually invoked collection-only batches each succeeded for the same historical date, 2026-11-17: SPAR 32,347 rows and Kaufland 23,593 rows in each run; file hashes matched between repetitions. This is a two-run same-date observation, not evidence of recurring daily scheduling or long-term reliability. No real-source PostgreSQL ingestion was performed.

An additional local aggregation of those two selected batch reports found **2/2 complete**, with durations about **35.0 and 31.8 seconds**. Reinspection of one feed per source counted SPAR 29,244 regular-only and 3,103 special-only prices, and Kaufland 21,995 regular-only and 1,598 equal dual-price entries. These counts are limited to the historical files and selected reports; no broader reliability inference is supported. After adding aggregate calculations, **53 tests passed locally** with the temporary PostgreSQL server and in the [GitHub-hosted run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45089822428) for `86fb5d6b6f15550de674c17d417c35f7b08cd8c6`.

On 2026-11-23, a further bounded collection-only batch for the same 2026-11-17 files succeeded. SPAR's date-specific index contained **144 entries**, with one selected and fetched file; Kaufland's multi-date index contained **2,490 entries**, with one selected and fetched file. These index totals have different scopes and are not product coverage. Synthetic PostgreSQL tests also checked reviewed-pair coverage with its queued-pair denominator; no real pair coverage was measured. The expanded suite passed **55 local tests** with temporary PostgreSQL and in the [GitHub-hosted run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45120773613) for `016e39b9b05e11b3b51725e4f5fde47f6fab3eca`.

An additional collection-only scheduling tick has synthetic tests for the Zagreb due time, at-most-one daily attempt, incomplete and failed batches and pre-run disk soft limit. The local suite passed **59 tests** with temporary PostgreSQL, and the [GitHub-hosted run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45121170894) for `77f2918b631e1d97b4f10de4a17b0655d5f218bd` passed **58 tests** before the additional failure-marker check. The PowerShell scripts parsed without syntax errors.

On 2026-11-23, the local Windows task `PricePulse-Local-Collect` was registered for the current interactive user with an hourly tick, overlap suppression and a 12:15 Zagreb due-time guard. Inspection showed it ready and the next tick at 01:20 Bogotá time. A manual pre-due invocation returned task result zero and produced no scheduled data output. This verifies registration and the pre-due path only: no automatic tick, live scheduled capture, missed-run recovery or long-term reliability has yet been observed. The task collects locally without database ingestion and applies the documented pre-run 1 GiB soft limit.

## Phase 1 closeout and Phase 2 authorization — 2026-11-22

The owner explicitly approved formal Phase 1 closeout and authorized continuing with Phase 2 on 2026-11-22. The decision accepts the bounded two-source acquisition and synthetic/hosted CI evidence recorded below; it does not establish continuous production reliability or rights to publish real retailer data.

## Phase 2 initial PostgreSQL validation — 2026-11-22

The initial schema and loader were tested against an isolated local PostgreSQL 18.7 cluster using synthetic rows. The full suite passed **38 tests**, including eight PostgreSQL integration tests for replay, changed file versions, relational constraints, duplicate GTINs, source-price exceptions, candidate review, two manually reviewed version-specific comparison pairs and independently calculated synthetic price-change counts. The temporary server was stopped after the run. The [GitHub-hosted run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45086760840) for `e7c17cba822019b1a67d11345cab6a1881a6fad1` passed **38 tests** with a temporary PostgreSQL service. The source inputs, expected prices and comparisons were synthetic; no real-data ingestion, independent human identity review, operational load or production reliability was established.

## Phase 1 PULSE-14 and PULSE-44 — local checks (2026-11-22)

The offline suite passed **29 tests** with `uv run --locked python -m pytest -q`. Synthetic tests cover both source dialects, price origins including absent and conflicting prices, invalid GTINs, duplicate or missing headers, malformed records and CSV syntax, extra columns, date/store provenance, SHA-256 verification, source failures and request policies. A malformed quoted CSV previously raised an unclassified `csv.Error`; the spider now closes with `schema_error` before emitting a manifest.

PULSE-44 adds a GitHub Actions workflow for push and pull requests using locked dependencies and offline synthetic tests. The [GitHub-hosted run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45083828028) for commit `a7831bae119096518555e8b15b5f4d6fa3ae61d4` succeeded on 2026-11-22: **29 tests passed** on Ubuntu. The workflow does not access retailer sites, schedule acquisition, deploy, or publish source data. This result does not establish live access or production reliability.

## Phase 1 PULSE-13 — 2026-11-22

The offline suite passed **21 tests**. Request-policy tests exercise robots rules, settings for concurrency, delay and timeout, domain restrictions, retry limits, HTTP 403/404/429 classification, malformed indexes, bounded selection and incomplete file responses. HTTP and transport failures were simulated; the checks do not establish production reliability.

A bounded SPAR 8702 run on 2026-11-22 requested the 2026-11-17 file. Scrapy recorded **3 GET requests and 3 HTTP 200 responses**, including one successful robots.txt request, the dated index and the selected CSV; no retries were recorded. It finished normally, emitted one manifest and 32,347 records, and the file hash matched the index. The final configuration used a fixed one-second delay and the strict robots middleware. This was a bounded run, not a rate or reliability benchmark. Genuine retailer data and logs remain local and ignored by Git.

Synthetic checks verify that the strict robots middleware denies requests when robots.txt retrieval returns HTTP 403 or fails. Scrapy can still exit with code zero after early spider closure, and durable failure manifests remain pending. At this PULSE-13 checkpoint, PULSE-14 and phase closeout were still pending; Phase 1 was subsequently closed.

## Phase 1 PULSE-12 — 2026-11-19

The owner authorized Phase 1 and PULSE-12 on 2026-11-19. Synthetic pytest checks passed: **4 tests**, covering both encodings and delimiters, regular/special/equal/conflicting and invalid prices, GTIN validation, unknown headers, store/date selection and URL restriction. Fixtures are synthetic and do not redistribute retailer products.

Bounded live Scrapy runs on 2026-11-19 (local time) requested the 2026-11-17 file for each selected store. Both returned HTTP 200 and emitted manifests: SPAR 8702 **32,347** rows and Kaufland 5630 **23,593** rows. SPAR's downloaded SHA-256 matched its index. An initial SPAR run identified 286 prices written with a leading comma; after supporting that form and repeating the run, all rows in both samples had usable prices under the current rules. This is a parser observation, not independent verification of all prices or product identities.

**Pending at this PULSE-12 checkpoint:** broader dates and schema drift, durable failure manifests and exit signaling, operational retry and scheduling reliability, independent data quality review, PostgreSQL and Tableau. Phase 1 was subsequently closed and initial PostgreSQL work is recorded above; publication rights remain unresolved. Real output remains local and ignored by Git.

## Status

**Phase 0 formally CLOSED by explicit owner approval on 2026-11-19**, based on bounded user-local technical feasibility evidence dated 2026-11-18. The pair is **SPAR Croatia / store 8702** and **Kaufland Croatia / store 5630**. The initial matching gate is **102 descriptor-consistent product pairs from 160 reviewed strict candidates**, with 58 unresolved. This is **not** external manufacturer/GS1 identity certification, production reliability evidence, permission to redistribute real data, or evidence of Phase 1 implementation.

## Owner closeout decision (2026-11-19)

**Approved:** formal closure of **Phase 0 — Project Definition and Source Feasibility** for SPAR Croatia (Zagreb Jankomir, store 8702) and Kaufland Croatia (Zagreb Antuna Šoljana, store 5630). The approved evidence scope is bounded Scrapy access, four fixed-store/date CSV snapshots, observed price-field behavior, and **102 description-consistent pairs among 160 prefiltered pairs reviewed**. The owner authorized updating GitHub documentation and Jira.

**Limitations retained at Phase 0 closeout:** 58 unresolved product-identity pairs; no external manufacturer/GS1 validation or production reliability proof; no PostgreSQL ingest or Tableau workbook at that checkpoint; no inferred stock availability or rights to publicly redistribute source observations. Phase 1 was separately authorized later on 2026-11-19.

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
| Source reuse and Tableau publication | REAL-DATA PUBLICATION ON HOLD | SPAR website terms restrict reproduction/distribution; NN 132/2026 automated-access text does not imply a general redistribution license. The public portfolio data approach is undecided; synthetic data is an option. |
| PostgreSQL and Tableau at the Phase 0 checkpoint | NOT IMPLEMENTED THEN | Phase 2 PostgreSQL work is recorded above; Tableau remains unimplemented. |

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

## Phase 3 accelerated recurring check — 2026-11-23

A temporary Windows Scheduled Task was configured to run two bounded collection-only batches at one-minute intervals against the 2026-11-17 historical files. Both batches reported success, the task returned zero and the temporary task was removed. Together with three earlier manual successful batches, this is a limited five-batch baseline using one historical date; it is not a daily uptime or missed-run measurement. Raw outputs remain private.

The permanent collection-only daily task was separately checked before its due time and did not capture. Its first actual due daily run and behavior over multiple dates were not observed during this check. The scheduler's warning rules are provisional and documented in [Reliability](RELIABILITY.md); local synthetic tests cover warning and recovery behavior. The complete local suite passed 61 tests with a temporary PostgreSQL instance, which was stopped afterward. The [GitHub-hosted CI run](https://github.com/angel-wm/pricepulse-retail-intelligence/actions/runs/45122553854) for commit `ba7b8c4faecc207603ff96261419c7d207132d7e` succeeded.

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

**Not tested or authorized at the Phase 0 checkpoint:** continuous scheduling/retry reliability; end-to-end PostgreSQL idempotency; external manufacturer/GS1 resolution for the 58 unresolved pairs; full-catalog matching precision; ambiguous dual-different source prices; data publication rights; Tableau workbook. Phase 0 closed on 2026-11-19; subsequent Phase 1 and synthetic Phase 2 evidence appears above.

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

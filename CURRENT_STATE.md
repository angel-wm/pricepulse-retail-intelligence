# Current state

**Phase 5 — AUTHORIZED AND IN PROGRESS from 2026-11-23.** Phases 0–2 and private Phase 4 are closed. Phase 3 remains open.

PULSE-12 implements bounded SPAR 8702 and Kaufland 5630 Scrapy acquisition, source-specific parsing and synthetic tests. One file per retailer for 2026-11-17 was retrieved and parsed in bounded local smoke tests. See [Validation](VALIDATION.md) and [Acquisition](ACQUISITION.md). These checks do not establish production reliability.

PULSE-13 adds bounded retry and timeout policies, classified failure logging, incomplete-response rejection and request-policy tests. A bounded SPAR smoke test recorded request counts and statuses; see [Validation](VALIDATION.md). PULSE-14 contract and schema cases have passed local synthetic tests.

PULSE-44 added checks-only GitHub Actions; PULSE-19 expanded CI and operational recovery and is now in review. The reviewed code baseline passed 62 local tests and hosted CI; see [Validation](VALIDATION.md).

Phase 2 delivered the PostgreSQL schema, local-file ingestion and explicit comparison review. A private review loaded and replayed one historical file per source and reconciled row counts. Four sample pairs were approved from the 6,418 eligible pairs for 17 November, and the SQL view reconciled the verified prices. See [PostgreSQL](POSTGRESQL.md) and [Validation](VALIDATION.md).

Phase 3 has a local run journal, two-store batch, feed completeness and index discovery checks, provisional quality signals, explicit PostgreSQL ingestion recovery and a local collection-only task. After the Kaufland filename fix, the permanent Windows task captured both real files on 2026-11-23 at a controlled one-time trigger and returned code 0. The original incomplete marker is archived and the normal hourly configuration was restored. Synthetic checks covered missed ticks and ingestion recovery. A normal eligible tick on another date and Windows behavior after a real interruption remain unobserved. See [Reliability](RELIABILITY.md) and [Validation](VALIDATION.md).

Phase 4 delivered an interactive English Tableau snapshot built from real data for two stores and two dates. It covers 112,170 listed-price observations, 17,803 same-store comparisons, four approved cross-store gaps and source-file quality. The private workbook and screenshot are ready for local use. Additional pair review, automatic refresh and public delivery remain open. See [Tableau analytics](TABLEAU.md) and [Validation](VALIDATION.md).

The Phase 5 technical review is complete for the original two-store baseline and private Tableau snapshot. It covers the fixed real-data baseline, SQL and live Tableau reconciliation, filter scenarios, the Docker-backed 65-test suite, and the documentation and synthetic fixture audit. See [Validation](VALIDATION.md#phase-5-technical-review--2026-11-23). Public portfolio delivery remains open.

[PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46) adds Konzum 1280 as the third local source. The manual and scheduled collectors use the three-store cohort. Apply the schema update before loading into an existing database. The updated private Tableau workbook covers all three stores on 17 and 23 November 2026. It includes 165,322 listed prices, 41,363 same-store comparisons and four reviewed products across all three chains. See [Tableau analytics](TABLEAU.md#three-source-workbook).

**Next gate:** review Phase 3 with the permanent-task capture evidence and observe the regular cadence on another date. Public delivery remains tracked under PULSE-23 and PULSE-26.

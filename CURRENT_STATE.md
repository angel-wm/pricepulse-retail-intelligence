# Current state

**Phase 5 — CLOSED on 2026-11-25.** Phases 0–2 and 4 are closed. Phase 3 remains open for the automatic collection check and owner review.

PULSE-12 implements bounded SPAR 8702 and Kaufland 5630 Scrapy acquisition, source-specific parsing and synthetic tests. One file per retailer for 2026-11-17 was retrieved and parsed in bounded local smoke tests. See [Validation](VALIDATION.md) and [Acquisition](ACQUISITION.md). These checks do not establish production reliability.

PULSE-13 adds bounded retry and timeout policies, classified failure logging, incomplete-response rejection and request-policy tests. A bounded SPAR smoke test recorded request counts and statuses; see [Validation](VALIDATION.md). PULSE-14 contract and schema cases have passed local synthetic tests.

PULSE-44 added checks-only GitHub Actions; PULSE-19 expanded CI and operational recovery and is now in review. The reviewed code baseline passed 62 local tests and hosted CI; see [Validation](VALIDATION.md).

Phase 2 delivered the PostgreSQL schema, local-file ingestion and explicit comparison review. A private review loaded and replayed one historical file per source and reconciled row counts. Four sample pairs were approved from the 6,418 eligible pairs for 17 November, and the SQL view reconciled the verified prices. See [PostgreSQL](POSTGRESQL.md) and [Validation](VALIDATION.md).

Phase 3 has a local run journal, three-store batch, feed completeness and index discovery checks, provisional quality signals, explicit PostgreSQL ingestion recovery and a local collection-only task. The normal 12:20 Bogotá tick started automatically on 25 November 2026. It captured Kaufland and Konzum and left an incomplete marker after SPAR changed its CSV layout. The updated parser accepted both layouts, and a separate SPAR retry recovered its 32,329 listed prices. The next full automatic capture with the fix remains to be observed. See [Reliability](RELIABILITY.md) and [Validation](VALIDATION.md#regular-windows-tick-and-spar-schema-recovery--2026-11-25).

Phase 4 delivered an interactive English Tableau snapshot built from real data for two stores and two dates. It covers 112,170 listed-price observations, 17,803 same-store comparisons, four approved cross-store gaps and source-file quality. The three-store workbook supersedes that Tableau package. Additional pair review and automatic refresh remain open. See [Tableau analytics](TABLEAU.md) and [Validation](VALIDATION.md).

Phase 5 closed after end-to-end validation, a reproducible Windows and PostgreSQL setup, and delivery of the public Tableau portfolio. The technical review covered the original two-store baseline. The published workbook covers three stores and has its own Desktop verification. See [Phase 5 closeout evidence](VALIDATION.md#phase-5-closeout--2026-11-25).

[PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46) adds Konzum 1280 as the third local source. The manual and scheduled collectors use the three-store cohort. Apply the schema update before loading into an existing database. The [portfolio workbook and screenshots](TABLEAU.md#portfolio-workbook) cover all three stores on 17 and 23 November 2026. The workbook includes 165,322 listed prices, 41,363 same-store comparisons and 13,700 searchable shared barcodes for 23 November. Four of the barcode matches passed manual review. Lidl remains outside the release scope.

On 24 November, the installed Windows task captured all three source files and
finished with code 0 and no quality alerts. [Validation](VALIDATION.md#installed-windows-collection-with-three-retailers--2026-11-24)
records the evidence and the limit on determining the original trigger.

**Next gate:** owner review of Phase 3, including regular cadence and behavior
after a real interruption.

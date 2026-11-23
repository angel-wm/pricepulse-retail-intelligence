# Current state

**Phase 4 — CLOSED for private Tableau analytics on 2026-11-23.** Phases 0–2 are closed. Phase 3 remains open and Phase 5 awaits authorization.

PULSE-12 implements bounded SPAR 8702 and Kaufland 5630 Scrapy acquisition, source-specific parsing and synthetic tests. One file per retailer for 2026-11-17 was retrieved and parsed in bounded local smoke tests. See [Validation](VALIDATION.md) and [Acquisition](ACQUISITION.md). These checks do not establish production reliability.

PULSE-13 adds bounded retry and timeout policies, classified failure logging, incomplete-response rejection and request-policy tests. A bounded SPAR smoke test recorded request counts and statuses; see [Validation](VALIDATION.md). PULSE-14 contract and schema cases have passed local synthetic tests.

PULSE-44 added checks-only GitHub Actions; PULSE-19 expanded CI and operational recovery and is now in review. The reviewed code baseline passed 62 local tests and hosted CI; see [Validation](VALIDATION.md).

Phase 2 delivered the PostgreSQL schema, local-file ingestion and explicit comparison review. A private review loaded and replayed one historical file per source and reconciled row counts. Four sample pairs were approved from the 6,418 eligible pairs for 17 November, and the SQL view reconciled the verified prices. See [PostgreSQL](POSTGRESQL.md) and [Validation](VALIDATION.md).

Phase 3 has a local run journal, two-store batch, feed completeness and index discovery checks, provisional quality signals, explicit PostgreSQL ingestion recovery and a local collection-only task. The corrected collector recovered Kaufland after a filename change. A temporary Windows task then collected both real files for 2026-11-23 at its trigger time. The permanent task's original incomplete marker is preserved. Controlled tests confirmed same-day collection after a missed tick and no automatic backfill for a fully missed date. Normal capture through the permanent task and Windows behavior after a real interruption remain unverified. Ingestion recovery was exercised only with synthetic data. See [Reliability](RELIABILITY.md) and [Validation](VALIDATION.md).

Phase 4 delivered an interactive English Tableau snapshot built from real data for two stores and two dates. It covers 112,170 listed-price observations, 17,803 same-store comparisons, four approved cross-store gaps and source-file quality. The private workbook and screenshot are ready for local use. Additional pair review, automatic refresh and public delivery remain open. See [Tableau analytics](TABLEAU.md) and [Validation](VALIDATION.md).

**Next gate:** validate the permanent collection task and complete owner review of Phase 3. Phase 5 requires separate authorization. Public delivery remains tracked under PULSE-23.

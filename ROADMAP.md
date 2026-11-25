# Roadmap

This is the phase-gated **plan and evidence-based status**. Feasibility probes are not production implementation.

## Work model and approval rules

The work unit is a **phase**: **planned → explicitly authorized → in progress → validated → closed**.

- **Phase 0 — formally CLOSED by explicit owner approval on 2026-11-19.** Bounded source access, price-field interpretation, same-store history and 102 description-consistent matches are recorded in [Validation](VALIDATION.md). This does not amount to external GS1 validation or operational reliability proof.
- **Phase 1 was formally closed by the owner on 2026-11-22. Phase 2 was authorized on the same date and formally closed on 2026-11-23 after synthetic integration checks and a bounded private real-file review.** Publication of real data remained outside that authorization.
- **Phase 3 was subsequently authorized by the owner before Phase 2 review and closeout.** Phase 3 awaits owner review, and real-source publication remains restricted. Phase 3 includes an owner-selected local collection-only schedule.
- **Phase 4 was authorized before the Phase 2 and Phase 3 reviews and closed on 2026-11-23 for private Tableau analytics.** Phase 3 remains open.
- **Phase 5 was authorized on 2026-11-23 and closed by the owner on 2026-11-25.** See the [closeout evidence](VALIDATION.md#phase-5-closeout--2026-11-25).
- Close a phase only with the results and evidence recorded in [Validation](VALIDATION.md) and [Current state](CURRENT_STATE.md).
- An external Jira board may track tasks; do not treat issue statuses as runtime verification.

## Planned phases

| Phase | Planned deliverable | Exit gate |
| --- | --- | --- |
| 0 — Grocery source feasibility | Kaufland + SPAR source access, actual price fields, two-day history and descriptor matching | **CLOSED 2026-11-19:** four store/date files; 102 conservative description-consistent cases in a 160-pair sample; publication of genuine retailer data remains restricted. |
| 1 — Scrapy acquisition | Separate SPAR JSON and Kaufland asset-index spiders; bounded CSV downloads; source-specific parsing contracts and fixtures; checks-only CI (PULSE-44) | **CLOSED 2026-11-22:** representative extraction, traceability, error-path tests and hosted CI evidence. |
| 2 — Data engineering | File provenance, parsing, validated PostgreSQL schema, daily immutable observations | **CLOSED 2026-11-23:** private load and replay of one historical file per retailer and four owner-approved price comparisons. See [Validation](VALIDATION.md). |
| 3 — Reliability | Scheduling, logs, monitoring, failure recovery and expanded CI as appropriate (PULSE-19) | Recorded successful and failed runs with measured behavior |
| 4 — Tableau analytics | Private Tableau workbook with real price history, catalog coverage and strict matching | **CLOSED 2026-11-23:** SQL-reconciled metrics and verified Desktop interaction. See [Validation](VALIDATION.md). |
| 5 — Validation and release | End-to-end checks, reproducible local setup, documentation and public Tableau portfolio | **CLOSED 2026-11-25:** validated workflow, published workbook and screenshots, and owner approval |

## Phase 5 deliverables

The owner authorized Konzum 1280 as the third local source on 2026-11-23.
[PULSE-46](https://angel231995.atlassian.net/browse/PULSE-46) records the completed integration and validation.
The owner confirmed on 2026-11-24 that Lidl stays outside this release and selected a real-data-only portfolio.
See [Source feasibility](SOURCE_FEASIBILITY.md#two-date-expansion-decision) for the comparison with Lidl.

| Work item | Evidence required |
| --- | --- |
| [PULSE-24](https://angel231995.atlassian.net/browse/PULSE-24) — Validate the flow | Record source acquisition or the archived capture baseline, replay exact file versions, and reconcile SQL results with Tableau. |
| [PULSE-25](https://angel231995.atlassian.net/browse/PULSE-25) — Verify local setup | Test a clean locked installation and the disposable PostgreSQL path. Check the links and reproduction commands. |
| [PULSE-26](https://angel231995.atlassian.net/browse/PULSE-26) — Prepare portfolio release | Verify the packaged workbook, presentation screenshots and download instructions for the real-data snapshot. |

## Phase 0 evidence checklist (completed; owner approved closeout 2026-11-19)

1. **Evidenced:** reviewed regulation effective 2026-11-17 and publication constraints. Real-data public sharing is **not cleared**.
2. **Evidenced:** user-local Scrapy probes obeyed robots guidance and retrieved both source indexes and sampled files with HTTP 200; no CAPTCHA bypass.
3. **Evidenced:** fixed Zagreb stores SPAR 8702 and Kaufland 5630 across 2026-11-16/17.
4. **Evidenced:** 8,869 same-day priced code matches and 4,155 strict candidates; private 160-pair review found 102 description-consistent pairs (58 unresolved).
5. **Evidenced:** two different publication dates for each fixed store, with promotions recovered from SPAR's special-price field; operational scheduling remains untested.
6. **Documented and approved:** source sharing restrictions, deferred stock KPI and explicit Phase 0 closeout on 2026-11-19. **Subsequently:** Phase 1 implementation was authorized on 2026-11-19.

**Fallback:** if either source fails the gate, assess another Croatian chain with official downloadable price lists before changing the engineering stack or scraping framework. Lidl remains excluded from the first cohort by scope decision.

Related detail: [Source feasibility](SOURCE_FEASIBILITY.md), [Project specification](PROJECT_SPEC.md).

Phase 1 checks-only CI was implemented for PULSE-44 and passed a hosted run recorded in [Validation](VALIDATION.md). It runs synthetic tests on code changes, without scheduled or live retailer scraping or deployment. PULSE-19 retains the later operational reliability and expanded CI work. This timing does not add a new Phase 1 exit criterion to the table above.

## Additional product-pair review

Review remaining candidates in private batches as needed for analytics. Use the barcode, pack size and variant, supported by product references where available. Ambiguous pairs remain pending. This expands the verified cohort after Phase 2 closeout.

## Planned local reproducibility improvement

The owner requested the Docker Compose PostgreSQL setup during Phase 5 while Phase 3 review remains open. [PULSE-45](https://angel231995.atlassian.net/browse/PULSE-45) covers a persistent development database, an isolated disposable test database and the [local setup guide](POSTGRESQL.md#local-postgresql-with-docker-compose). Phase 3 retains its own scheduled-run evidence requirement.

Keep the existing local collection-only scheduler and Scrapy execution unchanged for this improvement. Consider an application image separately if a concrete portability need arises.

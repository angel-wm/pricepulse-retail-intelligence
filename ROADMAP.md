# Roadmap

This is the phase-gated **plan and evidence-based status**. Feasibility probes are not production implementation.

## Work model and approval rules

The work unit is a **phase**: **planned → explicitly authorized → in progress → validated → closed**.

- **Phase 0 — formally CLOSED by explicit owner approval on 2026-11-19.** Bounded source access, price-field interpretation, same-store history and 102 description-consistent matches are recorded in [Validation](VALIDATION.md). This does not amount to external GS1 validation or operational reliability proof.
- **Phase 1 was formally closed by the owner on 2026-11-22. Phase 2 was authorized on the same date and is validated with synthetic data for owner review.** Publication of real data remained outside that authorization.
- **Phase 3 was subsequently authorized by the owner before Phase 2 review and closeout.** This is an explicit sequencing exception: both phases await owner review, and real-source publication remains restricted. Phase 3 includes an owner-selected local collection-only schedule.
- **Phase 4 was authorized by the owner before Phase 2 and Phase 3 reviews.** Those phases remain open; no genuine retailer data may be published without a verified rights basis.
- Close a phase only with the results and evidence recorded in [Validation](VALIDATION.md) and [Current state](CURRENT_STATE.md).
- An external Jira board may track tasks; do not treat issue statuses as runtime verification.

## Planned phases

| Phase | Planned deliverable | Exit gate |
| --- | --- | --- |
| 0 — Grocery source feasibility | Kaufland + SPAR source access, actual price fields, two-day history and descriptor matching | **CLOSED 2026-11-19:** four store/date files; 102 conservative description-consistent cases in a 160-pair sample; publication of genuine retailer data remains restricted. |
| 1 — Scrapy acquisition | Separate SPAR JSON and Kaufland asset-index spiders; bounded CSV downloads; source-specific parsing contracts and fixtures; checks-only CI (PULSE-44) | **CLOSED 2026-11-22:** representative extraction, traceability, error-path tests and hosted CI evidence. |
| 2 — Data engineering | File provenance, parsing, validated PostgreSQL schema, daily immutable observations | Checked idempotency, duplicate handling, historical integrity and data-quality tests |
| 3 — Reliability | Scheduling, logs, monitoring, failure recovery and expanded CI as appropriate (PULSE-19) | Recorded successful and failed runs with measured behavior |
| 4 — Tableau analytics | Local-source price history and strict matching; public demonstration data approach undecided | SQL-reconciled metrics; genuine retailer data may be published only if rights are established |
| 5 — Validation and release | README, architecture, test evidence, reproducible local setup and portfolio presentation | End-to-end tests, release documentation and explicit closeout |

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

## Planned local reproducibility improvement

In Phase 5, after owner review of Phases 2 and 3 and authorization of Phase 5 work, add a Docker Compose PostgreSQL setup for local development and synthetic integration tests ([PULSE-45](https://angel231995.atlassian.net/browse/PULSE-45)). Document persistence, safe volume removal, private credentials and a disposable test database. Keep genuine retailer data and credentials out of public artifacts. This is planned work, not a Phase 2 or 3 closure criterion or evidence of operational reliability.

Keep the existing local collection-only scheduler and Scrapy execution unchanged for this improvement. Consider an application image separately if a concrete portability need arises.

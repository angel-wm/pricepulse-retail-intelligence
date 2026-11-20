# Roadmap

This is the phase-gated **plan and evidence-based status**. Feasibility probes are not production implementation.

## Work model and approval rules

The work unit is a **phase**: **planned → explicitly authorized → in progress → validated → closed**.

- **Phase 0 — formally CLOSED by explicit owner approval on 2026-11-19.** Bounded source access, price-field interpretation, same-store history and 102 description-consistent matches are recorded in [Validation](VALIDATION.md). This does not amount to external GS1 validation or operational reliability proof.
- **Phase 1 implementation has not been authorized.** Planning, research, documentation and bounded user-executed feasibility tests do not authorize building spiders or a database.
- Close a phase only with the results and evidence recorded in [Validation](VALIDATION.md) and [Current state](CURRENT_STATE.md).
- An external Jira board may track tasks; do not treat issue statuses as runtime verification.

## Planned phases

| Phase | Planned deliverable | Exit gate |
| --- | --- | --- |
| 0 — Grocery source feasibility | Kaufland + SPAR source access, actual price fields, two-day history and descriptor matching | **CLOSED 2026-11-19:** four store/date files; 102 conservative description-consistent cases in a 160-pair sample; publication of genuine retailer data remains restricted. Phase 1 is not authorized. |
| 1 — Scrapy acquisition | Separate SPAR JSON and Kaufland asset-index spiders; bounded CSV downloads; source-specific parsing contracts and fixtures | Representative two-source extraction, source hash/date/store traceability and error-path tests |
| 2 — Data engineering | File provenance, parsing, validated PostgreSQL schema, daily immutable observations | Checked idempotency, duplicate handling, historical integrity and data-quality tests |
| 3 — Reliability | Scheduling, logs, monitoring, failure recovery, pytest and CI as appropriate | Recorded successful and failed runs with measured behavior |
| 4 — Tableau analytics | Local-source price history and strict matching; **synthetic public demonstration by default** | SQL-reconciled metrics; safe Tableau Public release only if rights are established |
| 5 — Validation and release | README, architecture, test evidence, reproducible local setup and portfolio presentation | End-to-end tests, release documentation and explicit closeout |

## Phase 0 evidence checklist (completed; owner approved closeout 2026-11-19)

1. **Evidenced:** reviewed regulation effective 2026-11-17 and publication constraints. Real-data public sharing is **not cleared**.
2. **Evidenced:** user-local Scrapy probes obeyed robots guidance and retrieved both source indexes and sampled files with HTTP 200; no CAPTCHA bypass.
3. **Evidenced:** fixed Zagreb stores SPAR 8702 and Kaufland 5630 across 2026-11-16/17.
4. **Evidenced:** 8,869 same-day priced code matches and 4,155 strict candidates; private 160-pair review found 102 description-consistent pairs (58 unresolved).
5. **Evidenced:** two different publication dates for each fixed store, with promotions recovered from SPAR's special-price field; operational scheduling remains untested.
6. **Documented and approved:** source sharing restrictions, deferred stock KPI and explicit Phase 0 closeout on 2026-11-19. **Still pending:** separate Phase 1 implementation authorization.

**Fallback:** if either source fails the gate, assess another Croatian chain with official downloadable price lists before changing the engineering stack or scraping framework. Lidl remains excluded from the first cohort by scope decision.

Related detail: [Source feasibility](SOURCE_FEASIBILITY.md), [Project specification](PROJECT_SPEC.md).

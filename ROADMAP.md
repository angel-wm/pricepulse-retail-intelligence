# Roadmap

This is the phase-gated **plan**, not an implementation progress report.

## Work model and approval rules

The work unit is a **phase**: **planned → explicitly authorized → in progress → validated → closed**.

- **Phase 0 — Source feasibility is in progress** following the user's request to investigate and document the replacement data category.
- **Phase 1 implementation has not been authorized.** Planning, research, documentation and bounded user-executed feasibility tests do not authorize building spiders or a database.
- Close a phase only with the results and evidence recorded in [Validation](VALIDATION.md) and [Current state](CURRENT_STATE.md).
- An external Jira board may track tasks; do not treat issue statuses as runtime verification.

## Planned phases

| Phase | Planned deliverable | Exit gate |
| --- | --- | --- |
| 0 — Grocery source feasibility | Verify Kaufland + SPAR access, schemas, current GTIN overlap, constraints and KPI scope | Two usable source files, >=100 validated shared GTINs, documented acceptable acquisition/publication boundaries |
| 1 — Scrapy acquisition | Source-specific list-index and file-download spiders; bounded, resilient runs | Repeatable downloads from both approved sources, recorded sample tests |
| 2 — Data engineering | File provenance, parsing, validated PostgreSQL schema, daily immutable observations | Checked idempotency, duplicate handling, historical integrity and data-quality tests |
| 3 — Reliability | Scheduling, logs, monitoring, failure recovery, pytest and CI as appropriate | Recorded successful and failed runs with measured behavior |
| 4 — Tableau analytics | Source-backed price comparison and trend dashboards | Verified metrics, correct matching/grain, sharing permission verified for publication |
| 5 — Validation and release | README, architecture, test evidence, reproducible local setup and portfolio presentation | End-to-end tests, release documentation and explicit closeout |

## Phase 0 sequence

1. Review official regulatory framework effective **2026-11-17**, including availability of automated retrieval, changing file formats and minimum 15-day archive availability.
2. Retrieve **robots.txt and live index/file responses using Scrapy** from official Kaufland and SPAR domains; honor access rules and stop upon blocks.
3. Select one physical store per chain in a comparable region, for the same recent date.
4. Measure unique valid GTINs in each store file, intersections, collisions, missing identifiers, unmatched variants and usable prices. **Pass target: >=100 validated products**.
5. Verify reproducible acquisition on another date, or retrieve an admissible historical publication; separate price-list timestamps from collection timestamps.
6. Document source terms and publication boundaries and close Phase 0 only when supported by evidence and approval.

**Fallback:** if either source fails the gate, assess another Croatian chain with official downloadable price lists before changing the engineering stack or scraping framework. Lidl remains excluded from the first cohort by scope decision.

Related detail: [Source feasibility](SOURCE_FEASIBILITY.md), [Project specification](PROJECT_SPEC.md).

# Roadmap

This roadmap is a **plan**, not an implementation progress report.

## Work model and approval rules

The native work unit is a **phase**. Work proceeds sequentially: **planned → explicitly authorized → in progress → validated → closed**.

- Planning or writing documentation does **not** authorize starting implementation.
- Authorize each phase deliberately, after reviewing scope and prerequisites.
- Close a phase only when its documented exit criteria have evidence; update [current state](CURRENT_STATE.md) and [validation](VALIDATION.md).
- Do not mark work as tested, complete, or released from intent alone.
- An external Jira board may track tasks, but this repository's documented state and evidence remain the source of truth until an explicit integration and authority change are recorded.

## Planned phases

| Phase | Planned deliverable | Exit gate (evidence required) |
| --- | --- | --- |
| 0 — Definition and feasibility | Business questions, sources and permissions, success criteria, scope and architecture | Source access and publication constraints documented; architecture reviewed |
| 1 — Scrapy development | One approved-source spider and explicit extraction contract | Repeatable representative extraction; error paths and rate limits checked |
| 2 — Data engineering | PostgreSQL schema, ingestion, quality checks, price-history model | Idempotent ingestion and historical observations independently validated |
| 3 — Automation and reliability | Scheduling, logs, failure handling, CI/tests where suitable | Recorded executions, failure recovery, and test results |
| 4 — Tableau analytics | Local workbook and shareable portfolio dashboard when permitted | Verified measures, filters, and publication permissions |
| 5 — Validation and portfolio release | Reproducibility, evidence, architecture, README and screenshots where relevant | End-to-end validation and documented release handoff |

## Phase 0 questions to resolve

- Which retail categories and business questions warrant price-history tracking?
- Which exact sources are accessible and suitable under their terms and robots guidance?
- What constitutes a stable product identifier and an observation timestamp?
- What currencies, units, availability states, and outliers need explicit contracts?
- Can products from different retailers be matched responsibly?
- What data, if any, may be published on Tableau Public?
- What scale and refresh frequency are feasible for a free, local workflow?

Proceed to Phase 1 only after Phase 0 has been authorized and closed with evidence.

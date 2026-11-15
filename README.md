# PricePulse — Retail Price Intelligence

PricePulse is a **planned** end-to-end retail price intelligence project. It aims to collect permitted public product information with Scrapy, preserve historical price and availability observations in PostgreSQL, and analyze trends with Tableau.

**Current status: PRE-PROJECT.** No retail source is approved; no scraper, database, pipeline, automation, or dashboard has been implemented or validated. Phase 0 (definition and feasibility) is planned but not started.

For project context and task-specific reading guidance, see [REPO_CONTEXT.md](REPO_CONTEXT.md).

## Why PricePulse?

The goal is to demonstrate an engineering workflow that converts responsibly collected product observations into reproducible, quality-checked analytical data. A portfolio reviewer should eventually be able to inspect source access decisions, extraction contracts, historical modeling, test evidence, and business-facing visualizations—not just a scraping script.

## Intended workflow

1. **Assess feasibility:** choose candidate retail sources and confirm permitted access, useful fields, and scope.
2. **Extract with Scrapy:** collect structured public product observations, respecting robots guidance, site terms, and reasonable request rates.
3. **Validate and persist:** enforce data contracts, preserve price history, and handle ingestion duplicates in PostgreSQL.
4. **Operate reliably:** add meaningful tests, logs, failure handling, and suitable scheduling.
5. **Analyze in Tableau:** explore price movements, availability, and defensible cross-retailer comparisons.

These are planned capabilities, **not implementation claims**. No second scraping framework is part of the initial scope. Product matching across retailers requires a distinct validation strategy.

## Planned technology

| Responsibility | Intended choice |
| --- | --- |
| Data collection | Python, Scrapy |
| Persistence and transformations | PostgreSQL, Python, SQL |
| Tests and scheduled checks | pytest, GitHub Actions where feasible |
| Business intelligence | Tableau Desktop Free Edition; Tableau Public only for shareable data |
| Version control | Git, GitHub |

The project prioritizes free, locally reproducible tooling. Playwright, BeautifulSoup, Scrapling, and Crawlee are **not** dependencies. A separate future Crawlee project will address a different technical problem.

## Start here

This is a **documentation-first** repository. There is no installation or scraper command yet.

- [Current state](CURRENT_STATE.md): what is implemented and what remains unverified.
- [Roadmap and phase gates](ROADMAP.md): planned sequence and approval rules.
- [Project specification](PROJECT_SPEC.md): scope, goals, constraints, and success criteria to refine.
- [Intended architecture](ARCHITECTURE.md): proposed responsibilities and data flow.
- [Decision log](DECISIONS.md): recorded choices and their rationale.
- [Validation record](VALIDATION.md): evidence status and future checks.
- [Agent guidance](AGENTS.md): repository-specific reading and execution boundaries.

## Constraints and publication

Source feasibility is a Phase 0 decision. Respect applicable law, site terms, robots.txt guidance, access controls, and rate limits. Do not bypass CAPTCHAs or anti-bot protections. Do not publish scraped data until its sharing rights have been verified. Tableau Public requires public/shareable data.

Repository documentation follows the [Repository Documentation Readability guide](https://github.com/angel-wm/repository-documentation-readability/blob/main/GUIDE.md) for presentation, while PricePulse's native source files remain authoritative for project facts.

## Handoff

The repository default branch is the intended documentation handoff location. Read the visible branch snapshot and [current state](CURRENT_STATE.md) before making claims about completed work. A planned phase is not permission to start it.

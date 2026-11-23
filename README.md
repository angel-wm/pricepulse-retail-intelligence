# PricePulse — Grocery Price Intelligence

PricePulse is a **documentation-first Data Engineering portfolio project** to acquire official Croatian grocery price-list files responsibly with Scrapy, validate product identities, store durable historical observations in PostgreSQL, and analyze comparable offers in Tableau.

**Current status (2026-11-23): Phase 1 is formally closed; Phases 2 and 3 await owner review; Phase 4 is in progress.** Bounded user-local Scrapy tests retrieved official files for **SPAR Croatia (Zagreb Jankomir, store 8702)** and **Kaufland Croatia (Zagreb Antuna Šoljana, store 5630)** for 16–17 November 2026. The 17 November files had **8,869 common priced GTINs**; a deterministic audit of 160 prefiltered pairs classified **102 description-consistent** and **58 unresolved**. This is not manufacturer verification or a claim about all 8,869 pairs. Phase 1 adapters have been implemented and smoke-tested; PostgreSQL has synthetic validation. A local collection-only task is registered; accelerated scheduled historical captures succeeded, while normal daily operation remains unobserved. Tableau is not implemented.

## What PricePulse aims to answer

- How do published prices for the same grocery product change over time?
- What is the price difference for the same verified GTIN/EAN between Kaufland and SPAR at comparable stores and dates?
- Which product categories show the largest price changes or cross-retailer spreads?
- How complete and reliable are daily retailer price-list publications?

**Availability/stock tracking is not an initial KPI:** the governing regulation does not require an explicit stock field. A product missing from a list must not be described as out of stock.

## Why this data source?

Croatian retailers publish official machine-readable price lists. The regulation effective **17 November 2026** expressly provides for automated collection and CSV/XML price lists. This is stronger evidence for the acquisition use case than attempting to crawl individual product pages protected by anti-bot systems.

Actual local source-access, two-date history, and price/identity evidence is in [Validation](VALIDATION.md) and [Source feasibility](SOURCE_FEASIBILITY.md). Initial same-date codes with price totaled 8,869 after promotional-price handling, but these are **not all verified product matches**. Previous music-retailer candidates were dropped after access blocks or restrictions. Public real-data redistribution remains on hold; the portfolio data approach has not been decided.

## Local quick start (Windows PowerShell)

**Prerequisites:** Git and `uv` installed; the repository targets Python **3.12**. These commands set up the Python environment but **do not** start production scraping or create a PostgreSQL database.

```powershell
cd "C:\Users\angel\Documents\Proyectos\pricepulse-retail-intelligence"
git pull --ff-only
uv sync
uv run python --version
uv run scrapy version
```

- `uv sync` creates or updates the project's `.venv` using `pyproject.toml` and `uv.lock`. No separate `uv venv` command is required for the usual project setup.
- `uv run <command>` uses the project environment **without requiring activation**. If you prefer activating it in the current PowerShell session, run `.\.venv\Scripts\Activate.ps1`; use `deactivate` to exit.
- Git commands (`status`, `pull`, `add`, `commit`, `push`) do **not** require an activated Python virtual environment. Check `git status` before committing or pulling if local changes exist.
- The repository contains two bounded Scrapy adapters and an initial PostgreSQL ingestion and review implementation. Synthetic PostgreSQL tests have passed locally and in GitHub-hosted CI. A local collection-only schedule is registered and a separate accelerated recurring task succeeded twice; normal daily operation remains unobserved; Tableau is not implemented. See [Acquisition](ACQUISITION.md), [PostgreSQL](POSTGRESQL.md) and [Reliability](RELIABILITY.md).

## Planned workflow

1. **Phase 0 — Feasibility:** bounded source access, two-date per-store price history, price-field parsing, and at least 100 descriptor-consistent product pairs — **formally closed on 2026-11-19**.
2. **Phase 1 — Scrapy (closed 2026-11-22):** two source-specific spiders discover SPAR's dated JSON manifests and Kaufland's asset index, then fetch permitted store price lists with bounded request rates and explicit parsing/error contracts.
3. **Phase 2 — Data engineering (in review):** preserve file provenance and hashes; parse **SPAR cp1250/semicolon** and **Kaufland UTF-8 BOM/tab** sources; handle regular/special price origins, GTIN and package checks, and ingest versioned, deduplicated store/date observations into PostgreSQL.
4. **Phase 3 — Reliability (awaiting owner review):** run evidence, recovery, local scheduling and provisional quality monitoring are implemented; see [Reliability](RELIABILITY.md).
5. **Phase 4 — Tableau (in progress):** analyze same-store price history and verified cross-retailer comparisons. The public portfolio data approach remains undecided; synthetic data is an option, and real-source publication requires separately verified redistribution rights. An initial private analytical export is documented in [Tableau analytics](TABLEAU.md); the workbook is not yet complete.
6. **Phase 5 — Release:** provide tested reproduction steps, measured results, documentation, and a portfolio-ready repository.

These phases mix completed work and planned deliverables; [Current state](CURRENT_STATE.md) and [Validation](VALIDATION.md) describe the implemented scope and its evidence.

## Technology

| Responsibility | Planned choice |
| --- | --- |
| Acquisition | Python 3.12, Scrapy, uv |
| File parsing and validation | Python standard library initially; explicit data contracts |
| Database and transformations | PostgreSQL, SQL, Python |
| Testing and automation | pytest; GitHub Actions where feasible |
| BI | Tableau Desktop Free Edition; Tableau Public only for appropriately shareable outputs |
| Version control | Git and GitHub |

Scrapy remains the primary acquisition framework. No additional scraping framework, paid service, or infrastructure is planned.

## Project references

- [Current state](CURRENT_STATE.md) — implemented versus pending work
- [Source feasibility](SOURCE_FEASIBILITY.md) — sources, evidence, tests, risks, and acceptance gates
- [Project specification](PROJECT_SPEC.md) — analytical scope and data contract
- [Roadmap](ROADMAP.md) — phase gates
- [Architecture](ARCHITECTURE.md) — proposed design
- [PostgreSQL](POSTGRESQL.md) — local ingestion, review and validation
- [Reliability](RELIABILITY.md) — run evidence, quality and schedule planning
- [Decisions](DECISIONS.md) — recorded decisions
- [Validation](VALIDATION.md) — actual evidence and outstanding tests
- [Repository context](REPO_CONTEXT.md) and [agent instructions](AGENTS.md) — navigation and working conventions

Repository documentation follows [Repository Documentation Readability](https://github.com/angel-wm/repository-documentation-readability). **Phase 0 was formally closed on 2026-11-19.** Phase 1 implementation was authorized on 2026-11-19; public release of genuine retailer data remains unapproved.

## License

Project-authored code and documentation are available under the [MIT License](LICENSE). Third-party data, trademarks, and other materials remain subject to their respective owners' rights and terms; this license does not grant permission to publish retailer data.

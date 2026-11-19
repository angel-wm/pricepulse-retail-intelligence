# Current state

## Current state

**Project status (2026-11-18): PHASE 0 — BOUNDED TECHNICAL FEASIBILITY VALIDATED; FORMAL CLOSEOUT PENDING.** The two sources can support initial engineering. This does not authorize Phase 1 implementation, real-data republication, or production reliability claims.

| Item | Recorded state |
| --- | --- |
| Active work | Phase 0 — owner review of evidence and closeout gate |
| Last completed phase | None |
| Planned source pair | **SPAR Croatia (store 8702, Jankomir)** and **Kaufland Croatia (store 5630, Antuna Šoljana)** — bounded feasibility qualified, not production onboarded |
| Initial scope exclusions | Lidl and musical-instrument retailers excluded from the initial source pair |
| Policy / sharing boundary | Official publication pages and NN 132/2026 reviewed; SPAR website terms restrict reproduction/redistribution. Bounded local tests succeeded; publishing real source files or a real-data Tableau extract remains blocked without separately verified rights. |
| Historical background | Secondary May 2025 analysis reported >=4,126 common barcodes across six chains excluding Lidl; **current 2026 results below supersede this as the primary feasibility evidence**. |
| Superseded candidates | UK music-retailer tests are archived in [Validation](VALIDATION.md); they do not define the current scope. |
| Acquisition evidence | Scrapy fetched both retailer indexes and **four fixed-store/date files** for 2026-11-16/17 with HTTP 200 (plus earlier exploratory CSV samples). Only bounded local tests, not scheduled reliability. |
| Current exact GTIN overlap | **8,869** shared priced GTIN candidates on 2026-11-17 (SPAR 8702 × Kaufland 5630); **7,772** present on both dates, **4,155** strict algorithmic candidates. |
| Same-store two-date history | **Promotion-aware initial check:** SPAR 31,277 code-stable entries (14 up, 54 down); Kaufland 15,533 (9 up, 69 down) from 2026-11-16/17. |
| Product identity QA | **102/160** descriptor-consistent sampled pairs; **58/160** held as ambiguous. Filtered sample, not GS1/manufacturer certification or full-catalog precision estimate. |\n| Price parsing rule | SPAR regular-only/special-only; Kaufland regular-only or both-equal. No dual-price conflict observed in four files. |\n| Production Scrapy, PostgreSQL, automation and Tableau | **Not implemented**; feasibility scripts were temporary, outside this repository |\n| Phase 1 authorization | **Not granted** |

## Next authorized action

**Next approval gate:** owner reviews Phase 0 evidence and explicitly closes the phase; **Phase 1 must then be explicitly authorized** before coding. The first Phase 1 scope is two Scrapy source adapters, file manifests and SHA-256 provenance, source-specific CSV dialects, price-origin contracts, representative fixtures, GTIN/package exception handling and non-evasive retry/rate policies. No genuine source observations may be distributed publicly without verified rights.

## Evidence and navigation

- [Source feasibility](SOURCE_FEASIBILITY.md) — source evidence, legal baseline, validation plan
- [Roadmap](ROADMAP.md) — phase gates
- [Project specification](PROJECT_SPEC.md) — intended contract and metrics
- [Validation](VALIDATION.md) — performed checks vs pending tests
- [Decisions](DECISIONS.md) — recorded scope choices

No **formal Phase 0 closeout** or production benchmark exists; technical feasibility findings are ready for the approval gate.

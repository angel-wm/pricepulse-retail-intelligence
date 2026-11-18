# Current state

## Current state

**Project status: PHASE 0 — FEASIBILITY IN PROGRESS.** The user approved investigating and documenting a switch to Croatian grocery price intelligence; **no implementation phase has started**.

| Item | Recorded state |
| --- | --- |
| Active work | Phase 0 — candidate-source evaluation and acceptance criteria |
| Last completed phase | None |
| Priority candidate sources | **Kaufland Croatia and SPAR Croatia** — not yet locally tested with Scrapy |
| Initial scope exclusions | Lidl and musical-instrument retailers excluded from the initial source pair |
| Regulatory/publication evidence | Official price-list pages and NN 132/2026 reviewed; first Scrapy probe obeyed robots and downloaded four CSVs; publication rights still need separate checks |
| Historical overlap indication | Third-party May 2025 analysis reported >=4,126 common barcodes across six chains excluding Lidl; **not a current local pair measurement** |
| Local feasibility evidence to date | Andertons: 3 product pages HTTP 200 with structured prices; Gear4music: 403; Bonners: 429; GigGear: 405 human verification — all **superseded candidate category**, not tests of grocery sources |
| Data access from Kaufland and SPAR | **Initial access PASS**: indexes HTTP 200; four official CSVs HTTP 200 and parsed. SPAR files for 2026-11-17 and 2026-11-18; Kaufland file for 2026-11-17. Schema/semantic QA remains pending. |
| Current exact GTIN overlap | **Not measured**: initial probe attempted 2026-11-18 only; Kaufland index had no matching 2026-11-18 asset label. Cross-retailer comparison should use common date 2026-11-17. |
| Scrapy spider / PostgreSQL / automation / Tableau | Not implemented |
| Phase 1 authorization | **Not granted** |

## Next authorized action

Perform **bounded same-date (2026-11-17) cross-retailer matching and product-quality tests**, subject to official robots guidance and source restrictions; record outputs in [Validation](VALIDATION.md). Update the candidate decision once both live sources and >=100 actual recent matches have been verified. Documentation changes do not authorize coding Phase 1.

## Evidence and navigation

- [Source feasibility](SOURCE_FEASIBILITY.md) — source evidence, legal baseline, validation plan
- [Roadmap](ROADMAP.md) — phase gates
- [Project specification](PROJECT_SPEC.md) — intended contract and metrics
- [Validation](VALIDATION.md) — performed checks vs pending tests
- [Decisions](DECISIONS.md) — recorded scope choices

No Phase 0 closeout or production benchmark exists.

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
| Data access from Kaufland and SPAR | **Confirmed initial access**: both indexes HTTP 200; 6 official CSV files downloaded HTTP 200 spanning 2026-11-16 to 2026-11-18. Format/parsing correctness subject to QA. |
| Current exact GTIN overlap | **8,263 EAN candidates** with valid parsed prices, SPAR Zagreb Jankomir × Kaufland Zagreb Antuna Šoljana 43, 2026-11-17; product/packaging equivalence audit still pending |
| Scrapy spider / PostgreSQL / automation / Tableau | Not implemented |
| Phase 1 authorization | **Not granted** |

## Next authorized action

Complete **same-store, two-date (2026-11-16/17) verification**, investigate missing SPAR price values, and audit 30 EAN-matched products for brand, quantity and variant consistency. Record outputs in [Validation](VALIDATION.md). Update the candidate decision once both live sources and >=100 actual recent matches have been verified. Documentation changes do not authorize coding Phase 1.

## Evidence and navigation

- [Source feasibility](SOURCE_FEASIBILITY.md) — source evidence, legal baseline, validation plan
- [Roadmap](ROADMAP.md) — phase gates
- [Project specification](PROJECT_SPEC.md) — intended contract and metrics
- [Validation](VALIDATION.md) — performed checks vs pending tests
- [Decisions](DECISIONS.md) — recorded scope choices

No Phase 0 closeout or production benchmark exists.

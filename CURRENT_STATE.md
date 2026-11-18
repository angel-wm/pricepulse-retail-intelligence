# Current state

## Current state

**Project status: PHASE 0 — FEASIBILITY IN PROGRESS.** The user approved investigating and documenting a switch to Croatian grocery price intelligence; **no implementation phase has started**.

| Item | Recorded state |
| --- | --- |
| Active work | Phase 0 — candidate-source evaluation and acceptance criteria |
| Last completed phase | None |
| Priority candidate sources | **Kaufland Croatia and SPAR Croatia** — initial download and overlap verified; formal Phase 0 closeout pending targeted QA |
| Initial scope exclusions | Lidl and musical-instrument retailers excluded from the initial source pair |
| Regulatory/publication evidence | Official publication sources and NN 132/2026 reviewed; SPAR general terms section 2.1 restrict reproduction/distribution. Local data testing continues; public release of genuine datasets is on hold pending verified sharing rights. |
| Historical overlap indication | Third-party May 2025 analysis reported >=4,126 common barcodes across six chains excluding Lidl; **not a current local pair measurement** |
| Local feasibility evidence to date | Andertons: 3 product pages HTTP 200 with structured prices; Gear4music: 403; Bonners: 429; GigGear: 405 human verification — all **superseded candidate category**, not tests of grocery sources |
| Data access from Kaufland and SPAR | **Confirmed initial access**: both indexes HTTP 200; 6 official CSV files downloaded HTTP 200 spanning 2026-11-16 to 2026-11-18. Format/parsing correctness subject to QA. |
| Current exact GTIN overlap | **8,263 checksum-valid shared GTIN candidates** with first-pass parsed prices, SPAR Jankomir 8702 × Kaufland Zagreb 5630, 2026-11-17. Sample of 30 found description and unit conflicts; 100 genuine like-for-like matches not formally enumerated. |
| Same-store two-date history | **Initial pass:** SPAR 8702: 28,217 code-stable day-to-day offers (14 rises, 40 falls); Kaufland 5630: 15,533 (9 rises, 69 falls); price parser not yet promotion-aware |\n| SPAR missing-price diagnostic | **Resolved structurally:** all 3,103 blank primary prices on 2026-11-17 had parseable special-price field; final selection semantics pending |\n| Source-population drift | Kaufland 5630 grew from 15,953 to 23,593 listed rows across 2026-11-16/17 (+47.9%); monitor population definitions |\n| Scrapy spider / PostgreSQL / automation / Tableau | Not implemented |
| Phase 1 authorization | **Not granted** |

## Next authorized action

Resolve **price-field semantics for SPAR promotions**, define/validate packaging and brand-equivalence rules on a reviewable >=100-product cohort, and decide public sharing boundaries. Initial access, same-store two-date history and a 30-code anomaly screen are documented in [Validation](VALIDATION.md). No Phase 1 implementation authorization has been given.

## Evidence and navigation

- [Source feasibility](SOURCE_FEASIBILITY.md) — source evidence, legal baseline, validation plan
- [Roadmap](ROADMAP.md) — phase gates
- [Project specification](PROJECT_SPEC.md) — intended contract and metrics
- [Validation](VALIDATION.md) — performed checks vs pending tests
- [Decisions](DECISIONS.md) — recorded scope choices

No Phase 0 closeout or production benchmark exists.

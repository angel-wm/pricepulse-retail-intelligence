# Current state

## Current state

**Project status: PHASE 0 — TECHNICAL FEASIBILITY VALIDATED; CLOSEOUT REVIEW READY.** Kaufland and SPAR have passed bounded source-access, price-history and documentary matching tests. **Formal closeout and Phase 1 implementation are not authorized yet.**

| Item | Recorded state |
| --- | --- |
| Active work | Phase 0 — final evidence and closeout decision |
| Last completed phase | None |
| Priority candidate sources | **Kaufland Croatia and SPAR Croatia** — qualified for planned local engineering by bounded feasibility tests |
| Initial scope exclusions | Lidl and musical-instrument retailers excluded from the initial source pair |
| Regulatory/publication evidence | Official publication sources and NN 132/2026 reviewed; SPAR general terms section 2.1 restrict reproduction/distribution. Local data testing continues; public release of genuine datasets is on hold pending verified sharing rights. |
| Historical overlap indication | Third-party May 2025 analysis reported >=4,126 common barcodes across six chains excluding Lidl; **not a current local pair measurement** |
| Local feasibility evidence to date | Andertons: 3 product pages HTTP 200 with structured prices; Gear4music: 403; Bonners: 429; GigGear: 405 human verification — all **superseded candidate category**, not tests of grocery sources |
| Data access from Kaufland and SPAR | **Confirmed initial access**: both indexes HTTP 200; 6 official CSV files downloaded HTTP 200 spanning 2026-11-16 to 2026-11-18. Format/parsing correctness subject to QA. |
| Current exact GTIN overlap | **8,869** shared priced GTIN candidates on 2026-11-17 (SPAR 8702 × Kaufland 5630); **7,772** present on both dates, **4,155** strict algorithmic candidates. |
| Same-store two-date history | **Promotion-aware initial check:** SPAR 31,277 code-stable entries (14 up, 54 down); Kaufland 15,533 (9 up, 69 down) from 2026-11-16/17. |
| Phase 1 authorization | **Not granted** |

## Next authorized action

**Review and approve Phase 0 closeout.** The initial feasible pair is Kaufland + SPAR Croatia. Design and implement source-specific Scrapy spiders, price-origin fields, versioned file manifests, store identity and parser tests **only after explicit Phase 1 authorization**. Continue to block public release of genuine source observations pending verified sharing rights.

## Evidence and navigation

- [Source feasibility](SOURCE_FEASIBILITY.md) — source evidence, legal baseline, validation plan
- [Roadmap](ROADMAP.md) — phase gates
- [Project specification](PROJECT_SPEC.md) — intended contract and metrics
- [Validation](VALIDATION.md) — performed checks vs pending tests
- [Decisions](DECISIONS.md) — recorded scope choices

No **formal Phase 0 closeout** or production benchmark exists; technical feasibility findings are ready for the approval gate.

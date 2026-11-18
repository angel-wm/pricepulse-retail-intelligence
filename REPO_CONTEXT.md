# Repository context

## Project

- Project: **PricePulse**, a planned Scrapy-based **Croatian grocery price-list intelligence** Data Engineering portfolio project.
- Convention version: **0.1**.
- Description: [README](README.md).
- Work Unit: **phase**; documentation maintenance can occur within the authorized Phase 0 feasibility study.
- Work Model: [roadmap and approval rules](ROADMAP.md#work-model-and-approval-rules).

## Published state

Publication/handoff source: the visible default-branch snapshot, interpreted with [Current state](CURRENT_STATE.md).
Repository/ref: [angel-wm/pricepulse-retail-intelligence](https://github.com/angel-wm/pricepulse-retail-intelligence), default branch `main`; do not assume a retrieved snapshot is the latest.
Remote readers describe only the published snapshot retrieved; unseen local work is **Unknown**. A working tree, commit, or phase closeout is not automatically a published release.

## Source map

| Topic / purpose | Source | Authority | Read when |
| --- | --- | --- | --- |
| Current state | [Current state](CURRENT_STATE.md#current-state) | Implementation and phase-state authority | Status / next steps |
| Planned work | [Roadmap](ROADMAP.md#planned-phases) | Phase order and gates, **not** execution permission | Planning |
| Scope / contract | [Project specification](PROJECT_SPEC.md) | Intended scope, definitions and success criteria | Business questions, contracts |
| Candidate sources / regulatory basis | [Source feasibility](SOURCE_FEASIBILITY.md) | Detailed evidence and pending feasibility gates, **not** proof of operational access | Source selection and matching |
| Architecture | [Architecture](ARCHITECTURE.md) | Intended responsibilities, not implemented code | Design changes |
| Decisions | [Decisions](DECISIONS.md) | Approved directions and explicit provisional choices | Rationale and trade-offs |
| Validation / evidence | [Validation](VALIDATION.md) | Actual checks, outcomes and known gaps | Quality, closeout |
| Repository guidance | [Agent instructions](AGENTS.md); [RDR skill](.agents/skills/repository-documentation-readability/SKILL.md) | Working instructions and presentation style | Documentation changes |

## Loading rules

- Read repository instructions and this map, then relevant documents only.
- Status: begin with `CURRENT_STATE.md`; claims of completed work require matching evidence in `VALIDATION.md`.
- Sources: read `SOURCE_FEASIBILITY.md` and `VALIDATION.md`; do not equate secondary studies with current local tests.
- Planning: read `ROADMAP.md` and the relevant `PROJECT_SPEC.md` scope.
- Architecture: read `ARCHITECTURE.md` and related decisions.
- History: select decisions by ID and follow supersession if present.
- **None** means recorded absence; **Not documented** means no maintained source; **Unknown** means evidence is insufficient.
- Resolve links relative to this map; the map indexes authorities without replacing them.
- Update the source map only when document locations or reading rules change, not for routine test progress.

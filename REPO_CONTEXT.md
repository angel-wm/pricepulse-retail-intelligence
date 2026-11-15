# Repository context

## Project

- Project: **PricePulse**, a planned Scrapy-based retail price intelligence and data engineering portfolio project.
- Convention version: **0.1**.
- Description: [README](README.md).
- Work Unit: **phase**, with documentation maintenance changes recorded separately when needed.
- Work Model: [roadmap and approval rules](ROADMAP.md#work-model-and-approval-rules).

## Published state

Publication/handoff source: the visible default-branch snapshot, interpreted with [current state](CURRENT_STATE.md).
Repository/ref: [angel-wm/pricepulse-retail-intelligence](https://github.com/angel-wm/pricepulse-retail-intelligence), default branch `main`; do not assume a retrieved snapshot is the latest.
Remote readers describe only the published snapshot retrieved; unseen local work is **Unknown**. A working tree, commit, or phase closeout is not automatically a published release. Local readers distinguish uncommitted changes, commits, and verified publication.

## Source map

| Topic / purpose | Source | Authority | Read when |
| --- | --- | --- | --- |
| State / Current Work | [Current state](CURRENT_STATE.md#current-state); select the explicitly active phase, if any | Authoritative for recorded phase state and implementation status | Status questions; selecting active work |
| Last Completed Work | [Current state](CURRENT_STATE.md#current-state), then the phase's closeout reference if one exists | State selects the phase; its closeout establishes recorded completion | Latest completion or a predecessor gate matters |
| Planned Work | [Roadmap](ROADMAP.md#planned-phases), with [approval rules](ROADMAP.md#work-model-and-approval-rules) | Authoritative for phase order and gates, **not** authorization to execute | Planning or defining next steps |
| Project scope | [Project specification](PROJECT_SPEC.md) | Authoritative for documented intended scope and outstanding feasibility questions | Clarifying objectives or boundaries |
| Architecture | [Intended architecture](ARCHITECTURE.md) | Authoritative for the **proposed** design, not implemented behavior | Design questions or impacted changes |
| Decisions | [Decisions](DECISIONS.md); select the relevant decision ID and recorded status | Authoritative for documented choices and rationale | Investigating why a choice was made |
| Validation / Evidence | [Validation](VALIDATION.md), selected by phase and stated baseline | Authority for **recorded** checks only; absent results do not imply a pass | Reviewing quality, evidence, or closeout |
| Repository guidance | [Agent instructions](AGENTS.md) and [installed RDR skill](.agents/skills/repository-documentation-readability/SKILL.md) | Working instructions and documentation presentation guidance | Writing or changing project material |

## Loading rules

- Start with applicable repository instructions and this map. Follow the relevant source links; do not load every file by default.
- For status, read **CURRENT_STATE.md**; expand to a named closeout only if one exists and is relevant.
- For planning, read **CURRENT_STATE.md**, **ROADMAP.md**, and the necessary **PROJECT_SPEC.md** scope; a planned phase is not approval.
- For review, select the active phase from current state, then read that phase's scope and validation evidence. If none is active, report that.
- For architecture, read the relevant part of **ARCHITECTURE.md** and any affected decisions.
- For history, select a decision ID from **DECISIONS.md**; follow a supersession reference if recorded.
- For evidence, select the phase and baseline in **VALIDATION.md**. Do not infer tests from planned checklists.
- Resolve links relative to this map. The source map is an index, not a substitute for source authority.
- **None** means explicitly recorded absence, **Not documented** means no maintained source, and **Unknown** means available information cannot determine the fact.
- When sources conflict, use topic authority, disclose unresolved conflicts, and stop once the task is adequately supported or the gap is identified.
- Update this map only when locations, authority, or loading rules change; update changing project status in **CURRENT_STATE.md**.

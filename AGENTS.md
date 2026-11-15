# Agent instructions

PricePulse is a **documentation-first, phase-gated** project. Do not infer implementation permission from a roadmap, README, or repository initialization.

## Read before working

1. Read [REPO_CONTEXT.md](REPO_CONTEXT.md) for topic authority and task-specific source selection.
2. For status or next steps, read [CURRENT_STATE.md](CURRENT_STATE.md) and [ROADMAP.md](ROADMAP.md).
3. For design work, read the relevant section of [PROJECT_SPEC.md](PROJECT_SPEC.md), [ARCHITECTURE.md](ARCHITECTURE.md), and [DECISIONS.md](DECISIONS.md).
4. For documentation creation or revisions, follow the installed [Repository Documentation Readability skill](.agents/skills/repository-documentation-readability/SKILL.md); load its references progressively.
5. Do not represent intentions as implementations or planned checks as passing evidence.

## Project constraints

- Use Python and Scrapy as the initial scraping approach; avoid introducing Playwright, BeautifulSoup, Scrapling, Selenium, or other scraping frameworks without demonstrated need and explicit user approval.
- Use PostgreSQL for planned persistence and Tableau for planned BI.
- Respect site terms, robots.txt guidance, access controls, request rates, and publication rights. Do not bypass CAPTCHAs, authentication, or anti-bot controls.
- Prefer free, locally reproducible tools, versioned data contracts, explicit provenance, idempotency, and measured reliability.
- Keep project documentation **in English**; discuss decisions with the user **in Spanish** unless asked otherwise.
- A separate Crawlee project must address a distinct technical problem.
- Obtain explicit authorization before starting a development phase, creating runtime infrastructure, scraping any live site, or publishing scraped data.
- Update state, decisions, and validation evidence in their authoritative documents. Update the context map only when sources or reading rules change.

## Handoff discipline

When reporting a result, state what was changed, what was actually validated, what remains planned or unverified, and the next approval gate. For external systems such as Jira, avoid inventing issue IDs or statuses.

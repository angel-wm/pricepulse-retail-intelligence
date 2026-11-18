# Agent instructions

PricePulse is a **documentation-first, phase-gated** project. A written plan, source research or an initialized repository does not authorize Phase 1 implementation.

## Read before working

1. Read [Repository context](REPO_CONTEXT.md) for topic authority.
2. Read [Current state](CURRENT_STATE.md) and [Roadmap](ROADMAP.md) for current phase and next gate.
3. For source work, consult [Source feasibility](SOURCE_FEASIBILITY.md) and [Validation](VALIDATION.md). Distinguish secondary historical evidence from live direct checks.
4. For design, read the relevant [Project specification](PROJECT_SPEC.md), [Architecture](ARCHITECTURE.md) and [Decisions](DECISIONS.md).
5. For documentation, follow [Repository Documentation Readability](.agents/skills/repository-documentation-readability/SKILL.md) and preserve facts, links and phase semantics.

## Project constraints

- Initial source category: Croatian grocery/household price lists. Priority **candidate** pair: Kaufland Croatia and SPAR Croatia; Lidl excluded from the first cohort.
- Use Python and Scrapy as the initial acquisition approach. Do not introduce Playwright, BeautifulSoup, Selenium, Scrapling or other scraping frameworks without technical justification and explicit approval.
- Use PostgreSQL for proposed historical persistence and Tableau as primary BI.
- Handle files, encoding, delimiters, decimal locale, GTIN validity, per-store price context, publication dates and provenance explicitly.
- Do not assume missing products are out of stock; no inventory KPI without source-backed inventory observations.
- Respect source terms, robots.txt, access controls and rate limits; never bypass CAPTCHA, authentication or anti-bot defenses.
- Keep raw data and derived public outputs subject to reviewed sharing rights. The legal provision for automated access is not a blanket redistribution license.
- Prefer free, locally reproducible tooling and measured evidence. Do not invent implementation progress or test results.
- Keep documentation **in English**; communicate with the user **in Spanish**, unless requested otherwise.
- A separate Crawlee project must solve a different problem.
- Authorization to investigate feasibility and update documentation **does not authorize Phase 1 coding, live production scraping, database provisioning or data publication**.

## Handoff discipline

On every work handoff, separate changed documents, actually validated observations, pending tests, and next authorization gate. Never invent Jira issue statuses or code/test results.

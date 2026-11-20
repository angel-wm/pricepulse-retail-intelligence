# Agent instructions

PricePulse is a **documentation-first, phase-gated** project. **Bounded Phase 0 feasibility tests succeeded and the owner formally closed Phase 0 on 2026-11-19**, but separate Phase 1 implementation authorization has **not** been granted. Do not equate tests in user-local temporary scripts with a production spider or pipeline.

## Read before working

1. Read [Repository context](REPO_CONTEXT.md) for topic authority.
2. Read [Current state](CURRENT_STATE.md) and [Roadmap](ROADMAP.md) for current phase and next gate.
3. For source work, consult [Source feasibility](SOURCE_FEASIBILITY.md) and [Validation](VALIDATION.md). Distinguish secondary historical evidence from live direct checks.
4. For design, read the relevant [Project specification](PROJECT_SPEC.md), [Architecture](ARCHITECTURE.md) and [Decisions](DECISIONS.md).
5. For documentation, follow [Repository Documentation Readability](.agents/skills/repository-documentation-readability/SKILL.md) and preserve facts, links and phase semantics.

## Project constraints

- Initial source category: Croatian grocery/household price lists. **Technically qualified source pair:** Kaufland Croatia and SPAR Croatia via bounded Phase 0 tests; Lidl excluded from v1. This is not Phase 1 implementation approval.
- Use Python and Scrapy as the initial acquisition approach. Do not introduce Playwright, BeautifulSoup, Selenium, Scrapling or other scraping frameworks without technical justification and explicit approval.
- Use PostgreSQL for proposed historical persistence and Tableau as primary BI.
- Handle source files and manifests, encoding/delimiters (SPAR cp1250/semicolon; Kaufland UTF-8 BOM/tab), locale decimals, source price field/origin, GTIN checks, package/variant exceptions, stable per-store identity, publication dates and raw file hashes explicitly.
- Do not assume missing products are out of stock; **no stock/availability KPI** without source-backed inventory observations. Do not interpret a blank SPAR regular-price field as an unpriced product if the special-price field is valid.
- Respect source terms, robots.txt, access controls and rate limits; never bypass CAPTCHA, authentication or anti-bot defenses.
- Keep raw files, product names, codes and retailer-specific prices out of public GitHub/Tableau assets unless their reuse rights are verified. A synthetic portfolio demo is preferable; the legal automated-access mandate is not a blanket redistribution license.
- Prefer free, locally reproducible tooling and measured evidence. Do not invent implementation progress or test results.
- Keep documentation **in English**; communicate with the user **in Spanish**, unless requested otherwise.
- A separate Crawlee project must solve a different problem.
- The owner **explicitly approved formal Phase 0 closeout** and synchronization of GitHub/Jira on **2026-11-19**, but explicitly **did not authorize Phase 1 coding**, scheduled production scraping, database provisioning, or data publication.

## Handoff discipline

On every work handoff, separate changed documents, actually validated observations, pending tests, and next authorization gate. Never invent Jira issue statuses or code/test results.

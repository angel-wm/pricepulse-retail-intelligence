# Intended architecture

**Status: proposed only.** No component or integration below is implemented or tested.

## Data flow

```text
Approved public retail source
            |
            v
      Scrapy spider
  (respect access policy)
            |
            v
  Structured observations
            |
            v
 Validation / normalization
            |
            v
 PostgreSQL ingestion layer
            |
            v
  Historical observation
   model + SQL analytics
            |
            v
   Tableau Desktop Free
     (local analysis)
            |
            v
 Tableau Public (optional,
 shareable export only)
```

The pipeline should retain source provenance and capture time so historical observations can be traced. The model must separate logical product identity, source-specific offers, and observed prices. Exact schema and keys are **to be designed**, not assumed.

## Responsibilities

| Component | Responsibility | Exclusion |
| --- | --- | --- |
| Scrapy | Crawl approved pages and extract source records | Does not decide cross-retailer equivalence |
| Validation / normalization | Apply explicit field and data-quality contracts | Does not silently discard unexpected records |
| PostgreSQL | Store validated records and history with deduplication rules | Does not invent missing prices |
| Python / SQL analytics | Build reproducible reporting definitions | Does not claim unmatched offers are the same product |
| Tableau | Explore and communicate validated measures | Does not replace source-quality checks |
| GitHub Actions (if suitable) | Run bounded tests or scheduling | Not a requirement to use paid or fragile live scraping CI |

## Architectural decision boundaries

- Start with **Scrapy alone**; add browser automation only if Phase 0/1 evidence demonstrates a concrete need and the user approves the change.
- Prefer local-first, free tools and explicit batch history over premature streaming or cloud orchestration.
- Keep credentials outside Git and private observations out of public dashboards unless publication rights are verified.
- Keep **Crawlee** work in a separate future project with a different engineering objective.

See [decision log](DECISIONS.md) for selected directions and [roadmap](ROADMAP.md) for implementation gates.

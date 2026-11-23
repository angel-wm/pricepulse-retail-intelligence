# Tableau analytics: work in progress

Phase 4 is authorized. Its target is a private Tableau dashboard using real retailer data. Phase 2 is closed. Phase 3 still awaits owner review.

## Private real-data workbook

Open `data/pricepulse-coverage-private-en.twbx` in Tableau Desktop. The English portfolio dashboard shows the four approved cross-store comparisons. Selecting a product in the price chart filters the gap chart to that product. Clearing the selection restores the four comparisons.

The expanded workbook includes 112,170 listed-price observations across both stores and both dates. **Price catalog** exposes individual observations. **Catalog coverage** shows counts by store and date. **Product price history** and **Price changes by store** cover the 17,803 same-store SKU comparisons returned by PostgreSQL for 17 to 23 November. These include unchanged prices. Raw retailer product titles are preserved as published.

The private review lists in `data/tableau-real-private/expanded/` rank additional same-date cross-store candidates. Start with the pairs whose brand and declared mass agree and whose remaining flag is the description or variant. Identity review is still required for each selected pair and exact file version.

The portfolio screenshot is stored locally at `data/phase4-check/pricepulse-portfolio-private-en.png`.

The workbook uses captures from SPAR 8702 and Kaufland 5630 for 17 and 23 November 2026. The full PostgreSQL export stays in ignored `data/tableau-real-private/`. Review decisions apply to exact file versions, so the 23 November observations do not carry forward the earlier approvals.

The supporting worksheets display same-store price changes and one record per store and date for coverage and freshness. The focused history has 16 priced rows for two dates. Four same-store changes satisfy the SQL identity and exception rules in that cohort. The quality worksheets describe all four source files. The 6-day gap is an interval between selected file dates. It does not describe a daily series or guarantee publication at a particular time.

The real workbook and screenshot are private. A future GitHub release needs a verified rights basis for retailer information shown in the image and embedded in the packaged workbook.

## Private analytical export

With a private database initialized and populated as described in [PostgreSQL](POSTGRESQL.md), choose explicit source-file IDs, at most one version for each chain, store and date. Set `PRICEPULSE_DSN` privately, then run for example:

```powershell
uv run --locked python -m pricepulse.analytics --file-id 1 --file-id 2 --directory data/tableau-private --as-of 2026-11-23
```

The IDs and reference date are examples, not verified source records. An invalid, duplicate or conflicting file selection fails before writing CSVs. The output may contain genuine retailer names, codes and prices: keep it private and do not commit, upload or publish it. The public portfolio data approach remains undecided; a separate, clearly labelled synthetic dataset is one option.

| Export | Grain and meaning |
| --- | --- |
| `observations.csv` | One priced source row in each selected file; includes store, date, product identifiers and regular/special origin. It includes rows that might have review exceptions, so it is not a verified cohort. |
| `changes.csv` | Adjacent selected observations for stable, exception-free same-store SKU and matching valid GTIN and descriptors. Differences are EUR; dates need not be consecutive calendar days. |
| `comparisons.csv` | Explicitly verified, exception-free same-date cross-chain pairs from selected file versions. `price_difference` is left minus right in EUR. Pair orientation is the recorded review orientation. |
| `quality.csv` | One selected file: priced and valid-GTIN rows divided by its source row count, with the reference date and file age in days. An empty file has an undefined fraction. File age uses the price-list date, not an observed publication timestamp. |

The same verified-pair rules and version guard used by Phase 2 apply here. GTIN checksum and descriptor review do not establish manufacturer certification. These exports do not prove stock availability. `price_changes` considers the preceding **selected** observation, so selecting a subset changes the comparison interval. See [Reliability](RELIABILITY.md) for the separate eligible-queued-pair coverage denominator; it is not full-catalogue overlap.

Tableau inferred normalized GTIN as a number when the CSV was opened. Change identifiers to text before using them in a view or join, so leading zeroes are preserved; use exact product/store/date grain and avoid summing prices across products or days.

## Fictional demo and local draft

The CSV files in `examples/tableau_synthetic` are generated from invented products and prices by `python -m pricepulse.synthetic_demo`, using `PRICEPULSE_TEST_DSN` for a disposable PostgreSQL database and a temporary schema. The named chains and store IDs define the demonstration context; values are not retailer observations. Synthetic match decisions are simulated, not a real review. The fixture comprises 24 observations, 16 changes, 12 matched pairs and six file-quality records; automated PostgreSQL tests check those counts and the fictional EUR -0.10 spreads.

Tableau Desktop Free Edition opened the fictional observations and displayed a preliminary price-history worksheet by date, chain and product and a second worksheet of same-day differences. Both were assembled into a preliminary dashboard. The 12 displayed fictional differences of -0.10 EUR agree with the exported synthetic comparison rows; filters and other measures have not been reconciled. A private draft was saved under `data/pricepulse-phase4-draft.twb`; it is an incomplete dashboard and is not fully validated. The installed edition explicitly says it cannot share or publish assets. [Tableau's edition comparison](https://help.tableau.com/current/pro/desktop/en-us/desktop_comparison.htm) and [Tableau Public FAQ](https://help.tableau.com/current/pro/desktop/en-us/public_faq.htm) distinguish this edition from the free Public authoring option. Do not share the Desktop Free draft; use an appropriate separately selected public authoring route for any synthetic demonstration.

## Outstanding work

Review the real workbook with the owner, confirm any remaining interactive filter scenarios and agree on the final presentation. Additional real pairs can be added after their exact file versions are reviewed. The Phase 4 closeout remains a separate owner decision.

# Tableau analytics: work in progress

Phase 4 is authorized. Its dashboard and SQL-to-Tableau reconciliation are not yet complete. Phase 2 and Phase 3 still await owner review.

## Private analytical export

With a private database initialized and populated as described in [PostgreSQL](POSTGRESQL.md), choose explicit source-file IDs, at most one version for each chain, store and date. Set `PRICEPULSE_DSN` privately, then run for example:

```powershell
uv run --locked python -m pricepulse.analytics --file-id 1 --file-id 2 --directory data/tableau-private --as-of 2026-11-23
```

The IDs and reference date are examples, not verified source records. An invalid, duplicate or conflicting file selection fails before writing CSVs. The output may contain genuine retailer names, codes and prices: keep it private and do not commit, upload or publish it. Use a separate, clearly labelled synthetic dataset for any public demonstration.

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

Tableau Desktop Free Edition opened the fictional observations and displayed a preliminary price-history worksheet by date, chain and product. A private draft was saved under `data/pricepulse-phase4-draft.twb`; it is incomplete and is not a validated dashboard. The installed edition explicitly says it cannot share or publish assets. [Tableau's edition comparison](https://help.tableau.com/current/pro/desktop/en-us/desktop_comparison.htm) and [Tableau Public FAQ](https://help.tableau.com/current/pro/desktop/en-us/public_faq.htm) distinguish this edition from the free Public authoring option. Do not share the Desktop Free draft; use an appropriate separately selected public authoring route for any synthetic demonstration.

## Outstanding work

Complete the Tableau workbook, reconcile displayed results and filters with the exported SQL, and review presentation and sharing rights before publishing. No public dashboard or source-data publication is claimed.

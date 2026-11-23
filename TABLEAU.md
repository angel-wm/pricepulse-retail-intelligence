# Tableau analytics

The private English dashboard covers three Zagreb stores on 17 and 23 November 2026. It uses exact file versions exported from local PostgreSQL.

## Three-source workbook

Open `data/pricepulse-three-sources-private-en.twbx` in Tableau Desktop. Use **Price catalog** for the 165,322 listed prices, **Catalog coverage** for the six store-date counts, and **Product price history** for the 41,363 same-store comparisons, including unchanged prices.

The opening dashboard shows four products reviewed across all three stores on 23 November. It shows each listed price and the spread between the highest and lowest prices. The database holds 12 pair decisions for these four three-store products plus four earlier SPAR–Kaufland decisions. These are documentary checks of the published GTIN, brand, variant, package and price context for the selected rows.

The screenshot, SQL exports and private review inputs are under `data/three-source-private/`. Keep the packaged workbook, screenshot and exports local.

## Original Phase 4 snapshot

Open `data/pricepulse-coverage-private-en.twbx` in Tableau Desktop. The English portfolio dashboard shows the four approved cross-store comparisons. Selecting a product in the price chart filters the gap chart to that product. Clearing the selection restores the four comparisons.

The expanded workbook includes 112,170 listed-price observations across both stores and both dates. **Price catalog** exposes individual observations. **Catalog coverage** shows counts by store and date. **Product price history** and **Price changes by store** cover the 17,803 same-store SKU comparisons returned by PostgreSQL for 17 to 23 November. These include unchanged prices. Raw retailer product titles are preserved as published.

The private review lists in `data/tableau-real-private/expanded/` rank additional same-date cross-store candidates. Start with the pairs whose brand and declared mass agree and whose remaining flag is the description or variant. Identity review is still required for each selected pair and exact file version.

The portfolio screenshot is stored locally at `data/phase4-check/pricepulse-portfolio-private-en.png`.

The full PostgreSQL export stays in ignored `data/tableau-real-private/`. Review decisions apply to exact file versions, so the 23 November observations do not carry forward the earlier approvals.

The supporting worksheets display same-store price changes and one record per store and date for coverage and freshness. The focused history has 16 priced rows for two dates. Four same-store changes satisfy the SQL identity and exception rules in that cohort. The quality worksheets describe all four source files. The 6-day gap is an interval between selected file dates. It does not describe a daily series or guarantee publication at a particular time.

The real workbook and screenshot are private. A future GitHub release needs a verified rights basis for retailer information shown in the image and embedded in the packaged workbook.

## Data attribution

> PricePulse analyzes official retail price lists published by SPAR Croatia (Zagreb Jankomir, store 8702) Kaufland Croatia (Zagreb Antuna Šoljana, store 5630), and Konzum Croatia (Zagreb Velimira Škorpika, store 1280), dated 17 and 23 November 2026. The three-store reviewed set uses the 23 November lists.

The official pages are the source links for a portfolio description or screenshot caption. [SPAR price lists](https://www.spar.hr/usluge/cjenici) · [Kaufland price lists](https://www.kaufland.hr/akcije-novosti/popis-mpc.html) · [Konzum price lists](https://www.konzum.hr/cjenici)

## Metric definitions and filter scope

| Measure | Calculation and cohort |
| --- | --- |
| Listed price | Resolved price in EUR for one store, selected file date and source SKU. Use a valid regular or special amount when the other field is blank, or the common amount when both valid values agree. Invalid, missing or conflicting prices do not enter the priced catalog. |
| Same-store price change | Current price minus previous price for the preceding selected observation of the same store/SKU, with matching valid GTIN and unchanged descriptors. Positive means an increase. Zero counts as unchanged. |
| Three-store price spread | Highest listed price minus lowest listed price for a product reviewed at all three selected stores on the same date. |
| Pair price difference | Left price minus right price in the recorded review orientation for the exact, same-date source rows. A positive value means the right-hand store costs less. |
| Relative change and gap | If calculated for analysis, divide same-store change by the previous price and cross-store gap by the right-hand comparison price. Multiply by 100 and omit a percentage if the denominator is missing or zero. The private workbook displays the absolute EUR values. |
| File quality | Priced and valid-GTIN row counts divided by the source row count. File age is the reference date minus the price-list date. Quality counts describe the file. |

The opening dashboard filters its gap chart by selected product. Its summary callouts describe the full reviewed cohort. The **Price catalog** has store, date and product filters. Each chain identifies one physical store in this snapshot. **Reviewed product prices** also carries a store ID filter. The catalog shows the regular, special or equal-dual-price origin as **Price type**. The current package has no dedicated promotion filter or category field. See the [technical review](VALIDATION.md#phase-5-technical-review--2026-11-23) for the tested interactions and their scope.

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

The CSV files in `examples/tableau_synthetic` are generated from invented products and prices by `python -m pricepulse.synthetic_demo`, using `PRICEPULSE_TEST_DSN` for a disposable PostgreSQL database and a temporary schema. The named chains and store IDs define the demonstration context; values are not retailer observations. Synthetic match decisions are simulated, not a real review. The fixture comprises 36 observations, 24 changes, 36 reviewed pairs and nine file-quality records. PostgreSQL tests check the counts and the three retailer-pair differences.

An earlier two-store draft in Tableau Desktop Free Edition opened the fictional observations and displayed a preliminary price-history worksheet by date, chain and product and a second worksheet of same-day differences. Both were assembled into a preliminary dashboard. The 12 displayed fictional differences of -0.10 EUR agree with the exported synthetic comparison rows; filters and other measures have not been reconciled. A private draft was saved under `data/pricepulse-phase4-draft.twb`; it is an incomplete dashboard and is not fully validated. The installed edition explicitly says it cannot share or publish assets. [Tableau's edition comparison](https://help.tableau.com/current/pro/desktop/en-us/desktop_comparison.htm) and [Tableau Public FAQ](https://help.tableau.com/current/pro/desktop/en-us/public_faq.htm) distinguish this edition from the free Public authoring option. Do not share the Desktop Free draft; use an appropriate separately selected public authoring route for any synthetic demonstration.

## Refresh and expansion

The Windows task collects source files. To update Tableau, load the selected captures into PostgreSQL, verify cross-store pairs for those exact file versions, and rerun the private analytical export. Refresh the workbook's packaged sources and the derived chart inputs, update the summary callouts, reconcile counts and gaps in Desktop, and save a new package and screenshot. The current workbook uses curated presentation inputs, so replacing the four core exports alone does not update every view. An automated collection-to-dashboard refresh remains follow-up work.

The catalog already includes all priced observations from the four selected files. Expand cross-store coverage in private review batches, starting with the prioritized candidates above. A candidate becomes a confirmed comparison after an explicit review decision for the selected files.

Public portfolio delivery remains open under PULSE-23. See [Source feasibility](SOURCE_FEASIBILITY.md) for the sharing constraint and [Validation](VALIDATION.md) for the private closeout evidence.

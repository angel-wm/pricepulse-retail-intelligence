# Tableau analytics

The private English dashboard covers three Zagreb stores on 17 and 23 November 2026. It uses exact file versions exported from local PostgreSQL.

## Private Tableau workbook

Open `data/tableau/PricePulse - Three-Store Price Comparison - Private.twbx`
in Tableau Desktop. The matching PNG has the same filename stem. This is the
sole dashboard and contains its CSV data within the package. The private
rebuild starts from this workbook, the PostgreSQL export and the local review
records. The original two-store Tableau package and screenshot were retired.

**Price catalog** shows 165,322 listed prices, including offers from products
listed by only one store. **Catalog coverage** shows all six store-date
counts and **Product price history** shows 41,363 same-store comparisons,
including unchanged prices.

The opening dashboard compares 13,700 barcodes across at least two stores on
23 November 2026. Of those, 5,961 appear at all three stores and 7,739
appear at two. Enter part of a product name or a barcode in **Search** and
press Enter. Clear the field and press Enter to restore all results. The
three retailer columns stay visible. A dash means there is no comparable
priced listing in that store's selected file.

**Barcode match** indicates a shared normalized code with one priced listing
per participating store. **Verified** identifies the four products that also
passed manual product, variant and pack review. Their charts appear below the
searchable table. The supporting pair worksheet includes their 12 reviewed
pairs and four historical SPAR–Kaufland decisions.

## Data attribution

> PricePulse analyzes official retail price lists published by SPAR Croatia (Zagreb Jankomir, store 8702), Kaufland Croatia (Zagreb Antuna Šoljana, store 5630), and Konzum Croatia (Zagreb Velimira Škorpika, store 1280), dated 17 and 23 November 2026. The three-store reviewed set uses the 23 November lists.

The official pages are the source links for a portfolio description or screenshot caption. [SPAR price lists](https://www.spar.hr/usluge/cjenici) · [Kaufland price lists](https://www.kaufland.hr/akcije-novosti/popis-mpc.html) · [Konzum price lists](https://www.konzum.hr/cjenici)

## Metric definitions and filter scope

| Measure | Calculation and cohort |
| --- | --- |
| Listed price | Resolved price in EUR for one store, selected file date and source SKU. Use a valid regular or special amount when the other field is blank, or the common amount when both valid values agree. Invalid, missing or conflicting prices do not enter the priced catalog. |
| Same-store price change | Current price minus previous price for the preceding selected observation of the same store/SKU, with matching valid GTIN and unchanged descriptors. Positive means an increase. Zero counts as unchanged. |
| Price spread | Highest listed price minus lowest listed price among the stores shown for the same code and date. The manually verified charts use all three stores. |
| Pair price difference | Left price minus right price in the recorded review orientation for the exact, same-date source rows. A positive value means the right-hand store costs less. |
| Relative change and gap | If calculated for analysis, divide same-store change by the previous price and cross-store gap by the right-hand comparison price. Multiply by 100 and omit a percentage if the denominator is missing or zero. The private workbook displays the absolute EUR values. |
| File quality | Priced and valid-GTIN row counts divided by the source row count. File age is the reference date minus the price-list date. Quality counts describe the file. |

Search filters the barcode table. The summary cards describe the full
23 November comparison set. Selecting a product in the manually verified
price chart filters its spread chart. The **Price catalog** has store, date
and product filters. Each chain identifies one physical store in this
snapshot. The catalog shows the regular, special or equal-dual-price origin
as **Price type**. See the [barcode explorer validation](VALIDATION.md#tableau-barcode-explorer--2026-11-24)
for the search checks.

## Private analytical export

With a private database initialized and populated as described in [PostgreSQL](POSTGRESQL.md), choose explicit source-file IDs, at most one version for each chain, store and date. Set `PRICEPULSE_DSN` privately, then run for example:

```powershell
uv run --locked python -m pricepulse.analytics --file-id 1 --file-id 2 --directory data/tableau-private --as-of 2026-11-23
```

The IDs and reference date are examples, not verified source records. An invalid, duplicate or conflicting file selection fails before writing CSVs. The output may contain genuine retailer names, codes and prices: keep it private and do not commit, upload or publish it. The portfolio is based on real observations. Review reuse rights for the exact workbook, image or extract before release.

| Export | Grain and meaning |
| --- | --- |
| `observations.csv` | One priced source row in each selected file; includes store, date, product identifiers and regular/special origin. It includes rows that might have review exceptions, so it is not a verified cohort. |
| `changes.csv` | Adjacent selected observations for stable, exception-free same-store SKU and matching valid GTIN and descriptors. Differences are EUR; dates need not be consecutive calendar days. |
| `comparisons.csv` | Explicitly verified, exception-free same-date cross-chain pairs from selected file versions. `price_difference` is left minus right in EUR. Pair orientation is the recorded review orientation. |
| `quality.csv` | One selected file: priced and valid-GTIN rows divided by its source row count, with the reference date and file age in days. An empty file has an undefined fraction. File age uses the price-list date, not an observed publication timestamp. |

The same verified-pair rules and version guard used by Phase 2 apply here. GTIN checksum and descriptor review do not establish manufacturer certification. These exports do not prove stock availability. `price_changes` considers the preceding **selected** observation, so selecting a subset changes the comparison interval. See [Reliability](RELIABILITY.md) for the separate eligible-queued-pair coverage denominator; it is not full-catalogue overlap.

Tableau inferred normalized GTIN as a number when the CSV was opened. Change identifiers to text before using them in a view or join, so leading zeroes are preserved; use exact product/store/date grain and avoid summing prices across products or days.

## Public portfolio

The owner selected a real-data-only portfolio. The GitHub documentation uses
measured results and cites the retailers' official price-list pages. Publishing
the genuine packaged workbook, screenshot or data extracts remains pending
verification of the reuse basis for the exact artifacts. See
[PULSE-23](https://angel231995.atlassian.net/browse/PULSE-23) and the
[source assessment](SOURCE_FEASIBILITY.md).

## Refresh and expansion

The Windows task collects source files. To update Tableau, load the selected captures into PostgreSQL, verify cross-store pairs for those exact file versions, and rerun the private analytical export. Refresh the workbook's packaged sources and the derived chart inputs, update the summary callouts, reconcile counts and gaps in Desktop, and save a new package and screenshot. The current workbook uses curated presentation inputs, so replacing the four core exports alone does not update every view. An automated collection-to-dashboard refresh remains follow-up work.

The catalog includes all priced observations from the six selected files. The
barcode comparison table uses the same-day subset described above. Expand
verified coverage through private review batches for the selected files.

Public portfolio delivery remains open under PULSE-23. See [Source feasibility](SOURCE_FEASIBILITY.md) for the sharing constraint and [Validation](VALIDATION.md) for the private closeout evidence.

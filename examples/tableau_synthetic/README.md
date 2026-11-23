# Synthetic Tableau example

All products, identifiers, prices and review decisions in these CSV files are fictional. Retailer and store labels provide illustrative context only.

## Inspect in Tableau

Open `comparisons.csv` as a text file data source. Put `left_chain`, `right_chain`, `price_list_date` and `left_sku` on Rows, then add `price_difference` to Text. Use a discrete exact date and text SKU fields. Expect 36 records across three dates, with 12 per retailer pair. Left-minus-right differences are −€0.10 for SPAR–Kaufland, €0.05 for SPAR–Konzum and €0.15 for Kaufland–Konzum. The companion files contain 36 price observations, 24 same-store comparisons and nine file-quality records. See [Tableau analytics](../../TABLEAU.md#private-analytical-export) for each file's grain.

## Regenerate from PostgreSQL

From the repository root, set `PRICEPULSE_TEST_DSN` to a [disposable PostgreSQL database](../../POSTGRESQL.md#validation), then run:

```powershell
uv run --locked python -m pricepulse.synthetic_demo
git diff --exit-code -- examples/tableau_synthetic/*.csv
```

The generator creates a temporary schema and rewrites these four CSVs. A clean diff confirms that the generated fixtures match the repository version.

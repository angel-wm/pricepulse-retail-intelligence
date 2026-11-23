# Synthetic Tableau example

All products, identifiers, prices and review decisions in these CSV files are fictional. Retailer and store labels provide illustrative context only.

## Inspect in Tableau

Open `comparisons.csv` as a text file data source. Put `price_list_date` and `left_sku` on Rows and add `price_difference` to Text. Use the exact date as a discrete dimension and set SKU fields to text. Expect 12 records across three dates, each with a left-minus-right gap of −€0.10. The companion files contain 24 price observations, 16 same-store comparisons and six file-quality records. See [Tableau analytics](../../TABLEAU.md#private-analytical-export) for each file's grain.

## Regenerate from PostgreSQL

From the repository root, set `PRICEPULSE_TEST_DSN` to a [disposable PostgreSQL database](../../POSTGRESQL.md#validation), then run:

```powershell
uv run --locked python -m pricepulse.synthetic_demo
git diff --exit-code -- examples/tableau_synthetic/*.csv
```

The generator creates a temporary schema and rewrites these four CSVs. A clean diff confirms that the generated fixtures match the repository version.

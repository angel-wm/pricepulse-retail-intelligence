# Bounded acquisition

The two Scrapy spiders select exactly one fixed store and one requested publication date. The output contains retailer data and must remain private; `data/` and `.jl` files are ignored by Git. Source access does not grant redistribution rights.

Install with `uv sync --locked`, create the `data` directory, then run from the repository root (choose an available date):

```powershell
uv run scrapy crawl spar -a date=2026-11-17 -O data/spar.jl
uv run scrapy crawl kaufland -a date=2026-11-17 -O data/kaufland.jl
uv run pytest -q
```

The spiders obey robots.txt, use one concurrent request, a delay and limited retries, reject cross-domain URLs and redirects, and do not bypass access controls. SPAR uses store 8702 and Kaufland 5630. A missing, duplicated or changed index entry stops acquisition. Dates and store IDs are selected from source filenames; retrieval time is separate and no publication timestamp is invented. Historical files may expire.

Each JSON Lines feed starts with a `manifest` containing source, store, requested file date, URL, retrieval time in UTC, HTTP status, SHA-256, dialect and row count. SPAR's supplied hash is also checked when present. Following `record` entries retain raw columns, source URL/hash, row number, date and store, raw and checksum-validated GTIN (14-digit normalized when valid), price fields and status. Price strings use decimal points. The regular or special price is selected when alone, or when both agree; different, missing or invalid prices are flagged and have no effective price. Package and variant identity are not inferred. Unknown required or duplicate headers and malformed rows stop parsing; additional columns are retained in the raw row.

Inspect the manifest and Scrapy logs after every run: Scrapy can return exit code zero even when a spider closes early. A failed request, blocked robots policy, schema change or absent manifest is not a successful acquisition. This prototype does not persist raw files, provide durable failure manifests, schedule runs, or guarantee completeness. See [Validation](VALIDATION.md) for the bounded evidence and remaining work.

# Bounded acquisition

The three Scrapy spiders select exactly one fixed store and one requested publication date. The output contains retailer data and must remain private; `data/` and `.jl` files are ignored by Git. Source access does not grant redistribution rights.

Install with `uv sync --locked`, create the `data` directory, then run from the repository root (choose an available date):

```powershell
uv run scrapy crawl spar -a date=2026-11-17 -O data/spar.jl
uv run scrapy crawl kaufland -a date=2026-11-17 -O data/kaufland.jl
uv run scrapy crawl konzum -a date=2026-11-17 -O data/konzum.jl
uv run python -m pytest -q
```

The checks-only GitHub Actions workflow runs the synthetic tests on pushes and pull requests using locked dependencies. It does not download live retailer data. Check [Validation](VALIDATION.md) for actual hosted-run evidence; the presence of a workflow alone does not prove it has passed on GitHub.

The spiders obey robots.txt, use at most one concurrent request per domain, a one-second delay, a 30-second timeout and at most two retries for transient errors (HTTP 408, 500, 502, 503 or 504 and Scrapy's retryable transport exceptions). They do not retry HTTP 403, 404 or 429; access restrictions and rate limits stop the run. Redirects, refresh redirects, non-HTTPS and cross-domain source links are rejected. Incomplete responses are rejected. The fixed stores are SPAR 8702, Kaufland 5630 and Konzum 1280. A missing, duplicated or changed index entry stops acquisition. Dates and store IDs are selected from source filenames; retrieval time is separate and no publication timestamp is invented. Historical files may expire.

Scrapy logs distinguish forbidden, missing and rate-limited responses, other HTTP and transport failures, malformed indexes, incomplete responses and file schema or hash errors. Review the `finish_reason`, downloader request and status counts, retry counts, robots statistics and manifest after each run. If robots.txt cannot be retrieved with HTTP 200, the custom middleware denies source requests and logs `pricepulse/robots_unavailable`.

Each JSON Lines feed starts with a `manifest` containing source, store, requested file date, URL, retrieval time in UTC, HTTP status, SHA-256, dialect and row count. SPAR's supplied hash is also checked when present. Following `record` entries retain raw columns, source URL/hash, row number, date and store, raw and checksum-validated GTIN (14-digit normalized when valid), price fields and status. Price strings use decimal points. The regular or special price is selected when alone, or when both agree; different, missing or invalid prices are flagged and have no effective price. Package and variant identity are not inferred. Unknown required or duplicate headers and malformed rows stop parsing; additional columns are retained in the raw row.

Successful manifests include discovery counts: total entries in the index, selected files for the requested store/date and fetched files. The index scopes differ by retailer: the SPAR index is date-specific, whereas the Kaufland index may contain multiple dates. Do not compare their total entry counts as store or product coverage.

SPAR uses semicolon-delimited CP1250 CSV in both observed layouts. Its older
layout provides separate regular and special amounts. The layout observed on
25 November 2026 puts the promotion indicator immediately after the listed
price and includes an anchor-price column. `NE` identifies a regular price
and `DA` identifies a promotional price. The anchor price stays in the raw
row. Category is optional and is null when its column is absent.

Kaufland filenames have two observed store/date layouts. The older layout puts `DDMMYYYY` after the store ID. The newer layout inserts the price-list descriptor and a numeric field before `YYYYMMDD`, followed by a four-digit time. The collector checks both layouts and requires one unambiguous match. See [Validation](VALIDATION.md) for the recorded filename change and manual recovery.

Konzum uses a dated HTML index and a comma-delimited UTF-8 CSV. The spider deduplicates repeated links to the same file and requires one file for store 1280 and the requested date. The retail-price column supplies the listed price. The promotion indicator routes it to the regular field (`NE`) or special field (`DA`). Unknown indicators are price exceptions. The promotion label, reference price and unit price remain in the raw row. Promotion eligibility still requires review for like-for-like comparisons.

Inspect the manifest and Scrapy logs after every run: Scrapy can return exit code zero even when a spider closes early. A failed request, blocked robots policy, schema change or absent manifest is not a successful acquisition. Use the [journaled collector](RELIABILITY.md#run-evidence) when you need raw files, a run report and feed completeness checks. See [Validation](VALIDATION.md) for the bounded evidence and remaining work.

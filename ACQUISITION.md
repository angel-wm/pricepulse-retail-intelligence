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

The spiders obey robots.txt, use at most one concurrent request per domain, a one-second delay, a 30-second timeout and at most two retries for transient errors (HTTP 408, 500, 502, 503 or 504 and Scrapy's retryable transport exceptions). Index and CSV requests stop on HTTP 403, 404 or 429 without retrying. Redirects, refresh redirects, non-HTTPS URLs and unapproved hosts are rejected. Konzum may link directly to its single approved CDN host, where the crawler checks robots.txt independently. Incomplete responses are rejected. The fixed stores are SPAR 8702, Kaufland 5630 and Konzum 1280. A missing, duplicated or changed index entry stops acquisition. Dates and store IDs are selected from source filenames; retrieval time is separate and no publication timestamp is invented. Historical files may expire.

Scrapy logs distinguish forbidden, missing and rate-limited responses, other HTTP and transport failures, malformed indexes, incomplete responses and file schema or hash errors. Review the `finish_reason`, downloader request and status counts, retry counts, robots statistics and manifest after each run. The middleware honors rules returned with HTTP 200. Other responses and retrieval errors deny requests and record `pricepulse/robots_unavailable`, except for HTTP 403 on robots.txt for the exact Konzum CDN host during a Konzum crawl. That response is treated as an unavailable robots file under [RFC 9309 §2.3.1.3](https://www.rfc-editor.org/rfc/rfc9309.html#section-2.3.1.3) and records `pricepulse/konzum_cdn_robots_unavailable`. Konzum identifies the publicly linked CSVs as suitable for automated processing. [Konzum price-list index](https://www.konzum.hr/cjenici)

Each JSON Lines feed starts with a `manifest` containing source, store, requested file date, URL, retrieval time in UTC, HTTP status, SHA-256, dialect and row count. SPAR's supplied hash is also checked when present. Following `record` entries retain raw columns, source URL/hash, row number, date and store, raw and checksum-validated GTIN (14-digit normalized when valid), price fields and status. Price strings use decimal points. The regular or special price is selected when alone, or when both agree; different, missing or invalid prices are flagged and have no effective price. Package and variant identity are not inferred. Unknown required or duplicate headers and malformed rows stop parsing; additional columns are retained in the raw row.

Successful manifests include discovery counts: total entries in the index, selected files for the requested store/date and fetched files. The index scopes differ by retailer: the SPAR index is date-specific, whereas the Kaufland index may contain multiple dates. Do not compare their total entry counts as store or product coverage.

SPAR uses semicolon-delimited CP1250 CSV in both observed layouts. Its older
layout provides separate regular and special amounts. The layout observed on
25 November 2026 puts the promotion indicator immediately after the listed
price and includes an anchor-price column. `NE` identifies a regular price
and `DA` identifies a promotional price. The anchor price stays in the raw
row. Category is optional and is null when its column is absent.

Kaufland filenames have two observed store/date layouts. The older layout puts `DDMMYYYY` after the store ID. The newer layout inserts the price-list descriptor and a numeric field before `YYYYMMDD`, followed by a four-digit time. The collector checks both layouts and requires one unambiguous match. See [Validation](VALIDATION.md) for the recorded filename change and manual recovery.

Konzum uses a dated HTML index and a comma-delimited UTF-8 CSV. The spider deduplicates repeated URLs and requires one file for store 1280 and the requested date across both legacy download links and direct CDN links. For a CDN link, the date prefix and embedded date must both match. The scheduler uses the same scoped robots policy as the manual collector. Review the logs when either policy or a file response blocks the download. See [operational evidence](VALIDATION.md#phase-3-operational-review--2026-11-27). The retail-price column supplies the listed price. The promotion indicator routes it to the regular field (`NE`) or special field (`DA`). Unknown indicators are price exceptions. The promotion label, reference price and unit price remain in the raw row. Promotion eligibility still requires review for like-for-like comparisons.

Inspect the manifest and Scrapy logs after every run: Scrapy can return exit code zero even when a spider closes early. A failed request, blocked robots policy, schema change or absent manifest is not a successful acquisition. Use the [journaled collector](RELIABILITY.md#run-evidence) when you need raw files, a run report and feed completeness checks. See [Validation](VALIDATION.md) for the bounded evidence and remaining work.

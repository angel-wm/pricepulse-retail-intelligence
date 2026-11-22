# Local PostgreSQL historical data

Phase 2 code loads a locally held source CSV into a private, dedicated PostgreSQL database. Do not put genuine retailer files, row-level output, database dumps or credentials in public assets. The prototype does not schedule collection or automatically retain the raw downloaded file.

## Initial setup and ingestion

Use a dedicated, empty database or schema. `init` applies the current initial SQL files to the connection's `search_path`; it is not a migration system for an existing deployment. Set `PRICEPULSE_DSN` privately using PostgreSQL connection parameters, then:

```powershell
uv sync --locked
uv run python -m pricepulse.ingest init
uv run python -m pricepulse.ingest load --source spar --store 8702 --date 2026-11-17 --url https://www.spar.hr/example.csv --collected-at 2026-11-22T23:00:00+00:00 --http-status 200 --csv data/private-source.csv
```

The path, URL, date and time above are illustrative placeholders, not a real acquisition record. Supply the actual file and metadata from a permitted retrieval. The loader computes SHA-256 from the bytes supplied but cannot independently verify the caller-provided URL, date, retrieval time or HTTP status. It rejects non-HTTPS or unapproved source hosts and currently supports only SPAR 8702 and Kaufland 5630. Collection is separate from ingestion; preserve the raw file privately if later verification is required.

Each file version is keyed by chain, store, publication date and raw-byte SHA-256. Replaying identical bytes records a new acquisition run but does not duplicate source rows or observations; changed bytes create a distinct version. A transaction rolls back database writes if ingestion fails. Original columns remain in private `source_row.raw_row`. Missing or duplicate source SKUs prevent price observation creation; invalid/duplicate GTINs, missing brand or quantity/unit and price problems create review exceptions. Invalid/conflicting prices remain raw and do not become zero.

## Analysis and review

`price_history` preserves file versions; `price_changes(array_of_file_ids)` requires the caller to choose at most one version for each store/date and reports changes only for source SKUs with the same checksum-valid GTIN and unchanged title, brand, quantity and unit, without ingestion exceptions. Changed descriptors are excluded pending review. A missing row is not an out-of-stock observation. `source_quality` gives counts per file. `verified_price_comparison` contains only explicitly reviewed row pairs, with the same date and checksum-valid shared GTIN, priced rows and no unresolved ingestion exceptions. Comparison decisions refer to exact file versions and must be recorded using `pricepulse.matching.record_review`; `comparison_flags` surfaces differing or missing descriptors, brands and quantities for human review. Brand aliases are explicit caller-provided mappings. GTIN checks and descriptor consistency are not manufacturer certification; multipacks, variants and gross/drained weights require review.

## Validation

Set `PRICEPULSE_TEST_DSN` to a **disposable test database** whose user may create and drop schemas, then run `uv run --locked python -m pytest -q`. Integration tests create and drop their own randomly named schemas. Without that variable they are skipped; a passing offline-only suite is not PostgreSQL integration evidence. The CI service uses a disposable synthetic PostgreSQL database. See [Validation](VALIDATION.md) for the observed results and remaining limits.

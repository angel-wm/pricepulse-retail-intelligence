# Local PostgreSQL historical data

Phase 2 code loads a locally held source CSV into a private, dedicated PostgreSQL database. Do not put genuine retailer files, row-level output, database dumps or credentials in public assets. The prototype does not schedule collection or automatically retain the raw downloaded file.

## Local PostgreSQL with Docker Compose

Use Docker Desktop in Linux container mode, or Docker Engine with the Compose plugin. Run these commands in PowerShell 7 from the repository root after the [Python setup](README.md#local-quick-start-windows-powershell). Compose runs PostgreSQL 18.7. Python, Scrapy and Tableau run on the host.

### Development database

```powershell
$env:PRICEPULSE_DB_PASSWORD = Read-Host 'Local PostgreSQL password' -MaskInput
docker compose up --wait db
$encodedPassword = [uri]::EscapeDataString($env:PRICEPULSE_DB_PASSWORD)
$env:PRICEPULSE_DSN = "postgresql://pricepulse:$encodedPassword@127.0.0.1:55432/pricepulse"
uv run --locked python -m pricepulse.ingest init
```

Set a private, nonempty password before the first start. PostgreSQL initializes the database and login once in the `postgres-data` volume. On subsequent starts, use the original password. Changing the environment variable alone leaves the stored password in place. The `init` command also applies schema updates. Run it on an existing private database before ingesting Konzum 1280. The update extends the retailer constraint and preserves existing files and observations.

The host port defaults to `55432`. If it is in use, set `PRICEPULSE_DB_PORT` before starting and use the same port in the DSN. The port binds to IPv4 loopback. The [official PostgreSQL 18 image](https://hub.docker.com/_/postgres) stores the cluster below `/var/lib/postgresql`.

Run `docker compose down` to stop the development service and retain its volume. Starting it again with the same Compose project reuses the data. **Adding `--volumes` permanently removes the project's development database.** Back up anything you need before resetting it. Run `docker compose ps` or `docker compose logs db` to diagnose startup problems.

### Disposable integration database

```powershell
$env:PRICEPULSE_TEST_DB_PASSWORD = [guid]::NewGuid().ToString('N')
docker compose up --wait db-test
$env:PRICEPULSE_TEST_DSN = "postgresql://pricepulse_test:$env:PRICEPULSE_TEST_DB_PASSWORD@127.0.0.1:55433/pricepulse_test"
uv run --locked python -m pytest -q
docker compose rm --stop --force db-test
Remove-Item Env:PRICEPULSE_TEST_DSN, Env:PRICEPULSE_TEST_DB_PASSWORD
```

The named test service starts its profile automatically and can run alongside development. It has a separate login and loopback port, and PostgreSQL writes to temporary memory-backed storage. Stopping it discards test data. The cleanup command only targets `db-test`. If you set `PRICEPULSE_TEST_DB_PORT`, use that port in the test DSN. Keep genuine data in your dedicated private development database.

## Initial setup and ingestion

Use a dedicated, empty database or schema. `init` applies the current initial SQL files to the connection's `search_path`; it is not a migration system for an existing deployment. Set `PRICEPULSE_DSN` privately using PostgreSQL connection parameters, then:

```powershell
uv sync --locked
uv run --locked python -m pricepulse.ingest init
uv run --locked python -m pricepulse.ingest load --source spar --store 8702 --date 2026-11-17 --url https://www.spar.hr/example.csv --collected-at 2026-11-22T23:00:00+00:00 --http-status 200 --csv data/private-source.csv
```

The path, URL, date and time above are illustrative placeholders, not a real acquisition record. Supply the actual file and metadata from a permitted retrieval. The loader computes SHA-256 from the bytes supplied but cannot independently verify the caller-provided URL, date, retrieval time or HTTP status. It rejects non-HTTPS or unapproved source hosts and currently supports only SPAR 8702 and Kaufland 5630. Collection is separate from ingestion; preserve the raw file privately if later verification is required.

Each file version is keyed by chain, store, publication date and raw-byte SHA-256. Replaying identical bytes records a new acquisition run but does not duplicate source rows or observations; changed bytes create a distinct version. A transaction rolls back database writes if ingestion fails. Original columns remain in private `source_row.raw_row`. Missing or duplicate source SKUs prevent price observation creation; invalid/duplicate GTINs, missing brand or quantity/unit and price problems create review exceptions. Invalid/conflicting prices remain raw and do not become zero.

For previously collected data, use the [recovery command](RELIABILITY.md#run-evidence) with the original successful run report, feed and archived CSV. It checks the recorded hashes before loading. Keep the successful capture reports and use the returned file IDs for the [Tableau export](TABLEAU.md#private-analytical-export).

## Analysis and review

`price_history` preserves file versions; `price_changes(array_of_file_ids)` requires the caller to choose at most one version for each store/date and reports changes only for source SKUs with the same checksum-valid GTIN and unchanged title, brand, quantity and unit, without ingestion exceptions. Changed descriptors are excluded pending review. A missing row is not an out-of-stock observation. `source_quality` gives counts per file. For two explicitly selected files, `pricepulse.matching.queue_candidates` queues same-GTIN priced rows for review and records descriptor differences; it never approves them or overwrites prior decisions. `verified_price_comparison` contains only explicitly reviewed row pairs, with the same date and checksum-valid shared GTIN, priced rows and no unresolved ingestion exceptions. Comparison decisions refer to exact file versions and must be recorded using `pricepulse.matching.record_review`; `comparison_flags` surfaces differing or missing descriptors, brands and quantities for human review. Brand aliases are explicit caller-provided mappings. GTIN checks and descriptor consistency are not manufacturer certification; multipacks, variants and gross/drained weights require review.

For a fixed store on two different dates, `queue_history_changes` flags changed GTIN or descriptors for the same SKU and records a review entry. It does not automatically resolve that change or add it back to `price_changes`.

Cross-retailer candidates are joined by normalized GTIN. The quantity check compares the declared mass only when both sources provide one. For SPAR, the quantity goes with its `kg` or `g` unit. For Kaufland, the quantity column explicitly says `(KG)` and the separate unit field is retained as source evidence. The check compares exact decimal values after converting to kilograms. It distinguishes different declared masses from quantities that cannot be compared, such as pieces or volume against mass. A mass agreement alone says nothing about the variant or sale package. Existing queued explanations and review events are historical records.

## Validation

Set `PRICEPULSE_TEST_DSN` to a **disposable test database** whose user may create and drop schemas, then run `uv run --locked python -m pytest -q`. Integration tests create and drop their own randomly named schemas. Without that variable they are skipped; a passing offline-only suite is not PostgreSQL integration evidence. The CI service uses a disposable synthetic PostgreSQL database. See [Validation](VALIDATION.md) for the observed results and remaining limits.

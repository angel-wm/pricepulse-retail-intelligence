# Local reliability work

Phase 3 is implemented and awaits owner review. The current tools record individual bounded crawls, support explicit ingestion recovery and calculate basic file-quality signals. A local collection-only recurring job is configured for the interactive user.

## Run evidence

Run one previously selected store and date from the repository root:

```powershell
uv run --locked python -m pricepulse.reliability --source spar --date 2026-11-17 --directory data/runs
```

Use `kaufland` for store 5630 or `konzum` for store 1280. Historical files may no longer be available. Each invocation creates a unique private JSON report, feed, raw CSV and Scrapy log. The report begins as `running`; successful completion requires a zero process exit, a normal Scrapy finish, a matching manifest, the raw-file SHA-256 and a complete feed with the expected count and row provenance. Other observed failures are `failed`, and a caught interruption is `interrupted`. An abrupt termination can leave `running`, which must be investigated rather than treated as success. The command exits nonzero for detected failures. A retry is a new run with separate evidence. Never commit or publish the reports, logs, raw CSV or feeds: they may contain genuine retailer data.

To ingest a successful report into the dedicated private database described in [PostgreSQL](POSTGRESQL.md), set `PRICEPULSE_DSN` and run `uv run --locked python -m pricepulse.recovery data/runs/<run-id>.json`. This separate step checks feed and raw hashes again and records ingestion status in the report. If a crash occurs after a database commit but before the report is updated, rerunning the command uses file-version idempotency to avoid duplicating observations; a replay may record another acquisition run. Recovery does not independently verify the original URL or acquisition time. A tampered or absent raw file must be investigated, not silently retried as valid.

To run the fixed three-store cohort manually, use `uv run --locked python -m pricepulse.batch --date 2026-11-17 --directory data/runs`. Without `--date`, it selects the current Zagreb date. Add `--ingest` only after configuring a private `PRICEPULSE_DSN` and initializing the intended database. The batch reports `incomplete` if any store fails or, in ingestion mode, fails to load. A lock prevents overlapping batches that use the same directory; different directories are not globally locked. After an abrupt termination, a stale `batch.lock` may remain: inspect the process and journal before clearing it. Running again creates separate crawl evidence; database file versions remain idempotent. The installed collection-only task uses the same cohort at the next eligible tick. Historical batch reports keep their original coverage. Apply the schema update in [PostgreSQL](POSTGRESQL.md#development-database) before using ingestion mode with an existing database.

`quality_summary` calculates file age, usable price exceptions, checksum-valid GTIN rate and optional row-count change against an explicitly supplied earlier successful run for the same source/store. The feed summary includes regular, special and equal dual-price counts. `batch_metrics` summarizes only the supplied finished batch reports, including per-source successes and elapsed durations; it does not discover omitted runs or establish a global reliability rate. The manual monitor accepts operator-supplied thresholds. The scheduled collector applies the provisional signals below; they are not an approved production SLA. An old or missing file does not prove missing inventory or store stock. Age is calculated from the supplied publication date and an explicitly supplied reference date; it is not proof of an actual publication timestamp.

The `pricepulse.monitor` command exposes these checks. Use actual private report paths and operator-selected thresholds; the following are illustrative:

```powershell
uv run --locked python -m pricepulse.monitor source --current data/runs/<run-id>.json --as-of 2026-11-23 --max-age-days 2
uv run --locked python -m pricepulse.monitor batches data/runs/<batch-id>.json
uv run --locked python -m pricepulse.monitor coverage <file-id-1> <file-id-2>
```

`source` and `batches` return exit code 2 when the selected thresholds or completed batch status indicate an alert. `coverage` requires `PRICEPULSE_DSN` and measures only eligible pairs already queued for review for the two explicitly selected files. It is not a percentage of either full catalogue or a measure of real-world availability. The source index counts in a successful run describe source-specific index scope, not product counts; see [Acquisition](ACQUISITION.md).

## Scheduling recommendation and dry run

The reviewed regulation specifies changed lists by 11:00 on the effective date and at least 15 days' availability of replaced files; see [Source feasibility](SOURCE_FEASIBILITY.md). A preliminary **12:15 Europe/Zagreb** daily check gives a margin, but is not a guarantee that either source will have a file available. Confirm current terms, robots rules and actual publication behavior before enabling a recurring live job.

```powershell
uv run --locked python -m pricepulse.scheduling --now 2026-11-22T09:00:00+00:00
```

This command only prints a proposed time; it does not schedule or perform a request. The function converts the Zagreb time to UTC for winter and summer. On 2026-11-23, the Phase 3 setup registered the Windows task **`PricePulse-Local-Collect`** for the current interactive user; the owner subsequently confirmed local collection only for now. It runs an hourly local tick that is due only after 12:15 Zagreb time and attempts collection at most once per Zagreb date. It runs only while that user is logged on, uses `data/scheduled`, performs collection only and stops starting new batches when that directory has reached a **1 GiB soft limit**. A batch can exceed the soft limit because it is checked before the run. No files are automatically deleted. A daily marker remains after an interruption or failure, so investigate and recover manually instead of expecting an automatic retry.

When Windows shows a nonzero result, inspect the daily marker and its linked batch before assuming the latest tick made a new download. An hourly tick returns a nonzero result again for an already recorded incomplete attempt. After correcting the cause, keep the original marker and its linked reports when recovering. A deliberate retry in the same scheduled directory requires archiving the existing daily marker before another eligible trigger. Check that the task is idle and that the trigger is still on the same Zagreb date. The recovery creates a new daily marker. See [Validation](VALIDATION.md) for the observed cases.

The installer refuses to overwrite an existing task of the same name. To pause the task, use `Disable-ScheduledTask -TaskName 'PricePulse-Local-Collect'`. Check the configuration and any pending marker before re-enabling it.

GitHub Actions could run tests, but storing genuine source output on hosted runners and publishing logs/artifacts needs a separate data-handling assessment. The 1 GiB pre-run soft limit is the current local retention guard; there is no automatic deletion. Real daily operation and longer-term thresholds remain to be assessed as evidence accumulates.

GitHub documents that [standard hosted-runner usage is free for public repositories](https://docs.github.com/en/actions/concepts/billing-and-usage), subject to service limits; storage and private-repository usage have different allowances. GitHub also says [scheduled workflows can be delayed or dropped and may be disabled after inactivity](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule). A local scheduler avoids transferring source output to a hosted runner but depends on the computer being available; neither option establishes daily coverage without observed runs.

## Provisional scheduled quality signals

Each successful scheduled collection records per-source quality and warnings in its private daily JSON marker. The initial signals are: file age over one day; absolute row-count change over 30% against the nearest earlier successful report for the same source and store; price exceptions over 1% of rows; and checksum-valid GTINs below 90% of rows. A future publication date is also flagged. With no eligible earlier report, row change is unknown and no change warning is generated. Age uses the file date, not an observed publication timestamp.

These are provisional engineering thresholds, not business targets or proof of inventory. Successful collection with warnings records `success_with_alerts` and returns a nonzero task result. Subsequent ticks retain a nonzero result for that day's failed or warned attempt until it is investigated; they do not silently retry. Inspect the private marker and batch reports under `data/scheduled`, then use the documented recovery process as appropriate.

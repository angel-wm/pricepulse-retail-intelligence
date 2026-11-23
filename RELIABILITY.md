# Local reliability work

Phase 3 is in progress while Phase 2 remains open for the owner's later review. The current tools record individual bounded crawls and calculate basic file-quality signals. They do not automatically ingest downloaded files into PostgreSQL or create recurring jobs.

## Run evidence

Run one previously selected store and date from the repository root:

```powershell
uv run --locked python -m pricepulse.reliability --source spar --date 2026-11-17 --directory data/runs
```

Use `kaufland` for store 5630. Historical files may no longer be available. Each invocation creates a unique private JSON report, feed and Scrapy log. The report begins as `running`; successful completion requires a zero process exit, a normal Scrapy finish, a matching manifest and a complete feed with the expected count and row provenance. Other observed failures are `failed`, and a caught interruption is `interrupted`. An abrupt termination can leave `running`, which must be investigated rather than treated as success. The command exits nonzero for detected failures. A retry is a new run with separate evidence; PostgreSQL ingestion remains a separate step. Never commit or publish the reports, logs or feeds: they may contain genuine retailer data.

`quality_summary` calculates file age, usable price exceptions, checksum-valid GTIN rate and optional row-count change against an explicitly supplied earlier successful run for the same source/store. Callers supply their own age and change thresholds; no production alert thresholds or reliability baseline have been established. An old or missing file does not prove missing inventory or store stock. Age is calculated from the supplied publication date and an explicitly supplied reference date; it is not proof of an actual publication timestamp.

## Scheduling recommendation and dry run

The reviewed regulation specifies changed lists by 11:00 on the effective date and at least 15 days' availability of replaced files; see [Source feasibility](SOURCE_FEASIBILITY.md). A preliminary **12:15 Europe/Zagreb** daily check gives a margin, but is not a guarantee that either source will have a file available. Confirm current terms, robots rules and actual publication behavior before enabling a recurring live job.

```powershell
uv run --locked python -m pricepulse.scheduling --now 2026-11-22T09:00:00+00:00
```

This command only prints a proposed time; it does not schedule or perform a request. The function converts the Zagreb time to UTC for winter and summer. Windows Task Scheduler is a local-first candidate when the machine and private storage are available; its actual account, time-zone behavior, missed-run and failure handling must be verified. GitHub Actions could run tests, but storing genuine source output on hosted runners and publishing logs/artifacts needs a separate data-handling assessment. Neither option is configured here. A schedule, real recurring outputs, retention policy and operational thresholds remain to be validated before claiming PULSE-18 or PULSE-20 complete.

GitHub documents that [standard hosted-runner usage is free for public repositories](https://docs.github.com/en/actions/concepts/billing-and-usage), subject to service limits; storage and private-repository usage have different allowances. GitHub also says [scheduled workflows can be delayed or dropped and may be disabled after inactivity](https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows#schedule). A local scheduler avoids transferring source output to a hosted runner but depends on the computer being available; neither option establishes daily coverage without observed runs.

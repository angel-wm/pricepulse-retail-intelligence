"""Inspect explicitly selected private run reports or queued review pairs."""
import argparse
import json
import os
from pathlib import Path

from pricepulse.reliability import batch_metrics, quality_summary


def read_report(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Inspect selected PricePulse run evidence")
    commands = parser.add_subparsers(dest="command", required=True)
    source = commands.add_parser("source")
    source.add_argument("--current", required=True, type=Path)
    source.add_argument("--previous", type=Path)
    source.add_argument("--as-of", required=True, help="reference date in YYYY-MM-DD")
    source.add_argument("--max-age-days", type=int)
    source.add_argument("--max-row-change", type=float, help="allowed fractional change, e.g. 0.2")
    batches = commands.add_parser("batches")
    batches.add_argument("reports", nargs="+", type=Path)
    coverage = commands.add_parser("coverage")
    coverage.add_argument("file_a", type=int)
    coverage.add_argument("file_b", type=int)
    args = parser.parse_args(argv)
    if args.command == "source":
        result = quality_summary(read_report(args.current), args.as_of,
                                 previous=read_report(args.previous) if args.previous else None,
                                 max_age_days=args.max_age_days, max_row_change=args.max_row_change)
        status = 2 if result["alerts"] else 0
    elif args.command == "batches":
        result = batch_metrics(read_report(path) for path in args.reports)
        status = 2 if result["incomplete_or_failed"] else 0
    else:
        import psycopg
        from pricepulse.metrics import reviewed_pair_coverage
        dsn = os.environ.get("PRICEPULSE_DSN")
        if not dsn:
            parser.error("set PRICEPULSE_DSN to the private PostgreSQL database")
        with psycopg.connect(dsn) as conn:
            result = reviewed_pair_coverage(conn, args.file_a, args.file_b)
        status = 0
    print(json.dumps(result, ensure_ascii=True))
    return status


if __name__ == "__main__":
    raise SystemExit(main())

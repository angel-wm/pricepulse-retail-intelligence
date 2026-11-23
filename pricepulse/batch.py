"""Run the fixed two-store cohort sequentially with a private batch journal."""
import json
from datetime import date, datetime, timezone
from pathlib import Path
from uuid import uuid4

from pricepulse.reliability import run_crawl, write_report


def run_batch(day, directory, *, ingest=None, crawl=run_crawl):
    date.fromisoformat(day)
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    lock = directory / "batch.lock"
    with lock.open("x", encoding="utf-8") as handle:
        handle.write(datetime.now(timezone.utc).isoformat() + "\n")
    run_id = uuid4().hex
    path = directory / ("batch-" + run_id + ".json")
    report = {"batch_id": run_id, "publication_date": day, "status": "running",
              "mode": "ingest" if ingest else "collect", "sources": {},
              "started_at_utc": datetime.now(timezone.utc).isoformat()}
    try:
        write_report(path, report)
        for source in ("spar", "kaufland"):
            report_path, result = crawl(source, day, directory)
            state = {"report": Path(report_path).name, "crawl_status": result["status"]}
            report["sources"][source] = state
            if result["status"] == "success" and ingest is not None:
                state["ingestion_status"] = ingest(report_path)["ingestion"]["status"]
            write_report(path, report)
        report["status"] = "success" if all(
            item["crawl_status"] == "success" and (ingest is None or item.get("ingestion_status") == "success")
            for item in report["sources"].values()
        ) and len(report["sources"]) == 2 else "incomplete"
    except Exception as exc:
        report.update(status="failed", reason=type(exc).__name__)
    except BaseException:
        report["status"] = "interrupted"
        raise
    finally:
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        try:
            write_report(path, report)
        finally:
            lock.unlink(missing_ok=True)
    return path, report


def main():
    import argparse
    import os
    import psycopg
    from pricepulse.recovery import resume_ingestion
    parser = argparse.ArgumentParser(description="Run one two-store batch; no scheduling is created")
    from pricepulse.scheduling import ZAGREB
    parser.add_argument("--date", default=None, help="price-list date (defaults to the current Zagreb date)")
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--ingest", action="store_true", help="also load successful source files into private PostgreSQL")
    args = parser.parse_args()
    day = args.date or datetime.now(ZAGREB).date().isoformat()
    if args.ingest:
        dsn = os.environ.get("PRICEPULSE_DSN")
        if not dsn:
            parser.error("set PRICEPULSE_DSN for ingestion")
        with psycopg.connect(dsn, autocommit=True) as conn:
            path, report = run_batch(day, args.directory, ingest=lambda p: resume_ingestion(p, conn))
    else:
        path, report = run_batch(day, args.directory)
    print(json.dumps({"report": str(path), "mode": report["mode"], "status": report["status"]}))
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())

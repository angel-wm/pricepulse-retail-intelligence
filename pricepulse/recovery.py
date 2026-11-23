"""Resume ingestion of a completed private crawl using its recorded raw bytes."""
import json
import os
import re
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path

from pricepulse.ingest import ingest_file
from pricepulse.reliability import inspect_feed, write_report


def resume_ingestion(report_path, conn):
    path = Path(report_path).resolve()
    if not re.fullmatch(r"[0-9a-f]{32}\.json", path.name):
        raise ValueError("invalid report filename")
    report = json.loads(path.read_text(encoding="utf-8"))
    run_id = path.stem
    if report.get("run_id") != run_id or report.get("status") != "success":
        raise ValueError("a successful crawl report is required")
    report["ingestion"] = {"status": "running", "started_at_utc": datetime.now(timezone.utc).isoformat()}
    write_report(path, report)
    try:
        source, day = report["source"], report["publication_date"]
        feed = path.parent / (run_id + ".jl")
        raw = (path.parent / (run_id + ".csv")).read_bytes()
        summary = inspect_feed(feed, source, day)
        if summary != report.get("summary") or sha256(raw).hexdigest() != summary["sha256"]:
            raise ValueError("run evidence or raw hash mismatch")
        with feed.open(encoding="utf-8") as stream:
            manifest = json.loads(next(stream))
        result = ingest_file(conn, source=source, store=summary["store_id"], day=day,
                             url=manifest["source_url"], collected_at=manifest["retrieved_at_utc"],
                             status=manifest["http_status"], body=raw)
        report["ingestion"].update(status="success", file_id=result["file_id"], new_version=result["new_version"])
    except Exception as exc:
        report["ingestion"].update(status="failed", reason=type(exc).__name__)
    report["ingestion"]["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_report(path, report)
    return report


def main():
    import argparse
    import psycopg
    parser = argparse.ArgumentParser(description="Resume ingestion from a successful private crawl report")
    parser.add_argument("report", type=Path)
    args = parser.parse_args()
    dsn = os.environ.get("PRICEPULSE_DSN")
    if not dsn:
        parser.error("set PRICEPULSE_DSN to the private PostgreSQL database")
    with psycopg.connect(dsn, autocommit=True) as conn:
        report = resume_ingestion(args.report, conn)
    print(json.dumps({"status": report["ingestion"]["status"], "reason": report["ingestion"].get("reason")}))
    return 0 if report["ingestion"]["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())

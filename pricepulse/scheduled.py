"""One safe scheduler tick; capture only, never deploy or ingest automatically."""
import argparse
import json
from datetime import datetime, time, timezone
from pathlib import Path

from pricepulse.batch import run_batch
from pricepulse.reliability import quality_summary, write_report
from pricepulse.scheduling import ZAGREB

SOFT_LIMIT_BYTES = 1024 * 1024 * 1024


def prior_report(directory, current):
    """Find the latest earlier completed source report in the same private directory."""
    summary = current["summary"]
    candidates = []
    for path in directory.glob("*.json"):
        try:
            item = json.loads(path.read_text(encoding="utf-8"))
            previous = item.get("summary", {})
            if (item.get("status") == "success" and previous.get("source") == summary["source"]
                    and previous.get("store_id") == summary["store_id"]
                    and previous.get("publication_date", "") < summary["publication_date"]
                    and previous.get("row_count", 0) > 0):
                candidates.append(item)
        except (OSError, ValueError, TypeError, AttributeError):
            continue
    return max(candidates, key=lambda x: (x["summary"]["publication_date"], x.get("finished_at_utc", "")), default=None)


def batch_quality(directory, batch_report, day):
    """Create provisional local warnings; they do not infer product availability."""
    results = {}
    alerts = []
    for source, state in batch_report.get("sources", {}).items():
        if state.get("crawl_status") != "success":
            continue
        path = directory / Path(state["report"]).name
        current = json.loads(path.read_text(encoding="utf-8"))
        result = quality_summary(current, day, previous=prior_report(directory, current), max_age_days=1, max_row_change=0.30)
        if result["price_exception_rate"] > 0.01:
            result["alerts"].append("price_exception_rate_exceeded")
        if result["checksum_valid_gtin_rate"] < 0.90:
            result["alerts"].append("checksum_valid_gtin_rate_low")
        results[source] = result
        alerts.extend({"source": source, "reason": reason} for reason in result["alerts"])
    return results, alerts


def tick(directory, now, *, batch=run_batch, soft_limit_bytes=SOFT_LIMIT_BYTES):
    if now.utcoffset() is None:
        raise ValueError("timestamp must have a timezone")
    local = now.astimezone(ZAGREB)
    if local.timetz().replace(tzinfo=None) < time(12, 15):
        return {"status": "not_due", "publication_date": local.date().isoformat()}
    if soft_limit_bytes < 1:
        raise ValueError("soft limit must be positive")
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    day = local.date().isoformat()
    marker = directory / ("daily-" + day + ".json")
    initial = {"publication_date": day, "status": "starting", "started_at_utc": now.astimezone(timezone.utc).isoformat()}
    try:
        with marker.open("x", encoding="utf-8") as stream:
            json.dump(initial, stream)
    except FileExistsError:
        try:
            previous_status = json.loads(marker.read_text(encoding="utf-8")).get("status", "unknown")
        except (OSError, ValueError, AttributeError):
            previous_status = "unknown"
        return {"status": "already_attempted", "publication_date": day, "previous_status": previous_status}
    try:
        used = sum(item.stat().st_size for item in directory.rglob("*") if item.is_file())
        if used >= soft_limit_bytes:
            initial.update(status="storage_limit", used_bytes=used, soft_limit_bytes=soft_limit_bytes)
        else:
            path, report = batch(day, directory)
            initial.update(status=report["status"], batch_report=Path(path).name, used_bytes_before=used)
            quality, alerts = batch_quality(directory, report, day)
            initial.update(quality=quality, alerts=alerts)
            if alerts and initial["status"] == "success":
                initial["status"] = "success_with_alerts"
    except Exception as exc:
        initial.update(status="failed", reason=type(exc).__name__)
    initial["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_report(marker, initial)
    return initial


def main():
    parser = argparse.ArgumentParser(description="Run one local scheduler tick in collection-only mode")
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--soft-limit-bytes", type=int, default=SOFT_LIMIT_BYTES)
    args = parser.parse_args()
    result = tick(args.directory, datetime.now(timezone.utc), soft_limit_bytes=args.soft_limit_bytes)
    print(json.dumps(result))
    successful = result["status"] in ("success", "not_due") or (result["status"] == "already_attempted" and result.get("previous_status") == "success")
    return 0 if successful else 1


if __name__ == "__main__":
    raise SystemExit(main())

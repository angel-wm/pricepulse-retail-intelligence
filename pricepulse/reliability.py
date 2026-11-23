"""Bounded local crawl evidence; it does not schedule runs or ingest into PostgreSQL."""
import json
import os
import re
import subprocess
import sys
from collections import Counter
from datetime import date, datetime, timezone
from hashlib import sha256
from pathlib import Path
from uuid import uuid4

STORES = {"spar": "8702", "kaufland": "5630"}
SHA256 = re.compile(r"[0-9a-f]{64}\Z")


def inspect_feed(path, source, day):
    """Validate a full feed and return counts, not retailer rows."""
    counts = Counter()
    manifest = None
    with Path(path).open(encoding="utf-8") as stream:
        for line in stream:
            item = json.loads(line)
            if not isinstance(item, dict):
                raise ValueError("feed item is not an object")
            if manifest is None:
                if item.get("type") != "manifest":
                    raise ValueError("feed does not begin with a manifest")
                manifest = item
                if (manifest.get("source") != source or manifest.get("store_id") != STORES[source]
                        or manifest.get("publication_date") != day or manifest.get("http_status") != 200
                        or not isinstance(manifest.get("sha256"), str) or not SHA256.fullmatch(manifest["sha256"])
                        or not isinstance(manifest.get("row_count"), int) or isinstance(manifest.get("row_count"), bool)
                        or manifest["row_count"] < 1):
                    raise ValueError("invalid source manifest")
                continue
            if (item.get("type") != "record" or item.get("source_chain") != source
                    or item.get("source_store_id") != STORES[source] or item.get("price_list_date") != day
                    or item.get("source_file_hash") != manifest["sha256"]):
                raise ValueError("record provenance mismatch")
            counts["rows"] += 1
            counts["usable_price"] += item.get("ingestion_status") == "ok"
            counts["checksum_valid_gtin"] += bool(item.get("gtin_normalized"))
            counts["review"] += item.get("ingestion_status") != "ok"
        if manifest is None or counts["rows"] != manifest["row_count"]:
            raise ValueError("incomplete feed or row count mismatch")
    return {"source": source, "store_id": STORES[source], "publication_date": day,
            "sha256": manifest["sha256"], "row_count": counts["rows"],
            "usable_price_count": counts["usable_price"], "checksum_valid_gtin_count": counts["checksum_valid_gtin"],
            "price_exception_count": counts["review"]}


def write_report(path, report):
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(report, ensure_ascii=True, indent=2) + "\n", encoding="utf-8")
    os.replace(temporary, path)


def quality_summary(report, as_of, *, previous=None, max_age_days=None, max_row_change=None):
    """Compare explicit completed runs; thresholds are supplied by the operator."""
    if report.get("status") != "success" or not isinstance(report.get("summary"), dict):
        raise ValueError("quality requires a successful run")
    summary = report["summary"]
    observed = date.fromisoformat(summary["publication_date"])
    today = date.fromisoformat(as_of)
    age = (today - observed).days
    if max_age_days is not None and max_age_days < 0:
        raise ValueError("max_age_days must not be negative")
    if max_row_change is not None and not 0 <= max_row_change:
        raise ValueError("max_row_change must not be negative")
    rows = summary["row_count"]
    if rows < 1:
        raise ValueError("row count must be positive")
    result = {"age_days": age, "rows": rows,
              "price_exception_rate": summary["price_exception_count"] / rows,
              "checksum_valid_gtin_rate": summary["checksum_valid_gtin_count"] / rows,
              "row_change_ratio": None, "alerts": []}
    if age < 0:
        result["alerts"].append("future_publication_date")
    if max_age_days is not None and age > max_age_days:
        result["alerts"].append("file_age_exceeded")
    if previous is not None:
        if previous.get("status") != "success" or not isinstance(previous.get("summary"), dict):
            raise ValueError("previous run must be successful")
        prior = previous["summary"]
        if (prior["source"], prior["store_id"]) != (summary["source"], summary["store_id"]):
            raise ValueError("previous run must use the same source and store")
        if date.fromisoformat(prior["publication_date"]) >= observed or prior["row_count"] < 1:
            raise ValueError("previous run must be an earlier nonempty file")
        change = (rows - prior["row_count"]) / prior["row_count"]
        result["row_change_ratio"] = change
        if max_row_change is not None and abs(change) > max_row_change:
            result["alerts"].append("row_count_change_exceeded")
    return result


def run_crawl(source, day, directory, timeout=600, runner=subprocess.run):
    """Perform one crawl and journal it; interrupted attempts are never marked successful."""
    if source not in STORES:
        raise ValueError("unsupported source")
    date.fromisoformat(day)
    if not 1 <= timeout <= 3600:
        raise ValueError("timeout must be between 1 and 3600 seconds")
    directory = Path(directory).resolve()
    directory.mkdir(parents=True, exist_ok=True)
    run_id = uuid4().hex
    report_path = directory / (run_id + ".json")
    feed_path = directory / (run_id + ".jl")
    log_path = directory / (run_id + ".log")
    raw_path = directory / (run_id + ".csv")
    report = {"run_id": run_id, "source": source, "store_id": STORES[source], "publication_date": day,
              "started_at_utc": datetime.now(timezone.utc).isoformat(), "status": "running"}
    write_report(report_path, report)
    command = [sys.executable, "-m", "scrapy", "crawl", source, "-a", "date=" + day, "-a", "raw_path=" + str(raw_path), "-O", str(feed_path),
               "-s", "LOG_FILE=" + str(log_path), "-s", "LOG_LEVEL=INFO"]
    try:
        result = runner(command, timeout=timeout, check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if result.returncode != 0:
            raise ValueError("crawler_process_failed")
        log = log_path.read_text(encoding="utf-8", errors="replace")
        if "Spider closed (finished)" not in log:
            reason = re.findall(r"Spider closed \(([^)]+)\)", log)
            raise ValueError("crawler_closed_" + (reason[-1] if reason else "without_finish"))
        report["summary"] = inspect_feed(feed_path, source, day)
        if sha256(raw_path.read_bytes()).hexdigest() != report["summary"]["sha256"]:
            raise ValueError("raw_file_hash_mismatch")
        report["status"] = "success"
    except subprocess.TimeoutExpired:
        report.update(status="failed", reason="timeout")
    except (OSError, ValueError, json.JSONDecodeError) as exc:
        report.update(status="failed", reason=str(exc)[:200])
    except BaseException:
        report.update(status="interrupted", reason="interrupted")
        report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
        write_report(report_path, report)
        raise
    report["finished_at_utc"] = datetime.now(timezone.utc).isoformat()
    write_report(report_path, report)
    return report_path, report


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run one bounded crawl and write private run evidence")
    parser.add_argument("--source", choices=tuple(STORES), required=True)
    parser.add_argument("--date", required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--timeout", type=int, default=600)
    args = parser.parse_args()
    path, report = run_crawl(args.source, args.date, args.directory, args.timeout)
    print(json.dumps({"report": str(path), "status": report["status"], "reason": report.get("reason")}))
    return 0 if report["status"] == "success" else 1


if __name__ == "__main__":
    raise SystemExit(main())

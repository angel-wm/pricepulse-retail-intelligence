"""One safe scheduler tick; capture only, never deploy or ingest automatically."""
import argparse
import json
from datetime import datetime, time, timezone
from pathlib import Path

from pricepulse.batch import run_batch
from pricepulse.reliability import write_report
from pricepulse.scheduling import ZAGREB

SOFT_LIMIT_BYTES = 1024 * 1024 * 1024


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
        return {"status": "already_attempted", "publication_date": day}
    try:
        used = sum(item.stat().st_size for item in directory.rglob("*") if item.is_file())
        if used >= soft_limit_bytes:
            initial.update(status="storage_limit", used_bytes=used, soft_limit_bytes=soft_limit_bytes)
        else:
            path, report = batch(day, directory)
            initial.update(status=report["status"], batch_report=Path(path).name, used_bytes_before=used)
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
    return 0 if result["status"] in ("success", "not_due", "already_attempted") else 1


if __name__ == "__main__":
    raise SystemExit(main())

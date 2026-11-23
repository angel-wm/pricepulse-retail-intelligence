import json
import subprocess
from hashlib import sha256
from types import SimpleNamespace

import pytest

from pricepulse.reliability import batch_metrics, quality_summary, run_crawl

DAY = "2026-11-17"
RAW = b"synthetic fixture"
DIGEST = sha256(RAW).hexdigest()


def items():
    return [{"type": "manifest", "source": "spar", "store_id": "8702", "publication_date": DAY,
             "http_status": 200, "sha256": DIGEST, "row_count": 1},
            {"type": "record", "source_chain": "spar", "source_store_id": "8702", "price_list_date": DAY,
             "source_file_hash": DIGEST, "ingestion_status": "ok", "price_origin": "special", "gtin_normalized": "04006381333931"}]


def runner_for(reason="finished", records=None, returncode=0):
    def runner(command, **kwargs):
        feed = command[command.index("-O") + 1]
        log = next(x.split("=", 1)[1] for x in command if x.startswith("LOG_FILE="))
        raw = next(x.split("=", 1)[1] for x in command if x.startswith("raw_path="))
        from pathlib import Path
        Path(feed).write_text("".join(json.dumps(x) + "\n" for x in (items() if records is None else records)), encoding="utf-8")
        Path(log).write_text("Spider closed (" + reason + ")\n", encoding="utf-8")
        Path(raw).write_bytes(RAW)
        return SimpleNamespace(returncode=returncode)
    return runner


def test_success_and_retry_leave_distinct_evidence(tmp_path):
    path, report = run_crawl("spar", DAY, tmp_path, runner=runner_for())
    assert report["status"] == "success" and report["summary"]["row_count"] == 1
    assert report["summary"]["price_origin_counts"]["special"] == 1
    assert json.loads(path.read_text())["status"] == "success"
    next_path, next_report = run_crawl("spar", DAY, tmp_path, runner=runner_for())
    assert next_path != path and next_report["status"] == "success"


@pytest.mark.parametrize("reason", ["http_forbidden", "http_rate_limited", "index_schema_error"])
def test_crawler_failures_are_recorded_even_when_exit_zero(tmp_path, reason):
    path, report = run_crawl("spar", DAY, tmp_path, runner=runner_for(reason=reason))
    assert report["status"] == "failed" and report["reason"] == "crawler_closed_" + reason
    assert json.loads(path.read_text())["status"] == "failed"


def test_incomplete_or_mismatched_feed_fails(tmp_path):
    for records in (items()[:1], [items()[0], {**items()[1], "source_file_hash": "b" * 64}]):
        _, report = run_crawl("spar", DAY, tmp_path, runner=runner_for(records=records))
        assert report["status"] == "failed"


def test_missing_output_fails_without_a_success_marker(tmp_path):
    def missing_files(command, **kwargs):
        return SimpleNamespace(returncode=0)
    path, report = run_crawl("spar", DAY, tmp_path, runner=missing_files)
    assert report["status"] == "failed"
    assert json.loads(path.read_text())["status"] == "failed"


def test_timeout_and_interruption_are_not_success(tmp_path):
    def timed_out(command, **kwargs):
        raise subprocess.TimeoutExpired(command, 1)
    _, report = run_crawl("spar", DAY, tmp_path, runner=timed_out)
    assert (report["status"], report["reason"]) == ("failed", "timeout")
    def interrupted(command, **kwargs):
        raise KeyboardInterrupt()
    with pytest.raises(KeyboardInterrupt):
        run_crawl("spar", DAY, tmp_path, runner=interrupted)
    states = [json.loads(p.read_text())["status"] for p in tmp_path.glob("*.json")]
    assert "interrupted" in states


def test_quality_uses_explicit_store_baseline_and_thresholds(tmp_path):
    _, report = run_crawl("spar", DAY, tmp_path, runner=runner_for())
    previous = {"status": "success", "summary": {**report["summary"], "publication_date": "2026-11-16", "row_count": 2}}
    result = quality_summary(report, "2026-11-20", previous=previous, max_age_days=2, max_row_change=0.2)
    assert result["age_days"] == 3 and result["row_change_ratio"] == -0.5
    assert set(result["alerts"]) == {"file_age_exceeded", "row_count_change_exceeded"}
    assert quality_summary(report, "2026-11-17")["row_change_ratio"] is None
    with pytest.raises(ValueError):
        quality_summary(report, "2026-11-20", previous={"status": "success", "summary": {**previous["summary"], "store_id": "other"}})


def test_batch_metrics_reports_only_explicit_batches():
    base = {"started_at_utc": "2026-11-22T23:00:00+00:00", "finished_at_utc": "2026-11-22T23:00:10+00:00"}
    completed = {**base, "status": "success", "sources": {"spar": {"crawl_status": "success"}, "kaufland": {"crawl_status": "success"}}}
    incomplete = {**base, "status": "incomplete", "sources": {"spar": {"crawl_status": "success"}, "kaufland": {"crawl_status": "failed"}}}
    result = batch_metrics([completed, incomplete])
    assert (result["batches"], result["completed"], result["incomplete_or_failed"]) == (2, 1, 1)
    assert result["source_success"] == {"spar": 2, "kaufland": 1, "konzum": 0}
    assert result["durations_seconds"] == [10, 10]
    with pytest.raises(ValueError):
        batch_metrics([{**base, "status": "running"}])

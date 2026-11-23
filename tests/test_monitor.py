import json

from pricepulse.monitor import main


def test_source_monitor_flags_old_report(tmp_path, capsys):
    report = {"status": "success", "summary": {"source": "spar", "store_id": "8702", "publication_date": "2026-11-17", "row_count": 2, "price_exception_count": 1, "checksum_valid_gtin_count": 2}}
    path = tmp_path / "run.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    assert main(["source", "--current", str(path), "--as-of", "2026-11-20", "--max-age-days", "2"]) == 2
    result = json.loads(capsys.readouterr().out)
    assert result["alerts"] == ["file_age_exceeded"]
    assert result["price_exception_rate"] == 0.5


def test_batch_monitor_returns_nonzero_for_incomplete(tmp_path, capsys):
    report = {"status": "incomplete", "started_at_utc": "2026-11-22T23:00:00+00:00", "finished_at_utc": "2026-11-22T23:01:00+00:00", "sources": {"spar": {"crawl_status": "success"}, "kaufland": {"crawl_status": "failed"}}}
    path = tmp_path / "batch.json"
    path.write_text(json.dumps(report), encoding="utf-8")
    assert main(["batches", str(path)]) == 2
    assert json.loads(capsys.readouterr().out)["incomplete_or_failed"] == 1

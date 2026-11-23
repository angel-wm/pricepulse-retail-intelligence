import json
from pathlib import Path

import pytest

from pricepulse.batch import run_batch


def fake_crawl(source, day, directory):
    return Path(directory) / (source + ".json"), {"status": "failed" if source == "kaufland" else "success"}


def test_partial_coverage_is_not_success_and_can_be_retried(tmp_path):
    seen = []
    def fake_ingest(path):
        seen.append(Path(path).name)
        return {"ingestion": {"status": "success"}}
    path, result = run_batch("2026-11-17", tmp_path, crawl=fake_crawl, ingest=fake_ingest)
    assert result["status"] == "incomplete" and result["mode"] == "ingest"
    assert seen == ["spar.json"] and result["sources"]["kaufland"]["crawl_status"] == "failed"
    assert json.loads(path.read_text())["status"] == "incomplete"
    assert not (tmp_path / "batch.lock").exists()
    second, _ = run_batch("2026-11-17", tmp_path, crawl=fake_crawl)
    assert path != second


def test_existing_lock_prevents_overlap(tmp_path):
    (tmp_path / "batch.lock").write_text("existing")
    with pytest.raises(FileExistsError):
        run_batch("2026-11-17", tmp_path, crawl=fake_crawl)

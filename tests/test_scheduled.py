import json
from datetime import datetime
from pathlib import Path

from pricepulse.scheduled import tick


def test_due_tick_runs_once_per_zagreb_date(tmp_path):
    calls = []
    def fake_batch(day, directory):
        calls.append(day)
        return Path(directory) / 'batch-example.json', {'status': 'success'}
    assert tick(tmp_path, datetime.fromisoformat('2026-11-23T11:00:00+01:00'), batch=fake_batch)['status'] == 'not_due'
    result = tick(tmp_path, datetime.fromisoformat('2026-11-23T12:20:00+01:00'), batch=fake_batch)
    assert result['status'] == 'success' and calls == ['2026-11-23']
    assert tick(tmp_path, datetime.fromisoformat('2026-11-23T13:20:00+01:00'), batch=fake_batch)['status'] == 'already_attempted'
    assert json.loads((tmp_path / 'daily-2026-11-23.json').read_text())['status'] == 'success'


def test_storage_limit_and_failed_attempt_do_not_retry_automatically(tmp_path):
    called = []
    result = tick(tmp_path, datetime.fromisoformat('2026-11-23T12:20:00+01:00'), batch=lambda *args: called.append(True), soft_limit_bytes=1)
    assert result['status'] == 'storage_limit' and not called
    assert tick(tmp_path, datetime.fromisoformat('2026-11-23T13:20:00+01:00'))['status'] == 'already_attempted'


def test_incomplete_batch_is_recorded_and_not_retried(tmp_path):
    result = tick(tmp_path, datetime.fromisoformat('2026-06-23T12:20:00+02:00'), batch=lambda day, directory: (Path(directory) / 'batch-example.json', {'status': 'incomplete'}))
    assert result['status'] == 'incomplete'
    assert tick(tmp_path, datetime.fromisoformat('2026-06-23T13:20:00+02:00'))['status'] == 'already_attempted'

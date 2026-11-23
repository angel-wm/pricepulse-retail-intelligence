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
    assert tick(tmp_path, datetime.fromisoformat('2026-11-23T13:20:00+01:00'), batch=fake_batch)['previous_status'] == 'success'
    assert json.loads((tmp_path / 'daily-2026-11-23.json').read_text())['status'] == 'success'


def test_storage_limit_and_failed_attempt_do_not_retry_automatically(tmp_path):
    called = []
    result = tick(tmp_path, datetime.fromisoformat('2026-11-23T12:20:00+01:00'), batch=lambda *args: called.append(True), soft_limit_bytes=1)
    assert result['status'] == 'storage_limit' and not called
    assert tick(tmp_path, datetime.fromisoformat('2026-11-23T13:20:00+01:00'))['previous_status'] == 'storage_limit'


def test_incomplete_batch_is_recorded_and_not_retried(tmp_path):
    result = tick(tmp_path, datetime.fromisoformat('2026-06-23T12:20:00+02:00'), batch=lambda day, directory: (Path(directory) / 'batch-example.json', {'status': 'incomplete'}))
    assert result['status'] == 'incomplete'
    assert tick(tmp_path, datetime.fromisoformat('2026-06-23T13:20:00+02:00'))['status'] == 'already_attempted'


def test_exception_marks_failed_and_keeps_daily_marker(tmp_path):
    def broken(day, directory):
        raise OSError("synthetic failure")
    result = tick(tmp_path, datetime.fromisoformat('2026-11-23T12:20:00+01:00'), batch=broken)
    assert result['status'] == 'failed' and result['reason'] == 'OSError'
    assert json.loads((tmp_path / 'daily-2026-11-23.json').read_text())['status'] == 'failed'
    assert tick(tmp_path, datetime.fromisoformat('2026-11-23T13:20:00+01:00'))['status'] == 'already_attempted'


def test_provisional_quality_alerts_are_recorded_without_changing_batch(tmp_path):
    def fake_batch(day, directory):
        source = {'status': 'success', 'summary': {'source': 'spar', 'store_id': '8702', 'publication_date': day, 'row_count': 100, 'price_exception_count': 2, 'checksum_valid_gtin_count': 80}}
        (Path(directory) / 'source.json').write_text(json.dumps(source))
        return Path(directory) / 'batch.json', {'status': 'success', 'sources': {'spar': {'crawl_status': 'success', 'report': 'source.json'}}}
    result = tick(tmp_path, datetime.fromisoformat('2026-11-23T12:20:00+01:00'), batch=fake_batch)
    assert result['status'] == 'success_with_alerts'
    assert {x['reason'] for x in result['alerts']} == {'price_exception_rate_exceeded', 'checksum_valid_gtin_rate_low'}


def test_quality_compares_latest_earlier_matching_store(tmp_path):
    from pricepulse.scheduled import batch_quality
    def report(day, rows, store='8702'):
        return {'status': 'success', 'summary': {'source': 'spar', 'store_id': store, 'publication_date': day, 'row_count': rows, 'price_exception_count': 0, 'checksum_valid_gtin_count': rows}}
    (tmp_path / 'previous.json').write_text(json.dumps(report('2026-11-22', 100)))
    (tmp_path / 'other.json').write_text(json.dumps(report('2026-11-22', 150, 'other')))
    (tmp_path / 'current.json').write_text(json.dumps(report('2026-11-23', 140)))
    results, alerts = batch_quality(tmp_path, {'sources': {'spar': {'crawl_status': 'success', 'report': 'current.json'}}}, '2026-11-23')
    assert results['spar']['row_change_ratio'] == 0.4
    assert alerts == [{'source': 'spar', 'reason': 'row_count_change_exceeded'}]

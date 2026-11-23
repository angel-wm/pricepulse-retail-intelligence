from datetime import datetime, timezone

import pytest

from pricepulse.scheduling import next_planned_run


def test_zagreb_schedule_handles_winter_and_summer_offsets():
    winter = next_planned_run(datetime.fromisoformat("2026-11-22T09:00:00+00:00"))
    summer = next_planned_run(datetime.fromisoformat("2026-06-22T09:00:00+00:00"))
    assert winter.isoformat() == "2026-11-22T12:15:00+01:00"
    assert summer.isoformat() == "2026-06-22T12:15:00+02:00"
    assert winter.astimezone(timezone.utc).hour == 11
    assert summer.astimezone(timezone.utc).hour == 10


def test_after_deadline_selects_next_day_and_rejects_naive_time():
    assert next_planned_run(datetime.fromisoformat("2026-11-22T11:15:00+00:00")).date().isoformat() == "2026-11-23"
    with pytest.raises(ValueError):
        next_planned_run(datetime(2026, 11, 22, 11, 0))

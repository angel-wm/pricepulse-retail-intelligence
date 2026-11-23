"""Dry-run schedule planning; no task or network request is created."""
import argparse
from datetime import datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

ZAGREB = ZoneInfo("Europe/Zagreb")


def next_planned_run(now):
    if now.utcoffset() is None:
        raise ValueError("timestamp must have a timezone")
    local = now.astimezone(ZAGREB)
    planned = datetime.combine(local.date(), time(12, 15), tzinfo=ZAGREB)
    if planned <= local:
        planned = datetime.combine(local.date() + timedelta(days=1), time(12, 15), tzinfo=ZAGREB)
    return planned


def main():
    parser = argparse.ArgumentParser(description="Print a proposed next run; does not configure a scheduler")
    parser.add_argument("--now", help="ISO 8601 timestamp with timezone; defaults to current UTC")
    args = parser.parse_args()
    now = datetime.fromisoformat(args.now) if args.now else datetime.now(timezone.utc)
    result = next_planned_run(now)
    print("Zagreb:", result.isoformat(), "UTC:", result.astimezone(timezone.utc).isoformat())


if __name__ == "__main__":
    main()

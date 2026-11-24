"""Create isolated inputs for the analytics export integration test."""
import csv
import io
from datetime import date
from itertools import combinations
from uuid import uuid4

import psycopg
from psycopg import sql

from pricepulse.analytics import export_analytics
from pricepulse.contracts import DIALECTS, FIELDS, STORES
from pricepulse.ingest import apply_schema, ingest_file
from pricepulse.matching import record_review


def gtin(n):
    base = f"{200000000000 + n:012d}"
    check = (-sum(int(c) * (3 if i % 2 else 1) for i, c in enumerate(base))) % 10
    return base + str(check)


def build(dsn, directory):
    schema = "pp_demo_" + uuid4().hex
    with psycopg.connect(dsn, autocommit=True) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {} ").format(sql.Identifier(schema)))
        try:
            conn.execute(sql.SQL("SET search_path TO {} ").format(sql.Identifier(schema)))
            apply_schema(conn)
            ids = []
            price_offsets = {"spar": 0, "kaufland": 10, "konzum": -5}
            for day_index, day in enumerate(("2026-01-01", "2026-01-02", "2026-01-03")):
                daily_files = []
                for source, store in STORES.items():
                    fields = FIELDS[source]
                    encoding, delimiter = DIALECTS[source]
                    stream = io.StringIO(newline="")
                    writer = csv.DictWriter(stream, fieldnames=list(fields.values()), delimiter=delimiter, lineterminator="\n")
                    writer.writeheader()
                    for i in range(1, 5):
                        cents = 100 + i * 35 + day_index * (i - 2) * 5 + price_offsets[source]
                        row = dict(code=f"fiction-{i}", title=f"Synthetic item {i}", brand="Fictional",
                                   quantity="1", unit="KOM", gtin=gtin(i))
                        if source == "konzum":
                            row.update(listed=f"{cents // 100}.{cents % 100:02d}", promotion="NE")
                        else:
                            row["regular"] = f"{cents // 100},{cents % 100:02d}"
                        writer.writerow({fields[key]: value for key, value in row.items()})
                    body = stream.getvalue().encode(encoding)
                    result = ingest_file(conn, source=source, store=store, day=day, url=f"https://www.{source}.hr/fictional-demo.csv", collected_at=f"{day}T12:00:00+00:00", status=200, body=body)
                    ids.append(result["file_id"])
                    daily_files.append(result["file_id"])
                for left, right in combinations(daily_files, 2):
                    for row in range(2, 6):
                        record_review(conn, (left, row), (right, row), "verified", "Fictional matching descriptors")
            export_analytics(conn, ids, directory, as_of=date(2026, 1, 3))
        finally:
            conn.execute("SET search_path TO public")
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))

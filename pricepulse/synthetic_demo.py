"""Build a fictional local BI dataset in a disposable PostgreSQL schema."""
import csv
import io
import os
from datetime import date
from pathlib import Path
from uuid import uuid4

import psycopg
from psycopg import sql

from pricepulse.analytics import export_analytics
from pricepulse.contracts import FIELDS
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
            for day_index, day in enumerate(("2026-01-01", "2026-01-02", "2026-01-03")):
                pair = []
                for source, store in (("spar", "8702"), ("kaufland", "5630")):
                    fields = FIELDS[source]
                    stream = io.StringIO(newline="")
                    writer = csv.DictWriter(stream, fieldnames=list(fields.values()), delimiter=";" if source == "spar" else "\t", lineterminator="\n")
                    writer.writeheader()
                    for i in range(1, 5):
                        cents = 100 + i * 35 + day_index * (i - 2) * 5 + (10 if source == "kaufland" else 0)
                        writer.writerow({fields["code"]: f"fiction-{i}", fields["title"]: f"Synthetic item {i}", fields["brand"]: "Fictional", fields["quantity"]: "1", fields["unit"]: "KOM", fields["regular"]: f"{cents // 100},{cents % 100:02d}", fields["gtin"]: gtin(i)})
                    body = stream.getvalue().encode("cp1250" if source == "spar" else "utf-8-sig")
                    result = ingest_file(conn, source=source, store=store, day=day, url=f"https://www.{source}.hr/fictional-demo.csv", collected_at=f"{day}T12:00:00+00:00", status=200, body=body)
                    ids.append(result["file_id"])
                    pair.append(result["file_id"])
                for row in range(2, 6):
                    record_review(conn, (pair[0], row), (pair[1], row), "verified", "Fictional matching descriptors")
            export_analytics(conn, ids, directory, as_of=date(2026, 1, 3))
        finally:
            conn.execute("SET search_path TO public")
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


if __name__ == "__main__":
    dsn = os.environ.get("PRICEPULSE_TEST_DSN")
    if not dsn:
        raise SystemExit("PRICEPULSE_TEST_DSN for a disposable database is required")
    build(dsn, Path("examples/tableau_synthetic"))

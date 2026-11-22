"""Run against a disposable PostgreSQL database when PRICEPULSE_TEST_DSN is set."""
import csv
import io
import os
from decimal import Decimal
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql

from pricepulse.contracts import FIELDS
from pricepulse.ingest import apply_schema, ingest_file
from pricepulse.matching import record_review

DSN = os.environ.get("PRICEPULSE_TEST_DSN")
pytestmark = pytest.mark.skipif(not DSN, reason="disposable PostgreSQL DSN not configured")


@pytest.fixture
def db():
    schema = "pp_test_" + uuid4().hex
    with psycopg.connect(DSN, autocommit=True) as conn:
        conn.execute(sql.SQL("CREATE SCHEMA {} ").format(sql.Identifier(schema)))
        try:
            conn.execute(sql.SQL("SET search_path TO {} ").format(sql.Identifier(schema)))
            apply_schema(conn)
            yield conn
        finally:
            conn.execute(sql.SQL("DROP SCHEMA {} CASCADE").format(sql.Identifier(schema)))


def synthetic_csv(price="1,00", extra=None, title="Example"):
    f = FIELDS["spar"]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(f.values()), delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerow({f["code"]: "sku-1", f["title"]: title, f["brand"]: "Example", f["quantity"]: "1", f["unit"]: "KOM", f["regular"]: price, f["gtin"]: "4006381333931"})
    if extra:
        writer.writerow(extra)
    return stream.getvalue().encode("cp1250")


def load(conn, body, day="2026-11-17"):
    return ingest_file(conn, source="spar", store="8702", day=day, url="https://www.spar.hr/example.csv", collected_at="2026-11-22T23:00:00+00:00", status=200, body=body)


def test_replay_version_and_constraints(db):
    first = load(db, synthetic_csv())
    replay = load(db, synthetic_csv())
    changed = load(db, synthetic_csv("1,20"))
    assert first["new_version"] and not replay["new_version"] and changed["new_version"]
    assert first["file_id"] == replay["file_id"] != changed["file_id"]
    assert db.execute("SELECT count(*) FROM source_file").fetchone()[0] == 2
    assert db.execute("SELECT count(*) FROM acquisition_run").fetchone()[0] == 3
    assert db.execute("SELECT count(*) FROM price_observation").fetchone()[0] == 2
    assert db.execute("SELECT effective_price FROM price_observation ORDER BY effective_price").fetchall() == [(Decimal("1.00"),), (Decimal("1.20"),)]
    with pytest.raises(psycopg.errors.CheckViolation), db.transaction():
        db.execute("UPDATE price_observation SET regular_price=NULL WHERE price_origin='regular'")


def test_duplicate_and_bad_price_are_preserved_for_review(db):
    f = FIELDS["spar"]
    load(db, synthetic_csv(extra={f["code"]: "sku-1", f["regular"]: "bad", f["gtin"]: "4006381333932"}))
    assert db.execute("SELECT count(*) FROM source_row").fetchone()[0] == 2
    assert db.execute("SELECT count(*) FROM price_observation").fetchone()[0] == 0
    reasons = {row[0] for row in db.execute("SELECT reason FROM review_exception")}
    assert {"duplicate_sku", "invalid_gtin", "price_invalid_price"} <= reasons
    assert db.execute("SELECT row_count,priced_rows,rows_for_review FROM source_quality").fetchone() == (2, 0, 2)
    before = db.execute("SELECT count(*) FROM source_file").fetchone()[0]
    with pytest.raises((ValueError, csv.Error)):
        load(db, b"invalid header\n")
    assert db.execute("SELECT count(*) FROM source_file").fetchone()[0] == before


def test_comparison_requires_version_specific_review_and_reconciles(db):
    first = load(db, synthetic_csv("1,00"))
    f = FIELDS["kaufland"]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(f.values()), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerow({f["code"]: "k-1", f["title"]: "Example", f["brand"]: "Example", f["quantity"]: "1", f["unit"]: "KOM", f["regular"]: "1,20", f["gtin"]: "4006381333931"})
    second = ingest_file(db, source="kaufland", store="5630", day="2026-11-17", url="https://www.kaufland.hr/file.csv", collected_at="2026-11-22T23:00:00+00:00", status=200, body=stream.getvalue().encode("utf-8-sig"))
    left, right = (first["file_id"], 2), (second["file_id"], 2)
    assert db.execute("SELECT count(*) FROM verified_price_comparison").fetchone()[0] == 0
    record_review(db, left, right, "review", "Awaiting product and pack review")
    assert db.execute("SELECT count(*) FROM verified_price_comparison").fetchone()[0] == 0
    record_review(db, left, right, "verified", "Synthetic descriptors and pack reviewed")
    assert db.execute("SELECT left_price,right_price,price_difference FROM verified_price_comparison").fetchall() == [(Decimal("1.00"), Decimal("1.20"), Decimal("-0.20"))]
    assert db.execute("SELECT count(*) FROM price_history").fetchone()[0] == 2
    record_review(db, right, left, "rejected", "Synthetic review reversed")
    assert db.execute("SELECT count(*) FROM verified_price_comparison").fetchone()[0] == 0
    assert db.execute("SELECT decision FROM comparison_review_event ORDER BY id").fetchall() == [("review",), ("verified",), ("rejected",)]


def test_price_changes_require_explicit_unambiguous_versions(db):
    first = load(db, synthetic_csv("1,00"), day="2026-11-16")
    second = load(db, synthetic_csv("1,20"))
    changed_version = load(db, synthetic_csv("1,30"))
    rows = db.execute("SELECT previous_price,current_price,difference FROM price_changes(%s)", ([first["file_id"], second["file_id"]],)).fetchall()
    assert rows == [(Decimal("1.00"), Decimal("1.20"), Decimal("0.20"))]
    with pytest.raises(psycopg.errors.RaiseException), db.transaction():
        db.execute("SELECT * FROM price_changes(%s)", ([first["file_id"], second["file_id"], changed_version["file_id"]],)).fetchall()
    changed_product = load(db, synthetic_csv("1,40", title="Example altered pack"), day="2026-11-18")
    assert db.execute("SELECT * FROM price_changes(%s)", ([second["file_id"], changed_product["file_id"]],)).fetchall() == []


def test_different_store_versions_cannot_overwrite_each_other(db):
    first = load(db, synthetic_csv())
    db.execute("INSERT INTO store VALUES ('spar','9999')")
    other = db.execute("INSERT INTO source_file(chain,store_id,price_list_date,sha256) VALUES ('spar','9999','2026-11-17',%s) RETURNING id", (first["sha256"],)).fetchone()[0]
    assert other != first["file_id"]
    assert db.execute("SELECT count(*) FROM source_file WHERE price_list_date='2026-11-17'").fetchone()[0] == 2
    with pytest.raises(psycopg.errors.ForeignKeyViolation), db.transaction():
        db.execute("INSERT INTO source_file(chain,store_id,price_list_date,sha256) VALUES ('spar','unknown','2026-11-17',%s)", (first["sha256"],))

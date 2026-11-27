"""Run against a disposable PostgreSQL database when PRICEPULSE_TEST_DSN is set."""
import csv
import io
import os
import json
from decimal import Decimal
from hashlib import sha256
from pathlib import Path
from types import SimpleNamespace
from uuid import uuid4

import psycopg
import pytest
from psycopg import sql

from pricepulse.contracts import DIALECTS, FIELDS, STORES, parse_csv
from pricepulse.ingest import apply_schema, ingest_file
from pricepulse.matching import queue_candidates, queue_history_changes, record_review
from pricepulse.metrics import reviewed_pair_coverage
from pricepulse.reliability import run_crawl
from pricepulse.recovery import resume_ingestion
from pricepulse.batch import run_batch

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


def test_duplicate_gtin_is_retained_and_flagged(db):
    f = FIELDS["spar"]
    load(db, synthetic_csv(extra={f["code"]: "sku-2", f["regular"]: "1,25", f["gtin"]: "4006381333931"}))
    assert db.execute("SELECT count(*) FROM source_row").fetchone()[0] == 2
    assert db.execute("SELECT count(*) FROM review_exception WHERE reason='duplicate_gtin'").fetchone()[0] == 2
    assert db.execute("SELECT count(*) FROM price_observation").fetchone()[0] == 2


def test_special_and_conflicting_prices_remain_auditable(db):
    f = FIELDS["spar"]
    extra = {f["code"]: "sku-2", f["regular"]: "2,00", f["special"]: "1,00"}
    body = synthetic_csv(price="", extra=extra)
    text = body.decode("cp1250")
    rows = list(csv.DictReader(io.StringIO(text), delimiter=";"))
    rows[0][f["special"]] = "0,75"
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(f.values()), delimiter=";", lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    load(db, stream.getvalue().encode("cp1250"))
    assert db.execute("SELECT effective_price,price_origin FROM price_observation").fetchall() == [(Decimal("0.75"), "special")]
    assert db.execute("SELECT count(*) FROM review_exception WHERE reason='price_conflicting_prices'").fetchone()[0] == 1
    assert db.execute("SELECT regular_raw,special_raw FROM source_row WHERE sku='sku-2'").fetchone() == ("2,00", "1,00")


def test_comparison_requires_version_specific_review_and_reconciles(db, tmp_path):
    sf = FIELDS["spar"]
    first = load(db, synthetic_csv("1,00", extra={sf["code"]: "s-2", sf["title"]: "Other", sf["brand"]: "Example", sf["quantity"]: "1", sf["unit"]: "KOM", sf["regular"]: "2,00", sf["gtin"]: "96385074"}))
    f = FIELDS["kaufland"]
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=list(f.values()), delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerow({f["code"]: "k-1", f["title"]: "Example", f["brand"]: "Example", f["quantity"]: "1", f["unit"]: "KOM", f["regular"]: "1,20", f["gtin"]: "4006381333931"})
    writer.writerow({f["code"]: "k-2", f["title"]: "Other variant", f["brand"]: "Example", f["quantity"]: "1", f["unit"]: "KOM", f["regular"]: "1,50", f["gtin"]: "96385074"})
    second = ingest_file(db, source="kaufland", store="5630", day="2026-11-17", url="https://www.kaufland.hr/file.csv", collected_at="2026-11-22T23:00:00+00:00", status=200, body=stream.getvalue().encode("utf-8-sig"))
    left, right = (first["file_id"], 2), (second["file_id"], 2)
    assert db.execute("SELECT count(*) FROM verified_price_comparison").fetchone()[0] == 0
    assert queue_candidates(db, first["file_id"], second["file_id"]) == {"candidates": 2, "queued": 2}
    assert reviewed_pair_coverage(db, first["file_id"], second["file_id"]) == {"eligible_queued_pairs": 2, "pending_pairs": 2, "verified_pairs": 0, "rejected_pairs": 0, "verified_fraction_of_queued": 0.0}
    assert "description_variant_or_pack_review" in db.execute("SELECT explanation FROM comparison_review WHERE left_row=3").fetchone()[0]
    assert queue_candidates(db, second["file_id"], first["file_id"]) == {"candidates": 2, "queued": 0}
    assert db.execute("SELECT count(*) FROM verified_price_comparison").fetchone()[0] == 0
    record_review(db, left, right, "verified", "Synthetic descriptors and pack reviewed")
    from datetime import date
    from pricepulse.analytics import export_analytics
    export_analytics(db, [first['file_id'], second['file_id']], tmp_path, as_of=date(2026, 11, 18))
    with (tmp_path / 'comparisons.csv').open(newline='', encoding='utf-8') as stream:
        comparisons = list(csv.DictReader(stream))
    assert len(comparisons) == 1 and comparisons[0]['price_difference'] == '-0.20'
    with (tmp_path / 'quality.csv').open(newline='', encoding='utf-8') as stream:
        quality = list(csv.DictReader(stream))
    assert len(quality) == 2 and all(row['file_age_days'] == '1' for row in quality)
    assert queue_candidates(db, first["file_id"], second["file_id"])["queued"] == 0
    assert db.execute("SELECT left_price,right_price,price_difference FROM verified_price_comparison").fetchall() == [(Decimal("1.00"), Decimal("1.20"), Decimal("-0.20"))]
    assert db.execute("SELECT count(*) FROM price_history").fetchone()[0] == 4
    with pytest.raises(psycopg.errors.UniqueViolation), db.transaction():
        db.execute("INSERT INTO comparison_review(left_file,left_row,right_file,right_row,decision,explanation) VALUES (%s,2,%s,3,'verified','duplicate')", (left[0], right[0]))
    record_review(db, (first["file_id"], 3), (second["file_id"], 3), "verified", "Synthetic variant wording manually reconciled")
    assert db.execute("SELECT price_difference FROM verified_price_comparison ORDER BY price_difference").fetchall() == [(Decimal("-0.20"),), (Decimal("0.50"),)]
    record_review(db, right, left, "rejected", "Synthetic review reversed")
    assert db.execute("SELECT count(*) FROM verified_price_comparison").fetchone()[0] == 1
    assert reviewed_pair_coverage(db, second["file_id"], first["file_id"])["verified_fraction_of_queued"] == 0.5
    assert db.execute("SELECT decision FROM comparison_review_event ORDER BY id").fetchall() == [("review",), ("review",), ("verified",), ("verified",), ("rejected",)]


def test_price_changes_require_explicit_unambiguous_versions(db, tmp_path):
    first = load(db, synthetic_csv("1,00"), day="2026-11-16")
    second = load(db, synthetic_csv("1,20"))
    changed_version = load(db, synthetic_csv("1,30"))
    rows = db.execute("SELECT previous_price,current_price,difference FROM price_changes(%s)", ([first["file_id"], second["file_id"]],)).fetchall()
    assert rows == [(Decimal("1.00"), Decimal("1.20"), Decimal("0.20"))]
    with pytest.raises(psycopg.errors.RaiseException), db.transaction():
        db.execute("SELECT * FROM price_changes(%s)", ([first["file_id"], second["file_id"], changed_version["file_id"]],)).fetchall()
    from datetime import date
    from pricepulse.analytics import export_analytics
    with pytest.raises(psycopg.errors.RaiseException):
        export_analytics(db, [first['file_id'], second['file_id'], changed_version['file_id']], tmp_path, as_of=date(2026, 11, 18))
    assert not list(tmp_path.glob('*.csv'))
    changed_product = load(db, synthetic_csv("1,40", title="Example altered pack"), day="2026-11-18")
    assert db.execute("SELECT * FROM price_changes(%s)", ([second["file_id"], changed_product["file_id"]],)).fetchall() == []
    assert queue_history_changes(db, second["file_id"], changed_product["file_id"]) == 1
    assert queue_history_changes(db, changed_product["file_id"], second["file_id"]) == 0
    assert "description_variant_or_pack_review" in db.execute("SELECT explanation FROM comparison_review").fetchone()[0]
    with pytest.raises(ValueError):
        record_review(db, (second["file_id"], 2), (changed_product["file_id"], 2), "verified", "Cannot verify same-chain comparison")


def test_different_store_versions_cannot_overwrite_each_other(db):
    first = load(db, synthetic_csv())
    db.execute("INSERT INTO store VALUES ('spar','9999')")
    other = db.execute("INSERT INTO source_file(chain,store_id,price_list_date,sha256) VALUES ('spar','9999','2026-11-17',%s) RETURNING id", (first["sha256"],)).fetchone()[0]
    assert other != first["file_id"]
    assert db.execute("SELECT count(*) FROM source_file WHERE price_list_date='2026-11-17'").fetchone()[0] == 2
    with pytest.raises(psycopg.errors.ForeignKeyViolation), db.transaction():
        db.execute("INSERT INTO source_file(chain,store_id,price_list_date,sha256) VALUES ('spar','unknown','2026-11-17',%s)", (first["sha256"],))


def test_price_change_counts_reconcile_with_fixture(db):
    f = FIELDS["spar"]
    def second(price):
        return {f["code"]: "sku-2", f["title"]: "Other", f["brand"]: "Example", f["quantity"]: "1", f["unit"]: "KOM", f["regular"]: price, f["gtin"]: "96385074"}
    first = load(db, synthetic_csv("1,00", extra=second("2,00")), day="2026-11-16")
    second_day = load(db, synthetic_csv("1,20", extra=second("1,50")))
    result = db.execute("""SELECT count(*) FILTER (WHERE difference>0), count(*) FILTER (WHERE difference<0), count(*) FILTER (WHERE difference=0)
                           FROM price_changes(%s)""", ([first["file_id"], second_day["file_id"]],)).fetchone()
    assert result == (1, 1, 0)  # Independently calculated from the two synthetic input rows.


def test_three_retailer_exports_reconcile_with_expected_values(tmp_path):
    from analytics_fixture import build
    build(DSN, tmp_path)
    def rows(name):
        with (tmp_path / f'{name}.csv').open(encoding='utf-8', newline='') as stream:
            return list(csv.DictReader(stream))
    observations, changes, comparisons, quality = (rows(n) for n in ('observations', 'changes', 'comparisons', 'quality'))
    assert (len(observations), len(changes), len(comparisons), len(quality)) == (36, 24, 36, 9)
    gaps = {("spar", "kaufland"): Decimal("-0.10"), ("spar", "konzum"): Decimal("0.05"),
            ("kaufland", "konzum"): Decimal("0.15")}
    for chains, gap in gaps.items():
        values = [Decimal(row["price_difference"]) for row in comparisons
                  if (row["left_chain"], row["right_chain"]) == chains]
        assert values == [gap] * 12
    assert all(row['priced_fraction'] == '1.00000000000000000000' for row in quality)


def test_resume_after_commit_interruption_is_idempotent(db, tmp_path, monkeypatch):
    import pricepulse.recovery as recovery
    body = synthetic_csv()
    digest = sha256(body).hexdigest()
    url = "https://www.spar.hr/example.csv"
    timestamp = "2026-11-22T23:00:00+00:00"
    rows = list(parse_csv(body, "spar", "8702", "2026-11-17", url, digest))
    def synthetic_runner(command, **kwargs):
        feed = Path(command[command.index("-O") + 1])
        raw = Path(next(x.split("=", 1)[1] for x in command if x.startswith("raw_path=")))
        log = Path(next(x.split("=", 1)[1] for x in command if x.startswith("LOG_FILE=")))
        manifest = {"type": "manifest", "source": "spar", "store_id": "8702", "publication_date": "2026-11-17", "http_status": 200, "source_url": url, "retrieved_at_utc": timestamp, "sha256": digest, "row_count": len(rows)}
        feed.write_text("".join(json.dumps(item) + "\n" for item in [manifest, *({"type": "record", **r} for r in rows)]), encoding="utf-8")
        raw.write_bytes(body)
        log.write_text("Spider closed (finished)\n", encoding="utf-8")
        return SimpleNamespace(returncode=0)
    path, result = run_crawl("spar", "2026-11-17", tmp_path, runner=synthetic_runner)
    assert result["status"] == "success"
    older_report = json.loads(path.read_text(encoding="utf-8"))
    older_report["summary"].pop("price_origin_counts")
    path.write_text(json.dumps(older_report), encoding="utf-8")
    original = recovery.ingest_file
    def committed_then_interrupted(*args, **kwargs):
        original(*args, **kwargs)
        raise RuntimeError("simulated interruption after commit")
    monkeypatch.setattr(recovery, "ingest_file", committed_then_interrupted)
    assert resume_ingestion(path, db)["ingestion"]["status"] == "failed"
    monkeypatch.setattr(recovery, "ingest_file", original)
    resumed = resume_ingestion(path, db)
    assert resumed["ingestion"]["status"] == "success" and not resumed["ingestion"]["new_version"]
    assert db.execute("SELECT count(*) FROM price_observation").fetchone()[0] == 1
    raw = path.with_suffix(".csv")
    raw.write_bytes(b"tampered")
    assert resume_ingestion(path, db)["ingestion"]["status"] == "failed"
    assert db.execute("SELECT count(*) FROM price_observation").fetchone()[0] == 1


def test_three_store_batch_and_replay(db, tmp_path):
    def crawl(source, day, directory):
        mapping = FIELDS[source]
        store = STORES[source]
        encoding, delimiter = DIALECTS[source]
        stream = io.StringIO(newline="")
        writer = csv.DictWriter(stream, fieldnames=list(mapping.values()), delimiter=delimiter, lineterminator="\n")
        writer.writeheader()
        values = dict(code="synthetic", title="Example", brand="Example", quantity="1", unit="KOM", gtin="4006381333931")
        if source == "konzum":
            values.update(listed="1.00", promotion="DA")
        else:
            values.update(regular="1,00")
        writer.writerow({mapping[key]: value for key, value in values.items()})
        body = stream.getvalue().encode(encoding)
        digest = sha256(body).hexdigest()
        url = f"https://www.{source}.hr/file.csv"
        if source == "konzum":
            url = "https://d2depcln7eup0h.cloudfront.net/synthetic.csv"
        rows = list(parse_csv(body, source, store, day, url, digest))
        def runner(command, **kwargs):
            feed = Path(command[command.index("-O") + 1])
            raw = Path(next(x.split("=", 1)[1] for x in command if x.startswith("raw_path=")))
            log = Path(next(x.split("=", 1)[1] for x in command if x.startswith("LOG_FILE=")))
            manifest = {"type": "manifest", "source": source, "store_id": store, "publication_date": day, "http_status": 200, "source_url": url, "retrieved_at_utc": "2026-11-22T23:00:00+00:00", "sha256": digest, "row_count": len(rows)}
            feed.write_text("".join(json.dumps(x) + "\n" for x in [manifest, *({"type": "record", **r} for r in rows)]), encoding="utf-8")
            raw.write_bytes(body)
            log.write_text("Spider closed (finished)\n", encoding="utf-8")
            return SimpleNamespace(returncode=0)
        return run_crawl(source, day, directory, runner=runner)
    for _ in range(2):
        _, result = run_batch("2026-11-17", tmp_path, crawl=crawl, ingest=lambda p: resume_ingestion(p, db))
        assert result["status"] == "success" and result["mode"] == "ingest"
    assert db.execute("SELECT count(*) FROM source_file").fetchone()[0] == 3
    assert db.execute("SELECT count(*) FROM price_observation").fetchone()[0] == 3
    assert db.execute("SELECT count(*) FROM acquisition_run").fetchone()[0] == 6
    apply_schema(db)
    assert db.execute("SELECT chain FROM retailer ORDER BY chain").fetchall() == [("kaufland",), ("konzum",), ("spar",)]

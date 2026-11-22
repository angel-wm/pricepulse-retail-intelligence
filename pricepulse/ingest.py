"""Transactional local CSV ingestion; raw source bytes never leave the caller."""
from collections import Counter
from datetime import date, datetime
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit

from psycopg.types.json import Jsonb

from pricepulse.contracts import parse_csv

STORES = {"spar": "8702", "kaufland": "5630"}


def ingest_file(conn, *, source, store, day, url, collected_at, status, body):
    if source not in STORES or store != STORES[source]:
        raise ValueError("unsupported source or store")
    date.fromisoformat(day)
    when = datetime.fromisoformat(collected_at)
    if when.utcoffset() is None:
        raise ValueError("collection timestamp must have a timezone")
    parts = urlsplit(url)
    if parts.scheme != "https" or parts.hostname != f"www.{source}.hr" or parts.username or parts.password or parts.port not in (None, 443):
        raise ValueError("unapproved source URL")
    if status != 200:
        raise ValueError("only successful file retrievals may be ingested")
    digest = sha256(body).hexdigest()
    rows = list(parse_csv(body, source, store, day, url, digest))
    if not rows:
        raise ValueError("empty source file")
    sku_count = Counter(row["code"].strip() for row in rows if row["code"].strip())
    gtin_count = Counter(row["gtin_normalized"] for row in rows if row["gtin_normalized"])
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("INSERT INTO retailer VALUES (%s) ON CONFLICT DO NOTHING", (source,))
        cur.execute("INSERT INTO store VALUES (%s,%s) ON CONFLICT DO NOTHING", (source, store))
        cur.execute("""INSERT INTO source_file(chain,store_id,price_list_date,sha256)
            VALUES (%s,%s,%s,%s) ON CONFLICT DO NOTHING RETURNING id""", (source, store, day, digest))
        result = cur.fetchone()
        is_new = result is not None
        if is_new:
            file_id = result[0]
        else:
            cur.execute("SELECT id FROM source_file WHERE chain=%s AND store_id=%s AND price_list_date=%s AND sha256=%s", (source, store, day, digest))
            file_id = cur.fetchone()[0]
        cur.execute("INSERT INTO acquisition_run(file_id,source_url,collected_at_utc,http_status) VALUES (%s,%s,%s,%s)", (file_id, url, when, status))
        if is_new:
            for row in rows:
                sku = row["code"].strip() or None
                if sku:
                    cur.execute("INSERT INTO source_product VALUES (%s,%s) ON CONFLICT DO NOTHING", (source, sku))
                cur.execute("""INSERT INTO source_row(file_id,chain,row_number,sku,gtin_raw,gtin_normalized,title,brand,quantity,unit,regular_raw,special_raw,raw_row,ingestion_status)
                    VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)""", (file_id, source, row["row_number"], sku, row["gtin_raw"], row["gtin_normalized"], row["title"], row["brand"], row["quantity"], row["unit"], row["regular"], row["special"], Jsonb(row["raw_row"]), row["ingestion_status"]))
                reasons = []
                if not sku:
                    reasons.append("missing_sku")
                elif sku_count[sku] > 1:
                    reasons.append("duplicate_sku")
                if row["gtin_raw"].strip() and not row["gtin_normalized"]:
                    reasons.append("invalid_gtin")
                if row["gtin_normalized"] and gtin_count[row["gtin_normalized"]] > 1:
                    reasons.append("duplicate_gtin")
                if not row["brand"].strip():
                    reasons.append("missing_brand")
                if not row["quantity"].strip() or not row["unit"].strip():
                    reasons.append("missing_quantity_or_unit")
                if row["ingestion_status"] != "ok":
                    reasons.append("price_" + row["ingestion_status"].replace(" ", "_"))
                for reason in reasons:
                    cur.execute("INSERT INTO review_exception VALUES (%s,%s,%s)", (file_id, row["row_number"], reason))
                if sku and sku_count[sku] == 1 and row["ingestion_status"] == "ok":
                    cur.execute("""INSERT INTO price_observation(file_id,row_number,regular_price,special_price,effective_price,price_origin)
                        VALUES (%s,%s,%s,%s,%s,%s)""", (file_id, row["row_number"], row["regular_price_eur"], row["special_price_eur"], row["effective_price_eur"], row["price_origin"]))
    return {"file_id": file_id, "sha256": digest, "new_version": is_new, "rows": len(rows)}


def apply_schema(conn):
    directory = Path(__file__).resolve().parent.parent / "sql"
    with conn.transaction(), conn.cursor() as cur:
        for path in sorted(directory.glob("*.sql")):
            cur.execute(path.read_text(encoding="utf-8"))


def main():
    import argparse
    import json
    import os
    import psycopg

    parser = argparse.ArgumentParser(description="Initialize or load a private PricePulse PostgreSQL database")
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("init", help="apply schema to the current search_path")
    load = commands.add_parser("load", help="ingest a locally held source CSV")
    load.add_argument("--source", choices=tuple(STORES), required=True)
    load.add_argument("--store", required=True)
    load.add_argument("--date", required=True)
    load.add_argument("--url", required=True)
    load.add_argument("--collected-at", required=True)
    load.add_argument("--http-status", type=int, required=True)
    load.add_argument("--csv", type=Path, required=True)
    args = parser.parse_args()
    dsn = os.environ.get("PRICEPULSE_DSN")
    if not dsn:
        parser.error("set PRICEPULSE_DSN to the private PostgreSQL database")
    with psycopg.connect(dsn) as conn:
        if args.command == "init":
            apply_schema(conn)
            conn.commit()
            print("Schema applied")
        else:
            result = ingest_file(conn, source=args.source, store=args.store, day=args.date, url=args.url, collected_at=args.collected_at, status=args.http_status, body=args.csv.read_bytes())
            conn.commit()
            print(json.dumps(result))


if __name__ == "__main__":
    main()

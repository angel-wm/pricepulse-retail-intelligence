"""Export explicitly selected private PostgreSQL versions for local BI analysis."""
import argparse
import csv
import os
from pathlib import Path

import psycopg


QUERIES = {
    "observations": """SELECT chain, store_id, price_list_date, file_id, sku, title,
        gtin_normalized, quantity, unit, effective_price, price_origin
        FROM price_history WHERE file_id = ANY(%s) ORDER BY chain, store_id, sku, price_list_date""",
    "changes": "SELECT * FROM price_changes(%s) ORDER BY chain, store_id, sku, observed_date",
    "comparisons": """SELECT * FROM verified_price_comparison
        WHERE left_file = ANY(%s) AND right_file = ANY(%s) ORDER BY price_list_date, review_id""",
    "quality": """SELECT *, priced_rows::numeric / NULLIF(row_count, 0) AS priced_fraction,
        valid_gtin_rows::numeric / NULLIF(row_count, 0) AS valid_gtin_fraction
        FROM source_quality WHERE file_id = ANY(%s) ORDER BY chain, store_id, price_list_date""",
}


def export_analytics(conn, file_ids, directory, *, as_of):
    """Select one file version per store/date and write local-only CSV exports."""
    if not file_ids:
        raise ValueError("at least one explicit file ID is required")
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    with conn.transaction(), conn.cursor() as cur:
        # Reuse the Phase 2 version guard before producing any exports.
        cur.execute("SELECT * FROM price_changes(%s)", (file_ids,))
        for name, query in QUERIES.items():
            params = (file_ids, file_ids) if name == "comparisons" else (file_ids,)
            cur.execute(query, params)
            rows = cur.fetchall()
            with (directory / f"{name}.csv").open("w", encoding="utf-8", newline="") as stream:
                writer = csv.writer(stream)
                columns = [item.name for item in cur.description]
                if name == "quality":
                    columns += ["reference_date", "file_age_days"]
                writer.writerow(columns)
                for row in rows:
                    if name == "quality":
                        row = (*row, as_of, (as_of - row[3]).days)
                    writer.writerow(row)


def main():
    from datetime import date

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--file-id", action="append", type=int, required=True)
    parser.add_argument("--directory", type=Path, required=True)
    parser.add_argument("--as-of", type=date.fromisoformat, required=True)
    args = parser.parse_args()
    dsn = os.environ.get("PRICEPULSE_DSN")
    if not dsn:
        parser.error("PRICEPULSE_DSN is required")
    with psycopg.connect(dsn) as conn:
        export_analytics(conn, args.file_id, args.directory, as_of=args.as_of)


if __name__ == "__main__":
    main()

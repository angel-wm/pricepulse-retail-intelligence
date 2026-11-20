"""Source-specific parsing, with explicit row exceptions."""
import csv
import io
import re
from decimal import Decimal, InvalidOperation

FIELDS = {
    "spar": {"title": "naziv", "code": "šifra", "brand": "marka", "quantity": "neto količina", "unit": "jedinica mjere", "regular": "MPC (EUR)", "special": "MPC za vrijeme posebnog oblika prodaje (EUR)", "gtin": "barkod", "category": "kategorija proizvoda"},
    "kaufland": {"title": "naziv proizvoda", "code": "šifra proizvoda", "brand": "marka proizvoda", "quantity": "neto količina(KG)", "unit": "jedinica mjere", "regular": "maloprod.cijena(EUR)", "special": "MPC poseb.oblik prod", "gtin": "barkod", "category": "kategorija proizvoda"},
}

def gtin(value):
    raw = value.strip()
    if not re.fullmatch(r"(?:\d{8}|\d{12,14})", raw):
        return None
    total = sum(int(n) * (3 if i % 2 == 0 else 1) for i, n in enumerate(reversed(raw[:-1])))
    return raw.zfill(14) if (10 - total % 10) % 10 == int(raw[-1]) else None

def amount(value):
    value = value.strip()
    if not value:
        return None
    if not re.fullmatch(r"(?:\d+(?:,\d+)?|,\d+)", value):
        raise ValueError("invalid price")
    try:
        result = Decimal(value.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("invalid price") from exc
    if result <= 0:
        raise ValueError("non-positive price")
    return result

def parse_csv(body, source, store_id, date, url, sha256):
    encoding, delimiter = ("cp1250", ";") if source == "spar" else ("utf-8-sig", "\t")
    reader = csv.DictReader(io.StringIO(body.decode(encoding), newline=""), delimiter=delimiter, strict=True)
    mapping = FIELDS[source]
    if not reader.fieldnames or len(set(reader.fieldnames)) != len(reader.fieldnames) or not set(mapping.values()).issubset(reader.fieldnames):
        raise ValueError("unknown or duplicate CSV headers")
    for row_number, row in enumerate(reader, 2):
        if None in row or any(v is None for v in row.values()):
            raise ValueError(f"malformed CSV row {row_number}")
        record = {key: row[column] for key, column in mapping.items()}
        record.update(source_chain=source, source_store_id=store_id, price_list_date=date, source_url=url, source_file_hash=sha256, raw_row=row, row_number=row_number)
        record["gtin_raw"] = record.pop("gtin")
        record["gtin_normalized"] = gtin(record["gtin_raw"])
        try:
            regular, special = amount(record["regular"]), amount(record["special"])
            if regular and special and regular != special:
                raise ValueError("conflicting prices")
            if not regular and not special:
                raise ValueError("missing price")
            record.update(regular_price_eur=str(regular) if regular else None, special_price_eur=str(special) if special else None, effective_price_eur=str(regular or special), price_origin="both_equal" if regular and special else "regular" if regular else "special", ingestion_status="ok")
        except ValueError as exc:
            record.update(regular_price_eur=None, special_price_eur=None, effective_price_eur=None, price_origin=None, ingestion_status=str(exc))
        yield record

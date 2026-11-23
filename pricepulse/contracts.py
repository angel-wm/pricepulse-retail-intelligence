"""Source-specific parsing, with explicit row exceptions."""
import csv
import io
import re
from decimal import Decimal, InvalidOperation

STORES = {"spar": "8702", "kaufland": "5630", "konzum": "1280"}
DIALECTS = {"spar": ("cp1250", ";"), "kaufland": ("utf-8-sig", "\t"), "konzum": ("utf-8-sig", ",")}

FIELDS = {
    "spar": {"title": "naziv", "code": "šifra", "brand": "marka", "quantity": "neto količina", "unit": "jedinica mjere", "regular": "MPC (EUR)", "special": "MPC za vrijeme posebnog oblika prodaje (EUR)", "gtin": "barkod", "category": "kategorija proizvoda"},
    "kaufland": {"title": "naziv proizvoda", "code": "šifra proizvoda", "brand": "marka proizvoda", "quantity": "neto količina(KG)", "unit": "jedinica mjere", "regular": "maloprod.cijena(EUR)", "special": "MPC poseb.oblik prod", "gtin": "barkod", "category": "kategorija proizvoda"},
    "konzum": {
        "title": "NAZIV PROIZVODA",
        "code": "ŠIFRA PROIZVODA",
        "brand": "MARKA PROIZVODA",
        "quantity": "NETO KOLIČINA",
        "unit": "JEDINICA MJERE",
        "listed": "MALOPRODAJNA CIJENA",
        "promotion": "POSEBAN OBLIK PRODAJE",
        "gtin": "BARKOD",
    },
}

def gtin(value):
    raw = value.strip()
    if not re.fullmatch(r"(?:\d{8}|\d{12,14})", raw):
        return None
    total = sum(int(n) * (3 if i % 2 == 0 else 1) for i, n in enumerate(reversed(raw[:-1])))
    return raw.zfill(14) if (10 - total % 10) % 10 == int(raw[-1]) else None

def amount(value, *, allow_dot=False):
    value = value.strip()
    if not value:
        return None
    separator = "[.,]" if allow_dot else ","
    if not re.fullmatch(rf"(?:\d+(?:{separator}\d+)?|{separator}\d+)", value):
        raise ValueError("invalid price")
    try:
        result = Decimal(value.replace(",", "."))
    except InvalidOperation as exc:
        raise ValueError("invalid price") from exc
    if result <= 0:
        raise ValueError("non-positive price")
    return result

def parse_csv(body, source, store_id, date, url, sha256):
    encoding, delimiter = DIALECTS[source]
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
        if source == "konzum":
            listed = record.pop("listed")
            promotion = record.pop("promotion").strip().upper()
            record.update(regular=listed if promotion == "NE" else "", special=listed if promotion == "DA" else "")
            if record["gtin_normalized"] == "00000000000000":
                record["gtin_normalized"] = None
        try:
            if source == "konzum" and promotion not in {"DA", "NE"}:
                raise ValueError("unknown promotion indicator")
            regular = amount(record["regular"], allow_dot=source == "konzum")
            special = amount(record["special"], allow_dot=source == "konzum")
            if regular and special and regular != special:
                raise ValueError("conflicting prices")
            if not regular and not special:
                raise ValueError("missing price")
            record.update(regular_price_eur=str(regular) if regular else None, special_price_eur=str(special) if special else None, effective_price_eur=str(regular or special), price_origin="both_equal" if regular and special else "regular" if regular else "special", ingestion_status="ok")
        except ValueError as exc:
            record.update(regular_price_eur=None, special_price_eur=None, effective_price_eur=None, price_origin=None, ingestion_status=str(exc))
        yield record

"""Conservative comparison review: equality of identifiers is not proof of identity."""
import re
from decimal import Decimal


def _declared_mass_kg(row, chain):
    """Interpret the source quantity field independently of the sale unit."""
    # Kaufland labels the quantity column in kg, regardless of its separate unit field.
    unit = "kg" if chain == "kaufland" else row["unit"].strip().casefold()
    value = row["quantity"].strip()
    if unit not in {"kg", "g"} or not re.fullmatch(r"[0-9]+(?:[.,][0-9]+)?", value):
        return None
    mass = Decimal(value.replace(",", ".") + ("e-3" if unit == "g" else ""))
    return mass if mass > 0 else None


def comparison_flags(left, right, brand_aliases=None, *, cross_retailer_chains=None):
    aliases = brand_aliases or {}
    def brand(value):
        value = " ".join(value.casefold().split())
        return aliases.get(value, value)
    flags = []
    if not left["gtin_normalized"] or left["gtin_normalized"] != right["gtin_normalized"]:
        flags.append("gtin_mismatch_or_invalid")
    if not left["brand"].strip() or not right["brand"].strip() or brand(left["brand"]) != brand(right["brand"]):
        flags.append("brand_review")
    if cross_retailer_chains is not None:
        left_chain, right_chain = cross_retailer_chains
        left_mass = _declared_mass_kg(left, left_chain)
        right_mass = _declared_mass_kg(right, right_chain)
        if left_mass is None or right_mass is None:
            flags.append("declared_mass_not_comparable")
        elif left_mass != right_mass:
            flags.append("declared_mass_difference_review")
    elif not left["quantity"].strip() or not right["quantity"].strip() or not left["unit"].strip() or not right["unit"].strip() or (left["quantity"].strip(), left["unit"].strip().casefold()) != (right["quantity"].strip(), right["unit"].strip().casefold()):
        flags.append("quantity_or_unit_review")
    if not left["title"].strip() or not right["title"].strip() or " ".join(left["title"].casefold().split()) != " ".join(right["title"].casefold().split()):
        flags.append("description_variant_or_pack_review")
    return flags


def queue_candidates(conn, file_a, file_b, brand_aliases=None):
    """Queue exact-GTIN candidates for two explicitly selected files; never approve them."""
    if file_a == file_b:
        raise ValueError("two distinct source files are required")
    first, second = sorted((file_a, file_b))
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("SELECT id,chain,price_list_date FROM source_file WHERE id IN (%s,%s) ORDER BY id", (first, second))
        files = cur.fetchall()
        if len(files) != 2 or files[0][1] == files[1][1] or files[0][2] != files[1][2]:
            raise ValueError("select two files from different chains for the same date")
        chains = (files[0][1], files[1][1])
        cur.execute("""SELECT l.row_number, r.row_number, l.gtin_normalized,
                              l.title,l.brand,l.quantity,l.unit,r.title,r.brand,r.quantity,r.unit
                       FROM source_row l JOIN source_row r ON l.gtin_normalized=r.gtin_normalized
                       JOIN price_observation lp ON (lp.file_id,lp.row_number)=(l.file_id,l.row_number)
                       JOIN price_observation rp ON (rp.file_id,rp.row_number)=(r.file_id,r.row_number)
                       WHERE l.file_id=%s AND r.file_id=%s AND l.gtin_normalized IS NOT NULL
                         AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(l.file_id,l.row_number))
                         AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(r.file_id,r.row_number))""", (first, second))
        pairs = cur.fetchall()
        added = 0
        for lrow, rrow, code, lt, lb, lq, lu, rt, rb, rq, ru in pairs:
            left = dict(gtin_normalized=code, title=lt, brand=lb, quantity=lq, unit=lu)
            right = dict(gtin_normalized=code, title=rt, brand=rb, quantity=rq, unit=ru)
            flags = comparison_flags(left, right, brand_aliases, cross_retailer_chains=chains)
            explanation = "Candidate requires human review" + (": " + ", ".join(flags) if flags else "; descriptors consistent")
            cur.execute("""INSERT INTO comparison_review(left_file,left_row,right_file,right_row,decision,explanation)
                           VALUES (%s,%s,%s,%s,'review',%s)
                           ON CONFLICT (left_file,left_row,right_file,right_row) DO NOTHING RETURNING id""", (first,lrow,second,rrow,explanation))
            result = cur.fetchone()
            if result:
                added += 1
                cur.execute("INSERT INTO comparison_review_event(review_id,decision,explanation) VALUES (%s,'review',%s)", (result[0], explanation))
    return {"candidates": len(pairs), "queued": added}


def queue_history_changes(conn, file_a, file_b):
    """Queue changed same-store SKU descriptors for two explicitly selected dates."""
    if file_a == file_b:
        raise ValueError("two distinct source files are required")
    first, second = sorted((file_a, file_b))
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("SELECT chain,store_id,price_list_date FROM source_file WHERE id IN (%s,%s) ORDER BY id", (first, second))
        files = cur.fetchall()
        if len(files) != 2 or files[0][:2] != files[1][:2] or files[0][2] == files[1][2]:
            raise ValueError("select two dates for the same source and store")
        cur.execute("""SELECT l.row_number,r.row_number,l.gtin_normalized,r.gtin_normalized,
                              l.title,l.brand,l.quantity,l.unit,r.title,r.brand,r.quantity,r.unit
                       FROM source_row l JOIN source_row r ON l.sku=r.sku AND l.chain=r.chain
                       WHERE l.file_id=%s AND r.file_id=%s AND l.sku IS NOT NULL
                         AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(l.file_id,l.row_number))
                         AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(r.file_id,r.row_number))""", (first, second))
        pairs = cur.fetchall()
        added = 0
        for lr, rr, lg, rg, lt, lb, lq, lu, rt, rb, rq, ru in pairs:
            flags = comparison_flags(dict(gtin_normalized=lg, title=lt, brand=lb, quantity=lq, unit=lu), dict(gtin_normalized=rg, title=rt, brand=rb, quantity=rq, unit=ru))
            if not flags:
                continue
            explanation = "Historical descriptor change requires review: " + ", ".join(flags)
            cur.execute("""INSERT INTO comparison_review(left_file,left_row,right_file,right_row,decision,explanation)
                           VALUES (%s,%s,%s,%s,'review',%s)
                           ON CONFLICT (left_file,left_row,right_file,right_row) DO NOTHING RETURNING id""", (first,lr,second,rr,explanation))
            result = cur.fetchone()
            if result:
                added += 1
                cur.execute("INSERT INTO comparison_review_event(review_id,decision,explanation) VALUES (%s,'review',%s)", (result[0], explanation))
    return added


def record_review(conn, left, right, decision, explanation):
    """Persist an explicit human decision for two exact file rows, never an automatic match."""
    if decision not in {"verified", "rejected", "review"} or not explanation.strip():
        raise ValueError("decision and explanation are required")
    with conn.transaction(), conn.cursor() as cur:
        cur.execute("""SELECT f.chain,f.price_list_date,r.gtin_normalized,
                   EXISTS(SELECT 1 FROM price_observation p WHERE (p.file_id,p.row_number)=(r.file_id,r.row_number)),
                   EXISTS(SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(r.file_id,r.row_number))
                   FROM source_row r JOIN source_file f ON f.id=r.file_id
                   WHERE (r.file_id,r.row_number) IN ((%s,%s),(%s,%s))
                   ORDER BY r.file_id,r.row_number""", (*left, *right))
        rows = cur.fetchall()
        if len(rows) != 2:
            raise ValueError("two distinct source rows are required")
        if decision == "verified" and (rows[0][0] == rows[1][0] or rows[0][1] != rows[1][1] or not rows[0][2] or rows[0][2] != rows[1][2] or not all(r[3] and not r[4] for r in rows)):
            raise ValueError("verified comparison requires same date, valid shared GTIN, two chains, prices and no unresolved ingestion exceptions")
        l, r = sorted((left, right))
        cur.execute("""INSERT INTO comparison_review(left_file,left_row,right_file,right_row,decision,explanation)
                       VALUES (%s,%s,%s,%s,%s,%s)
                       ON CONFLICT (left_file,left_row,right_file,right_row)
                       DO UPDATE SET decision=EXCLUDED.decision, explanation=EXCLUDED.explanation, reviewed_at=now()
                       RETURNING id""", (*l,*r,decision,explanation))
        review_id = cur.fetchone()[0]
        cur.execute("INSERT INTO comparison_review_event(review_id,decision,explanation) VALUES (%s,%s,%s)", (review_id, decision, explanation))

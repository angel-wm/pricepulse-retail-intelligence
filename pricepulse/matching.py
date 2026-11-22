"""Conservative comparison review: equality of identifiers is not proof of identity."""

def comparison_flags(left, right, brand_aliases=None):
    aliases = brand_aliases or {}
    def brand(value):
        value = " ".join(value.casefold().split())
        return aliases.get(value, value)
    flags = []
    if not left["gtin_normalized"] or left["gtin_normalized"] != right["gtin_normalized"]:
        flags.append("gtin_mismatch_or_invalid")
    if not left["brand"].strip() or not right["brand"].strip() or brand(left["brand"]) != brand(right["brand"]):
        flags.append("brand_review")
    if not left["quantity"].strip() or not right["quantity"].strip() or not left["unit"].strip() or not right["unit"].strip() or (left["quantity"].strip(), left["unit"].strip().casefold()) != (right["quantity"].strip(), right["unit"].strip().casefold()):
        flags.append("quantity_or_unit_review")
    if not left["title"].strip() or not right["title"].strip() or " ".join(left["title"].casefold().split()) != " ".join(right["title"].casefold().split()):
        flags.append("description_variant_or_pack_review")
    return flags


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

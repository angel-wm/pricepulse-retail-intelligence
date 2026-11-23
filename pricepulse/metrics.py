"""Metrics for explicitly selected source versions, without inferring inventory."""

def reviewed_pair_coverage(conn, file_a, file_b):
    """Count eligible queued pairs; the denominator is not either retailer's catalogue."""
    if file_a == file_b:
        raise ValueError("two distinct files required")
    left, right = sorted((file_a, file_b))
    with conn.cursor() as cur:
        cur.execute("SELECT chain,price_list_date FROM source_file WHERE id IN (%s,%s) ORDER BY id", (left, right))
        files = cur.fetchall()
        if len(files) != 2 or files[0][0] == files[1][0] or files[0][1] != files[1][1]:
            raise ValueError("select different chains on the same date")
        cur.execute("""SELECT count(*),
                     count(*) FILTER (WHERE c.decision='review'),
                     count(*) FILTER (WHERE c.decision='verified'),
                     count(*) FILTER (WHERE c.decision='rejected')
                     FROM comparison_review c
                     JOIN source_row l ON (l.file_id,l.row_number)=(c.left_file,c.left_row)
                     JOIN source_row r ON (r.file_id,r.row_number)=(c.right_file,c.right_row)
                     JOIN price_observation lp ON (lp.file_id,lp.row_number)=(l.file_id,l.row_number)
                     JOIN price_observation rp ON (rp.file_id,rp.row_number)=(r.file_id,r.row_number)
                     WHERE c.left_file=%s AND c.right_file=%s
                       AND l.gtin_normalized IS NOT NULL AND l.gtin_normalized=r.gtin_normalized
                       AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(l.file_id,l.row_number))
                       AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(r.file_id,r.row_number))""", (left, right))
        queued, pending, verified, rejected = cur.fetchone()
    return {"eligible_queued_pairs": queued, "pending_pairs": pending, "verified_pairs": verified,
            "rejected_pairs": rejected, "verified_fraction_of_queued": verified / queued if queued else None}

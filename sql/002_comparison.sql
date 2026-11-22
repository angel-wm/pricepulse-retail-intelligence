-- Decisions apply only to these exact rows and source-file versions.
CREATE TABLE IF NOT EXISTS comparison_review (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    left_file bigint NOT NULL,
    left_row integer NOT NULL,
    right_file bigint NOT NULL,
    right_row integer NOT NULL,
    decision text NOT NULL CHECK (decision IN ('verified', 'rejected', 'review')),
    explanation text NOT NULL CHECK (length(trim(explanation)) > 0),
    reviewed_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (left_file, left_row) REFERENCES source_row(file_id, row_number),
    FOREIGN KEY (right_file, right_row) REFERENCES source_row(file_id, row_number),
    UNIQUE (left_file, left_row, right_file, right_row),
    CHECK (left_file <> right_file)
);
CREATE UNIQUE INDEX IF NOT EXISTS comparison_one_left_per_file ON comparison_review(left_file,left_row,right_file) WHERE decision='verified';
CREATE UNIQUE INDEX IF NOT EXISTS comparison_one_right_per_file ON comparison_review(right_file,right_row,left_file) WHERE decision='verified';

CREATE TABLE IF NOT EXISTS comparison_review_event (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    review_id bigint NOT NULL REFERENCES comparison_review(id),
    decision text NOT NULL CHECK (decision IN ('verified', 'rejected', 'review')),
    explanation text NOT NULL CHECK (length(trim(explanation)) > 0),
    recorded_at timestamptz NOT NULL DEFAULT now()
);

CREATE OR REPLACE VIEW price_history AS
SELECT f.chain, f.store_id, f.price_list_date, f.id AS file_id, f.sha256,
       r.row_number, r.sku, r.gtin_raw, r.gtin_normalized, r.title, r.brand, r.quantity, r.unit,
       p.effective_price, p.price_origin
FROM source_file f JOIN source_row r ON r.file_id=f.id
JOIN price_observation p ON (p.file_id,p.row_number)=(r.file_id,r.row_number);

CREATE OR REPLACE VIEW source_quality AS
SELECT f.id AS file_id, f.chain, f.store_id, f.price_list_date, f.sha256,
       count(r.row_number) AS row_count,
       count(r.row_number) FILTER (WHERE r.gtin_normalized IS NOT NULL) AS valid_gtin_rows,
       count(p.row_number) AS priced_rows,
       count(r.row_number) FILTER (WHERE EXISTS
           (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(r.file_id,r.row_number))) AS rows_for_review
FROM source_file f LEFT JOIN source_row r ON r.file_id=f.id
LEFT JOIN price_observation p ON (p.file_id,p.row_number)=(r.file_id,r.row_number)
GROUP BY f.id;

-- Pair identity is version-specific and manually reviewed. No GTIN-only join.
CREATE OR REPLACE VIEW verified_price_comparison AS
SELECT c.id AS review_id, l.price_list_date,
       l.chain AS left_chain, l.store_id AS left_store, l.file_id AS left_file,
       l.sku AS left_sku, l.effective_price AS left_price,
       r.chain AS right_chain, r.store_id AS right_store, r.file_id AS right_file,
       r.sku AS right_sku, r.effective_price AS right_price,
       l.effective_price-r.effective_price AS price_difference
FROM comparison_review c
JOIN price_history l ON (l.file_id,l.row_number)=(c.left_file,c.left_row)
JOIN price_history r ON (r.file_id,r.row_number)=(c.right_file,c.right_row)
WHERE c.decision='verified' AND l.price_list_date=r.price_list_date
  AND l.chain <> r.chain AND l.gtin_normalized = r.gtin_normalized
  AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(l.file_id,l.row_number))
  AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(r.file_id,r.row_number));

-- The caller must select one file version per chain/store/date explicitly.
CREATE OR REPLACE FUNCTION price_changes(selected_file_ids bigint[])
RETURNS TABLE(chain text, store_id text, sku text, previous_date date, observed_date date,
              previous_price numeric, current_price numeric, difference numeric)
LANGUAGE plpgsql STABLE AS $$
BEGIN
    IF selected_file_ids IS NULL OR cardinality(selected_file_ids)=0 OR
       (SELECT count(DISTINCT f.id) FROM source_file f WHERE f.id=ANY(selected_file_ids)) <> cardinality(selected_file_ids) OR
       EXISTS (SELECT 1 FROM source_file f WHERE f.id=ANY(selected_file_ids)
               GROUP BY f.chain,f.store_id,f.price_list_date HAVING count(*) > 1) THEN
        RAISE EXCEPTION 'select existing unique files, at most one version per store and date';
    END IF;
    RETURN QUERY
      WITH cohort AS (
          SELECT h.chain,h.store_id,h.sku,h.price_list_date,h.effective_price,
                 h.gtin_normalized,h.title,h.brand,h.quantity,h.unit,
                 lag(h.price_list_date) OVER w AS prev_date,
                 lag(h.effective_price) OVER w AS prev_price,
                 lag(h.gtin_normalized) OVER w AS prev_gtin,
                 lag(h.title) OVER w AS prev_title,
                 lag(h.brand) OVER w AS prev_brand,
                 lag(h.quantity) OVER w AS prev_quantity,
                 lag(h.unit) OVER w AS prev_unit
          FROM price_history h WHERE h.file_id=ANY(selected_file_ids)
            AND NOT EXISTS (SELECT 1 FROM review_exception e WHERE (e.file_id,e.row_number)=(h.file_id,h.row_number))
          WINDOW w AS (PARTITION BY h.chain,h.store_id,h.sku ORDER BY h.price_list_date)
      )
      SELECT c.chain,c.store_id,c.sku,c.prev_date,c.price_list_date,
             c.prev_price,c.effective_price,c.effective_price-c.prev_price
      FROM cohort c WHERE c.prev_date IS NOT NULL AND c.gtin_normalized IS NOT NULL
        AND c.gtin_normalized=c.prev_gtin AND c.title<>''
        AND (c.title,c.brand,c.quantity,c.unit)=(c.prev_title,c.prev_brand,c.prev_quantity,c.prev_unit);
END $$;

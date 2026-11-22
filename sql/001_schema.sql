-- Phase 2: local historical facts, never infer inventory from list membership.
CREATE TABLE IF NOT EXISTS retailer (
    chain text PRIMARY KEY CHECK (chain IN ('spar', 'kaufland'))
);
CREATE TABLE IF NOT EXISTS store (
    chain text NOT NULL REFERENCES retailer(chain),
    store_id text NOT NULL CHECK (store_id <> ''),
    PRIMARY KEY (chain, store_id)
);
CREATE TABLE IF NOT EXISTS source_product (
    chain text NOT NULL REFERENCES retailer(chain),
    sku text NOT NULL CHECK (sku <> ''),
    PRIMARY KEY (chain, sku)
);
CREATE TABLE IF NOT EXISTS source_file (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    chain text NOT NULL,
    store_id text NOT NULL,
    price_list_date date NOT NULL,
    sha256 text NOT NULL CHECK (sha256 ~ '^[0-9a-f]{64}$'),
    FOREIGN KEY (chain, store_id) REFERENCES store(chain, store_id),
    UNIQUE (chain, store_id, price_list_date, sha256),
    UNIQUE (id, chain)
);
CREATE TABLE IF NOT EXISTS acquisition_run (
    id bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    file_id bigint NOT NULL REFERENCES source_file(id),
    source_url text NOT NULL,
    collected_at_utc timestamptz NOT NULL,
    http_status integer NOT NULL CHECK (http_status BETWEEN 200 AND 299),
    loaded_at_utc timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE IF NOT EXISTS source_row (
    file_id bigint NOT NULL,
    chain text NOT NULL,
    row_number integer NOT NULL CHECK (row_number >= 2),
    sku text,
    gtin_raw text NOT NULL,
    gtin_normalized text CHECK (gtin_normalized IS NULL OR gtin_normalized ~ '^[0-9]{14}$'),
    title text NOT NULL,
    brand text NOT NULL,
    quantity text NOT NULL,
    unit text NOT NULL,
    regular_raw text NOT NULL,
    special_raw text NOT NULL,
    raw_row jsonb NOT NULL,
    ingestion_status text NOT NULL,
    FOREIGN KEY (file_id, chain) REFERENCES source_file(id, chain),
    FOREIGN KEY (chain, sku) REFERENCES source_product(chain, sku),
    PRIMARY KEY (file_id, row_number)
);
CREATE TABLE IF NOT EXISTS price_observation (
    file_id bigint NOT NULL,
    row_number integer NOT NULL,
    regular_price numeric CHECK (regular_price > 0),
    special_price numeric CHECK (special_price > 0),
    effective_price numeric NOT NULL CHECK (effective_price > 0),
    price_origin text NOT NULL CHECK (price_origin IN ('regular', 'special', 'both_equal')),
    PRIMARY KEY (file_id, row_number),
    FOREIGN KEY (file_id, row_number) REFERENCES source_row(file_id, row_number),
    CHECK ((price_origin = 'regular' AND regular_price IS NOT NULL AND regular_price = effective_price AND special_price IS NULL)
        OR (price_origin = 'special' AND special_price IS NOT NULL AND special_price = effective_price AND regular_price IS NULL)
        OR (price_origin = 'both_equal' AND regular_price IS NOT NULL AND special_price IS NOT NULL AND regular_price = effective_price AND special_price = effective_price))
);
CREATE TABLE IF NOT EXISTS review_exception (
    file_id bigint NOT NULL,
    row_number integer NOT NULL,
    reason text NOT NULL,
    PRIMARY KEY (file_id, row_number, reason),
    FOREIGN KEY (file_id, row_number) REFERENCES source_row(file_id, row_number)
);
CREATE INDEX IF NOT EXISTS source_file_store_date_idx ON source_file(chain, store_id, price_list_date);
CREATE INDEX IF NOT EXISTS source_row_product_idx ON source_row(chain, sku);
CREATE INDEX IF NOT EXISTS source_row_gtin_idx ON source_row(gtin_normalized) WHERE gtin_normalized IS NOT NULL;

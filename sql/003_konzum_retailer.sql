-- Expand the retailer constraint on fresh and existing PricePulse schemas.
ALTER TABLE retailer DROP CONSTRAINT IF EXISTS retailer_chain_check;
ALTER TABLE retailer ADD CONSTRAINT retailer_chain_check
    CHECK (chain IN ('spar', 'kaufland', 'konzum'));

CREATE TABLE IF NOT EXISTS token_transfers (
    id BIGSERIAL PRIMARY KEY,
    tx_hash TEXT NOT NULL UNIQUE,
    block_number BIGINT NOT NULL,
    event_index INT,
    from_address TEXT NOT NULL,
    to_address TEXT NOT NULL,
    token_address TEXT NOT NULL,
    amount NUMERIC(36, 18) NOT NULL,
    status TEXT NOT NULL DEFAULT 'processed',
    processed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_token_transfers_block_number ON token_transfers (block_number);
CREATE INDEX IF NOT EXISTS idx_token_transfers_token_address ON token_transfers (token_address);
CREATE INDEX IF NOT EXISTS idx_token_transfers_from_address ON token_transfers (from_address);
CREATE INDEX IF NOT EXISTS idx_token_transfers_to_address ON token_transfers (to_address);
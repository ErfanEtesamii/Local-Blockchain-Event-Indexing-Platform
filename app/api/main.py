from fastapi import FastAPI
from app.api.database import get_connection
from decimal import Decimal

app = FastAPI(title="Blockchain Indexer API")

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/transfers")
def list_transfers():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    id,
                    tx_hash,
                    block_number,
                    event_index,
                    from_address,
                    to_address,
                    token_address,
                    amount::text AS amount,
                    status,
                    processed_at,
                    created_at
                FROM token_transfers
                ORDER BY id DESC
            """)
            rows = cur.fetchall()
    return {"data": rows}
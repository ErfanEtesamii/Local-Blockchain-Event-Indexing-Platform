from app.indexer.blockchain_client import fetch_events
from app.indexer.processor import normalize_transfer
from app.api.database import get_connection

def save_transfer(transfer):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO token_transfers (
                    tx_hash,
                    block_number,
                    event_index,
                    from_address,
                    to_address,
                    token_address,
                    amount,
                    status
                ) VALUES (
                    %(tx_hash)s,
                    %(block_number)s,
                    %(event_index)s,
                    %(from_address)s,
                    %(to_address)s,
                    %(token_address)s,
                    %(amount)s,
                    %(status)s
                )
                ON CONFLICT (tx_hash) DO NOTHING
            """, transfer)
        conn.commit()

def main():
    events = fetch_events()
    for event in events:
        transfer = normalize_transfer(event)
        save_transfer(transfer)
    print(f"Processed {len(events)} events")

if __name__ == "__main__":
    main()
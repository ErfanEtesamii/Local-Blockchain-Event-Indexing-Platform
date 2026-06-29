import logging

from app.api.database import get_connection
from app.indexer.blockchain_client import fetch_events
from app.indexer.processor import (
    InvalidTransferEvent,
    normalize_transfer,
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)


def save_transfer(transfer):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
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
                """,
                transfer,
            )
        conn.commit()


def main():
    logger.info("Indexer started")

    events = fetch_events()
    logger.info("Fetched %s events", len(events))

    processed = 0
    invalid = 0
    failed = 0

    for event in events:
        try:
            transfer = normalize_transfer(event)
            save_transfer(transfer)

            processed += 1
            logger.info("Processed transfer %s", transfer["tx_hash"])

        except InvalidTransferEvent as exc:
            invalid += 1
            logger.warning("Skipping invalid event: %s", exc)

        except Exception:
            failed += 1
            logger.exception("Unexpected error while processing event")

    logger.info("Indexer finished")
    logger.info("Processed events : %s", processed)
    logger.info("Invalid events  : %s", invalid)
    logger.info("Failed events   : %s", failed)


if __name__ == "__main__":
    main()
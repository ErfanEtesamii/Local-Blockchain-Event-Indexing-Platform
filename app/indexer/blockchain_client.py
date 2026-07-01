import logging
import time

logger = logging.getLogger(__name__)


class BlockchainConnectionError(Exception):
    """Raised when the blockchain data source can't be reached."""


def _fetch_raw_events():
    """
    Placeholder for the real blockchain data source call.

    Right now this just returns a fixed mock event so the rest of the
    pipeline (processor -> database -> API) can be built and tested
    locally before wiring up a real chain/provider connection.
    """
    return [
        {
            "tx_hash": "0xindexerhash001",
            "block_number": 123457,
            "event_index": 0,
            "from_address": "0xaaa111",
            "to_address": "0xbbb222",
            "token_address": "0xtoken123",
            "amount": "250.5",
        }
    ]


def fetch_events(max_retries=3, backoff_seconds=2):
    """
    Fetch blockchain events with basic retry handling.

    The mock source below doesn't actually fail on its own, but the
    retry wrapper is here so that swapping _fetch_raw_events() for a
    real RPC/provider call later won't require touching main.py.
    """
    attempt = 0

    while True:
        attempt += 1
        try:
            return _fetch_raw_events()
        except Exception as exc:
            if attempt >= max_retries:
                raise BlockchainConnectionError(
                    f"failed to fetch events after {attempt} attempts: {exc}"
                ) from exc

            wait = backoff_seconds * attempt
            logger.warning(
                "fetch_events attempt %s failed (%s), retrying in %ss",
                attempt, exc, wait,
            )
            time.sleep(wait)

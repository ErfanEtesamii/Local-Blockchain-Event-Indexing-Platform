import logging
import os
import time

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

logger = logging.getLogger(__name__)

RPC_URL = os.getenv("RPC_URL")


class BlockchainConnectionError(Exception):
    """Raised when the blockchain data source can't be reached."""


def get_web3():
    """
    Create and validate a Web3 client.
    """
    if not RPC_URL:
        raise RuntimeError("RPC_URL is not configured")

    web3 = Web3(Web3.HTTPProvider(RPC_URL))

    if not web3.is_connected():
        raise RuntimeError("Unable to connect to Ethereum RPC")

    return web3


def get_latest_block():
    """
    Return the latest block number.
    """
    web3 = get_web3()

    return web3.eth.block_number


def _fetch_raw_events():
    """
    Temporary implementation.

    Confirms the RPC connection is alive and logs the latest block
    number. Real event retrieval (pulling transfer logs from specific
    blocks) will be implemented in the next task.
    """
    latest_block = get_latest_block()

    logger.info("Connected to Ethereum. Latest block: %s", latest_block)

    return []


def fetch_events(max_retries=3, backoff_seconds=2):
    """
    Fetch blockchain events with basic retry handling.

    Wraps the RPC connection/fetch step so a transient network issue
    (timeout, RPC provider hiccup) doesn't crash the whole indexer run.
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

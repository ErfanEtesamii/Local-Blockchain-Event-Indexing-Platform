import logging
import os
import time

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

logger = logging.getLogger(__name__)

RPC_URL = os.getenv("RPC_URL")

# how many transactions to process per run - blocks can have hundreds
# of them, and we want to keep each run quick for now
TX_LIMIT = int(os.getenv("INDEXER_TX_LIMIT", "20"))

# used as the token_address for native ETH transfers, since these
# aren't ERC-20 token transfers and don't have a contract address
NATIVE_TOKEN_ADDRESS = "0x0000000000000000000000000000000000000000"


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
    Read the transactions from the latest block and turn them into
    our internal event format.
    """
    web3 = get_web3()
    block = web3.eth.get_block("latest", full_transactions=True)

    logger.info(
        "Reading block %s, %s transactions found",
        block["number"],
        len(block["transactions"]),
    )

    events = []

    for tx in block["transactions"][:TX_LIMIT]:
        if tx["to"] is None:
            # contract creation transactions have no "to" address, skip them
            continue

        events.append(
            {
                "tx_hash": tx["hash"].hex(),
                "block_number": tx["blockNumber"],
                "event_index": tx["transactionIndex"],
                "from_address": tx["from"],
                "to_address": tx["to"],
                "token_address": NATIVE_TOKEN_ADDRESS,
                "amount": str(tx["value"]),
            }
        )

    return events


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
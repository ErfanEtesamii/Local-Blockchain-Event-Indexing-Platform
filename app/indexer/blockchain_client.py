import os

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()

RPC_URL = os.getenv("RPC_URL")


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


def fetch_events():
    """
    Temporary implementation.

    Event retrieval will be implemented in the next task.
    """

    latest_block = get_latest_block()

    print(f"Connected to Ethereum. Latest block: {latest_block}")

    return []
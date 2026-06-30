import os

from dotenv import load_dotenv
from web3 import Web3

load_dotenv()


RPC_URL = os.getenv("RPC_URL")


def get_web3():
    """
    Create a Web3 client.

    The blockchain connection is initialized here so the rest
    of the application remains independent from the provider.
    """

    if not RPC_URL:
        raise RuntimeError("RPC_URL is not configured")

    return Web3(Web3.HTTPProvider(RPC_URL))


def fetch_events():
    """
    Temporary implementation.

    A Web3 client is initialized successfully, while blockchain
    events are still mocked. Event retrieval will be implemented
    in the next task.
    """

    get_web3()

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
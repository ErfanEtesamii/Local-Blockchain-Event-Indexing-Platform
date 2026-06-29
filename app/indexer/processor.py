class InvalidTransferEvent(Exception):
    """Raised when a blockchain event is missing required fields."""


REQUIRED_FIELDS = [
    "tx_hash",
    "block_number",
    "from_address",
    "to_address",
    "token_address",
    "amount",
]


def validate_transfer(event):
    """
    Validate that all required fields exist before processing.
    """

    for field in REQUIRED_FIELDS:
        if field not in event:
            raise InvalidTransferEvent(f"Missing required field: {field}")

        if event[field] is None:
            raise InvalidTransferEvent(f"Field '{field}' cannot be None")

        if isinstance(event[field], str) and not event[field].strip():
            raise InvalidTransferEvent(f"Field '{field}' cannot be empty")


def normalize_transfer(event):
    validate_transfer(event)

    return {
        "tx_hash": event["tx_hash"],
        "block_number": event["block_number"],
        "event_index": event.get("event_index"),
        "from_address": event["from_address"],
        "to_address": event["to_address"],
        "token_address": event["token_address"],
        "amount": event["amount"],
        "status": "processed",
    }
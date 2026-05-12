def normalize_transfer(event):
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
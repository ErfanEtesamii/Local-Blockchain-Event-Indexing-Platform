from pydantic import BaseModel
from datetime import datetime
from decimal import Decimal
from typing import Optional

class TokenTransfer(BaseModel):
    id: int
    tx_hash: str
    block_number: int
    event_index: Optional[int] = None
    from_address: str
    to_address: str
    token_address: str
    amount: Decimal
    status: str
    processed_at: datetime
    created_at: datetime
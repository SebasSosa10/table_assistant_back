from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class ConversationStatus(StrEnum):
    ACTIVE = "active"
    CLOSED = "closed"


@dataclass
class Conversation:
    id: int | None
    restaurant_id: int
    table_id: int
    user_id: int | None
    session_id: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime

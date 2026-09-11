from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class MessageRole(StrEnum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


@dataclass
class Message:
    id: int | None
    conversation_id: int
    role: MessageRole
    content: str
    metadata: dict | None
    created_at: datetime

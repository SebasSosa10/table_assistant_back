from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from conversation.domain.entities.conversation import Conversation, ConversationStatus
from conversation.domain.entities.message import Message, MessageRole


class ConversationCreateSchema(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={"example": {"restaurant_id": 1, "table_id": 1}},
    )

    restaurant_id: int = Field(gt=0)
    table_id: int = Field(gt=0)
    user_id: int | None = Field(default=None, gt=0)


class MessageCreateSchema(BaseModel):
    content: str = Field(min_length=1, max_length=4000)


class MessageResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    conversation_id: int
    role: MessageRole
    content: str
    metadata: dict | None
    created_at: datetime

    @classmethod
    def from_entity(cls, message: Message) -> "MessageResponseSchema":
        return cls(
            id=message.id,
            conversation_id=message.conversation_id,
            role=message.role,
            content=message.content,
            metadata=message.metadata,
            created_at=message.created_at,
        )


class ConversationResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: int
    table_id: int
    user_id: int | None
    session_id: str
    status: ConversationStatus
    created_at: datetime
    updated_at: datetime
    messages: list[MessageResponseSchema] = []

    @classmethod
    def from_entity(
        cls,
        conversation: Conversation,
        messages: list[Message] | None = None,
    ) -> "ConversationResponseSchema":
        return cls(
            id=conversation.id,
            restaurant_id=conversation.restaurant_id,
            table_id=conversation.table_id,
            user_id=conversation.user_id,
            session_id=conversation.session_id,
            status=conversation.status,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
            messages=[
                MessageResponseSchema.from_entity(message) for message in (messages or [])
            ],
        )


class SendMessageResponseSchema(BaseModel):
    user_message: MessageResponseSchema
    assistant_message: MessageResponseSchema

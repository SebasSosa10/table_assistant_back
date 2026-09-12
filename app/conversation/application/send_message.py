from datetime import datetime, timezone

from conversation.domain.entities.conversation import ConversationStatus
from conversation.domain.entities.message import Message, MessageRole
from conversation.domain.ports.assistant_port import AssistantPort
from conversation.domain.ports.conversation_repository import ConversationRepository
from conversation.domain.ports.message_repository import MessageRepository
from shared.config.settings import settings
from shared.exceptions import ConflictError, NotFoundError


class SendMessage:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
        assistant: AssistantPort,
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository
        self.assistant = assistant

    def execute(self, conversation_id: int, content: str) -> tuple[Message, Message]:
        conversation = self.conversation_repository.get_by_id(conversation_id)
        if conversation is None:
            raise NotFoundError("Conversación no encontrada")
        if conversation.status == ConversationStatus.CLOSED:
            raise ConflictError("No se puede enviar mensajes a una conversación cerrada")

        now = datetime.now(timezone.utc)
        user_message = self.message_repository.create(
            Message(
                id=None,
                conversation_id=conversation_id,
                role=MessageRole.USER,
                content=content.strip(),
                metadata=None,
                created_at=now,
            )
        )

        history = self.message_repository.list_by_conversation(conversation_id)
        assistant_content = self.assistant.complete(
            [{"role": message.role.value, "content": message.content} for message in history]
        )

        assistant_message = self.message_repository.create(
            Message(
                id=None,
                conversation_id=conversation_id,
                role=MessageRole.ASSISTANT,
                content=assistant_content,
                metadata={"model": settings.openrouter_model},
                created_at=datetime.now(timezone.utc),
            )
        )
        return user_message, assistant_message

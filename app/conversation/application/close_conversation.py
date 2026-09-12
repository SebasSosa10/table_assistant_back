from datetime import datetime, timezone

from conversation.domain.entities.conversation import Conversation, ConversationStatus
from conversation.domain.ports.conversation_repository import ConversationRepository
from shared.exceptions import ConflictError, NotFoundError


class CloseConversation:
    def __init__(self, conversation_repository: ConversationRepository):
        self.conversation_repository = conversation_repository

    def execute(self, conversation_id: int) -> Conversation:
        conversation = self.conversation_repository.get_by_id(conversation_id)
        if conversation is None:
            raise NotFoundError("Conversación no encontrada")
        if conversation.status == ConversationStatus.CLOSED:
            raise ConflictError("La conversación ya está cerrada")

        conversation.status = ConversationStatus.CLOSED
        conversation.updated_at = datetime.now(timezone.utc)
        return self.conversation_repository.update(conversation)

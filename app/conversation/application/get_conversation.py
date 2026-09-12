from conversation.domain.entities.conversation import Conversation
from conversation.domain.entities.message import Message
from conversation.domain.ports.conversation_repository import ConversationRepository
from conversation.domain.ports.message_repository import MessageRepository
from shared.exceptions import NotFoundError


class GetConversation:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        message_repository: MessageRepository,
    ):
        self.conversation_repository = conversation_repository
        self.message_repository = message_repository

    def execute(self, conversation_id: int) -> tuple[Conversation, list[Message]]:
        conversation = self.conversation_repository.get_by_id(conversation_id)
        if conversation is None:
            raise NotFoundError("Conversación no encontrada")
        messages = self.message_repository.list_by_conversation(conversation_id)
        return conversation, messages

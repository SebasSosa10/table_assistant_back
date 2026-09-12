from abc import ABC, abstractmethod

from conversation.domain.entities.conversation import Conversation


class ConversationRepository(ABC):
    @abstractmethod
    def create(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, conversation_id: int) -> Conversation | None:
        raise NotImplementedError

    @abstractmethod
    def update(self, conversation: Conversation) -> Conversation:
        raise NotImplementedError

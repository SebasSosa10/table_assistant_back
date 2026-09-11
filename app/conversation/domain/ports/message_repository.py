from abc import ABC, abstractmethod

from conversation.domain.entities.message import Message


class MessageRepository(ABC):
    @abstractmethod
    def create(self, message: Message) -> Message:
        raise NotImplementedError

    @abstractmethod
    def list_by_conversation(self, conversation_id: int) -> list[Message]:
        raise NotImplementedError

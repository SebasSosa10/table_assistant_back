from sqlalchemy import select
from sqlalchemy.orm import Session

from conversation.domain.entities.message import Message, MessageRole
from conversation.domain.ports.message_repository import MessageRepository
from conversation.infrastructure.models.message_model import MessageModel


class MessageRepositoryImpl(MessageRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, message: Message) -> Message:
        model = MessageModel(
            conversation_id=message.conversation_id,
            role=message.role.value,
            content=message.content,
            extra_data=message.metadata,
            created_at=message.created_at,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def list_by_conversation(self, conversation_id: int) -> list[Message]:
        stmt = (
            select(MessageModel)
            .where(MessageModel.conversation_id == conversation_id)
            .order_by(MessageModel.created_at.asc(), MessageModel.id.asc())
        )
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def _to_entity(self, model: MessageModel) -> Message:
        return Message(
            id=model.id,
            conversation_id=model.conversation_id,
            role=MessageRole(model.role),
            content=model.content,
            metadata=model.extra_data,
            created_at=model.created_at,
        )

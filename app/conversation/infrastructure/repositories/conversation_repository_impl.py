from sqlalchemy.orm import Session

from conversation.domain.entities.conversation import Conversation, ConversationStatus
from conversation.domain.ports.conversation_repository import ConversationRepository
from conversation.infrastructure.models.conversation_model import ConversationModel


class ConversationRepositoryImpl(ConversationRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, conversation: Conversation) -> Conversation:
        model = ConversationModel(
            restaurant_id=conversation.restaurant_id,
            table_id=conversation.table_id,
            user_id=conversation.user_id,
            session_id=conversation.session_id,
            status=conversation.status.value,
            created_at=conversation.created_at,
            updated_at=conversation.updated_at,
        )
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, conversation_id: int) -> Conversation | None:
        model = self.session.get(ConversationModel, conversation_id)
        return self._to_entity(model) if model else None

    def update(self, conversation: Conversation) -> Conversation:
        model = self.session.get(ConversationModel, conversation.id)
        if model is None:
            raise ValueError("Conversación no encontrada")

        model.status = conversation.status.value
        model.updated_at = conversation.updated_at
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def _to_entity(self, model: ConversationModel) -> Conversation:
        return Conversation(
            id=model.id,
            restaurant_id=model.restaurant_id,
            table_id=model.table_id,
            user_id=model.user_id,
            session_id=str(model.session_id),
            status=ConversationStatus(model.status),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

from datetime import datetime, timezone
from uuid import uuid4

from conversation.domain.entities.conversation import Conversation, ConversationStatus
from conversation.domain.ports.conversation_repository import ConversationRepository
from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from shared.exceptions import NotFoundError
from table.domain.ports.table_repository import TableRepository
from user.domain.ports.user_repository import UserRepository


class CreateConversation:
    def __init__(
        self,
        conversation_repository: ConversationRepository,
        restaurant_repository: RestaurantRepository,
        table_repository: TableRepository,
        user_repository: UserRepository,
    ):
        self.conversation_repository = conversation_repository
        self.restaurant_repository = restaurant_repository
        self.table_repository = table_repository
        self.user_repository = user_repository

    def execute(
        self,
        restaurant_id: int,
        table_id: int,
        user_id: int | None = None,
    ) -> Conversation:
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError("Restaurante no encontrado")

        table = self.table_repository.get_by_id(table_id)
        if table is None:
            raise NotFoundError("Mesa no encontrada")
        if table.restaurant_id != restaurant_id:
            raise NotFoundError("La mesa no pertenece a ese restaurante")

        user_id = self._optional_id(user_id)
        if user_id is not None:
            user = self.user_repository.get_by_id(user_id)
            if user is None:
                raise NotFoundError("Usuario no encontrado")

        now = datetime.now(timezone.utc)
        conversation = Conversation(
            id=None,
            restaurant_id=restaurant_id,
            table_id=table_id,
            user_id=user_id,
            session_id=str(uuid4()),
            status=ConversationStatus.ACTIVE,
            created_at=now,
            updated_at=now,
        )
        return self.conversation_repository.create(conversation)

    def _optional_id(self, value: int | None) -> int | None:
        if value is None or value <= 0:
            return None
        return value

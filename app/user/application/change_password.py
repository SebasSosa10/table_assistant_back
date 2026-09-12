from datetime import datetime, timezone

from shared.exceptions import NotFoundError
from shared.utils.password import hash_password
from user.domain.entities.user import User
from user.domain.ports.user_repository import UserRepository


class ChangePassword:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int, password: str) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")

        user.password_hash = hash_password(password)
        user.updated_at = datetime.now(timezone.utc)
        return self.repository.update(user)

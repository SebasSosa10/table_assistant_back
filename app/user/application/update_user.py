from datetime import datetime, timezone

from shared.exceptions import ConflictError, NotFoundError
from shared.utils.password import hash_password
from user.domain.entities.user import User
from user.domain.ports.user_repository import UserRepository


class UpdateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int, data: dict) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")

        if "email" in data and data["email"] is not None:
            normalized_email = data["email"].lower().strip()
            existing = self.repository.get_by_email(normalized_email)
            if existing is not None and existing.id != user.id:
                raise ConflictError("Ya existe un usuario con ese correo")
            user.email = normalized_email

        if "name" in data and data["name"] is not None:
            user.name = data["name"]
        if "password" in data and data["password"] is not None:
            user.password_hash = hash_password(data["password"])
        if "role" in data and data["role"] is not None:
            user.role = data["role"]
        if "phone" in data:
            user.phone = data["phone"]
        if "restaurant_id" in data:
            user.restaurant_id = data["restaurant_id"]
        if "is_active" in data and data["is_active"] is not None:
            user.is_active = data["is_active"]

        user.updated_at = datetime.now(timezone.utc)
        return self.repository.update(user)

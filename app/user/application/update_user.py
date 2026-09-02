from datetime import datetime, timezone

from shared.exceptions import ConflictError, NotFoundError
from shared.utils.password import hash_password
from user.domain.entities.user import User, UserRole
from user.domain.ports.user_repository import UserRepository


class UpdateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(
        self,
        user_id: int,
        name: str | None = None,
        email: str | None = None,
        password: str | None = None,
        role: UserRole | None = None,
        phone: str | None = None,
        restaurant_id: int | None = None,
        is_active: bool | None = None,
    ) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")

        if email is not None:
            normalized_email = email.lower().strip()
            existing = self.repository.get_by_email(normalized_email)
            if existing is not None and existing.id != user.id:
                raise ConflictError("Ya existe un usuario con ese correo")
            user.email = normalized_email

        if name is not None:
            user.name = name
        if password is not None:
            user.password_hash = hash_password(password)
        if role is not None:
            user.role = role
        if phone is not None:
            user.phone = phone
        if restaurant_id is not None:
            user.restaurant_id = restaurant_id
        if is_active is not None:
            user.is_active = is_active

        user.updated_at = datetime.now(timezone.utc)
        return self.repository.update(user)

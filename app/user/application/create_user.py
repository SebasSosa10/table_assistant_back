from datetime import datetime, timezone

from shared.exceptions import ConflictError
from shared.utils.password import hash_password
from user.domain.entities.user import User, UserRole
from user.domain.ports.user_repository import UserRepository


class CreateUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(
        self,
        name: str,
        email: str,
        password: str,
        role: UserRole,
        phone: str | None = None,
        restaurant_id: int | None = None,
    ) -> User:
        if self.repository.get_by_email(email):
            raise ConflictError("Ya existe un usuario con ese correo")

        now = datetime.now(timezone.utc)
        user = User(
            id=None,
            name=name,
            email=email.lower().strip(),
            password_hash=hash_password(password),
            role=role,
            phone=phone,
            restaurant_id=restaurant_id,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        return self.repository.create(user)

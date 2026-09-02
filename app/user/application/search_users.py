from user.domain.entities.user import User, UserRole
from user.domain.ports.user_repository import UserRepository


class SearchUsers:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(
        self,
        name: str | None = None,
        email: str | None = None,
        role: UserRole | None = None,
        restaurant_id: int | None = None,
        is_active: bool | None = None,
    ) -> list[User]:
        return self.repository.search(
            name=name,
            email=email,
            role=role,
            restaurant_id=restaurant_id,
            is_active=is_active,
        )

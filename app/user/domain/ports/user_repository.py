from abc import ABC, abstractmethod

from user.domain.entities.user import User, UserRole


class UserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, user_id: int) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> User | None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        name: str | None = None,
        email: str | None = None,
        role: UserRole | None = None,
        restaurant_id: int | None = None,
        is_active: bool | None = None,
    ) -> list[User]:
        raise NotImplementedError

    @abstractmethod
    def update(self, user: User) -> User:
        raise NotImplementedError

    @abstractmethod
    def delete(self, user_id: int) -> None:
        raise NotImplementedError

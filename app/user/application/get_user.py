from shared.exceptions import NotFoundError
from user.domain.entities.user import User
from user.domain.ports.user_repository import UserRepository


class GetUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int) -> User:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")
        return user

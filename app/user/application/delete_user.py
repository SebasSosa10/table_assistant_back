from shared.exceptions import NotFoundError
from user.domain.ports.user_repository import UserRepository


class DeleteUser:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user_id: int) -> None:
        user = self.repository.get_by_id(user_id)
        if user is None:
            raise NotFoundError("Usuario no encontrado")
        self.repository.delete(user_id)

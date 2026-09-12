from user.domain.entities.user import User
from user.domain.ports.user_repository import UserRepository


class GetUsers:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self) -> list[User]:
        return self.repository.get_all()

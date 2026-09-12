from sqlalchemy import select
from sqlalchemy.orm import Session

from user.domain.entities.user import User, UserRole
from user.domain.ports.user_repository import UserRepository
from user.infrastructure.models.user_model import UserModel


class UserRepositoryImpl(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, user: User) -> User:
        model = self._to_model(user)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, user_id: int) -> User | None:
        model = self.session.get(UserModel, user_id)
        return self._to_entity(model) if model else None

    def get_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).where(UserModel.email == email.lower().strip())
        model = self.session.scalar(stmt)
        return self._to_entity(model) if model else None

    def get_all(self) -> list[User]:
        stmt = select(UserModel).order_by(UserModel.created_at.desc())
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def search(
        self,
        name: str | None = None,
        email: str | None = None,
        role: UserRole | None = None,
        restaurant_id: int | None = None,
        is_active: bool | None = None,
    ) -> list[User]:
        stmt = select(UserModel)

        if name:
            stmt = stmt.where(UserModel.name.ilike(f"%{name}%"))
        if email:
            stmt = stmt.where(UserModel.email.ilike(f"%{email}%"))
        if role:
            stmt = stmt.where(UserModel.role == role.value)
        if restaurant_id:
            stmt = stmt.where(UserModel.restaurant_id == restaurant_id)
        if is_active is not None:
            stmt = stmt.where(UserModel.is_active == is_active)

        stmt = stmt.order_by(UserModel.created_at.desc())
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def update(self, user: User) -> User:
        model = self.session.get(UserModel, user.id)
        if model is None:
            raise ValueError("Usuario no encontrado")

        model.name = user.name
        model.email = user.email
        model.password_hash = user.password_hash
        model.role = user.role.value
        model.phone = user.phone
        model.restaurant_id = user.restaurant_id
        model.is_active = user.is_active
        model.updated_at = user.updated_at

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, user_id: int) -> None:
        model = self.session.get(UserModel, user_id)
        if model is None:
            return
        self.session.delete(model)
        self.session.commit()

    def _to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password_hash=model.password_hash,
            role=self._parse_role(model.role),
            phone=model.phone,
            restaurant_id=model.restaurant_id,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _parse_role(self, value: str) -> UserRole:
        aliases = {
            "admin": UserRole.ADMIN,
            "manager": UserRole.ADMINISTRATOR,
            "waiter": UserRole.WAITER,
        }
        try:
            return UserRole(value)
        except ValueError:
            role = aliases.get((value or "").lower())
            if role is None:
                raise
            return role

    def _to_model(self, user: User) -> UserModel:
        return UserModel(
            name=user.name,
            email=user.email,
            password_hash=user.password_hash,
            role=user.role.value,
            phone=user.phone,
            restaurant_id=user.restaurant_id,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

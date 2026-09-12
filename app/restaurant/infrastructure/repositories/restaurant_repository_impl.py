from sqlalchemy import select
from sqlalchemy.orm import Session

from restaurant.domain.entities.restaurant import Restaurant
from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from restaurant.infrastructure.models.restaurant_model import RestaurantModel


class RestaurantRepositoryImpl(RestaurantRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, restaurant: Restaurant) -> Restaurant:
        model = self._to_model(restaurant)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        model = self.session.get(RestaurantModel, restaurant_id)
        return self._to_entity(model) if model else None

    def get_all(self) -> list[Restaurant]:
        stmt = select(RestaurantModel).order_by(RestaurantModel.created_at.desc())
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def search(
        self,
        name: str | None = None,
        is_active: bool | None = None,
    ) -> list[Restaurant]:
        stmt = select(RestaurantModel)

        if name:
            stmt = stmt.where(RestaurantModel.name.ilike(f"%{name}%"))
        if is_active is not None:
            stmt = stmt.where(RestaurantModel.is_active == is_active)

        stmt = stmt.order_by(RestaurantModel.created_at.desc())
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def update(self, restaurant: Restaurant) -> Restaurant:
        model = self.session.get(RestaurantModel, restaurant.id)
        if model is None:
            raise ValueError("Restaurante no encontrado")

        model.name = restaurant.name
        model.description = restaurant.description
        model.is_active = restaurant.is_active
        model.updated_at = restaurant.updated_at

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, restaurant_id: int) -> None:
        model = self.session.get(RestaurantModel, restaurant_id)
        if model is None:
            return
        self.session.delete(model)
        self.session.commit()

    def _to_entity(self, model: RestaurantModel) -> Restaurant:
        return Restaurant(
            id=model.id,
            name=model.name,
            description=model.description,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, restaurant: Restaurant) -> RestaurantModel:
        return RestaurantModel(
            name=restaurant.name,
            description=restaurant.description,
            is_active=restaurant.is_active,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at,
        )

from datetime import datetime, timezone

from restaurant.domain.entities.restaurant import Restaurant
from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from shared.exceptions import NotFoundError


class UpdateRestaurant:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def execute(self, restaurant_id: int, data: dict) -> Restaurant:
        restaurant = self.repository.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError("Restaurante no encontrado")

        if "name" in data and data["name"] is not None:
            restaurant.name = data["name"].strip()
        if "description" in data:
            restaurant.description = data["description"]
        if "is_active" in data and data["is_active"] is not None:
            restaurant.is_active = data["is_active"]

        restaurant.updated_at = datetime.now(timezone.utc)
        return self.repository.update(restaurant)

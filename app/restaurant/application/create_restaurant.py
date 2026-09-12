from datetime import datetime, timezone

from restaurant.domain.entities.restaurant import Restaurant
from restaurant.domain.ports.restaurant_repository import RestaurantRepository


class CreateRestaurant:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def execute(
        self,
        name: str,
        description: str | None = None,
    ) -> Restaurant:
        now = datetime.now(timezone.utc)
        restaurant = Restaurant(
            id=None,
            name=name.strip(),
            description=description,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        return self.repository.create(restaurant)

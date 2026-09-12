from restaurant.domain.entities.restaurant import Restaurant
from restaurant.domain.ports.restaurant_repository import RestaurantRepository


class SearchRestaurants:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def execute(
        self,
        name: str | None = None,
        is_active: bool | None = None,
    ) -> list[Restaurant]:
        return self.repository.search(
            name=name,
            is_active=is_active,
        )

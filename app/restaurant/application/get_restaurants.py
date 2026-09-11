from restaurant.domain.entities.restaurant import Restaurant
from restaurant.domain.ports.restaurant_repository import RestaurantRepository


class GetRestaurants:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def execute(self) -> list[Restaurant]:
        return self.repository.get_all()

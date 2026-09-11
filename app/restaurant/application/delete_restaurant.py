from shared.exceptions import NotFoundError
from restaurant.domain.ports.restaurant_repository import RestaurantRepository


class DeleteRestaurant:
    def __init__(self, repository: RestaurantRepository):
        self.repository = repository

    def execute(self, restaurant_id: int) -> None:
        restaurant = self.repository.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError("Restaurante no encontrado")
        self.repository.delete(restaurant_id)

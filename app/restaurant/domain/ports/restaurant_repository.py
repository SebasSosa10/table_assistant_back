from abc import ABC, abstractmethod

from restaurant.domain.entities.restaurant import Restaurant


class RestaurantRepository(ABC):
    @abstractmethod
    def create(self, restaurant: Restaurant) -> Restaurant:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, restaurant_id: int) -> Restaurant | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[Restaurant]:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        name: str | None = None,
        is_active: bool | None = None,
    ) -> list[Restaurant]:
        raise NotImplementedError

    @abstractmethod
    def update(self, restaurant: Restaurant) -> Restaurant:
        raise NotImplementedError

    @abstractmethod
    def delete(self, restaurant_id: int) -> None:
        raise NotImplementedError

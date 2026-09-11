from abc import ABC, abstractmethod

from table.domain.entities.restaurant_table import RestaurantTable


class TableRepository(ABC):
    @abstractmethod
    def create(self, table: RestaurantTable) -> RestaurantTable:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, table_id: int) -> RestaurantTable | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_restaurant_and_number(
        self,
        restaurant_id: int,
        number: str,
    ) -> RestaurantTable | None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> list[RestaurantTable]:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        restaurant_id: int | None = None,
        number: str | None = None,
        is_active: bool | None = None,
    ) -> list[RestaurantTable]:
        raise NotImplementedError

    @abstractmethod
    def update(self, table: RestaurantTable) -> RestaurantTable:
        raise NotImplementedError

    @abstractmethod
    def delete(self, table_id: int) -> None:
        raise NotImplementedError

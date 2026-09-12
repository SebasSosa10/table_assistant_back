from table.domain.entities.restaurant_table import RestaurantTable
from table.domain.ports.table_repository import TableRepository


class SearchTables:
    def __init__(self, repository: TableRepository):
        self.repository = repository

    def execute(
        self,
        restaurant_id: int | None = None,
        number: str | None = None,
        is_active: bool | None = None,
    ) -> list[RestaurantTable]:
        return self.repository.search(
            restaurant_id=restaurant_id,
            number=number,
            is_active=is_active,
        )

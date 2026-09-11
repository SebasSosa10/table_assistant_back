from table.domain.entities.restaurant_table import RestaurantTable
from table.domain.ports.table_repository import TableRepository


class GetTables:
    def __init__(self, repository: TableRepository):
        self.repository = repository

    def execute(self) -> list[RestaurantTable]:
        return self.repository.get_all()

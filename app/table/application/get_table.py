from shared.exceptions import NotFoundError
from table.domain.entities.restaurant_table import RestaurantTable
from table.domain.ports.table_repository import TableRepository


class GetTable:
    def __init__(self, repository: TableRepository):
        self.repository = repository

    def execute(self, table_id: int) -> RestaurantTable:
        table = self.repository.get_by_id(table_id)
        if table is None:
            raise NotFoundError("Mesa no encontrada")
        return table

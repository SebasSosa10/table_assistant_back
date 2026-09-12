from shared.exceptions import NotFoundError
from table.domain.ports.table_repository import TableRepository


class DeleteTable:
    def __init__(self, repository: TableRepository):
        self.repository = repository

    def execute(self, table_id: int) -> None:
        table = self.repository.get_by_id(table_id)
        if table is None:
            raise NotFoundError("Mesa no encontrada")
        self.repository.delete(table_id)

from datetime import datetime, timezone

from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from shared.exceptions import ConflictError, NotFoundError
from table.domain.entities.restaurant_table import RestaurantTable
from table.domain.ports.table_repository import TableRepository


class UpdateTable:
    def __init__(
        self,
        table_repository: TableRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.table_repository = table_repository
        self.restaurant_repository = restaurant_repository

    def execute(self, table_id: int, data: dict) -> RestaurantTable:
        table = self.table_repository.get_by_id(table_id)
        if table is None:
            raise NotFoundError("Mesa no encontrada")

        if "restaurant_id" in data and data["restaurant_id"] is not None:
            restaurant = self.restaurant_repository.get_by_id(data["restaurant_id"])
            if restaurant is None:
                raise NotFoundError("Restaurante no encontrado")
            table.restaurant_id = data["restaurant_id"]

        if "number" in data and data["number"] is not None:
            table.number = data["number"].strip()

        if "number" in data or "restaurant_id" in data:
            existing = self.table_repository.get_by_restaurant_and_number(
                table.restaurant_id,
                table.number,
            )
            if existing is not None and existing.id != table.id:
                raise ConflictError("Ya existe una mesa con ese número en el restaurante")

        if "label" in data:
            label = data["label"]
            table.label = label.strip() if label else None
        if "is_active" in data and data["is_active"] is not None:
            table.is_active = data["is_active"]

        table.updated_at = datetime.now(timezone.utc)
        return self.table_repository.update(table)

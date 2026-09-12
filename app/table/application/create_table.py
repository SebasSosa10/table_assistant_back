from datetime import datetime, timezone

from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from shared.exceptions import ConflictError, NotFoundError
from table.domain.entities.restaurant_table import RestaurantTable
from table.domain.ports.table_repository import TableRepository


class CreateTable:
    def __init__(
        self,
        table_repository: TableRepository,
        restaurant_repository: RestaurantRepository,
    ):
        self.table_repository = table_repository
        self.restaurant_repository = restaurant_repository

    def execute(
        self,
        restaurant_id: int,
        number: str,
        label: str | None = None,
    ) -> RestaurantTable:
        restaurant = self.restaurant_repository.get_by_id(restaurant_id)
        if restaurant is None:
            raise NotFoundError("Restaurante no encontrado")

        normalized_number = number.strip()
        existing = self.table_repository.get_by_restaurant_and_number(
            restaurant_id,
            normalized_number,
        )
        if existing is not None:
            raise ConflictError("Ya existe una mesa con ese número en el restaurante")

        now = datetime.now(timezone.utc)
        table = RestaurantTable(
            id=None,
            restaurant_id=restaurant_id,
            number=normalized_number,
            label=label.strip() if label else None,
            is_active=True,
            created_at=now,
            updated_at=now,
        )
        return self.table_repository.create(table)

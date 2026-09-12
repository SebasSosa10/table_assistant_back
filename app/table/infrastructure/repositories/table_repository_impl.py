from sqlalchemy import select
from sqlalchemy.orm import Session

from table.domain.entities.restaurant_table import RestaurantTable
from table.domain.ports.table_repository import TableRepository
from table.infrastructure.models.restaurant_table_model import RestaurantTableModel


class TableRepositoryImpl(TableRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, table: RestaurantTable) -> RestaurantTable:
        model = self._to_model(table)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def get_by_id(self, table_id: int) -> RestaurantTable | None:
        model = self.session.get(RestaurantTableModel, table_id)
        return self._to_entity(model) if model else None

    def get_by_restaurant_and_number(
        self,
        restaurant_id: int,
        number: str,
    ) -> RestaurantTable | None:
        stmt = select(RestaurantTableModel).where(
            RestaurantTableModel.restaurant_id == restaurant_id,
            RestaurantTableModel.number == number.strip(),
        )
        model = self.session.scalar(stmt)
        return self._to_entity(model) if model else None

    def get_all(self) -> list[RestaurantTable]:
        stmt = select(RestaurantTableModel).order_by(
            RestaurantTableModel.restaurant_id.asc(),
            RestaurantTableModel.number.asc(),
        )
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def search(
        self,
        restaurant_id: int | None = None,
        number: str | None = None,
        is_active: bool | None = None,
    ) -> list[RestaurantTable]:
        stmt = select(RestaurantTableModel)

        if restaurant_id:
            stmt = stmt.where(RestaurantTableModel.restaurant_id == restaurant_id)
        if number:
            stmt = stmt.where(RestaurantTableModel.number.ilike(f"%{number}%"))
        if is_active is not None:
            stmt = stmt.where(RestaurantTableModel.is_active == is_active)

        stmt = stmt.order_by(
            RestaurantTableModel.restaurant_id.asc(),
            RestaurantTableModel.number.asc(),
        )
        models = self.session.scalars(stmt).all()
        return [self._to_entity(model) for model in models]

    def update(self, table: RestaurantTable) -> RestaurantTable:
        model = self.session.get(RestaurantTableModel, table.id)
        if model is None:
            raise ValueError("Mesa no encontrada")

        model.restaurant_id = table.restaurant_id
        model.number = table.number
        model.label = table.label
        model.is_active = table.is_active
        model.updated_at = table.updated_at

        self.session.commit()
        self.session.refresh(model)
        return self._to_entity(model)

    def delete(self, table_id: int) -> None:
        model = self.session.get(RestaurantTableModel, table_id)
        if model is None:
            return
        self.session.delete(model)
        self.session.commit()

    def _to_entity(self, model: RestaurantTableModel) -> RestaurantTable:
        return RestaurantTable(
            id=model.id,
            restaurant_id=model.restaurant_id,
            number=model.number,
            label=model.label,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, table: RestaurantTable) -> RestaurantTableModel:
        return RestaurantTableModel(
            restaurant_id=table.restaurant_id,
            number=table.number,
            label=table.label,
            is_active=table.is_active,
            created_at=table.created_at,
            updated_at=table.updated_at,
        )

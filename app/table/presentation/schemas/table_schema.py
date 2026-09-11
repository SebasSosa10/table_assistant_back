from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from table.domain.entities.restaurant_table import RestaurantTable


class TableCreateSchema(BaseModel):
    restaurant_id: int
    number: str = Field(min_length=1, max_length=30)
    label: str | None = Field(default=None, max_length=100)


class TableUpdateSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"label": "Terraza"}},
    )

    restaurant_id: int | None = None
    number: str | None = Field(default=None, min_length=1, max_length=30)
    label: str | None = Field(default=None, max_length=100)
    is_active: bool | None = None


class TableResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    restaurant_id: int
    number: str
    label: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, table: RestaurantTable) -> "TableResponseSchema":
        return cls(
            id=table.id,
            restaurant_id=table.restaurant_id,
            number=table.number,
            label=table.label,
            is_active=table.is_active,
            created_at=table.created_at,
            updated_at=table.updated_at,
        )

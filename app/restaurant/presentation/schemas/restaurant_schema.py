from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from restaurant.domain.entities.restaurant import Restaurant


class RestaurantCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    description: str | None = None


class RestaurantUpdateSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"name": "La Mesa"}},
    )

    name: str | None = Field(default=None, min_length=1, max_length=150)
    description: str | None = None
    is_active: bool | None = None


class RestaurantResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, restaurant: Restaurant) -> "RestaurantResponseSchema":
        return cls(
            id=restaurant.id,
            name=restaurant.name,
            description=restaurant.description,
            is_active=restaurant.is_active,
            created_at=restaurant.created_at,
            updated_at=restaurant.updated_at,
        )

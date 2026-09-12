from dataclasses import dataclass
from datetime import datetime


@dataclass
class RestaurantTable:
    id: int | None
    restaurant_id: int
    number: str
    label: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

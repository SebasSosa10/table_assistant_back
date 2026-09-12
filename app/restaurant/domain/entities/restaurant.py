from dataclasses import dataclass
from datetime import datetime


@dataclass
class Restaurant:
    id: int | None
    name: str
    description: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

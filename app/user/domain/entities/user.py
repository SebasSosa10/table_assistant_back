from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum


class UserRole(StrEnum):
    ADMIN = "Admin"
    OWNER = "Dueño"
    ADMINISTRATOR = "Administrador"
    WAITER = "Mesero"
    CUSTOMER = "Cliente"


@dataclass
class User:
    id: int | None
    name: str
    email: str
    password_hash: str
    role: UserRole
    phone: str | None
    restaurant_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

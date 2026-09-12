from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from user.domain.entities.user import User, UserRole


class UserCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: UserRole = UserRole.WAITER
    phone: str | None = Field(default=None, max_length=30)
    restaurant_id: int | None = None


class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserChangePasswordSchema(BaseModel):
    password: str = Field(min_length=8, max_length=128)


class UserUpdateSchema(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        json_schema_extra={"example": {"name": "Joan"}},
    )

    name: str | None = Field(default=None, min_length=1, max_length=150)
    email: EmailStr | None = None
    password: str | None = Field(default=None, min_length=8, max_length=128)
    role: UserRole | None = None
    phone: str | None = Field(default=None, max_length=30)
    restaurant_id: int | None = None
    is_active: bool | None = None


class UserResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    email: EmailStr
    role: UserRole
    phone: str | None
    restaurant_id: int | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, user: User) -> "UserResponseSchema":
        return cls(
            id=user.id,
            name=user.name,
            email=user.email,
            role=user.role,
            phone=user.phone,
            restaurant_id=user.restaurant_id,
            is_active=user.is_active,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )


class LoginResponseSchema(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponseSchema

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from shared.exceptions import ConflictError, NotFoundError
from user.application.create_user import CreateUser
from user.application.delete_user import DeleteUser
from user.application.get_user import GetUser
from user.application.search_users import SearchUsers
from user.application.update_user import UpdateUser
from user.domain.entities.user import UserRole
from user.domain.ports.user_repository import UserRepository
from user.infrastructure.repositories.user_repository_impl import UserRepositoryImpl
from user.presentation.schemas.user_schema import (
    UserCreateSchema,
    UserResponseSchema,
    UserUpdateSchema,
)

router = APIRouter(prefix="/users", tags=["users"])


def get_user_repository(session: Session = Depends(get_db)) -> UserRepository:
    return UserRepositoryImpl(session)


@router.post("", response_model=UserResponseSchema, status_code=status.HTTP_201_CREATED)
def create_user(
    payload: UserCreateSchema,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponseSchema:
    try:
        user = CreateUser(repository).execute(
            name=payload.name,
            email=payload.email,
            password=payload.password,
            role=payload.role,
            phone=payload.phone,
            restaurant_id=payload.restaurant_id,
        )
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    return UserResponseSchema.from_entity(user)


@router.get("", response_model=list[UserResponseSchema])
def search_users(
    name: str | None = Query(default=None),
    email: str | None = Query(default=None),
    role: UserRole | None = Query(default=None),
    restaurant_id: int | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    repository: UserRepository = Depends(get_user_repository),
) -> list[UserResponseSchema]:
    users = SearchUsers(repository).execute(
        name=name,
        email=email,
        role=role,
        restaurant_id=restaurant_id,
        is_active=is_active,
    )
    return [UserResponseSchema.from_entity(user) for user in users]


@router.get("/{user_id}", response_model=UserResponseSchema)
def get_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponseSchema:
    try:
        user = GetUser(repository).execute(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return UserResponseSchema.from_entity(user)


@router.put("/{user_id}", response_model=UserResponseSchema)
def update_user(
    user_id: int,
    payload: UserUpdateSchema,
    repository: UserRepository = Depends(get_user_repository),
) -> UserResponseSchema:
    try:
        user = UpdateUser(repository).execute(
            user_id=user_id,
            name=payload.name,
            email=payload.email,
            password=payload.password,
            role=payload.role,
            phone=payload.phone,
            restaurant_id=payload.restaurant_id,
            is_active=payload.is_active,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    return UserResponseSchema.from_entity(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    user_id: int,
    repository: UserRepository = Depends(get_user_repository),
) -> None:
    try:
        DeleteUser(repository).execute(user_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc

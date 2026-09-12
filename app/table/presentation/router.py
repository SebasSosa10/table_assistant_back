from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from restaurant.infrastructure.repositories.restaurant_repository_impl import (
    RestaurantRepositoryImpl,
)
from shared.exceptions import ConflictError, NotFoundError
from table.application.create_table import CreateTable
from table.application.delete_table import DeleteTable
from table.application.get_table import GetTable
from table.application.get_tables import GetTables
from table.application.search_tables import SearchTables
from table.application.update_table import UpdateTable
from table.domain.ports.table_repository import TableRepository
from table.infrastructure.repositories.table_repository_impl import TableRepositoryImpl
from table.presentation.schemas.table_schema import (
    TableCreateSchema,
    TableResponseSchema,
    TableUpdateSchema,
)

router = APIRouter(prefix="/tables", tags=["tables"])


def get_table_repository(session: Session = Depends(get_db)) -> TableRepository:
    return TableRepositoryImpl(session)


def get_restaurant_repository(session: Session = Depends(get_db)) -> RestaurantRepository:
    return RestaurantRepositoryImpl(session)


@router.post("", response_model=TableResponseSchema, status_code=status.HTTP_201_CREATED)
def create_table(
    payload: TableCreateSchema,
    table_repository: TableRepository = Depends(get_table_repository),
    restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> TableResponseSchema:
    try:
        table = CreateTable(table_repository, restaurant_repository).execute(
            restaurant_id=payload.restaurant_id,
            number=payload.number,
            label=payload.label,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    return TableResponseSchema.from_entity(table)


@router.get("", response_model=list[TableResponseSchema])
def get_tables(
    table_repository: TableRepository = Depends(get_table_repository),
) -> list[TableResponseSchema]:
    tables = GetTables(table_repository).execute()
    return [TableResponseSchema.from_entity(table) for table in tables]


@router.get("/search", response_model=list[TableResponseSchema])
def search_tables(
    restaurant_id: int | None = Query(default=None),
    number: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    table_repository: TableRepository = Depends(get_table_repository),
) -> list[TableResponseSchema]:
    tables = SearchTables(table_repository).execute(
        restaurant_id=restaurant_id,
        number=number,
        is_active=is_active,
    )
    return [TableResponseSchema.from_entity(table) for table in tables]


@router.get("/{table_id}", response_model=TableResponseSchema)
def get_table(
    table_id: int,
    table_repository: TableRepository = Depends(get_table_repository),
) -> TableResponseSchema:
    try:
        table = GetTable(table_repository).execute(table_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return TableResponseSchema.from_entity(table)


@router.patch("/{table_id}", response_model=TableResponseSchema)
def update_table(
    table_id: int,
    payload: TableUpdateSchema,
    table_repository: TableRepository = Depends(get_table_repository),
    restaurant_repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> TableResponseSchema:
    data = payload.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )
    try:
        table = UpdateTable(table_repository, restaurant_repository).execute(
            table_id=table_id,
            data=data,
        )
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    except ConflictError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=exc.message) from exc
    return TableResponseSchema.from_entity(table)


@router.delete("/{table_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_table(
    table_id: int,
    table_repository: TableRepository = Depends(get_table_repository),
) -> None:
    try:
        DeleteTable(table_repository).execute(table_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from db.session import get_db
from restaurant.application.create_restaurant import CreateRestaurant
from restaurant.application.delete_restaurant import DeleteRestaurant
from restaurant.application.get_restaurant import GetRestaurant
from restaurant.application.get_restaurants import GetRestaurants
from restaurant.application.search_restaurants import SearchRestaurants
from restaurant.application.update_restaurant import UpdateRestaurant
from restaurant.domain.ports.restaurant_repository import RestaurantRepository
from restaurant.infrastructure.repositories.restaurant_repository_impl import (
    RestaurantRepositoryImpl,
)
from restaurant.presentation.schemas.restaurant_schema import (
    RestaurantCreateSchema,
    RestaurantResponseSchema,
    RestaurantUpdateSchema,
)
from shared.exceptions import NotFoundError

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


def get_restaurant_repository(session: Session = Depends(get_db)) -> RestaurantRepository:
    return RestaurantRepositoryImpl(session)


@router.post("", response_model=RestaurantResponseSchema, status_code=status.HTTP_201_CREATED)
def create_restaurant(
    payload: RestaurantCreateSchema,
    repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> RestaurantResponseSchema:
    restaurant = CreateRestaurant(repository).execute(
        name=payload.name,
        description=payload.description,
    )
    return RestaurantResponseSchema.from_entity(restaurant)


@router.get("", response_model=list[RestaurantResponseSchema])
def get_restaurants(
    repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> list[RestaurantResponseSchema]:
    restaurants = GetRestaurants(repository).execute()
    return [RestaurantResponseSchema.from_entity(restaurant) for restaurant in restaurants]


@router.get("/search", response_model=list[RestaurantResponseSchema])
def search_restaurants(
    name: str | None = Query(default=None),
    is_active: bool | None = Query(default=None),
    repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> list[RestaurantResponseSchema]:
    restaurants = SearchRestaurants(repository).execute(
        name=name,
        is_active=is_active,
    )
    return [RestaurantResponseSchema.from_entity(restaurant) for restaurant in restaurants]


@router.get("/{restaurant_id}", response_model=RestaurantResponseSchema)
def get_restaurant(
    restaurant_id: int,
    repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> RestaurantResponseSchema:
    try:
        restaurant = GetRestaurant(repository).execute(restaurant_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return RestaurantResponseSchema.from_entity(restaurant)


@router.patch("/{restaurant_id}", response_model=RestaurantResponseSchema)
def update_restaurant(
    restaurant_id: int,
    payload: RestaurantUpdateSchema,
    repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> RestaurantResponseSchema:
    data = payload.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Debes enviar al menos un campo para actualizar",
        )
    try:
        restaurant = UpdateRestaurant(repository).execute(restaurant_id=restaurant_id, data=data)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc
    return RestaurantResponseSchema.from_entity(restaurant)


@router.delete("/{restaurant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_restaurant(
    restaurant_id: int,
    repository: RestaurantRepository = Depends(get_restaurant_repository),
) -> None:
    try:
        DeleteRestaurant(repository).execute(restaurant_id)
    except NotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=exc.message) from exc

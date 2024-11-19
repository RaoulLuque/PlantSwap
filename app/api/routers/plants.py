import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.crud import plants_crud
from app.api.dependencies import SessionDep, CurrentUserDep
from app.models import PlantPublic, PlantCreate, Plant, PlantsPublic

# Router for api endpoints regarding plants/creation of ad functionality
router = APIRouter()


@router.post("/plants/create", response_model=PlantPublic)
def create_plant_ad(
    session: SessionDep, current_user: CurrentUserDep, plant_in: PlantCreate
):
    """
    Create new plant ad.
    :param current_user: Currently logged-in user
    :param session: Current database session.
    :param plant_in: Plant data for the to-be-created plant ad.
    :return: Name, description, owner_id and id of the created plant.
    """
    plant: Plant = plants_crud.create_plant(session, current_user, plant_in)
    return plant


@router.get("/plants/", response_model=PlantsPublic)
def read_plants(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all existing plant ads.
    :param session: Current database session.
    :param skip: Number of plant ads to skip.
    :param limit: Limit of plant ads to retrieve.
    :return: List of plants with number of plants as a PlantsPublic instance.
    """
    statement = select(Plant).offset(skip).limit(limit)
    plants = session.exec(statement).all()
    count = len(plants)
    return PlantsPublic(data=plants, count=count)


@router.get("/plants/{id}", response_model=PlantPublic)
def read_plant(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Retrieve plant with given id.
    :param id: id of plant.
    :param session: Current database session.
    :return: Plant with given id, if exists.
    """
    plant = session.get(Plant, id)
    if plant is None:
        raise HTTPException(
            status_code=404,
            detail="No plant with the given id exists.",
        )
    return plant


@router.post("/plants/{id}", response_model=PlantPublic)
def delete_plant(
    session: SessionDep, current_user: CurrentUserDep, id: uuid.UUID
) -> Any:
    """
    Delete plant with given id if current_user is owner.
    :param current_user: Currently logged-in user
    :param id: id of plant to be deleted.
    :param session: Current database session.
    :return: Plant with given id, if deleted successfully.
    """
    plant = session.get(Plant, id)
    if plant is None:
        raise HTTPException(
            status_code=404,
            detail="No plant with the given id exists.",
        )
    if not current_user.is_superuser:
        if plant.owner_id != current_user.id:
            raise HTTPException(
                status_code=401,
                detail="You are not the owner of the plant.",
            )
    session.delete(plant)
    session.commit()
    return plant

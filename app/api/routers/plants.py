import uuid
from typing import Any

from fastapi import APIRouter, HTTPException, UploadFile, Form

from app.core.config import settings
from app.core.crud import plants_crud
from app.api.dependencies import SessionDep, CurrentUserDep
from app.models import PlantPublic, Plant, PlantsPublic, PlantCreate

# Router for api endpoints regarding plants/creation of ad functionality
router = APIRouter()


@router.post("/plants/create", response_model=PlantPublic)
def create_plant_ad(
    session: SessionDep,
    current_user: CurrentUserDep,
    name: str = Form(...),
    description: str | None = Form(None),
    city: str = Form(...),
    tags: list[str] = Form([]),
    image: UploadFile | str | None = None,
):
    """
    Create a new plant ad.
    :param current_user: Currently logged-in user.
    :param session: Current database session.
    :param name: Name of the plant.
    :param description: Description of the plant.
    :param city: City of the plant.
    :param tags: Tags of the plant.
    :param image: Optional image of the plant.
    :return: Name, description, owner_id and id of the created plant.
    """
    # Remove empty string tags
    tags = [tag for tag in tags if tag != ""]
    plant_in = PlantCreate(name=name, description=description, city=city, tags=tags)
    if isinstance(image, str) or image is None:
        image = None
    else:
        if not settings.USE_IMAGE_UPLOAD:
            raise HTTPException(
                status_code=500,
                detail="Image upload is not configured for the app.",
            )

    plant: Plant = plants_crud.create_plant(session, current_user, plant_in, image)
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
    plants_public = plants_crud.get_all_plant_ads(session, skip, limit)
    return plants_public


@router.get("/plants/own", response_model=PlantsPublic)
def read_my_plants(
    session: SessionDep, current_user: CurrentUserDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve all existing plant ads.
    :param session: Current database session.
    :param current_user: Currently logged-in user.
    :param skip: Number of plant ads to skip.
    :param limit: Limit of plant ads to retrieve.
    :return: List of plants with number of plants as a PlantsPublic instance.
    """
    plants_public = plants_crud.get_all_plant_ads_from_one_user(
        session, current_user.id, skip, limit
    )
    return plants_public


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
    plant = plants_crud.delete_plant_ad(session, plant)
    return plant

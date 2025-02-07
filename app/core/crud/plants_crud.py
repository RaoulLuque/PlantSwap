import uuid

from fastapi import UploadFile
from sqlmodel import Session, select

from app.core.config import settings
from app.core.images import upload_image_to_cloudinary, delete_image_from_cloudinary
from app.models import User, PlantCreate, Plant, PlantsPublic


def create_plant(
    session: Session,
    user: User,
    plant_in: PlantCreate,
    image: UploadFile | None = None,
) -> Plant:
    """
    Create a new plant ad.
    :param session: Current database session
    :param user: User creating the plant ad
    :param plant_in: Data for the to-be-created plant ad
    :param image: Optional image of the plant
    :return: Created plant instance
    """
    # Obtain plant id to pass it to image upload
    plant: Plant = Plant.model_validate(
        plant_in, update={"owner_id": user.id, "image_url": None}
    )

    # Handle image upload or set image_url to None
    image_url = None
    if image is not None:
        image_url = upload_image_to_cloudinary(image, str(plant.id))
    plant.image_url = image_url
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant


def get_all_plant_ads(
    session: Session, skip: int = 0, limit: int = 100
) -> PlantsPublic:
    """
    Retrieve all existing plant ads up to the given limit with the given offset.
    :param session: Current database session
    :param skip: Number of ads to skip
    :param limit: Limit of ads to retrieve
    :return: List of plant ads with number of ads as a PlantsPublic instance
    """
    statement = select(Plant).offset(skip).limit(limit)
    plants = session.exec(statement).all()
    count = len(plants)
    return PlantsPublic(data=plants, count=count)  # type: ignore


def get_all_plant_ads_from_one_user(
    session: Session,
    user_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
) -> PlantsPublic:
    """
    Retrieve all existing plant ads up to the given limit with the given offset from a specific user.
    :param session: Current database session
    :param user_id: User id to retrieve plant ads from
    :param skip: Number of ads to skip
    :param limit: Limit of ads to retrieve
    :return: List of plant ads with number of ads as a PlantsPublic instance
    """
    statement = select(Plant).where(Plant.owner_id == user_id).offset(skip).limit(limit)
    plants = session.exec(statement).all()
    count = len(plants)
    return PlantsPublic(data=plants, count=count)  # type: ignore


def delete_plant_ad(session: Session, plant: Plant) -> Plant:
    """
    Delete plant ad from database and delete image from image hosting if it exists.
    :param session: Database session
    :param plant: Plant ad to be deleted
    """
    if plant.image_url is not None and settings.USE_IMAGE_UPLOAD:
        delete_image_from_cloudinary(str(plant.id))
    session.delete(plant)
    session.commit()
    return plant

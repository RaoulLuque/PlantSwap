from sqlmodel import Session, select

from app.models import User, PlantCreate, Plant, PlantsPublic


def create_plant(session: Session, user: User, plant_in: PlantCreate) -> Plant:
    """
    Create a new plant ad.
    :param session: Current database session
    :param user: User creating the plant ad
    :param plant_in: Data for the to-be-created plant ad
    :return: Created plant instance
    """
    plant: Plant = Plant.model_validate(plant_in, update={"owner_id": user.id})
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


def delete_plant_ad(session: Session, plant: Plant) -> Plant:
    """
    Delete plant ad from database.
    :param session: Database session
    :param plant: Plant ad to be deleted
    """
    session.delete(plant)
    session.commit()
    return plant

from sqlmodel import Session

from app.models import User, PlantCreate, Plant


def create_plant(session: Session, user: User, plant_in: PlantCreate) -> Plant:
    plant: Plant = Plant.model_validate(plant_in, update={"owner_id": user.id})
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant

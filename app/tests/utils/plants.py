from contextlib import contextmanager
from typing import Generator, Tuple

from sqlmodel import Session

from app.core import crud
from app.models import User, Plant, UserCreate, PlantCreate
from app.tests.utils.utils import random_email, random_lower_string


@contextmanager
def create_random_plant(
    database: Session,
) -> Generator[Tuple[User, str, Plant], None, None]:
    """
    Context manager for creating a random plant with random email and password.
    :param database: Database session.
    :return: User, (un-hashed) password and plant.
    """
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = crud.create_user(database, user_create)
    plant_in = PlantCreate(name="Monstera", description="Nice")
    plant = crud.create_plant(database, user, plant_in)
    try:
        yield user, password, plant
    finally:
        crud.delete_user(database, user)


def assert_if_plant_and_json_response_plant_match(
    plant: Plant, json_plant: dict[str, str]
) -> None:
    """
    Asserts if the plant instance and the JSON response plant match.
    :param plant: Plant instance
    :param json_plant: JSON response user
    :return: None
    """
    assert plant
    assert json_plant
    assert plant.name == json_plant["name"]
    assert plant.description == json_plant["description"]
    assert str(plant.id) == json_plant["id"]
    assert str(plant.owner_id) == json_plant["owner_id"]

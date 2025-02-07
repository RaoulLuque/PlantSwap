from contextlib import contextmanager
from typing import Generator, Tuple

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.crud import users_crud, plants_crud
from app.models import User, Plant, UserCreate, PlantCreate
from app.tests.utils.users import get_user_authentication_cookie
from app.tests.utils.utils import random_email, random_lower_string


@contextmanager
def create_random_plant(
    client: TestClient,
    database: Session,
) -> Generator[Tuple[User, str, tuple[str, str], Plant], None, None]:
    """
    Context manager for creating a random plant with random email and password.
    :param client: TestClient.
    :param database: Database session.
    :return: User, (un-hashed) password and plant.
    """
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = users_crud.create_user(database, user_create)
    auth_cookie = get_user_authentication_cookie(client, str(username), password)
    plant_in = PlantCreate(name="Monstera", description="Nice", tags=[])
    plant = plants_crud.create_plant(database, user, plant_in)
    try:
        yield user, password, auth_cookie, plant
    finally:
        users_crud.delete_user(database, user)


@contextmanager
def create_random_plant_for_given_user(
    database: Session,
    user: User,
) -> Generator[Plant, None, None]:
    """
    Context manager for creating a random plant for a given user.
    :param database: Database session.
    :param user: User to create plant ad for.
    :return: Plant that was just created.
    """
    plant_in = PlantCreate(name="Monstera", description="Nice", tags=[])
    plant = plants_crud.create_plant(database, user, plant_in)
    try:
        yield plant
    finally:
        plants_crud.delete_plant_ad(database, plant)


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

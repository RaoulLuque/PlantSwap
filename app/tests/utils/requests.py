from contextlib import contextmanager
from typing import Generator, Tuple

from sqlmodel import Session

from app.core.crud import users_crud, plants_crud, requests_crud
from app.models import Plant, User, UserCreate, PlantCreate, TradeRequest
from app.tests.utils.utils import random_email, random_lower_string


@contextmanager
def create_random_trade_request(
    database: Session,
) -> Generator[Tuple[User, str, Plant, User, str, Plant, TradeRequest], None, None]:
    """
    Context manager for creating a random plant with random email and password.
    :param database: Database session.
    :return: User, (un-hashed) password and plant.
    """
    username_one = random_email()
    username_two = random_email()
    while username_one == username_two:
        username_two = random_email()
    password_one = random_lower_string()
    password_two = random_lower_string()
    while password_one == password_two:
        password_two = random_lower_string()
    user_create_one = UserCreate(email=username_one, password=password_one)
    user_create_two = UserCreate(email=username_two, password=password_two)
    user_one = users_crud.create_user(database, user_create_one)
    user_two = users_crud.create_user(database, user_create_two)
    plant_in_one = PlantCreate(name="Monstera", description="Nice")
    plant_in_two = PlantCreate(name="Monstera", description="Nice")
    plant_one = plants_crud.create_plant(database, user_one, plant_in_one)
    plant_two = plants_crud.create_plant(database, user_two, plant_in_two)
    trade_request = requests_crud.create_trade_request_from_plant_ids(
        database, plant_one.id, plant_two.id
    )
    try:
        yield (
            user_one,
            password_one,
            plant_one,
            user_two,
            password_two,
            plant_two,
            trade_request,
        )
    finally:
        users_crud.delete_user(database, user_one)
        users_crud.delete_user(database, user_two)


def assert_if_trade_request_json_and_trade_request_data_match(
    outgoing_plant: Plant,
    incoming_plant: Plant,
    json_trade_request: dict[str, str],
    message: str | None = None,
    accepted: bool = False,
) -> None:
    """
    Asserts if the request json and the request data match.
    :param outgoing_plant: Outgoing plant instance
    :param incoming_plant: Incoming plant instance
    :param json_trade_request: Response trade request as JSON dict
    :param message: Optional message
    :return: None
    """
    assert json_trade_request
    assert str(outgoing_plant.id) == json_trade_request["outgoing_plant_id"]
    assert str(incoming_plant.id) == json_trade_request["incoming_plant_id"]
    assert str(outgoing_plant.owner_id) == json_trade_request["outgoing_user_id"]
    assert str(incoming_plant.owner_id) == json_trade_request["incoming_user_id"]
    assert message == json_trade_request["message"]
    assert accepted == json_trade_request["accepted"]

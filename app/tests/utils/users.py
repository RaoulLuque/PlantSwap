from contextlib import contextmanager
from typing import Generator, Tuple

from sqlmodel import Session
from starlette.testclient import TestClient

from app.core.crud import users_crud
from app.core.config import settings
from app.models import User, UserCreate
from app.tests.utils.utils import random_email, random_lower_string


@contextmanager
def create_random_user(
    database: Session,
) -> Generator[Tuple[User, str], None, None]:
    """
    Context manager for creating a random user with random email and password.
    :param database: Database session.
    :return: User and (un-hashed) password.
    """
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = users_crud.create_user(database, user_create)
    try:
        yield user, password
    finally:
        users_crud.delete_user(database, user)


def get_user_token_headers(
    client: TestClient, email: str, password: str
) -> dict[str, str]:
    """
    Returns the token headers used for authentication for the given user(data)
    :param client: TestClient
    :param email: Email of user
    :param password: (Non-hashed) Password of user
    :return: Dictionary with token headers
    """
    login_data = {
        "username": email,
        "password": password,
    }
    r = client.post("/login/token", data=login_data)
    tokens = r.json()
    if "access_token" in tokens:
        a_token = tokens["access_token"]
    else:
        a_token = None
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    """
    Returns the token headers used for authentication of the default superuser of the app
    :param client: TestClient
    :return: Dictionary with token headers
    """
    headers = get_user_token_headers(
        client, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD
    )
    return headers


def assert_if_user_and_json_response_user_match(user: User, json_user: dict) -> None:
    """
    Asserts if the User instance and the JSON response user match.
    :param user: User instance
    :param json_user: Response user as JSON dict
    :return: None
    """
    assert user
    assert json_user
    assert json_user["id"] == str(user.id)
    assert json_user["email"] == user.email
    assert json_user["is_active"] == user.is_active
    assert json_user["is_superuser"] == user.is_superuser
    assert json_user["full_name"] == user.full_name

import random
import string
from contextlib import contextmanager

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core import crud
from app.core.config import settings
from app.models import UserCreate, User


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


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


@contextmanager
def create_random_user(database: Session):
    """
    Context manager for creating a random user with random email and password.
    :param database: Database session.
    :return: User and (un-hashed) password.
    """
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = crud.create_user(database, user_create)
    try:
        yield user, password
    finally:
        crud.delete_user(database, user)


def assert_if_user_and_json_response_user_match(user: User, json_user: dict) -> None:
    """
    Asserts if the User instance and the JSON response user match.
    :param user: User instance
    :param json_user: JSON response user
    :return: None
    """
    assert user
    assert json_user
    assert json_user["id"] == str(user.id)
    assert json_user["email"] == user.email
    assert json_user["is_active"] == user.is_active
    assert json_user["is_superuser"] == user.is_superuser
    assert json_user["full_name"] == user.full_name

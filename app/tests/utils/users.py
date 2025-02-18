from contextlib import contextmanager
from typing import Generator, Tuple

from sqlmodel import Session
from starlette.testclient import TestClient

from app.api.dependencies import ACCESS_TOKEN_COOKIE_NAME
from app.core.crud import users_crud
from app.core.config import settings
from app.models import User, UserCreate
from app.tests.utils.utils import random_email, random_lower_string


@contextmanager
def create_random_user(
    client: TestClient, database: Session
) -> Generator[Tuple[User, str, tuple[str, str]], None, None]:
    """
    Context manager for creating a random user with random email and password.
    :param client: TestClient
    :param database: Database session.
    :return: User and (un-hashed) password.
    """
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = users_crud.create_user(database, user_create)
    auth_cookie = get_user_authentication_cookie(client, str(username), password)
    try:
        yield user, password, auth_cookie
    finally:
        users_crud.delete_user(database, user)


def get_user_authentication_cookie(
    client: TestClient, email: str, password: str
) -> tuple[str, str]:
    """
    Returns the cookie for oauth authentication for the given user(data) (tuple with name : value). If the login is wrong
    an empty string is returned as the value of the cookie.
    :param client: TestClient
    :param email: Email of user
    :param password: (Non-hashed) Password of user
    :return: Tuple with cookie name and value
    """
    login_data = {
        "username": email,
        "password": password,
    }
    response = client.post("/login/token", data=login_data)
    access_token_cookie_value = ""
    print("Response cookies:", response.cookies)
    if ACCESS_TOKEN_COOKIE_NAME in response.cookies:
        print("Empty cookie:", access_token_cookie_value)
        access_token_cookie_value = response.cookies[ACCESS_TOKEN_COOKIE_NAME]
    print("Cookie tuple before returning:", ACCESS_TOKEN_COOKIE_NAME, access_token_cookie_value)
    return ACCESS_TOKEN_COOKIE_NAME, access_token_cookie_value


def get_superuser_authentication_cookie(client: TestClient) -> tuple[str, str]:
    """
    Returns the cookie used for authentication of the default superuser of the app
    :param client: TestClient
    :return: Tuple with cookie name and value
    """
    cookie = get_user_authentication_cookie(
        client, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD
    )
    print("superuser auth cookie:", cookie)
    return cookie


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

import random
import string

from fastapi.testclient import TestClient

from app.core.config import settings


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_email() -> str:
    return f"{random_lower_string()}@{random_lower_string()}.com"


def get_user_token_headers(client: TestClient, email: str, password: str) -> dict[str, str]:
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
    headers = get_user_token_headers(client, settings.FIRST_SUPERUSER, settings.FIRST_SUPERUSER_PASSWORD)
    return headers

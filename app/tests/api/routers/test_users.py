from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core import crud
from app.core.config import settings
from app.tests.utils.utils import random_email, random_lower_string


def test_read_users_me_superuser(
        client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    r = client.get("/users/me", headers=superuser_token_headers)
    current_user = r.json()
    assert current_user
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_create_user_new_email(
        client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    r = client.post(
        "/users/",
        json=data,
    )
    assert 200 <= r.status_code < 300
    created_user = r.json()
    user = crud.get_user_by_email(session=db, email=username)
    assert user
    assert user.email == created_user["email"]


def test_create_user_existing_email(
        client: TestClient, superuser_token_headers: dict[str, str], db: Session
) -> None:
    data = {"email": settings.FIRST_SUPERUSER, "password": "password"}
    r = client.post(
        "/users/",
        json=data,
    )
    assert r.status_code == 400
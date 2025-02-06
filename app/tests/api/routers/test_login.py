from fastapi.testclient import TestClient
from sqlmodel import Session

from app.api.dependencies import ACCESS_TOKEN_COOKIE_NAME
from app.core.config import settings
from app.core.security import get_password_hash
from app.models import User, UserCreate
from app.tests.utils.utils import random_email, random_lower_string


def test_get_oauth_cookie_superuser(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    response = client.post("/login/token", data=login_data)
    cookies = response.cookies
    response_json = response.json()
    assert response.status_code == 200
    assert response_json == {"message": "Login successful"}
    assert cookies[ACCESS_TOKEN_COOKIE_NAME]


def test_get_ouath_cookie_incorrect_username(client: TestClient) -> None:
    login_data = {
        "username": "",
        "password": "incorrect",
    }
    response = client.post("/login/token", data=login_data)
    assert response.status_code == 400
    assert response.cookies == {}


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    response = client.post("/login/token", data=login_data)
    assert response.status_code == 400
    assert response.cookies == {}


def test_get_access_token_inactive_user(client: TestClient, db: Session) -> None:
    user_create = UserCreate(
        email=random_email(),
        password=random_lower_string(),
        is_active=False,
    )
    user_in_db = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    db.add(user_in_db)
    db.commit()
    db.refresh(user_in_db)
    login_data = {
        "username": user_in_db.email,
        "password": user_create.password,
    }
    response = client.post("/login/token", data=login_data)
    assert response.status_code == 400
    assert response.json() == {"detail": "Inactive user"}
    assert response.cookies == {}
    db.delete(user_in_db)
    db.commit()

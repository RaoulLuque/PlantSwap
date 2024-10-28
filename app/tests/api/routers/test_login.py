from fastapi.testclient import TestClient

from app.core.config import settings


def test_get_access_token_superuser(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/login/token", data=login_data)
    tokens = r.json()
    assert r.status_code == 200
    assert "access_token" in tokens
    assert tokens["access_token"]


def test_get_access_token_incorrect_username(client: TestClient) -> None:
    login_data = {
        "username": "",
        "password": "incorrect",
    }
    r = client.post("/login/token", data=login_data)
    assert r.status_code == 400


def test_get_access_token_incorrect_password(client: TestClient) -> None:
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": "incorrect",
    }
    r = client.post("/login/token", data=login_data)
    assert r.status_code == 400

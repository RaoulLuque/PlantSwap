import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core import crud
from app.core.config import settings
from app.tests.utils.utils import (
    random_email,
    random_lower_string,
    get_user_token_headers,
    create_random_user,
    assert_if_user_and_json_response_user_match,
)


def test_read_users_me_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get("/users/me", headers=superuser_token_headers)
    current_user = response.json()
    assert current_user
    assert current_user["id"] is not None
    assert current_user["is_active"] is True
    assert current_user["is_superuser"]
    assert current_user["email"] == settings.FIRST_SUPERUSER


def test_read_users_me_invalid_token(client: TestClient) -> None:
    user_headers = get_user_token_headers(client, "", "")
    response = client.get("/users/me", headers=user_headers)
    detail = response.json()
    assert detail == {"detail": "Could not validate credentials"}
    headers = response.headers
    assert headers.get("www-authenticate") == "Bearer"


def test_read_user_superuser(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get("/users/me", headers=superuser_token_headers)
    current_user = response.json()
    id = current_user["id"]
    response_two = client.get(f"/users/{id}")
    current_user_two = response_two.json()
    assert current_user == current_user_two


def test_read_user_random_user(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user, _):
        id = user.id
        response = client.get(f"/users/{id}")
        user_two = response.json()
        assert_if_user_and_json_response_user_match(user, user_two)


def test_read_user_not_found(client: TestClient) -> None:
    # This test is flaky since it might generate an existing one
    non_existing_id: uuid.UUID = uuid.uuid4()
    response = client.get(f"/users/{non_existing_id}")
    assert response.status_code == 404
    assert response.json() == {"detail": "No user with the given id exists."}


def test_create_user_new_email(client: TestClient, db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post(
        "/users/signup",
        json=data,
    )
    assert 200 <= response.status_code < 300
    created_user = response.json()
    user = crud.get_user_by_email(session=db, email=username)
    assert user
    assert_if_user_and_json_response_user_match(user, created_user)
    crud.delete_user(db, user)


def test_create_user_existing_email(client: TestClient, db: Session) -> None:
    data = {"email": settings.FIRST_SUPERUSER, "password": "password"}
    response = client.post(
        "/users/signup",
        json=data,
    )
    assert response.status_code == 400


def test_delete_user_not_found(
    client: TestClient, superuser_token_headers: dict[str, str]
) -> None:
    non_existing_id: uuid.UUID = uuid.uuid4()
    response = client.post(f"/users/{non_existing_id}", headers=superuser_token_headers)
    assert response.status_code == 404


def test_delete_user_not_enough_permissions(
    client: TestClient, db: Session, superuser_token_headers
) -> None:
    with create_random_user(db) as (user, password):
        headers = get_user_token_headers(client, user.email, password)
        superuser_id = client.get("/users/me", headers=superuser_token_headers).json()[
            "id"
        ]
        response = client.post(f"/users/{superuser_id}", headers=headers)
        assert response.status_code == 401
        assert response.json() == {
            "detail": "You are not allowed to delete other users."
        }


def test_create_user_read_user_and_delete_user(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user, password):
        id = user.id
        response_read_user = client.get(f"/users/{id}")
        user_two = response_read_user.json()
        assert_if_user_and_json_response_user_match(user, user_two)
        headers = get_user_token_headers(client, user.email, password)
        response_delete_user = client.post(f"/users/{id}", headers=headers)
        assert response_delete_user.status_code == 200
        user_two = response_delete_user.json()
        assert_if_user_and_json_response_user_match(user, user_two)

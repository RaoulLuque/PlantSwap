import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.crud import users_crud
from app.core.config import settings
from app.models import UserCreate
from app.tests.utils.utils import (
    random_email,
    random_lower_string,
)
from app.tests.utils.users import (
    create_random_user,
    get_user_token_headers,
    assert_if_user_and_json_response_user_match,
)


def test_read_users_me_superuser(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    response = client.get("/users/me", headers=superuser_token_headers)
    current_user = response.json()
    superuser = users_crud.get_user_by_email(db, settings.FIRST_SUPERUSER)
    assert superuser
    assert_if_user_and_json_response_user_match(superuser, current_user)


def test_read_users_me_random_user(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user, password):
        user_headers = get_user_token_headers(client, user.email, password)
        response = client.get("/users/me", headers=user_headers)
        json_user = response.json()
        db_user = users_crud.get_user_by_email(db, user.email)
        assert db_user
        assert_if_user_and_json_response_user_match(db_user, json_user)


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


def test_read_users(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user_one, _):
        with create_random_user(db) as (user_two, _):
            response = client.get("/users/")
            response_json = response.json()
            print(response_json)
            assert_if_user_and_json_response_user_match(
                user_one, response_json["data"][1]
            )
            assert_if_user_and_json_response_user_match(
                user_two, response_json["data"][2]
            )
            assert len(response_json["data"]) >= 3


def test_read_plants_limit(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user_one, _):
        with create_random_user(db) as (user_two, _):
            with create_random_user(db) as (user_three, _):
                limit = 2
                response = client.get(f"/users/?limit={limit}")
                response_json = response.json()
                assert len(response_json["data"]) == 2


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
    user = users_crud.get_user_by_email(session=db, email=str(username))
    assert user
    assert_if_user_and_json_response_user_match(user, created_user)
    users_crud.delete_user(db, user)


def test_create_user_existing_email(client: TestClient, db: Session) -> None:
    data = {"email": settings.FIRST_SUPERUSER, "password": "password"}
    response = client.post(
        "/users/signup",
        json=data,
    )
    assert response.status_code == 400


def test_delete_user_existing_user(client: TestClient, db: Session):
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = users_crud.create_user(db, user_create)
    headers = get_user_token_headers(client, str(username), password)
    response = client.post(f"/users/{user.id}", headers=headers)
    assert response.status_code == 200
    assert_if_user_and_json_response_user_match(user, response.json())


def test_delete_user_existing_user_superuser(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    username = random_email()
    password = random_lower_string()
    user_create = UserCreate(email=username, password=password)
    user = users_crud.create_user(db, user_create)
    response = client.post(f"/users/{user.id}", headers=superuser_token_headers)
    assert response.status_code == 200
    assert_if_user_and_json_response_user_match(user, response.json())


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
    username = random_email()
    password = random_lower_string()
    data = {"email": username, "password": password}
    response = client.post(
        "/users/signup",
        json=data,
    )
    assert 200 <= response.status_code < 300
    user = users_crud.get_user_by_email(db, str(data["email"]))
    assert user
    id = user.id
    response_read_user = client.get(f"/users/{id}")
    user_two = response_read_user.json()
    assert_if_user_and_json_response_user_match(user, user_two)
    headers = get_user_token_headers(client, str(user.email), password)
    response_delete_user = client.post(f"/users/{id}", headers=headers)
    assert response_delete_user.status_code == 200
    user_two = response_delete_user.json()
    assert_if_user_and_json_response_user_match(user, user_two)

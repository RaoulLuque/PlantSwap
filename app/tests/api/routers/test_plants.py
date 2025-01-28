import io
import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.utils import (
    random_lower_string,
)
from app.tests.utils.plants import (
    create_random_plant,
    assert_if_plant_and_json_response_plant_match,
)
from app.tests.utils.users import create_random_user, get_user_token_headers


def test_create_plant_new_plant(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user, password):
        user_headers = get_user_token_headers(client, user.email, password)
        data = {
            "name": random_lower_string(),
            "description": random_lower_string(),
        }
        response = client.post(
            "/plants/create", data=data, files=None, headers=user_headers
        )
        print(response)
        assert 200 == response.status_code
        response_json = response.json()
        assert response_json["name"] == data["name"]
        assert response_json["description"] == data["description"]


def test_create_plant_and_check_if_deleted_when_user_is_deleted(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    with create_random_plant(db) as (user, password, plant):
        assert user
        assert password
        assert plant
        plant_id = plant.id
    response = client.get(f"/plants/{plant_id}", headers=superuser_token_headers)
    assert response.status_code == 404
    assert response.json() == {"detail": "No plant with the given id exists."}


def test_create_plant_not_logged_in(client: TestClient) -> None:
    data = {"name": random_lower_string(), "description": random_lower_string()}
    response = client.post("/plants/create", json=data)
    assert 401 == response.status_code
    assert response.json() == {"detail": "Not authenticated"}


@pytest.mark.usefixtures("settings_override")
def test_create_plant_no_image(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user, password):
        assert not settings.USE_IMAGE_UPLOAD
        user_headers = get_user_token_headers(client, user.email, password)

        # Simulate a file upload
        file_content = b"This is a test image file"
        file = ("image", ("test_image.png", io.BytesIO(file_content), "image/png"))

        data = {
            "name": random_lower_string(),
            "description": random_lower_string(),
        }
        response = client.post(
            "/plants/create", data=data, files=[file], headers=user_headers
        )
        assert 500 == response.status_code
        assert response.json() == {
            "detail": "Image upload is not configured for the app."
        }


def test_read_plants(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (_, _, plant_one):
        with create_random_plant(db) as (_, _, plant_two):
            response = client.get("/plants/")
            response_json = response.json()
            assert_if_plant_and_json_response_plant_match(
                plant_one, response_json["data"][0]
            )
            assert_if_plant_and_json_response_plant_match(
                plant_two, response_json["data"][1]
            )
            assert len(response_json["data"]) >= 2


def test_read_plants_limit(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (_, _, plant_one):
        with create_random_plant(db) as (_, _, plant_two):
            with create_random_plant(db) as (_, _, plant_three):
                limit = 2
                response = client.get(f"/plants/?limit={limit}")
                response_json = response.json()
                assert len(response_json["data"]) == 2


def test_read_plant_existing_plant(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (_, _, plant):
        response = client.get(f"/plants/{plant.id}")
        response_json = response.json()
        assert_if_plant_and_json_response_plant_match(plant, response_json)


def test_read_plant_not_found(client: TestClient) -> None:
    id = uuid.uuid4()
    response = client.get(f"/plants/{id}")
    response_json = response.json()
    assert response.status_code == 404
    assert response_json == {"detail": "No plant with the given id exists."}


def test_delete_plant_superuser_success(
    client: TestClient, db: Session, superuser_token_headers: dict[str, str]
) -> None:
    with create_random_plant(db) as (_, _, plant):
        response = client.post(f"/plants/{plant.id}", headers=superuser_token_headers)
        assert response.status_code == 200
        response_json = response.json()
        assert_if_plant_and_json_response_plant_match(plant, response_json)


def test_delete_plant_user_not_authorized(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (_, _, plant):
        with create_random_user(db) as (user, password):
            user_headers = get_user_token_headers(client, user.email, password)
            response = client.post(f"/plants/{plant.id}", headers=user_headers)
            assert response.status_code == 401
            assert response.json() == {"detail": "You are not the owner of the plant."}


def test_delete_plant_not_authenticated(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (_, _, plant):
        response = client.post(f"/plants/{plant.id}")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_delete_plant_user_success(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (user, password, plant):
        user_headers = get_user_token_headers(client, user.email, password)
        response = client.post(f"/plants/{plant.id}", headers=user_headers)
        assert response.status_code == 200
        response_json = response.json()
        assert_if_plant_and_json_response_plant_match(plant, response_json)


def test_delete_plant_not_found(client: TestClient, db: Session) -> None:
    with create_random_user(db) as (user, password):
        user_headers = get_user_token_headers(client, user.email, password)
        response = client.post(f"/plants/{uuid.uuid4()}", headers=user_headers)
        print(response.json())
        assert response.status_code == 404
        assert response.json() == {"detail": "No plant with the given id exists."}

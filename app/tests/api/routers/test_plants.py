import io
import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.config import settings
from app.tests.utils.utils import (
    random_lower_string,
)
from app.tests.utils.plants import (
    create_random_plant,
    assert_if_plant_and_json_response_plant_match,
    create_random_plant_for_given_user,
)
from app.tests.utils.users import create_random_user


def test_create_plant_new_plant(client: TestClient, db: Session) -> None:
    with create_random_user(client, db) as (user, password, auth_cookie):
        data = {
            "name": random_lower_string(),
            "description": random_lower_string(),
            "city": random_lower_string(),
        }
        response = client.post(
            "/plants/create", data=data, files=None, cookies=[auth_cookie]
        )
        assert 200 == response.status_code
        response_json = response.json()
        assert response_json["name"] == data["name"]
        assert response_json["description"] == data["description"]


def test_create_plant_new_plant_with_tags(client: TestClient, db: Session) -> None:
    with create_random_user(client, db) as (user, password, auth_cookie):
        data = {
            "name": random_lower_string(),
            "description": random_lower_string(),
            "city": random_lower_string(),
            "tags": ["", "test", "testing", "testinging", ""]
        }
        response = client.post(
            "/plants/create", data=data, files=None, cookies=[auth_cookie]
        )
        assert 200 == response.status_code
        response_json = response.json()
        assert response_json["name"] == data["name"]
        assert response_json["description"] == data["description"]
        assert response_json["tags"].sort() == ["test", "testing", "testinging"].sort()


def test_create_plant_and_check_if_deleted_when_user_is_deleted(
    client: TestClient, db: Session, superuser_auth_cookie: tuple[str, str]
) -> None:
    with create_random_plant(client, db) as (user, password, auth_cookie, plant):
        assert user
        assert password
        assert plant
        plant_id = plant.id
    response = client.get(f"/plants/{plant_id}", cookies=[superuser_auth_cookie])
    assert response.status_code == 404
    assert response.json() == {"detail": "No plant with the given id exists."}


def test_create_plant_not_logged_in(client: TestClient) -> None:
    data = {
        "name": random_lower_string(),
        "description": random_lower_string(),
        "city": random_lower_string(),
    }
    response = client.post("/plants/create", json=data)
    assert 401 == response.status_code
    assert response.json() == {"detail": "Not authenticated"}


def test_create_plant_no_image(client: TestClient, db: Session) -> None:
    with create_random_user(client, db) as (user, password, auth_cookie):
        assert not settings.USE_IMAGE_UPLOAD

        # Simulate a file upload
        file_content = b"This is a test image file"
        file = ("image", ("test_image.png", io.BytesIO(file_content), "image/png"))

        data = {
            "name": random_lower_string(),
            "description": random_lower_string(),
            "city": random_lower_string(),
        }
        response = client.post(
            "/plants/create", data=data, files=[file], cookies=[auth_cookie]
        )
        assert 500 == response.status_code
        assert response.json() == {
            "detail": "Image upload is not configured for the app."
        }


def test_read_plants(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (_, _, _, plant_one):
        with create_random_plant(client, db) as (_, _, _, plant_two):
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
    with create_random_plant(client, db) as (_, _, _, plant_one):
        with create_random_plant(client, db) as (_, _, _, plant_two):
            with create_random_plant(client, db) as (_, _, _, plant_three):
                limit = 2
                response = client.get(f"/plants/?limit={limit}")
                response_json = response.json()
                assert len(response_json["data"]) == 2


def test_read_own_plants(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (_, _, auth_cookie, plant_one):
        response = client.get("/plants/own", cookies=[auth_cookie])
        response_json = response.json()
        print(response_json)
        assert_if_plant_and_json_response_plant_match(
            plant_one, response_json["data"][0]
        )
        assert len(response_json["data"]) == 1


def test_read_plants_own_with_others_existing(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (_, _, auth_cookie, plant_one):
        with create_random_plant(client, db) as (_, _, _, plant_two):
            with create_random_plant(client, db) as (_, _, _, plant_three):
                response = client.get("/plants/own", cookies=[auth_cookie])
                response_json = response.json()
                assert_if_plant_and_json_response_plant_match(
                    plant_one, response_json["data"][0]
                )
                assert len(response_json["data"]) == 1


def test_read_own_plants_limit(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (user, _, auth_cookie, _):
        with create_random_plant_for_given_user(db, user) as _:
            with create_random_plant_for_given_user(db, user) as _:
                limit = 2
                response = client.get(f"/plants/?limit={limit}", cookies=[auth_cookie])
                response_json = response.json()
                assert len(response_json["data"]) == 2


def test_read_plant_existing_plant(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (_, _, _, plant):
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
    client: TestClient, db: Session, superuser_auth_cookie
) -> None:
    with create_random_plant(client, db) as (_, _, _, plant):
        print(superuser_auth_cookie)
        response = client.post(f"/plants/{plant.id}", cookies=[superuser_auth_cookie])
        assert response.status_code == 200
        response_json = response.json()
        assert_if_plant_and_json_response_plant_match(plant, response_json)


def test_delete_plant_user_not_authorized(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (_, _, _, plant):
        with create_random_user(client, db) as (user, password, auth_cookie):
            response = client.post(f"/plants/{plant.id}", cookies=[auth_cookie])
            assert response.status_code == 401
            assert response.json() == {"detail": "You are not the owner of the plant."}


def test_delete_plant_not_authenticated(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (_, _, _, plant):
        response = client.post(f"/plants/{plant.id}")
        assert response.status_code == 401
        assert response.json() == {"detail": "Not authenticated"}


def test_delete_plant_user_success(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (user, password, auth_cookie, plant):
        response = client.post(f"/plants/{plant.id}", cookies=[auth_cookie])
        assert response.status_code == 200
        response_json = response.json()
        assert_if_plant_and_json_response_plant_match(plant, response_json)


def test_delete_plant_not_found(client: TestClient, db: Session) -> None:
    with create_random_user(client, db) as (user, password, auth_cookie):
        response = client.post(f"/plants/{uuid.uuid4()}", cookies=[auth_cookie])
        print(response.json())
        assert response.status_code == 404
        assert response.json() == {"detail": "No plant with the given id exists."}

import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.crud import requests_crud
from app.models import Plant, TradeRequest
from app.tests.utils.plants import create_random_plant
from app.tests.utils.requests import (
    assert_if_trade_request_json_and_trade_request_data_match,
    create_random_trade_request,
)
from app.tests.utils.users import get_user_token_headers, create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_trade_request_new_request(client: TestClient, db: Session) -> None:
    with create_random_plant(db) as (user_one, password_one, plant_one):
        with create_random_plant(db) as (user_two, password_two, plant_two):
            user_one_headers = get_user_token_headers(
                client, user_one.email, password_one
            )
            response = client.post(
                f"/requests/create/{plant_one.id}/{plant_two.id}",
                headers=user_one_headers,
            )
            assert 200 == response.status_code
            db.refresh(plant_one)
            db.refresh(plant_two)
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()
            )


def test_create_trade_request_check_if_request_is_deleted_when_plant_is_deleted(
    client: TestClient, db: Session
) -> None:
    with create_random_plant(db) as (user_one, password_one, plant_one):
        with create_random_user(db) as (user_two, password_two):
            user_two_headers = get_user_token_headers(
                client, user_two.email, password_two
            )
            data = {"name": random_lower_string(), "description": random_lower_string()}
            response = client.post(
                "/plants/create", json=data, headers=user_two_headers
            )
            plant_two: Plant | None = db.get(Plant, response.json()["id"])
            assert plant_two
            user_one_headers = get_user_token_headers(
                client, user_one.email, password_one
            )
            response = client.post(
                f"/requests/create/{plant_one.id}/{plant_two.id}",
                headers=user_one_headers,
            )
            assert 200 == response.status_code
            db.refresh(plant_one)
            db.refresh(plant_two)
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()
            )
            response = client.post(f"/plants/{plant_two.id}", headers=user_two_headers)
            print(response)
            assert 200 == response.status_code
            trade_request = db.get(TradeRequest, (plant_one.id, plant_two.id))
            assert trade_request is None


def test_create_trade_request_plant_not_owned(client: TestClient, db: Session):
    with create_random_plant(db) as (user_one, password_one, plant_one):
        with create_random_plant(db) as (user_two, password_two, plant_two):
            user_one_headers = get_user_token_headers(
                client, user_one.email, password_one
            )
            response = client.post(
                f"/requests/create/{plant_two.id}/{plant_one.id}",
                headers=user_one_headers,
            )
            assert 401 == response.status_code
            assert {
                "detail": "You cannot trade other people's plants (you do not own the plant you want to offer)."
            } == response.json()


def test_create_trade_request_incoming_plant_does_not_exist(
    client: TestClient, db: Session
):
    with create_random_plant(db) as (user_one, password_one, plant_one):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        # Possibly flaky test if the randomly generated UUID is already in use
        response = client.post(
            f"/requests/create/{plant_one.id}/{uuid.uuid4()}",
            headers=user_one_headers,
        )
        assert 404 == response.status_code
        assert {"detail": "The plant you want does not exist."} == response.json()


def test_create_trade_request_trade_with_self(client: TestClient, db: Session):
    with create_random_plant(db) as (user_one, password_one, plant_one):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        # Possibly flaky test if the randomly generated UUID is already in use
        response = client.post(
            f"/requests/create/{plant_one.id}/{plant_one.id}",
            headers=user_one_headers,
        )
        assert 418 == response.status_code
        assert {"detail": "You cannot trade with yourself."} == response.json()


def test_create_trade_request_existing_trade_request(client: TestClient, db: Session):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request,
    ):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        response = client.post(
            f"/requests/create/{plant_one.id}/{plant_two.id}",
            headers=user_one_headers,
        )
        assert 409 == response.status_code
        assert {
            "detail": "You already have a trade request for these two plants."
        } == response.json()


def test_read_specific_outgoing_trade_request_existing_trade_request(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request,
    ):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        response = client.get(
            f"/requests/outgoing/{plant_one.id}/{plant_two.id}",
            headers=user_one_headers,
        )
        assert 200 == response.status_code
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one, plant_two, response.json()
        )


def test_read_specific_outgoing_trade_request_plant_not_owned(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request,
    ):
        user_two_headers = get_user_token_headers(client, user_two.email, password_two)
        response = client.get(
            f"/requests/outgoing/{plant_one.id}/{plant_two.id}",
            headers=user_two_headers,
        )
        assert 401 == response.status_code
        assert {
            "detail": "You do not own a plant with the provided outgoing plant id."
        } == response.json()


def test_read_specific_outgoing_trade_request_trade_request_not_found(
    client: TestClient, db: Session
):
    with create_random_plant(db) as (user_one, password_one, plant_one):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        response = client.get(
            f"/requests/outgoing/{plant_one.id}/{uuid.uuid4()}",
            headers=user_one_headers,
        )
        assert 404 == response.status_code
        assert {
            "detail": "No trade request with the given plant ids exists."
        } == response.json()


def test_read_specific_incoming_trade_request_existing_trade_request(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request,
    ):
        user_two_headers = get_user_token_headers(client, user_two.email, password_two)
        response = client.get(
            f"/requests/incoming/{plant_one.id}/{plant_two.id}",
            headers=user_two_headers,
        )
        assert 200 == response.status_code
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one, plant_two, response.json()
        )


def test_read_specific_incoming_trade_request_plant_not_owned(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request,
    ):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        response = client.get(
            f"/requests/incoming/{plant_one.id}/{plant_two.id}",
            headers=user_one_headers,
        )
        assert 401 == response.status_code
        assert {
            "detail": "You do not own a plant with the provided incoming plant id."
        } == response.json()


def test_read_specific_incoming_trade_request_trade_request_not_found(
    client: TestClient, db: Session
):
    with create_random_plant(db) as (user_one, password_one, plant_one):
        user_one_headers = get_user_token_headers(client, user_one.email, password_one)
        response = client.get(
            f"/requests/incoming/{uuid.uuid4()}/{plant_one.id}",
            headers=user_one_headers,
        )
        assert 404 == response.status_code
        assert {
            "detail": "No trade request with the given plant ids exists."
        } == response.json()


def test_read_own_outgoing_trade_requests_no_requests(client: TestClient, db: Session):
    with create_random_user(db) as (user, password):
        user_headers = get_user_token_headers(client, user.email, password)
        response = client.get("/requests/outgoing/", headers=user_headers)
        assert 200 == response.status_code
        assert [] == response.json()["data"]
        assert 0 == response.json()["count"]


def test_read_own_outgoing_trade_requests_two_requests(client: TestClient, db: Session):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(db) as (_, _, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_one.id, plant_three.id
            )
            user_one_headers = get_user_token_headers(
                client, user_one.email, password_one
            )
            response = client.get("/requests/outgoing/", headers=user_one_headers)
            assert 200 == response.status_code
            assert 2 == len(response.json()["data"])
            assert 2 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0]
            )
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_three, response.json()["data"][1]
            )


def test_read_own_outgoing_trade_requests_two_requests_limit_to_one(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(db) as (_, _, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_one.id, plant_three.id
            )
            user_one_headers = get_user_token_headers(
                client, user_one.email, password_one
            )
            limit = 1
            response = client.get(
                f"/requests/outgoing/?limit={limit}", headers=user_one_headers
            )
            assert 200 == response.status_code
            assert 1 == len(response.json()["data"])
            assert 1 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0]
            )


def test_read_own_incoming_trade_requests_no_requests(client: TestClient, db: Session):
    with create_random_user(db) as (user, password):
        user_headers = get_user_token_headers(client, user.email, password)
        response = client.get("/requests/incoming/", headers=user_headers)
        assert 200 == response.status_code
        assert [] == response.json()["data"]
        assert 0 == response.json()["count"]


def test_read_own_incoming_trade_requests_two_requests(client: TestClient, db: Session):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(db) as (_, _, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_three.id, plant_two.id
            )
            user_two_headers = get_user_token_headers(
                client, user_two.email, password_two
            )
            response = client.get("/requests/incoming/", headers=user_two_headers)
            assert 200 == response.status_code
            assert 2 == len(response.json()["data"])
            assert 2 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0]
            )
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_three, plant_two, response.json()["data"][1]
            )


def test_read_own_incoming_trade_requests_two_requests_limit_to_one(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(db) as (_, _, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_three.id, plant_two.id
            )
            user_two_headers = get_user_token_headers(
                client, user_two.email, password_two
            )
            limit = 1
            response = client.get(
                f"/requests/incoming/?limit={limit}", headers=user_two_headers
            )
            assert 200 == response.status_code
            assert 1 == len(response.json()["data"])
            assert 1 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0]
            )


def test_read_own_trade_requests_no_requests(client: TestClient, db: Session):
    with create_random_user(db) as (user, password):
        user_headers = get_user_token_headers(client, user.email, password)
        response = client.get("/requests/all/", headers=user_headers)
        assert 200 == response.status_code
        assert [] == response.json()["data"]
        assert 0 == response.json()["count"]


def test_read_own_trade_requests_two_requests(client: TestClient, db: Session):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(db) as (_, _, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_two.id, plant_three.id
            )
            user_two_headers = get_user_token_headers(
                client, user_two.email, password_two
            )
            response = client.get("/requests/all/", headers=user_two_headers)
            assert 200 == response.status_code
            assert 2 == len(response.json()["data"])
            assert 2 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0]
            )
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_two, plant_three, response.json()["data"][1]
            )


def test_read_own_trade_requests_two_requests_limit_to_one(
    client: TestClient, db: Session
):
    with create_random_trade_request(db) as (
        user_one,
        password_one,
        plant_one,
        user_two,
        password_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(db) as (_, _, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_two.id, plant_three.id
            )
            user_two_headers = get_user_token_headers(
                client, user_two.email, password_two
            )
            limit = 1
            skip = 1
            response = client.get(
                f"/requests/all/?limit={limit}&skip={skip}", headers=user_two_headers
            )
            assert 200 == response.status_code
            assert 1 == len(response.json()["data"])
            assert 1 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_two, plant_three, response.json()["data"][0]
            )

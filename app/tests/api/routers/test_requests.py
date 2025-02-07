import uuid

from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.core.crud import requests_crud
from app.models import TradeRequest, Message, Plant
from app.tests.utils.plants import create_random_plant
from app.tests.utils.requests import (
    assert_if_trade_request_json_and_trade_request_data_match,
    create_random_trade_request,
)
from app.tests.utils.users import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_trade_request_new_request(client: TestClient, db: Session) -> None:
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        with create_random_plant(client, db) as (
            user_two,
            password_two,
            auth_cookie_two,
            plant_two,
        ):
            # Use the auth cookie from the user that owns plant_one
            response = client.post(
                f"/requests/create/{plant_one.id}/{plant_two.id}",
                cookies=[auth_cookie_one],
            )
            assert response.status_code == 200
            db.refresh(plant_one)
            db.refresh(plant_two)
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json(), []
            )


def test_create_trade_request_check_if_request_is_deleted_when_plant_is_deleted(
    client: TestClient, db: Session
) -> None:
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        with create_random_user(client, db) as (
            user_two,
            password_two,
            auth_cookie_two,
        ):
            data = {"name": random_lower_string(), "description": random_lower_string()}
            response = client.post(
                "/plants/create", data=data, cookies=[auth_cookie_two]
            )
            plant_two: Plant | None = db.get(Plant, response.json()["id"])
            assert plant_two
            response = client.post(
                f"/requests/create/{plant_one.id}/{plant_two.id}",
                cookies=[auth_cookie_one],
            )
            assert response.status_code == 200
            db.refresh(plant_one)
            db.refresh(plant_two)
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json(), []
            )
            response = client.post(f"/plants/{plant_two.id}", cookies=[auth_cookie_two])
            assert response.status_code == 200
            trade_request = db.get(TradeRequest, (plant_one.id, plant_two.id))
            assert trade_request is None


def test_create_trade_request_with_message(client: TestClient, db: Session):
    with create_random_plant(client, db) as (
        user_one,
        _,
        auth_cookie_one,
        plant_one,
    ):
        with create_random_plant(client, db) as (
            _,
            _,
            _,
            plant_two,
        ):
            message_content = random_lower_string()
            response = client.post(
                f"/requests/create/{plant_one.id}/{plant_two.id}",
                data={"message": message_content},
                cookies=[auth_cookie_one],
            )
            assert response.status_code == 200
            messages = [
                Message(
                    sender_id=user_one.id,
                    content=message_content,
                    outgoing_plant_id=plant_one.id,
                    incoming_plant_id=plant_two.id,
                )
            ]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json(), messages
            )


def test_check_if_messages_are_being_deleted_when_trade_request_is_deleted(
    client: TestClient, db: Session
):
    with create_random_plant(client, db) as (
        user_one,
        _,
        auth_cookie_one,
        plant_one,
    ):
        with create_random_plant(client, db) as (
            _,
            _,
            _,
            plant_two,
        ):
            message_content = random_lower_string()
            trade_request = requests_crud.create_trade_request_from_plant_ids(
                db, plant_one.id, plant_two.id, message_content
            )
            message_id = trade_request.messages[0].id
    assert db.get(TradeRequest, (plant_one.id, message_id)) is None
    assert db.get(Message, message_id) is None


def test_create_trade_request_plant_not_owned(client: TestClient, db: Session):
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        with create_random_plant(client, db) as (
            user_two,
            password_two,
            auth_cookie_two,
            plant_two,
        ):
            response = client.post(
                f"/requests/create/{plant_two.id}/{plant_one.id}",
                cookies=[auth_cookie_one],
            )
            assert response.status_code == 401
            assert {
                "detail": "You cannot trade other people's plants (you do not own the plant you want to offer)."
            } == response.json()


def test_create_trade_request_incoming_plant_does_not_exist(
    client: TestClient, db: Session
):
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        response = client.post(
            f"/requests/create/{plant_one.id}/{uuid.uuid4()}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 404
        assert {"detail": "The plant you want does not exist."} == response.json()


def test_create_trade_request_trade_with_self(client: TestClient, db: Session):
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        response = client.post(
            f"/requests/create/{plant_one.id}/{plant_one.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 418
        assert {"detail": "You cannot trade with yourself."} == response.json()


def test_create_trade_request_existing_trade_request(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.post(
            f"/requests/create/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 409
        assert {
            "detail": "You already have a trade request for these two plants."
        } == response.json()


def test_read_specific_outgoing_trade_request_existing_trade_request(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.get(
            f"/requests/outgoing/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 200
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one, plant_two, response.json(), []
        )


def test_read_specific_outgoing_trade_request_plant_not_owned(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.get(
            f"/requests/outgoing/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_two],
        )
        assert response.status_code == 401
        assert {
            "detail": "You do not own a plant with the provided outgoing plant id."
        } == response.json()


def test_read_specific_outgoing_trade_request_trade_request_not_found(
    client: TestClient, db: Session
):
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        response = client.get(
            f"/requests/outgoing/{plant_one.id}/{uuid.uuid4()}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 404
        assert {
            "detail": "No trade request with the given plant ids exists."
        } == response.json()


def test_read_specific_incoming_trade_request_existing_trade_request(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.get(
            f"/requests/incoming/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_two],
        )
        assert response.status_code == 200
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one, plant_two, response.json(), []
        )


def test_read_specific_incoming_trade_request_plant_not_owned(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.get(
            f"/requests/incoming/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 401
        assert {
            "detail": "You do not own a plant with the provided incoming plant id."
        } == response.json()


def test_read_specific_incoming_trade_request_trade_request_not_found(
    client: TestClient, db: Session
):
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        response = client.get(
            f"/requests/incoming/{uuid.uuid4()}/{plant_one.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 404
        assert {
            "detail": "No trade request with the given plant ids exists."
        } == response.json()


def test_read_own_outgoing_trade_requests_no_requests(client: TestClient, db: Session):
    with create_random_user(client, db) as (user, password, auth_cookie):
        response = client.get("/requests/outgoing/", cookies=[auth_cookie])
        assert response.status_code == 200
        assert [] == response.json()["data"]
        assert 0 == response.json()["count"]


def test_read_own_outgoing_trade_requests_two_requests(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(client, db) as (user, pwd, auth_cookie, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_one.id, plant_three.id
            )
            response = client.get("/requests/outgoing/", cookies=[auth_cookie_one])
            assert response.status_code == 200
            assert 2 == len(response.json()["data"])
            assert 2 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0], []
            )
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_three, response.json()["data"][1], []
            )


def test_read_own_outgoing_trade_requests_two_requests_limit_to_one(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(client, db) as (user, pwd, auth_cookie, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_one.id, plant_three.id
            )
            limit = 1
            response = client.get(
                f"/requests/outgoing/?limit={limit}", cookies=[auth_cookie_one]
            )
            assert response.status_code == 200
            assert 1 == len(response.json()["data"])
            assert 1 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0], []
            )


def test_read_own_incoming_trade_requests_no_requests(client: TestClient, db: Session):
    with create_random_user(client, db) as (user, password, auth_cookie):
        response = client.get("/requests/incoming/", cookies=[auth_cookie])
        assert response.status_code == 200
        assert [] == response.json()["data"]
        assert 0 == response.json()["count"]


def test_read_own_incoming_trade_requests_two_requests(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(client, db) as (user, pwd, auth_cookie, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_three.id, plant_two.id
            )
            response = client.get("/requests/incoming/", cookies=[auth_cookie_two])
            assert response.status_code == 200
            assert 2 == len(response.json()["data"])
            assert 2 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0], []
            )
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_three, plant_two, response.json()["data"][1], []
            )


def test_read_own_incoming_trade_requests_two_requests_limit_to_one(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(client, db) as (user, pwd, auth_cookie, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_three.id, plant_two.id
            )
            limit = 1
            response = client.get(
                f"/requests/incoming/?limit={limit}", cookies=[auth_cookie_two]
            )
            assert response.status_code == 200
            assert 1 == len(response.json()["data"])
            assert 1 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0], []
            )


def test_read_own_trade_requests_no_requests(client: TestClient, db: Session):
    with create_random_user(client, db) as (user, password, auth_cookie):
        response = client.get("/requests/all/", cookies=[auth_cookie])
        assert response.status_code == 200
        assert [] == response.json()["data"]
        assert 0 == response.json()["count"]


def test_read_own_trade_requests_two_requests(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(client, db) as (user, pwd, auth_cookie, plant_three):
            requests_crud.create_trade_request_from_plant_ids(
                db, plant_two.id, plant_three.id
            )
            response = client.get("/requests/all/", cookies=[auth_cookie_two])
            assert response.status_code == 200
            assert 2 == len(response.json()["data"])
            assert 2 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_one, plant_two, response.json()["data"][0], []
            )
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_two, plant_three, response.json()["data"][1], []
            )


def test_read_own_trade_requests_two_requests_limit_to_one(
    client: TestClient, db: Session
):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request_one,
    ):
        with create_random_plant(client, db) as (user, pwd, auth_cookie, plant_three):
            trade_request_two = requests_crud.create_trade_request_from_plant_ids(
                db, plant_two.id, plant_three.id
            )
            limit = 1
            skip = 1
            response = client.get(
                f"/requests/all/?limit={limit}&skip={skip}", cookies=[auth_cookie_two]
            )
            assert response.status_code == 200
            assert 1 == len(response.json()["data"])
            assert 1 == response.json()["count"]
            assert_if_trade_request_json_and_trade_request_data_match(
                plant_two, plant_three, response.json()["data"][0], []
            )
        assert (
            db.get(
                TradeRequest,
                (
                    trade_request_two.outgoing_plant_id,
                    trade_request_two.incoming_plant_id,
                ),
            )
            is None
        )


def test_accept_trade_request_successful(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.post(
            f"/requests/accept/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_two],
        )
        assert response.status_code == 200
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one,
            plant_two,
            response.json(),
            [],
            accepted=True,
        )


def test_accept_trade_request_plant_not_owned(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.post(
            f"/requests/accept/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 401
        assert {
            "detail": "You do not own a plant with the provided incoming plant id."
        } == response.json()


def test_accept_trade_request_trade_request_not_found(client: TestClient, db: Session):
    with create_random_plant(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
    ):
        response = client.post(
            f"/requests/accept/{uuid.uuid4()}/{plant_one.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 404
        assert {
            "detail": "No trade request with the given plant ids exists."
        } == response.json()


def test_delete_trade_request_success_user_one(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.post(
            f"/requests/delete/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_one],
        )
        assert response.status_code == 200
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one, plant_two, response.json(), []
        )
        trade_request_none: TradeRequest | None = db.exec(
            select(TradeRequest)
            .where(TradeRequest.outgoing_plant_id == trade_request.outgoing_plant_id)
            .where(TradeRequest.incoming_plant_id == trade_request.incoming_plant_id)
        ).first()
        assert trade_request_none is None


def test_delete_trade_request_success_user_two(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        response = client.post(
            f"/requests/delete/{plant_one.id}/{plant_two.id}",
            cookies=[auth_cookie_two],
        )
        assert response.status_code == 200
        assert_if_trade_request_json_and_trade_request_data_match(
            plant_one, plant_two, response.json(), []
        )
        trade_request_none: TradeRequest | None = db.exec(
            select(TradeRequest)
            .where(TradeRequest.outgoing_plant_id == trade_request.outgoing_plant_id)
            .where(TradeRequest.incoming_plant_id == trade_request.incoming_plant_id)
        ).first()
        assert trade_request_none is None


def test_delete_trade_request_not_authorized(client: TestClient, db: Session):
    with create_random_trade_request(client, db) as (
        user_one,
        password_one,
        auth_cookie_one,
        plant_one,
        user_two,
        password_two,
        auth_cookie_two,
        plant_two,
        trade_request,
    ):
        with create_random_user(client, db) as (
            user_three,
            password_three,
            auth_cookie_three,
        ):
            response = client.post(
                f"/requests/delete/{plant_one.id}/{plant_two.id}",
                cookies=[auth_cookie_three],
            )
            assert response.status_code == 404
            assert {
                "detail": "No trade request with the given plant ids exists."
            } == response.json()
            trade_request_in_db = db.get(TradeRequest, (plant_one.id, plant_two.id))
            assert trade_request_in_db is not None

from fastapi.testclient import TestClient
from sqlmodel import Session

from app.tests.utils.plants import create_random_plant
from app.tests.utils.requests import (
    assert_if_trade_request_json_and_trade_request_data_match,
)
from app.tests.utils.users import get_user_token_headers


def test_create_request_new_request(client: TestClient, db: Session) -> None:
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

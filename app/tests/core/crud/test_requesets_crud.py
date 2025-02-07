import uuid

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.core.crud import requests_crud
from app.core.crud.requests_crud import get_all_trade_requests
from app.tests.utils.plants import create_random_plant
from app.tests.utils.users import create_random_user


def test_create_trade_request_from_plant_ids_outgoing_plant_does_not_exist(
    client: TestClient, db: Session
):
    with create_random_plant(client, db) as (_, _, _, plant):
        with pytest.raises(ValueError) as e:
            requests_crud.create_trade_request_from_plant_ids(
                db, uuid.uuid4(), plant.id
            )
        assert e is not None
        assert e.value.args[0] == "One of the plants does not exist."


def test_create_trade_request_from_plant_ids_incoming_plant_does_not_exist(
    client: TestClient, db: Session
):
    with create_random_plant(client, db) as (_, _, _, plant):
        with pytest.raises(ValueError) as e:
            requests_crud.create_trade_request_from_plant_ids(
                db, plant.id, uuid.uuid4()
            )
        assert e is not None
        assert e.value.args[0] == "One of the plants does not exist."


def test_get_all_trade_requests_outgoing_and_incoming_only(
    client: TestClient, db: Session
):
    with create_random_user(client, db) as (user, _, _):
        with pytest.raises(ValueError) as e:
            get_all_trade_requests(
                user, db, 0, 100, outgoing_only=True, incoming_only=True
            )
        assert e is not None
        assert e.value.args[0] == "Cannot filter by both outgoing and incoming only."

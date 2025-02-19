import os

# Set the environment variable before any other imports
os.environ["USE_IMAGE_UPLOAD"] = "False"
os.environ["CLOUDINARY_CLOUD_NAME"] = "Test"
os.environ["CLOUDINARY_API_KEY"] = "Test"
os.environ["CLOUDINARY_API_SECRET"] = "Test"

from collections.abc import Generator

import pytest
from fastapi import Response
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from app.core.db import engine, init_db
from app.main import app
from app.models import User, Plant, TradeRequest
from app.tests.utils.users import get_superuser_authentication_cookie


@pytest.fixture(autouse=True)
def override_set_cookie(monkeypatch):
    original_set_cookie = Response.set_cookie

    def fake_set_cookie(self, key, **kwargs):
        kwargs.pop("domain", None)
        return original_set_cookie(self, key, **kwargs)

    monkeypatch.setattr(Response, "set_cookie", fake_set_cookie)


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture
def superuser_auth_cookie(client: TestClient, override_set_cookie) -> tuple[str, str]:
    return get_superuser_authentication_cookie(client)


@pytest.fixture(scope="session", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        # Delete the user and item column in DB to remove any edits made by tests
        statement = delete(Plant)
        session.execute(statement)
        statement = delete(User)
        session.execute(statement)
        session.commit()
        statement = delete(TradeRequest)
        session.execute(statement)
        session.commit()

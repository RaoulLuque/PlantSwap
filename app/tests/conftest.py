from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete
from pathlib import Path
from dotenv import load_dotenv

from app.core.db import engine, init_db
from app.main import app
from app.models import User, Plant, TradeRequest
from app.tests.utils.users import get_superuser_token_headers


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)


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


@pytest.fixture(scope="session", autouse=True)
def settings_override():
    print("Test")
    # This is run before any imports allowing us to inject
    # dependencies via environment variables into Settings
    # This just affects the variables in this process's environment

    # Find the .env file for the test environment
    test_env = str(Path(__file__).parent / "test.env")
    # Load the environment variables and overwrite any existing ones
    load_dotenv(test_env, override=True)

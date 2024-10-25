from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.tests.utils.utils import get_superuser_token_headers


@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def superuser_token_headers(client: TestClient) -> dict[str, str]:
    return get_superuser_token_headers(client)

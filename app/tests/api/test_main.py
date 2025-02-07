from urllib.request import Request

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app.main import validation_exception_handler


def test_read_main(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200


def test_read_health(client: TestClient):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"message": "Healthy!"}


@pytest.mark.asyncio
async def test_validation_exception_handler():
    request = Request("http://localhost")
    request_validation_error = HTTPException(status_code=422, detail="Validation error")
    response = await validation_exception_handler(request, request_validation_error)
    assert response.status_code == 422
    print(response.body)
    assert (
        response.body
        == b'{"status_code":10422,"message":"422: Validation error","data":null}'
    )

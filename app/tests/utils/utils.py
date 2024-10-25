from fastapi.testclient import TestClient

from app.core.config import settings


def get_superuser_token_headers(client: TestClient) -> dict[str, str]:
    """
    Returns the token headers used for authentication of the default superuser of the app
    :param client: TestClient
    :return: Dictionary with token headers
    """
    login_data = {
        "username": settings.FIRST_SUPERUSER,
        "password": settings.FIRST_SUPERUSER_PASSWORD,
    }
    r = client.post("/login/token", data=login_data)
    tokens = r.json()
    a_token = tokens["access_token"]
    headers = {"Authorization": f"Bearer {a_token}"}
    return headers

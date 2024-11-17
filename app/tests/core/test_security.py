from app.core.security import create_access_token


def test_create_access_token():
    data = {"sub": "", "exp": ""}
    create_access_token(data, None)
    assert data["exp"] == ""

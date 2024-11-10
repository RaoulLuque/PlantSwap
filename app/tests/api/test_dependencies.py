from unittest.mock import patch, PropertyMock

import pytest
from fastapi import HTTPException, status

from app.api.dependencies import User, get_current_active_user, get_current_user
from app.tests.utils.utils import random_email, random_lower_string


@pytest.mark.asyncio
async def test_get_current_user():
    mocked_jwt_payload = {"sub": None}

    with patch("jwt.decode", return_value=mocked_jwt_payload):
        with pytest.raises(HTTPException) as exception_info:
            await get_current_user(None, None)
        response = exception_info.value
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.detail == "Could not validate credentials"
        assert response.headers == {"WWW-Authenticate": "Bearer"}


@pytest.mark.asyncio
async def test_get_current_active_user_inactive_user():
    user = User(email=random_email(), hashed_password=random_lower_string())
    with patch("app.api.dependencies.User.is_active", new_callable=PropertyMock) as a:
        a.return_value = False
        with pytest.raises(HTTPException) as exception_info:
            await get_current_active_user(user)
        response = exception_info.value
        assert response.status_code == 400
        assert response.detail == "Inactive user"


@pytest.mark.asyncio
async def test_get_current_active_user_active_user():
    user = User(email=random_email(), hashed_password=random_lower_string())
    with patch("app.api.dependencies.User.is_active", new_callable=PropertyMock) as a:
        a.return_value = True
        response_user = await get_current_active_user(user)
        assert user == response_user

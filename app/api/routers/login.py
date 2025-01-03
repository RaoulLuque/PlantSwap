from datetime import timedelta
from typing import Annotated

from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep
from app.core.crud.users_crud import authenticate_user
from app.core.security import create_access_token
from app.core.config import settings
from app.models import Token

# Router for api endpoints regarding login functionality
router = APIRouter()


@router.post("/login/token")
async def login_for_access_token(
    session: SessionDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    """
    OAuth2 Login endpoint according to spec.
    :param session: Database session to check if plant exists
    :param form_data: User data to identify
    :return: Token used for further identification
    """
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

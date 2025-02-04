from datetime import timedelta

from fastapi import Depends, APIRouter, HTTPException, Response
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import SessionDep, ACCESS_TOKEN_COOKIE_NAME
from app.core.crud.users_crud import authenticate_user
from app.core.security import create_access_token
from app.core.config import settings

# Router for api endpoints regarding login functionality
router = APIRouter()


@router.post("/login/token")
async def login_for_access_token(
    response: Response,
    session: SessionDep,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    OAuth2 Login endpoint according to spec with cookies.
    :param session: Database session to check if plant exists
    :param form_data: User data to identify
    :param response: Response object to set cookie
    :return: Message indicating successful login. Cookie is sent in response as HTTP only cookie.
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

    # Set the access token in an HttpOnly cookie
    response.set_cookie(
        key=ACCESS_TOKEN_COOKIE_NAME,
        value=access_token,
        httponly=True,
        max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,  # Ensure the cookie is only sent over HTTPS
        samesite="lax",  # Prevent CSRF attacks
    )

    return {"message": "Login successful"}


@router.post("/logout")
async def logout(response: Response):
    """
    Logout endpoint to delete the access token cookie.
    :param response: Response object to delete cookie
    :return: Message indicating successful logout
    """
    response.delete_cookie(ACCESS_TOKEN_COOKIE_NAME)
    return {"message": "Logout successful"}

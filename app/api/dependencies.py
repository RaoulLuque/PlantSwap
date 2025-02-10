from collections.abc import Generator
from typing import Annotated, Optional

import jwt
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.core import security
from app.core.crud.users_crud import get_user_by_email
from app.core.db import engine
from app.models import TokenData, User

# Object used to let FastAPI know that we want to authenticate using OAuth2
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/login/token")


def get_db() -> Generator[Session, None, None]:
    """
    Get database access if a session exists.
    """
    with Session(engine) as session:
        yield session


# Dependency for when database wants to be accessed
SessionDep = Annotated[Session, Depends(get_db)]

# Define the name of the cookie that will store the token
ACCESS_TOKEN_COOKIE_NAME = "access_token"


# Dependency to extract the token from the cookie
async def get_token(request: Request) -> str | None:
    """
    Get the access token from the cookie, or return None if it's missing.
    """
    return request.cookies.get(ACCESS_TOKEN_COOKIE_NAME)


TokenDep = Annotated[str | None, Depends(get_token)]


async def get_current_user(token: TokenDep, session: SessionDep) -> User:
    """
    Returns the current user if the token is valid.
    :param token: Token used for validation
    :param session: Database session
    :return: User data including hashed password
    """
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
        )
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data: TokenData = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    if token_data.email is None:
        raise credentials_exception
    user = get_user_by_email(session, token_data.email)
    if user is None:
        raise credentials_exception
    return user


# Dependency for when current user data is wanted
CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_user_optional(token: TokenDep, session: SessionDep) -> Optional[User]:
    """
    Returns the current user if a token is provided and it is valid, otherwise returns None.
    :param token: Token used for validation
    :param session: Database session
    :return: User data including hashed password
    """
    if token is None:
        return None
    else:
        return await get_current_user(token, session)


# Dependency for when the user may not be logged in or they may be and if so the user data is wanted
OptionalCurrentUserDep = Annotated[Optional[User], Depends(get_current_user_optional)]


async def get_current_active_user(
    current_user: CurrentUserDep,
) -> User:
    """
    Checks if current user exists, is valid and is active.
    :param current_user: Current user as dependency
    :return: Current user including hashed password
    """
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

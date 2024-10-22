from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError
from sqlmodel import Session

from app.core.config import settings
from app.core import security
from app.core.crud import get_user_by_email
from app.core.db import engine
from app.models import TokenData, User

# Object used to let FastAPI know that we want to authenticate using OAuth2
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"/token"
)


def get_db() -> Generator[Session, None, None]:
    """
    Get database access if a session exists.
    """
    with Session(engine) as session:
        yield session


# Dependency for when database wants to be accessed
SessionDep = Annotated[Session, Depends(get_db)]
# Dependency for when user has to identify that their logged in
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(token: TokenDep, session: SessionDep) -> User:
    """
    Returns the current user if the token is valid.
    :param token: Token used for validation
    :param session: Database session
    :return: User data including hashed password
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[security.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except InvalidTokenError:
        raise credentials_exception
    user = get_user_by_email(session, token_data.email)
    if user is None:
        raise credentials_exception
    return user


# Dependency for when current user data is wanted
CurrentUserDep = Annotated[User, Depends(get_current_user)]


async def get_current_active_user(
        current_user: CurrentUserDep,
) -> User:
    """
    Checks if current user exists, is valid and is active.
    :param current_user: Current user as dependency
    :return: Current user including hashed password
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

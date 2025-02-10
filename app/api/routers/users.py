import uuid
from typing import Any, Optional

from fastapi import APIRouter, HTTPException, Depends

from app.core.crud import users_crud
from app.api.dependencies import CurrentUserDep, SessionDep, OptionalCurrentUserDep
from app.models import UserPublic, UserCreate, User, UsersPublic

# Router for api endpoints regarding user functionality
router = APIRouter()


@router.get("/users/me", response_model=UserPublic)
async def read_users_me(
    current_user: CurrentUserDep,
):
    """
    Retrieve own user data.
    :param current_user: The currently logged-in user.
    :return: User data excluding password in shape of a UserPublic instance.
    """
    return current_user


@router.get("/users/{id}", response_model=UserPublic)
def read_user(session: SessionDep, id: uuid.UUID) -> Any:
    """
    Retrieve user with given id.
    :param id: id of user.
    :param session: Current database session.
    :return: User with given id, if exists.
    """
    user = session.get(User, id)
    if user is None:
        raise HTTPException(
            status_code=404,
            detail="No user with the given id exists.",
        )
    return user


@router.get("/users/", response_model=UsersPublic)
def read_users(session: SessionDep, skip: int = 0, limit: int = 100) -> Any:
    """
    Retrieve all existing users.
    :param session: Current database session.
    :param skip: Number of users to skip.
    :param limit: Limit of users to retrieve.
    :return: List of users with number of users as a UsersPublic instance.
    """
    users_public = users_crud.get_all_users(session, skip=skip, limit=limit)
    return users_public


@router.post("/users/signup", response_model=UserPublic)
def create_user(session: SessionDep, optional_current_user: OptionalCurrentUserDep,  user_in: UserCreate):
    """
    Create new user.
    :param session: Current database session.
    :param optional_current_user: None if the user is not logged in or currently logged-in user otherwise
    :param user_in: The user data for the to-be-created user.
    :return: User data excluding password in shape of a UserPublic instance.
    """
    if optional_current_user is None and user_in.is_superuser:
        raise HTTPException(
            status_code=401,
            detail="You are not authorized to create superusers.",
        )
    if optional_current_user is not None:
        if not optional_current_user.is_superuser:
            raise HTTPException(
                status_code=401,
                detail="You are not authorized to create superusers.",
            )
    user = users_crud.get_user_by_email(session, str(user_in.email))
    if user:
        raise HTTPException(
            status_code=400,
            detail="A user with this email already exists.",
        )
    user = users_crud.create_user(session, user_in)
    return user


@router.post("/users/{id}", response_model=UserPublic)
def delete_user(
    session: SessionDep, current_user: CurrentUserDep, id: uuid.UUID
) -> Any:
    """
    Delete user with given id if it matches current_user id or current_user is a superuser.
    :param current_user: Currently logged-in user
    :param id: id of user to be deleted.
    :param session: Current database session.
    :return: User with given id, if deleted successfully.
    """
    if current_user.is_superuser:
        user = session.get(User, id)
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="No user with the given id exists.",
            )
        user = users_crud.delete_user(session, user)
        return user
    else:
        if id != current_user.id:
            raise HTTPException(
                status_code=401,
                detail="You are not allowed to delete other users.",
            )
        user = session.get(User, id)
        user = users_crud.delete_user(session, user)  # type: ignore # (user is not None since exception would have been raised)
        return user

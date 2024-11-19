import uuid
from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app.core.crud import users_crud
from app.api.dependencies import CurrentUserDep, SessionDep
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
    :return: List of users with number of users as a UsersPublic instance
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    count = len(users)
    return UsersPublic(data=users, count=count)


@router.post("/users/signup", response_model=UserPublic)
def create_user(session: SessionDep, user_in: UserCreate):
    """
    Create new user.
    :param session: Current database session.
    :param user_in: The user data for the to-be-created user.
    :return: User data excluding password in shape of a UserPublic instance.
    """
    user = users_crud.get_user_by_email(session, str(user_in.email))
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
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
        session.delete(user)
        session.commit()
        return user
    else:
        if id != current_user.id:
            raise HTTPException(
                status_code=401,
                detail="You are not allowed to delete other users.",
            )
        user = session.get(User, id)
        session.delete(user)
        session.commit()
        return user

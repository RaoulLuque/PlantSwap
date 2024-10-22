from fastapi import APIRouter, HTTPException

from app.api.dependencies import CurrentUserDep, SessionDep
from app.core import crud
from app.models import UserPublic, UserCreate

# Router for api endpoints regarding user functionality
router = APIRouter()


@router.get("/users/me/", response_model=UserPublic)
async def read_users_me(
        current_user: CurrentUserDep,
):
    """
    Retrieve own user data.
    :param current_user: The currently logged-in user.
    :return: User data excluding password in shape of a UserPublic instance.
    """
    return current_user


@router.post(
    "/", response_model=UserPublic
)
def create_user(session: SessionDep, user_in: UserCreate):
    """
    Create new user.
    :param session: The current session of the database.
    :param user_in: The user data for the to-be-created user.
    :return: User data excluding password in shape of a UserPublic instance.
    """
    user = crud.get_user_by_email(session, user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    user = crud.create_user(session, user_in)
    return user

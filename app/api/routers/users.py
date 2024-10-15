from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import CurrentUser
from app.models import User

router = APIRouter()


@router.get("/users/me/", response_model=User)
async def read_users_me(
        current_user: CurrentUser,
):
    return current_user


@router.get("/users/me/items/")
async def read_own_items(
        current_user: CurrentUser,
):
    return [{"item_id": "Foo", "owner": current_user.username}]

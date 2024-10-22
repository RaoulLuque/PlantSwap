from fastapi import APIRouter
from app.api.routers import login, users

# Merge different api router to one for easier inclusion
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])

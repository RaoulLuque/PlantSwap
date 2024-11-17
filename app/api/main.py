from fastapi import APIRouter
from app.api.routers import login, users, plants

# Merge different api router to one for easier inclusion
api_router = APIRouter()
api_router.include_router(login.router, tags=["login"])
api_router.include_router(users.router, tags=["users"])
api_router.include_router(plants.router, tags=["plants"])

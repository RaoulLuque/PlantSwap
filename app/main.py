import logging

from fastapi import FastAPI
from .api.main import api_router
from .core.db import init_db

# Initialize the FastAPI app
app = FastAPI()
# Include the API endpoints specified in /api/routers/...
app.include_router(api_router)
# Initialize the database
init_db()

# Mute module 'bcrypt' has no attribute '__about__' Warning
logging.getLogger('passlib').setLevel(logging.ERROR)


@app.get("/")
async def root():
    return {"message": "Hello World!"}

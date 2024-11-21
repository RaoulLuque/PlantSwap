import logging

from fastapi import FastAPI
from sqlmodel import Session

from .api.main import api_router
from .core.db import init_db, engine

# Initialize the FastAPI app
app = FastAPI(title="PlantSwap")

# Set up logger
logger = logging.getLogger("uvicorn.error")
logger.info(msg="----- ----- APPLICATION STARTING ----- -----")

# Mute module 'bcrypt' has no attribute '__about__' Warning
logging.getLogger("passlib").setLevel(logging.ERROR)

# Include the API endpoints specified in /api/routers/...
app.include_router(api_router)
# Initialize the database
init_db(Session(engine))


@app.get("/")
async def root():
    return {"message": "Hello World!"}

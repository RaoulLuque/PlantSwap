import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
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

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the API endpoints specified in /api/routers/...
app.include_router(api_router)
# Initialize the database
init_db(Session(engine))


@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"message": "Healthy!"}

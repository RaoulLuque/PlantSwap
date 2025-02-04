import logging

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session

from .api.main import api_router
from .core.config import settings
from .core.db import init_db, engine
from .core.images import set_cloudinary_config

# Initialize the FastAPI app
app = FastAPI(title="PlantSwap")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    exc_str = f"{exc}".replace("\n", " ").replace("   ", " ")
    logging.error(f"{request}: {exc_str}")
    content = {"status_code": 10422, "message": exc_str, "data": None}
    return JSONResponse(
        content=content, status_code=status.HTTP_422_UNPROCESSABLE_ENTITY
    )


# Set up logger
logger = logging.getLogger("uvicorn.error")
logger.info(msg="----- ----- APPLICATION STARTING ----- -----")

# Mute module 'bcrypt' has no attribute '__about__' Warning
logging.getLogger("passlib").setLevel(logging.ERROR)

# Setup CORS for frontend
origins: list[str] = [settings.FRONTEND_URL]

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
# Set cloudinary config
set_cloudinary_config()


@app.get("/", response_class=RedirectResponse)
async def root():
    return RedirectResponse(url="/docs")


@app.get("/health")
async def health_check():
    return {"message": "Healthy!"}

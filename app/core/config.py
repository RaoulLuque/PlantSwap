import secrets
from pydantic import PostgresDsn, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic_core import MultiHostUrl


class Settings(BaseSettings):
    """
    Settings class containing .env file settings
    """

    model_config = SettingsConfigDict(
        # Use top level .env file (one level above ./app/)
        env_file="../.env",
        env_ignore_empty=True,
        extra="ignore",
    )
    # SECRETS
    SECRET_KEY: str = secrets.token_urlsafe(32)
    FIRST_SUPERUSER: str = "admin@example.com"
    FIRST_SUPERUSER_PASSWORD: str = "password"
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8

    # POSTGRES
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "password"
    POSTGRES_DB: str = "postgres"

    @computed_field  # type: ignore[prop-decorator]
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        return MultiHostUrl.build(
            scheme="postgresql+psycopg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )


settings = Settings()  # type: ignore

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": True,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"},
        "custom_formatter": {
            "format": "%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "stream_handler": {
            "formatter": "custom_formatter",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",  # Default is stderr
        },
        "file_handler": {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "custom_formatter",
            "filename": "app.log",
            "maxBytes": 1024 * 1024 * 1,  # = 1MB
            "backupCount": 3,
        },
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["default", "file_handler"],
            "level": "TRACE",
            "propagate": False,
        },
        "uvicorn.access": {
            "handlers": ["stream_handler", "file_handler"],
            "level": "TRACE",
            "propagate": False,
        },
        "uvicorn.error": {
            "handlers": ["stream_handler", "file_handler"],
            "level": "TRACE",
            "propagate": False,
        },
        "uvicorn.asgi": {
            "handlers": ["stream_handler", "file_handler"],
            "level": "TRACE",
            "propagate": False,
        },
    },
}

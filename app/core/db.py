from sqlmodel import Session, create_engine, select

from app.core.crud import users_crud
from app.core.config import settings

# Models need to be imported before database is initialized
from app import models  # noqa: F401

# Engine used to communicate with database
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session):
    """
    Initialize database and create admin user in database using credentials from .env file.
    """
    from sqlmodel import SQLModel

    SQLModel.metadata.create_all(engine)
    user = session.exec(
        select(models.User).where(models.User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = models.UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        users_crud.create_user(session=session, user_create=user_in)

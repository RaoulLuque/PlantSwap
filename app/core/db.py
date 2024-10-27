from sqlmodel import Session, create_engine, select, SQLModel
from app.core import crud
from app.core.config import settings
from app.models import User, UserCreate

# Engine used to communicate with database
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


def init_db(session: Session):
    """
    Initialize database and create admin user in database using credentials from .env file.
    """
    SQLModel.metadata.create_all(engine)
    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()
    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

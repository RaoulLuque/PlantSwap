from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import User, UserCreate, PlantCreate, Plant


def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create user entry in database.
    :param session: Database session
    :param user_create: User data for the user to be created
    :return:
    """
    db_obj = User.model_validate(
        user_create, update={"hashed_password": get_password_hash(user_create.password)}
    )
    session.add(db_obj)
    session.commit()
    session.refresh(db_obj)
    return db_obj


def get_user_by_email(session: Session, email: str) -> User | None:
    """
    Return instance of User with user data or None if user doesn't exist.
    :param session: Database session
    :param email: Email of user
    :return: User data including hashed password
    """
    statement = select(User).where(User.email == email)
    session_user = session.exec(statement).first()
    return session_user


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """
    Check user email and password against database.
    :param session: Database session
    :param email: Email of user
    :param password: Hashed password of user
    :return: User if credentials match user in database and None otherwise
    """
    db_user = get_user_by_email(session=session, email=email)
    if not db_user:
        return None
    if not verify_password(password, db_user.hashed_password):
        return None
    return db_user


def delete_user(session: Session, user: User) -> User:
    """
    Delete user from database.
    :param session: Database session
    :param user: User to be deleted
    """
    session.delete(user)
    session.commit()
    return user


def create_plant(session: Session, user: User, plant_in: PlantCreate) -> Plant:
    plant: Plant = Plant.model_validate(plant_in, update={"owner_id": user.id})
    session.add(plant)
    session.commit()
    session.refresh(plant)
    return plant

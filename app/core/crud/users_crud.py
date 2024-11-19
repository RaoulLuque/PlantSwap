from sqlmodel import Session, select

from app.core.security import get_password_hash, verify_password
from app.models import UserCreate, User, UsersPublic


def create_user(session: Session, user_create: UserCreate) -> User:
    """
    Create user entry in database.
    :param session: Database session
    :param user_create: User data for the user to be created
    :return: user that was created including hashed password
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
    # noinspection Pydantic
    statement = select(User).where(User.email == email)  # type: ignore
    session_user = session.exec(statement).first()  # type: ignore
    return session_user


def get_all_users(session: Session, skip: int = 0, limit: int = 100) -> UsersPublic:
    """
    Retrieve all existing users up to the given limit with the given offset.
    :param session: Current database session
    :param skip: Number of users to skip
    :param limit: Limit of users to retrieve
    :return: List of users with number of users as a UsersPublic instance
    """
    statement = select(User).offset(skip).limit(limit)
    users = session.exec(statement).all()
    count = len(users)
    return UsersPublic(data=users, count=count)  # type: ignore


def authenticate_user(session: Session, email: str, password: str) -> User | None:
    """
    Check user email and password against database.
    :param session: Database session
    :param email: Email of user
    :param password: Hashed password of user
    :return: user if credentials match user in database and None otherwise
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

from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from .config import settings

# Algorithm used for password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Algorithm used for JWT encoding
ALGORITHM = "HS256"


def verify_password(plain_password, hashed_password):
    """
    Check if plain and hashed password match.
    :param plain_password: Password in plaintext
    :param hashed_password: Hashed password
    :return: True if plain password matches hashed password
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """
    Hashes the password
    :param password: Password to be hashed
    :return: Hashed password as str
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """
    Create access token using the 'ALGORITHM' algorithm and the 'SECRET_KEY' specified in .env
    :param data: Data to be encoded in JWT token
    :param expires_delta: Duration when the token will expire
    :return: The encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

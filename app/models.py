import uuid

from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field


# Shared user properties in Database
class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True, max_length=255)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = Field(default=None, max_length=255)


# User properties to return via API, id is always required
class UserPublic(UserBase):
    id: uuid.UUID


# User properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# User database model, database table inferred from class name
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str


# Token data class for JWT Encoding
class TokenData(BaseModel):
    email: str | None = None


# Session token used with OAuth2
class Token(BaseModel):
    access_token: str
    token_type: str

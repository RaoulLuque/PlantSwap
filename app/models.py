import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlmodel import SQLModel, Field, Relationship


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


# User database model
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    plants: list["Plant"] = Relationship(back_populates="owner", cascade_delete=True)


# Shared properties of plant ad in database
class PlantBase(SQLModel):
    name: str = Field(min_length=1, max_length=255)
    description: str | None = Field(default=None, max_length=255)


# Properties to receive on plant creation
class PlantCreate(PlantBase):
    pass


# Plant database model
class Plant(PlantBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(max_length=255)
    creation_date: datetime = Field(default=datetime.now())
    owner_id: uuid.UUID = Field(
        foreign_key="user.id", nullable=False, ondelete="CASCADE"
    )
    owner: User = Relationship(back_populates="plants")


# Plant properties to return via API, id is always required
class PlantPublic(PlantBase):
    id: uuid.UUID
    owner_id: uuid.UUID
    # name: str
    # description: str | None


class PlantsPublic(SQLModel):
    data: list[PlantPublic]
    count: int


# Token data class for JWT Encoding
class TokenData(BaseModel):
    email: str | None = None


# Session token used with OAuth2
class Token(BaseModel):
    access_token: str
    token_type: str

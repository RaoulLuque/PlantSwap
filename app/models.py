import uuid
from datetime import datetime

from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import RelationshipProperty
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


# Class to return multiple UserPublic instances at the same time
class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


# User properties to receive via API on creation
class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=40)


# User database model
class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    plants: list["Plant"] = Relationship(back_populates="owner", cascade_delete=True)
    incoming_requests: list["TradeRequest"] = Relationship(
        sa_relationship=RelationshipProperty(
            "TradeRequest",
            back_populates="incoming_user",
            foreign_keys="[TradeRequest.incoming_user_id]",
        ),
        cascade_delete=True,
    )
    outgoing_requests: list["TradeRequest"] = Relationship(
        sa_relationship=RelationshipProperty(
            "TradeRequest",
            back_populates="outgoing_user",
            foreign_keys="[TradeRequest.outgoing_user_id]",
        ),
        cascade_delete=True,
    )


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
    # This attribute is of no real use, it simply takes care of deleting the corresponding
    # trade requests of a plant when the respective plant is deleted
    trade_requests: list["TradeRequest"] = Relationship(
        sa_relationship=RelationshipProperty("TradeRequest", back_populates="plant"),
        cascade_delete=True,
    )


# Plant properties to return via API, id is always required
class PlantPublic(PlantBase):
    id: uuid.UUID
    owner_id: uuid.UUID


# Class to return multiple PlantPublic instances at the same time
class PlantsPublic(SQLModel):
    data: list[PlantPublic]
    count: int


# Link model (table) for many-to-many relationship of incoming and outgoing trade requests
class TradeRequest(SQLModel, table=True):
    outgoing_user_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        foreign_key="user.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    outgoing_user: User = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="outgoing_requests",
            foreign_keys="[TradeRequest.outgoing_user_id]",
        )
    )
    incoming_user_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        foreign_key="user.id",
        primary_key=True,
        ondelete="CASCADE",
    )
    incoming_user: User = Relationship(
        sa_relationship=RelationshipProperty(
            "User",
            back_populates="incoming_requests",
            foreign_keys="[TradeRequest.incoming_user_id]",
        )
    )
    plant_id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        foreign_key="plant.id",
        ondelete="CASCADE",
    )
    plant: Plant = Relationship(back_populates="trade_requests")
    message: str | None = Field(default=None, max_length=255)


# Token data class for JWT Encoding
class TokenData(BaseModel):
    email: str | None = None


# Session token used with OAuth2
class Token(BaseModel):
    access_token: str
    token_type: str

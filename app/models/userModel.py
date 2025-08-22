from __future__ import annotations
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime
from enum import Enum


class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, unique=True)
    full_name: str
    email_address: str = Field(index=True, unique=True)
    hashed_password: str
    channel: str = Field(default="web")
    role: UserRole = Field(default=UserRole.USER)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_active: bool = Field(default=True)
    last_login: Optional[datetime] = None


    # COMENTAR TEMPORALMENTE LAS RELACIONES
    # chats: List["Chat"] = Relationship(back_populates="user", sa_relationship_kwargs={'lazy': 'selectin'})
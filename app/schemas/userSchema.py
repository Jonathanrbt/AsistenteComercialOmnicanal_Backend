from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    USER = "user"
    ADMIN = "admin"

class UserCreate(SQLModel):
    full_name: str
    email_address: str
    password: str
    channel: str = "web"
    role: UserRole = UserRole.USER

class UserLogin(SQLModel):
    email_address: str
    password: str

class UserPublic(SQLModel):
    id: int
    user_id: str
    full_name: str
    email_address: str
    channel: str
    role: UserRole
    created_at: datetime
    last_login: Optional[datetime] = None
    is_active: bool

class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(SQLModel):
    email_address: Optional[str] = None
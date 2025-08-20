from __future__ import annotations
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .userModel import User
    from .messageModel import Message

class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    last_message: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    total_messages: int = 0

    user: "User" = Relationship(back_populates="chats")
    messages: List["Message"] = Relationship(back_populates="chat")
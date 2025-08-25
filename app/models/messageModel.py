from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

if TYPE_CHECKING:
    from .chatModel import Chat

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chats.id")
    role: str  
    text: str
    ts: datetime = Field(default_factory=datetime.utcnow)

    chat: "Chat" = Relationship(back_populates="messages")
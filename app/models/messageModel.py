from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    chat_id: int = Field(foreign_key="chats.id")
    role: str  
    text: str
    ts: datetime = Field(default_factory=datetime.utcnow)

    # COMENTAR TEMPORALMENTE LAS RELACIONES
    # chat: "Chat" = Relationship(back_populates="messages", sa_relationship_kwargs={'lazy': 'joined'})
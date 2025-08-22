from __future__ import annotations
from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field

class Chat(SQLModel, table=True):
    __tablename__ = "chats"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    last_message: Optional[str] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    total_messages: int = 0

    # COMENTAR TEMPORALMENTE LAS RELACIONES
    # user: "User" = Relationship(back_populates="chats", sa_relationship_kwargs={'lazy': 'joined'})
    # messages: List["Message"] = Relationship(back_populates="chat", sa_relationship_kwargs={'lazy': 'selectin'})
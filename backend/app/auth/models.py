from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    Text,
    TIMESTAMP
)
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.postgree import Base


# USERS
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)
    auth_provider = Column(String, nullable=False, default="password")
    is_admin = Column(Boolean, default=False)

    sessions = relationship(
        "ChatSession",
        back_populates="user",
        cascade="all, delete"
    )


# CHAT SESSIONS
class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    title = Column(String, default="New Chat")
    created_at = Column(TIMESTAMP, default=datetime.utcnow)


    active_context = Column(Text, nullable=True)
    context_type = Column(String, nullable=True)  

    user = relationship("User", back_populates="sessions")
    messages = relationship(
        "ChatMessage",
        back_populates="session",
        cascade="all, delete"
    )

#CHAT MESSAGES
class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(
        Integer,
        ForeignKey("chat_sessions.id", ondelete="CASCADE"),
        index=True
    )

    role = Column(String, nullable=False)        
    modality = Column(String, nullable=False)   
    content = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

    session = relationship("ChatSession", back_populates="messages")


#MEMORY METADATA
class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    modality = Column(String, nullable=False)
    source = Column(String)        
    preview = Column(String(500))
    created_at = Column(TIMESTAMP, default=datetime.utcnow)

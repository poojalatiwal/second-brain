from sqlalchemy import Column, Integer, String, Boolean
from app.db.postgree import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=True)   # ⬅️ allow NULL for OAuth
    auth_provider = Column(String, nullable=False, default="password")  # ⬅️ NEW
    is_admin = Column(Boolean, default=False)

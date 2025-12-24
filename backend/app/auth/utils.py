from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from app.config import settings
from app.db.postgree import get_db
from .models import User

pwd_hasher = PasswordHasher()

# ------------ PASSWORDS ------------
def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_hasher.verify(hashed, password)
    except:
        return False

# ------------ JWT CONFIG ------------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=30)
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

def create_refresh_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

def decode_token(token: str):
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")

# ------------ CURRENT USER ------------
def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    data = decode_token(token)
    user_id = data.get("sub")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user

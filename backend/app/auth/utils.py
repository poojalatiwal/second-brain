from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer
from argon2 import PasswordHasher
from sqlalchemy.orm import Session

from app.config import settings
from app.db.postgree import get_db
from .models import User


# -------------------------------------
# PASSWORD HASHING (Argon2)
# -------------------------------------
pwd_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_hasher.verify(hashed, password)
    except Exception:
        return False


# -------------------------------------
# JWT SECURITY  (REPLACED OAuth2 → HTTPBearer)
# -------------------------------------
auth_scheme = HTTPBearer()  # ⭐ FIXED


def create_access_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(minutes=settings.JWT_ACCESS_EXPIRE_MINUTES)
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)


def create_refresh_token(user_id: int):
    payload = {
        "sub": str(user_id),
        "exp": datetime.utcnow() + timedelta(days=settings.JWT_REFRESH_EXPIRE_DAYS)
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)


def decode_token(token: str):
    try:
        return jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        raise HTTPException(401, "Invalid or expired token")


# -------------------------------------
# GET CURRENT USER (TOKEN REQUIRED)
# -------------------------------------
def get_current_user(
    token = Depends(auth_scheme),
    db: Session = Depends(get_db)
):
    token = token.credentials  # ⭐ IMPORTANT FIX

    data = decode_token(token)
    user_id = data.get("sub")

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(401, "User not found")

    return user


# -------------------------------------
# ADMIN CHECK
# -------------------------------------
def require_admin(user: User):
    if not user.is_admin:
        raise HTTPException(403, "Admin access required")

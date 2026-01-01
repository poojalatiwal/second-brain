from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from sqlalchemy.orm import Session

from app.config import settings
from app.db.postgree import get_db
from .models import User

# =====================================
# PASSWORD HASHING (ARGON2)
# =====================================
pwd_hasher = PasswordHasher()

def hash_password(password: str) -> str:
    return pwd_hasher.hash(password)

def verify_password(password: str, hashed: str) -> bool:
    try:
        return pwd_hasher.verify(hashed, password)
    except VerifyMismatchError:
        return False

# =====================================
# JWT CONFIG
# =====================================
security = HTTPBearer()

def create_access_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_EXPIRE_MINUTES
        ),
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

def create_refresh_token(user_id: int) -> str:
    payload = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": datetime.utcnow() + timedelta(
            days=settings.JWT_REFRESH_EXPIRE_DAYS
        ),
    }
    return jwt.encode(payload, settings.JWT_SECRET, settings.JWT_ALGORITHM)

def decode_token(token: str) -> dict:
    try:
        return jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired. Please login again.",
        )

# =====================================
# GET CURRENT USER
# =====================================
def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db),
) -> User:
    token = credentials.credentials
    payload = decode_token(token)

    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type",
        )

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )

    user = db.query(User).filter(User.id == int(user_id)).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
        )

    return user

# =====================================
# ADMIN GUARD
# =====================================
def require_admin(current_user: User = Depends(get_current_user)) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user

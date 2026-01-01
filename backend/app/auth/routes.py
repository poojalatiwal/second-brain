from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.postgree import get_db
from .models import User
from .schema import SignupRequest, LoginRequest, UserResponse
from .utils import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token
)

router = APIRouter(prefix="/auth")

# -------------------- SIGNUP --------------------
@router.post("/signup", response_model=UserResponse)
def signup(data: SignupRequest, db: Session = Depends(get_db)):

    # email already exists
    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    user = User(
        username=data.username,
        email=data.email,
        password_hash=hash_password(data.password)
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id)
    )

# -------------------- LOGIN --------------------
@router.post("/login", response_model=UserResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return UserResponse(
        id=user.id,
        username=user.username,
        email=user.email,
        is_admin=user.is_admin,
        access_token=create_access_token(user.id),
        refresh_token=create_refresh_token(user.id)
    )

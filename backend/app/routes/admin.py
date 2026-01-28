from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.postgree import get_db
from app.auth.models import User
from app.auth.utils import get_current_user, require_admin
from app.db.qdrant_db import qdrant as qdrant_client

router = APIRouter(prefix="/admin", tags=["Admin"])



#  GET ALL USERS

@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    curr_user: dict = Depends(get_current_user)
):
    require_admin(curr_user)

    users = db.query(User).all()

    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin,
        }
        for u in users
    ]



# 2️ SYSTEM LOGS 

@router.get("/logs")
def get_logs(curr_user: dict = Depends(get_current_user)):
    require_admin(curr_user)

    return [
        {"event": "User signup", "detail": "test@example.com"},
        {"event": "Memory ingested", "source": "PDF"},
        {"event": "Chat request", "mode": "memory"},
    ]



#  SYSTEM STATS

@router.get("/stats")
def get_admin_stats(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    require_admin(current_user)

    total_users = db.query(User).count()
    admin_users = db.query(User).filter(User.is_admin == True).count()

    try:
        collection = qdrant_client.get_collection("memory")
        total_vectors = collection.points_count or 0
    except Exception:
        total_vectors = 0

    return {
        "total_users": total_users,
        "admin_users": admin_users,
        "total_vectors": total_vectors,
        "estimated_docs": total_vectors // 5  
    }

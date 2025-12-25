from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.postgree import get_db
from app.auth.models import User
from app.auth.utils import get_current_user, require_admin

# ✅ IMPORTANT FIX:
# We import "qdrant" but rename it locally as qdrant_client
from app.db.qdrant_db import qdrant as qdrant_client

router = APIRouter(prefix="/admin", tags=["Admin"])


# ---------------------------
# 1) GET ALL USERS
# ---------------------------
@router.get("/users")
def get_users(
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)
):
    require_admin(curr_user)

    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,
            "is_admin": u.is_admin
        }
        for u in users
    ]


# ---------------------------
# 2) SYSTEM LOGS (Activity)
# ---------------------------
@router.get("/logs")
def get_logs(curr_user: User = Depends(get_current_user)):
    require_admin(curr_user)

    # Placeholder logs (replace with DB logs later)
    return [
        {"event": "User signup", "user": "test@example.com"},
        {"event": "Knowledge ingested", "source": "PDF"},
        {"event": "Chat request", "model": "GPT-4"},
    ]


# ---------------------------
# 3) SYSTEM STATISTICS
# ---------------------------
@router.get("/stats")
def get_system_stats(
    db: Session = Depends(get_db),
    curr_user: User = Depends(get_current_user)
):
    require_admin(curr_user)

    total_users = db.query(User).count()

    # Retrieve vector statistics from Qdrant
    try:
        stats = qdrant_client.get_collection("memory")
        total_vectors = stats.points_count
    except Exception:
        total_vectors = 0

    return {
        "total_users": total_users,
        "total_vectors": total_vectors,
        "total_docs": total_vectors // 5  # adjust based on actual chunking strategy
    }

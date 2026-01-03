from fastapi import APIRouter, Depends, HTTPException
from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
from app.auth.utils import get_current_user
from app.auth.models import User
import uuid

router = APIRouter()

@router.post("/text")
async def ingest_text(
    text: str,
    current_user: dict = Depends(get_current_user) # ✅ AUTH REQUIRED
):
    if not text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")

    chunks = chunk_text(text)

    for chunk in chunks:
        emb = get_embedding(chunk)

        insert_vector(
            id=str(uuid.uuid4()),
            embedding=emb,
            payload={
                "text": chunk,
                "modality": "text",
                "user_id": current_user["id"]   # ✅ CRITICAL FIX
            }
        )

    return {
        "status": "ok",
        "chunks": len(chunks),
        "user_id":current_user["id"]
    }

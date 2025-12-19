from fastapi import APIRouter
from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
import uuid

router = APIRouter()

@router.post("/text")
async def ingest_text(text: str):
    chunks = chunk_text(text)

    for chunk in chunks:
        emb = get_embedding(chunk)
        insert_vector(
            id=str(uuid.uuid4()),
            embedding=emb,
            payload={"text": chunk, "modality": "text"}
        )

    return {"status": "ok", "chunks": len(chunks)}

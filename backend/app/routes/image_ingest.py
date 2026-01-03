from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import fitz  # PyMuPDF
import uuid
import tempfile

from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
from app.auth.utils import get_current_user
from app.auth.models import User

router = APIRouter()

@router.post("/image")
async def ingest_image(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user)  # ✅ AUTH
):
    if not file.filename:
        raise HTTPException(400, "No image file provided")

    img_bytes = await file.read()

    # Save temporarily
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(img_bytes)
        tmp_path = tmp.name

    # Load image into PDF page for OCR
    doc = fitz.open()
    page = doc.new_page()
    page.insert_image(page.rect, filename=tmp_path)

    text = page.get_text("text")

    if not text.strip():
        raise HTTPException(400, "Could not extract text from image")

    chunks = chunk_text(text)
    stored_ids = []

    for chunk in chunks:
        emb = get_embedding(chunk)
        uid = str(uuid.uuid4())

        insert_vector(
            id=uid,
            embedding=emb,
            payload={
                "text": chunk,
                "modality": "image",
                "filename": file.filename,
                "user_id": current_user["id"]    # ✅ CRITICAL FIX
            }
        )

        stored_ids.append(uid)

    return {
        "status": "stored",
        "user_id": current_user["id"] ,
        "filename": file.filename,
        "chunks_stored": len(stored_ids),
        "preview": text[:200] + "..."
    }

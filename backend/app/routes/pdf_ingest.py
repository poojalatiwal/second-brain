from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from pypdf import PdfReader
from io import BytesIO
import uuid

from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
from app.auth.utils import get_current_user
from app.auth.models import User

router = APIRouter()

@router.post("/pdf")
async def ingest_pdf(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)   # ✅ AUTH
):
    if not file.filename:
        raise HTTPException(400, "No PDF file provided")

    # 1️⃣ Read PDF bytes
    pdf_bytes = await file.read()

    # 2️⃣ Load PDF
    reader = PdfReader(BytesIO(pdf_bytes))

    # 3️⃣ Extract text
    full_text = ""
    for page in reader.pages:
        text = page.extract_text()
        if text:
            full_text += text + "\n"

    if not full_text.strip():
        raise HTTPException(400, "Could not extract text from PDF")

    # 4️⃣ Chunk text
    chunks = chunk_text(full_text)

    stored_ids = []

    # 5️⃣ Embed + store WITH user_id
    for chunk in chunks:
        emb = get_embedding(chunk)
        uid = str(uuid.uuid4())

        insert_vector(
            id=uid,
            embedding=emb,
            payload={
                "text": chunk,
                "modality": "pdf",
                "filename": file.filename,
                "user_id": current_user.id   # ✅ CRITICAL FIX
            }
        )

        stored_ids.append(uid)

    return {
        "status": "stored",
        "user_id": current_user.id,
        "filename": file.filename,
        "pages": len(reader.pages),
        "chunks_stored": len(stored_ids)
    }

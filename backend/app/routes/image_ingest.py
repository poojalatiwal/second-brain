from fastapi import APIRouter, UploadFile, File
import fitz  # PyMuPDF OCR
import uuid
import tempfile
from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector

router = APIRouter()

@router.post("/image")
async def ingest_image(file: UploadFile = File(...)):
    img_bytes = await file.read()

    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(img_bytes)
        tmp_path = tmp.name

    doc = fitz.open()
    page = doc.new_page()
    page.insert_image(page.rect, filename=tmp_path)

    text = page.get_text("text")

    if not text.strip():
        return {"error": "Could not extract text from image"}

    chunks = chunk_text(text)

    stored = []

    for chunk in chunks:
        emb = get_embedding(chunk)
        uid = str(uuid.uuid4())

        insert_vector(
            id=uid,
            embedding=emb,
            payload={
                "text": chunk,
                "modality": "image",
                "filename": file.filename
            }
        )
        stored.append(uid)

    return {
        "extracted_text": text[:200] + "...",
        "chunks_stored": len(stored),
        "ids": stored
    }

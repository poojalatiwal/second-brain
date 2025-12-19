from fastapi import APIRouter, UploadFile, File
from pypdf import PdfReader
from io import BytesIO
from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
import uuid

router = APIRouter()

@router.post("/pdf")
async def ingest_pdf(file: UploadFile = File(...)):
    # 1. Read PDF file bytes
    pdf_bytes = await file.read()

    # 2. Wrap bytes so PdfReader can `.seek()`
    reader = PdfReader(BytesIO(pdf_bytes))

    # 3. Extract text page-by-page
    full_text = ""
    for page in reader.pages:
        full_text += page.extract_text() + "\n"

    # 4. Chunk text
    chunks = chunk_text(full_text)

    # 5. Embed + save to Qdrant
    for chunk in chunks:
        emb = get_embedding(chunk)
        insert_vector(
            id=str(uuid.uuid4()),
            embedding=emb,
            payload={
                "text": chunk,
                "modality": "pdf"
            }
        )

    return {
        "status": "ok",
        "pages": len(reader.pages),
        "chunks": len(chunks)
    }

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from groq import Groq
import uuid

from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
from app.auth.utils import get_current_user
from app.auth.models import User
from app.config import settings

# ✅ THIS WAS MISSING
router = APIRouter()

client = Groq(api_key=settings.GROQ_API_KEY)


@router.post("/audio")
async def ingest_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    if not file or not file.filename:
        raise HTTPException(400, "No audio file provided")

    audio_bytes = await file.read()

    # 1️⃣ Transcribe audio
    transcript = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(file.filename, audio_bytes),
    )

    text = transcript.text.strip()
    if not text:
        raise HTTPException(400, "Audio transcription failed")

    # 2️⃣ CREATE SUMMARY (IMPORTANT)
    summary_prompt = f"""
Summarize the following audio transcription in 3–5 bullet points.

Transcript:
{text}
"""

    summary_resp = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": summary_prompt}]
    )

    summary = summary_resp.choices[0].message.content.strip()

    # 3️⃣ Store SUMMARY
    insert_vector(
        id=str(uuid.uuid4()),
        embedding=get_embedding(summary),
        payload={
            "text": summary,
            "modality": "audio_summary",
            "user_id": current_user.id,
            "filename": file.filename
        }
    )

    # 4️⃣ Store FULL TRANSCRIPT (chunked)
    for chunk in chunk_text(text):
        insert_vector(
            id=str(uuid.uuid4()),
            embedding=get_embedding(chunk),
            payload={
                "text": chunk,
                "modality": "audio",
                "user_id": current_user.id,
                "filename": file.filename
            }
        )

    return {
        "status": "stored",
        "user_id": current_user.id,
        "summary": summary
    }

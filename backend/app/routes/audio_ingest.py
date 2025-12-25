from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from groq import Groq
from app.services.embedder import get_embedding
from app.db.qdrant_db import insert_vector
from app.auth.utils import get_current_user
from app.auth.models import User
from app.config import settings
import uuid

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)

@router.post("/audio")
async def ingest_audio(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)   # ✅ AUTH
):
    if not file.filename:
        raise HTTPException(400, "No audio file provided")

    # Read audio file bytes
    audio_bytes = await file.read()

    # Transcribe using Groq Whisper
    transcript = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(file.filename, audio_bytes),
    )

    text = transcript.text.strip()
    if not text:
        raise HTTPException(400, "Audio transcription failed")

    print("🎧 TRANSCRIBED TEXT:", text)

    # Embed transcription
    emb = get_embedding(text)

    # Store in Qdrant WITH user_id
    insert_vector(
        id=str(uuid.uuid4()),
        embedding=emb,
        payload={
            "text": text,
            "modality": "audio",
            "user_id": current_user.id     # ✅ CRITICAL FIX
        }
    )

    return {
        "status": "stored",
        "user_id": current_user.id,
        "transcription": text
    }

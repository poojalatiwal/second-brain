# app/routes/audio_ingest.py

from fastapi import APIRouter, UploadFile, File
from groq import Groq
from app.services.embedder import get_embedding
from app.db.qdrant_db import insert_vector
import uuid
from app.config import settings

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)

@router.post("/audio")
async def ingest_audio(file: UploadFile = File(...)):
    # Read audio file bytes
    audio_bytes = await file.read()

    # Use Groq Whisper for transcription
    transcript = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=("audio.wav", audio_bytes),  # name + bytes
    )

    text = transcript.text
    print("TRANSCRIBED TEXT:", text)

    # Chunking not needed for short audios. If needed, add.
    emb = get_embedding(text)

    insert_vector(
        id=str(uuid.uuid4()),
        embedding=emb,
        payload={"text": text, "modality": "audio"}
    )

    return {
        "status": "stored",
        "transcription": text
    }

from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from groq import Groq

from app.config import settings
from app.services.embedder import get_embedding
from app.db.qdrant_db import search_vectors
from app.auth.utils import get_current_user
from app.auth.models import User

router = APIRouter()
client = Groq(api_key=settings.GROQ_API_KEY)


@router.post("/audio")
async def chat_with_audio(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user) 
):
    """
    Conversational audio → text → memory-aware response
    """

    if not file.filename:
        raise HTTPException(400, "No audio file provided")


    audio_bytes = await file.read()


    transcript = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(file.filename, audio_bytes),
    )

    user_text = transcript.text.strip()
    if not user_text:
        raise HTTPException(400, "Could not transcribe audio")


    emb = get_embedding(user_text)

    results = search_vectors(
        vector=emb,
        user_id=current_user["id"] ,    
        top_k=5
    )


    context_list = [
        point.payload.get("text", "")
        for point in results
        if point.payload is not None
    ]

    context = "\n".join(context_list) if context_list else ""


    prompt = f"""
You are the user's AI assistant.

Use the following memory ONLY if relevant.

Memory:
{context if context else "No memory available."}

User (from audio): {user_text}

Respond naturally.
"""


    reply = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = reply.choices[0].message.content

    return {
        "user_id": current_user["id"] ,
        "user_said": user_text,
        "assistant_reply": answer,
        "memory_used": context if context else "No relevant memory found",
        "matches_found": len(context_list)
    }

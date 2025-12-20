# app/routes/audio_chat.py

from fastapi import APIRouter, UploadFile, File
from groq import Groq
from app.config import settings
from app.services.embedder import get_embedding
from app.db.qdrant_db import search_vectors

router = APIRouter()

# Initialize Groq Client
client = Groq(api_key=settings.GROQ_API_KEY)

@router.post("/audio")
async def chat_with_audio(file: UploadFile = File(...)):
    """
    Conversational audio → text → memory-aware response
    """

    # Step 1: Read uploaded audio bytes
    audio_bytes = await file.read()

    # Step 2: Groq Whisper transcription
    transcript = client.audio.transcriptions.create(
        model="whisper-large-v3-turbo",
        file=(file.filename, audio_bytes),   # <- automatically handles format
    )
    user_text = transcript.text.strip()

    # Step 3: Search Memory
    emb = get_embedding(user_text)
    results = search_vectors(emb, top_k=5)

    # Extract memory context
    context = "\n".join([
        point.payload.get("text", "")
        for point in results
        if point.payload is not None
    ])

    # Step 4: Build final LLM prompt
    prompt = f"""
You are the user's AI assistant.

Use the following stored memory ONLY if relevant:

Memory:
{context}

User (from audio): {user_text}

Respond naturally. 
If memory has no answer, reply normally as a general AI assistant.
"""

    # Step 5: Ask Groq LLM
    reply = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = reply.choices[0].message.content

    # Step 6: Return combined details
    return {
        "user_said": user_text,
        "assistant_reply": answer,
        "memory_used": context if context else "No relevant memory found"
    }

import uuid
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from app.services.embedder import get_embedding
from app.db.qdrant_db import search_vectors, insert_vector
from app.auth.utils import get_current_user
from app.config import settings
from groq import Groq

router = APIRouter(prefix="/memory", tags=["Memory"])
client = Groq(api_key=settings.GROQ_API_KEY)


class MemoryQuestion(BaseModel):
    question: str


@router.post("/")
async def ask_from_memory(
    data: MemoryQuestion,
    current_user=Depends(get_current_user)
):
    question = data.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    embedding = get_embedding(question)

    results = search_vectors(
        vector=embedding,
        user_id=current_user.id,
        top_k=5
    )

    context_chunks = [
        p.payload["text"]
        for p in results
        if p.payload and "text" in p.payload
    ]

    context = "\n\n".join(context_chunks) if context_chunks else "No relevant memory found."

    prompt = f"""
You are a memory-based assistant.

Use ONLY the memory below to answer.

Memory:
{context}

Question:
{question}

Rules:
- Answer only from memory
- If not found, say exactly: "I don't know."
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content.strip()

    # ✅ SAVE CHAT TO MEMORY HISTORY
    insert_vector(
        id=str(uuid.uuid4()),
        embedding=get_embedding(f"{question} {answer}"),
        payload={
            "text": f"Q: {question}\nA: {answer}",
            "user_id": current_user.id,
            "modality": "chat",
        }
    )

    return {
        "answer": answer,
        "matches_found": len(context_chunks),
    }

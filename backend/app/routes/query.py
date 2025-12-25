from fastapi import APIRouter, Depends, HTTPException
from app.services.embedder import get_embedding
from app.db.qdrant_db import search_vectors
from app.auth.utils import get_current_user
from app.config import settings
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)

router = APIRouter()


@router.post("/")
async def ask_brain(
    question: str,
    current_user=Depends(get_current_user)   # ✅ require login
):
    if not question.strip():
        raise HTTPException(400, "Question cannot be empty")

    # 1. Embed question
    emb = get_embedding(question)

    # 2. Search only THIS USER’s memory
    results = search_vectors(
        vector=emb,
        user_id=current_user.id,      # ✅ critical fix
        top_k=5
    )

    # 3. Extract context
    context_list = [
        p.payload.get("text", "")
        for p in results
        if p.payload is not None
    ]

    context = "\n".join(context_list) if context_list else "No relevant memory found."

    # 4. Build prompt
    prompt = f"""
You are a helpful assistant.

Context from user’s memory:
{context}

Question: {question}

Answer based ONLY on the above context. 
If the context does not contain the answer, say "I don't know."
"""

    # 5. Call GROQ
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "context_used": context,
        "matches_found": len(context_list)
    }

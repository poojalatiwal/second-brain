from fastapi import APIRouter
from app.services.embedder import get_embedding
from app.db.qdrant_db import search_vectors
from app.config import settings
from groq import Groq

client = Groq(api_key=settings.GROQ_API_KEY)

router = APIRouter()

@router.post("/")
async def ask_brain(question: str):
    # 1. Embed question
    emb = get_embedding(question)

    # 2. Search Qdrant
    results = search_vectors(emb, top_k=5)

    print("RAW QDRANT RESULTS:", results)

    # 3. Extract context from payload
    context = "\n".join([
    point.payload.get("text", "")
    for point in results
    if point.payload is not None
])


    # 4. Build prompt
    prompt = f"""
Context:
{context}

Question: {question}

Answer based ONLY on the context. If unsure, say you don't know.
"""

    # 5. Call GROQ (FREE)
    response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[
        {"role": "user", "content": prompt}
    ]
)


    answer = response.choices[0].message.content

    return {
        "answer": answer,
        "context_used": context
    }

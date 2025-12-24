from fastapi import APIRouter, UploadFile, File, Depends   # <-- FIXED
from pydantic import BaseModel
from app.db.qdrant_db import insert_vector, search_vectors, qdrant
from sentence_transformers import SentenceTransformer
from app.auth.utils import get_current_user   # <-- FIXED
from groq import Groq
from app.config import settings
import uuid
import fitz
import tempfile
import base64


router = APIRouter()

# ---- Embedding Model ----
embedder = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return embedder.encode(text).tolist()

groq_client = Groq(api_key=settings.GROQ_API_KEY)

# ============================================================
# 1) ADD MEMORY
# ============================================================
class AddMemory(BaseModel):
    text: str

@router.post("/add")
async def add_memory(data: AddMemory, user_id: int = Depends(get_current_user)):
    embedding = get_embedding(data.text)
    memory_id = str(uuid.uuid4())

    insert_vector(
        id=memory_id,
        embedding=embedding,
        payload={
            "text": data.text,
            "user_id": user_id
        }
    )

    return {"id": memory_id, "text": data.text}

# ============================================================
# 2) SEARCH MEMORY
# ============================================================
@router.get("/search")
async def search_memory(query: str, user_id: int = Depends(get_current_user)):
    emb = get_embedding(query)

    results = search_vectors(
        vector=emb,
        top_k=5,
        user_id=user_id
    )
    formatted = [
        {
            "id": p.id,
            "score": p.score,
            "text": p.payload.get("text")
        }
        for p in results
    ]

    return {"query": query, "results": formatted}


# ============================================================
# 3) DELETE MEMORY
# ============================================================
@router.delete("/delete/{memory_id}")
async def delete_memory(memory_id: str):
    try:
        qdrant.delete(
            collection_name="memory",
            points_selector={"points": [memory_id]}
        )
        return {"deleted": memory_id}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# 4) UPDATE MEMORY
# ============================================================
class UpdateMemory(BaseModel):
    new_text: str

@router.put("/update/{memory_id}")
async def update_memory(memory_id: str, data: UpdateMemory):
    new_embed = get_embedding(data.new_text)

    insert_vector(
        id=memory_id,
        embedding=new_embed,
        payload={"text": data.new_text}
    )

    return {"updated": memory_id, "new_text": data.new_text}


# ============================================================
# 5) SUMMARIZE MEMORY
# ============================================================
@router.get("/summarize")
async def summarize_memory():
    points, _ = qdrant.scroll(collection_name="memory", limit=10000)

    if not points:
        return {"summary": "No memory available."}

    combined_text = "\n".join([p.payload.get("text") for p in points])

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following memory knowledge base in clear bullet points:\n\n{combined_text}"
            }
        ]
    )

    return {"summary": response.choices[0].message.content}

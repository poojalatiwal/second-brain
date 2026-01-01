from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
import uuid

from app.db.qdrant_db import insert_vector, search_vectors, qdrant
from app.auth.utils import get_current_user
from app.auth.models import User
from app.services.embedder import get_embedding
from groq import Groq
from app.config import settings
from qdrant_client.models import Filter, FieldCondition, MatchValue, PointIdsList

router = APIRouter()
groq_client = Groq(api_key=settings.GROQ_API_KEY)

# ============================================================
# 1) ADD MEMORY
# ============================================================
class AddMemory(BaseModel):
    text: str

@router.post("/add")
async def add_memory(
    data: AddMemory,
    current_user: User = Depends(get_current_user)
):
    embedding = get_embedding(data.text)
    memory_id = str(uuid.uuid4())

    insert_vector(
        id=memory_id,
        embedding=embedding,
        payload={
            "text": data.text,
            "user_id": current_user.id
        }
    )

    return {
        "id": memory_id,
        "user_id": current_user.id,
        "text": data.text
    }


# ============================================================
# 2) SEARCH MEMORY
# ============================================================
@router.get("/search")
async def search_memory(
    query: str,
    current_user: User = Depends(get_current_user)
):
    emb = get_embedding(query)

    results = search_vectors(
        vector=emb,
        user_id=current_user.id,
        top_k=5
    )

    return {
        "query": query,
        "user_id": current_user.id,
        "results": [
            {
                "id": p.id,
                "score": p.score,
                "text": p.payload.get("text")
            }
            for p in results
        ]
    }


# ============================================================
# 3) DELETE MEMORY (USER-SAFE)
# ============================================================
@router.delete("/delete/{memory_id}")
async def delete_memory(
    memory_id: str,
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Verify ownership
    points, _ = qdrant.scroll(
        collection_name="memory",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=current_user.id)
                )
            ]
        ),
        limit=1000
    )

    if memory_id not in [str(p.id) for p in points]:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 2️⃣ ✅ CORRECT DELETE
    qdrant.delete(
        collection_name="memory",
        points_selector=PointIdsList(points=[memory_id])
    )

    return {
        "deleted": memory_id,
        "user_id": current_user.id
    }



# ============================================================
# 4) UPDATE MEMORY (USER-SAFE)
# ============================================================
class UpdateMemory(BaseModel):
    new_text: str
@router.put("/update/{memory_id}")
async def update_memory(
    memory_id: str,
    data: UpdateMemory,
    current_user: User = Depends(get_current_user)
):
    # 1️⃣ Verify ownership
    points, _ = qdrant.scroll(
        collection_name="memory",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=current_user.id)
                )
            ]
        ),
        limit=1000
    )

    if memory_id not in [str(p.id) for p in points]:
        raise HTTPException(status_code=403, detail="Not authorized")

    # 2️⃣ UPSERT = UPDATE
    embedding = get_embedding(data.new_text)

    insert_vector(
        id=memory_id,          # SAME ID → overwrite
        embedding=embedding,
        payload={
            "text": data.new_text,
            "user_id": current_user.id
        }
    )

    return {
        "updated": memory_id,
        "new_text": data.new_text
    }

# ============================================================
# 5) SUMMARIZE MEMORY (USER-ONLY)
# ============================================================
@router.get("/summarize")
async def summarize_memory(
    current_user: User = Depends(get_current_user)
):
    points, _ = qdrant.scroll(
        collection_name="memory",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=current_user.id)
                )
            ]
        ),
        limit=1000
    )

    if not points:
        return {"summary": "No memory available."}

    combined_text = "\n".join(
        p.payload.get("text", "")
        for p in points
        if p.payload
    )

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "user",
                "content": (
                    "Summarize the following memory knowledge base "
                    "in clear bullet points:\n\n" + combined_text
                )
            }
        ]
    )

    return {
        "user_id": current_user.id,
        "summary": response.choices[0].message.content
    }
@router.get("/history")
async def memory_history(
    limit: int = 50,
    current_user: User = Depends(get_current_user)
):
    points, _ = qdrant.scroll(
        collection_name="memory",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=current_user.id)
                )
            ]
        ),
        limit=limit,
        with_payload=True
    )

    items = [
        {
            "id": str(p.id),
            "text": p.payload.get("text", ""),
            "preview": p.payload.get("text", "")[:120],
            "modality": p.payload.get("modality", "text"),
            "created_at": p.payload.get("timestamp"),
        }
        for p in points
    ]

    items.sort(key=lambda x: x["created_at"] or "", reverse=True)

    return { "items": items }

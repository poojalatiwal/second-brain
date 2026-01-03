from fastapi import APIRouter, Depends, HTTPException

from app.services.embedder import get_embedding
from app.db.qdrant_db import qdrant
from app.auth.utils import get_current_user

# ✅ IMPORTANT: MatchText MUST be imported
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    MatchText,   # 🔥 THIS WAS MISSING
)

router = APIRouter(prefix="/hybrid-search", tags=["Hybrid Search"])


@router.get("/")
async def hybrid_search(
    query: str,
    current_user: dict = Depends(get_current_user),
):
    query = query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")

    user_id = current_user["id"]

    # --------------------------------------------------
    # USER FILTER
    # --------------------------------------------------
    user_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            )
        ]
    )

    # --------------------------------------------------
    # 1️⃣ SEMANTIC SEARCH (VECTOR SEARCH)
    # --------------------------------------------------
    embedding = get_embedding(query)

    semantic_result = qdrant.query_points(
        collection_name="memory",
        query=embedding,
        query_filter=user_filter,
        limit=5,
        with_payload=True,
        timeout=10,   # ✅ cloud-safe
    )

    semantic_hits = [
        {
            "text": p.payload.get("text", ""),
            "score": p.score,
            "source": "semantic",
        }
        for p in semantic_result.points
        if p.payload
    ]

    # --------------------------------------------------
    # 2️⃣ KEYWORD SEARCH (TEXT INDEX)
    # --------------------------------------------------
    keyword_filter = Filter(
        must=[
            FieldCondition(
                key="text",
                match=MatchText(text=query),   # ✅ NOW WORKS
            ),
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            ),
        ]
    )

    keyword_points, _ = qdrant.scroll(
        collection_name="memory",
        scroll_filter=keyword_filter,
        limit=10,
        with_payload=True,
        timeout=10,
    )

    keyword_hits = [
        {
            "text": p.payload.get("text", ""),
            "score": None,
            "source": "keyword",
        }
        for p in keyword_points
        if p.payload
    ]

    # --------------------------------------------------
    # 3️⃣ MERGE + DEDUPLICATE
    # --------------------------------------------------
    seen = set()
    combined = []

    for item in semantic_hits + keyword_hits:
        text = item["text"]
        if text and text not in seen:
            seen.add(text)
            combined.append(item)

    return {
        "user_id": user_id,
        "query": query,
        "results": combined,
        "semantic_count": len(semantic_hits),
        "keyword_count": len(keyword_hits),
        "total": len(combined),
    }

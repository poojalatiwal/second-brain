from fastapi import APIRouter, Depends, HTTPException
from app.services.embedder import get_embedding
from app.db.qdrant_db import qdrant
from app.auth.utils import get_current_user
from app.auth.models import User
from qdrant_client.models import Filter, FieldCondition, MatchValue

router = APIRouter()


@router.get("/")
async def hybrid_search(
    query: str,
    current_user: User = Depends(get_current_user)
):
    if not query.strip():
        raise HTTPException(400, "Query cannot be empty")

    # --------------------------------------------------
    # USER FILTER
    # --------------------------------------------------
    user_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=current_user.id)
            )
        ]
    )

    # --------------------------------------------------
    # 1️⃣ SEMANTIC SEARCH (VECTOR)
    # --------------------------------------------------
    embedding = get_embedding(query)

    semantic_result = qdrant.query_points(
        collection_name="memory",
        query=embedding,
        query_filter=user_filter,
        limit=5,
        with_payload=True
    )

    semantic_hits = [
        {
            "text": p.payload.get("text", ""),
            "score": p.score
        }
        for p in semantic_result.points
    ]

    # --------------------------------------------------
    # 2️⃣ KEYWORD SEARCH (TEXT MATCH)
    # --------------------------------------------------
    keyword_result, _ = qdrant.scroll(
        collection_name="memory",
        scroll_filter=Filter(
            must=[
                FieldCondition(
                    key="text",
                    match={"text": query}
                ),
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=current_user.id)
                )
            ]
        ),
        limit=20
    )

    keyword_hits = [
        p.payload.get("text", "")
        for p in keyword_result
    ]

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------
    return {
        "user_id": current_user.id,
        "semantic": semantic_hits,
        "keyword": keyword_hits
    }

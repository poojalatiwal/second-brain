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
    current_user: User = Depends(get_current_user)   # ✅ AUTH
):
    if not query.strip():
        raise HTTPException(400, "Query cannot be empty")

    # --------------------------------------------------
    # USER FILTER (CRITICAL)
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
    # 1️⃣ SEMANTIC SEARCH
    # --------------------------------------------------
    sem_vec = get_embedding(query)

    sem_results = qdrant.query_points(
        collection_name="memory",
        query=sem_vec,
        limit=5,
        with_payload=True,
        filter=user_filter        # ✅ USER-SCOPED
    )

    # --------------------------------------------------
    # 2️⃣ KEYWORD SEARCH
    # --------------------------------------------------
    kw_results, _ = qdrant.scroll(
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

    # --------------------------------------------------
    # RESPONSE
    # --------------------------------------------------
    return {
        "user_id": current_user.id,
        "semantic": [
            {
                "text": p.payload.get("text", ""),
                "score": p.score
            }
            for p in sem_results.points
        ],
        "keyword": [
            p.payload.get("text", "")
            for p in kw_results
        ]
    }

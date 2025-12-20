from fastapi import APIRouter
from app.services.embedder import get_embedding
from app.db.qdrant_db import qdrant

router = APIRouter()

@router.get("/")
async def hybrid_search(query: str):
    # semantic
    sem_vec = get_embedding(query)

    sem_results = qdrant.query_points(
        collection_name="memory",
        query=sem_vec,
        limit=5,
        with_payload=True
    )

    # keyword match
    kw_results = qdrant.scroll(
        collection_name="memory",
        scroll_filter={"must": [{"key": "text", "match": {"text": query}}]},
        limit=20
    )[0]

    return {
        "semantic": [
            {"text": p.payload["text"], "score": p.score}
            for p in sem_results.points
        ],
        "keyword": [
            p.payload["text"]
            for p in kw_results
        ]
    }

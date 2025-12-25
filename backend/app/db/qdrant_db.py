from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, Filter, FieldCondition, MatchValue
from app.config import settings
from datetime import datetime


# ------------------------------------------------------
# QDRANT CLIENT INITIALIZATION
# ------------------------------------------------------

qdrant = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    prefer_grpc=False
)


# ------------------------------------------------------
# CREATE COLLECTION IF NOT EXISTS
# ------------------------------------------------------

def init_qdrant():
    collections = [c.name for c in qdrant.get_collections().collections]

    if "memory" not in collections:
        qdrant.create_collection(
            collection_name="memory",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        print("✅ Created Qdrant collection: memory")
    else:
        print("📌 Qdrant collection already exists: memory")


# ------------------------------------------------------
# INSERT VECTOR
# ------------------------------------------------------

def insert_vector(id: str, embedding: list, payload: dict):
    payload["timestamp"] = datetime.utcnow().isoformat()

    try:
        qdrant.upsert(
            collection_name="memory",
            points=[
                {
                    "id": id,
                    "vector": embedding,
                    "payload": payload,
                }
            ],
        )
        print(f"✅ Inserted vector: {id}")
    except Exception as e:
        print("❌ ERROR INSERTING INTO QDRANT:", e)
        raise e


# ------------------------------------------------------
# SEARCH VECTOR (FIXED)
# ------------------------------------------------------

def search_vectors(vector: list, user_id: int, top_k: int = 5):
    """
    Searches memory only for the given user_id.
    Compatible with NEW Qdrant Python SDK.
    """

    query_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id)
            )
        ]
    )

    result = qdrant.query_points(
        collection_name="memory",
        query=vector,
        query_filter=query_filter,   # ✅ FIXED (not filter=)
        limit=top_k,
        with_payload=True
    )

    return result.points   # ✅ FIXED (points, not point)

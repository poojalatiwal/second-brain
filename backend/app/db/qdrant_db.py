from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance
from app.config import settings
from datetime import datetime   # ✅ missing import

# Create Qdrant client (REST mode)
qdrant = QdrantClient(
    url=settings.QDRANT_URL,
    prefer_grpc=False
)

def init_qdrant():
    """
    Creates collection ONLY if not exist.
    """
    collections = [c.name for c in qdrant.get_collections().collections]

    if "memory" not in collections:
        qdrant.create_collection(
            collection_name="memory",
            vectors_config=VectorParams(
                size=384,
                distance=Distance.COSINE
            )
        )
        print("✅ Created new Qdrant collection")
    else:
        print("📌 Qdrant collection already exists — not recreating")



def insert_vector(id, embedding, payload):
    """
    Inserts a vector + metadata into Qdrant.
    """
    payload["timestamp"] = datetime.utcnow().isoformat()   # ✅ add timestamp

    try:
        qdrant.upsert(
            collection_name="memory",
            points=[{
                "id": id,
                "vector": embedding,
                "payload": payload
            }]
        )
        print("✅ Inserted:", id)
    except Exception as e:
        print("❌ ERROR INSERTING INTO QDRANT:", e)
        raise e


def search_vectors(vector, user_id, top_k=5):
    result = qdrant.query_points(
        collection_name="memory",
        query=vector,
        limit=top_k,
        with_payload=True,
        filter={
            "must": [
                {"key": "user_id", "match": {"value": user_id}}
            ]
        }
    )
    return result.points

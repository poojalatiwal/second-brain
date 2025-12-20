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
    Creates (or recreates) the memory collection.
    Must match the embedding dim: 384 for MiniLM-L6-v2.
    """
    qdrant.recreate_collection(
        collection_name="memory",
        vectors_config=VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    )
    print("✅ Qdrant collection created: memory")


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


def search_vectors(vector, top_k=5):
    try:
        result = qdrant.query_points(
            collection_name="memory",
            query_vector=vector,     # ✅ correct param
            limit=top_k,
            with_payload=True
        )

        return result.points

    except Exception as e:
        print("❌ ERROR SEARCHING QDRANT:", e)
        return []

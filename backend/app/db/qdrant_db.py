from qdrant_client import QdrantClient
from qdrant_client.models import (
    Filter,
    FieldCondition,
    MatchValue,
    MatchText
)
from app.config import settings
from datetime import datetime
import time

qdrant = QdrantClient(
    url=settings.QDRANT_URL,
    api_key=settings.QDRANT_API_KEY,
    prefer_grpc=False,
    timeout=60,
)

COLLECTION_NAME = "memory"
EMBEDDING_SIZE = 1024 

from qdrant_client.models import PayloadSchemaType

def ensure_qdrant_collection():
    collections = qdrant.get_collections().collections
    names = [c.name for c in collections]

    if COLLECTION_NAME not in names:
        qdrant.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=VectorParams(
                size=EMBEDDING_SIZE,
                distance=Distance.COSINE,
            )
        )

    indexes = [
        ("user_id", PayloadSchemaType.INTEGER),
        ("text", PayloadSchemaType.TEXT),      
        ("modality", PayloadSchemaType.KEYWORD) 
    ]

    for field, schema in indexes:
        try:
            qdrant.create_payload_index(
                collection_name=COLLECTION_NAME,
                field_name=field,
                field_schema=schema,
            )
        except Exception:
            pass 


# INSERT VECTOR
def insert_vector(id: str, embedding: list, payload: dict):
    payload["timestamp"] = datetime.utcnow().isoformat()

    qdrant.upsert(
        collection_name=COLLECTION_NAME,
        points=[
            {
                "id": id,
                "vector": embedding,
                "payload": payload,
            }
        ],
    )

# SEARCH VECTORS
def search_vectors(vector: list, user_id: int, top_k: int = 5):
    query_filter = Filter(
        must=[
            FieldCondition(
                key="user_id",
                match=MatchValue(value=user_id),
            )
        ]
    )

    for attempt in range(2):  
        try:
            result = qdrant.query_points(
                collection_name=COLLECTION_NAME,
                query=vector,
                query_filter=query_filter,
                limit=top_k,
                with_payload=True,
            )
            return result.points
        except Exception as e:
            if attempt == 1:
                raise
            time.sleep(1)  
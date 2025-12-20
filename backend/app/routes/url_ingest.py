from fastapi import APIRouter
import requests
from bs4 import BeautifulSoup
import uuid
from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector

router = APIRouter()

@router.post("/url")
async def ingest_url(url: str):
    try:
        html = requests.get(url, timeout=10).text
    except:
        return {"error": "Failed to fetch URL"}

    soup = BeautifulSoup(html, "html.parser")

    # Extract visible text
    text = "\n".join([t.get_text(strip=True) for t in soup.find_all(["p", "h1", "h2", "h3", "li"])])

    chunks = chunk_text(text)

    stored_ids = []

    for chunk in chunks:
        emb = get_embedding(chunk)
        uid = str(uuid.uuid4())

        insert_vector(
            id=uid,
            embedding=emb,
            payload={
                "text": chunk,
                "modality": "url",
                "source_url": url
            }
        )

        stored_ids.append(uid)

    return {
        "url": url,
        "chunks_stored": len(stored_ids),
        "ids": stored_ids
    }

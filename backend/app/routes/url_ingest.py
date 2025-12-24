from fastapi import APIRouter, Request, Query
import requests
from bs4 import BeautifulSoup
import uuid
from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector

router = APIRouter()

@router.api_route("/url", methods=["GET", "POST"])
async def ingest_url(request: Request, url: str = Query(None)):
    # POST body support
    if request.method == "POST" and url is None:
        body = await request.json()
        url = body.get("url")

    if not url:
        return {"error": "URL is required"}

    # Fetch page
    try:
        html = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        ).text
    except Exception as e:
        return {"error": f"Failed to fetch URL: {str(e)}"}

    soup = BeautifulSoup(html, "html.parser")
    text = "\n".join(
        t.get_text(strip=True)
        for t in soup.find_all(["p", "h1", "h2", "h3", "li"])
    )

    chunks = chunk_text(text)
    ids = []

    for chunk in chunks:
        emb = get_embedding(chunk)
        uid = str(uuid.uuid4())
        insert_vector(id=uid, embedding=emb, payload={"text": chunk, "source": url})
        ids.append(uid)

    return {"url": url, "chunks_stored": len(ids), "ids": ids}


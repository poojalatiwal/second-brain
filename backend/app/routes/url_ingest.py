from fastapi import APIRouter, Request, Query, Depends, HTTPException
import requests
from bs4 import BeautifulSoup
import uuid

from app.services.embedder import get_embedding
from app.services.chunker import chunk_text
from app.db.qdrant_db import insert_vector
from app.auth.utils import get_current_user
from app.auth.models import User

router = APIRouter()


@router.api_route("/url", methods=["GET", "POST"])
async def ingest_url(
    request: Request,
    url: str = Query(None),
    current_user: dict = Depends(get_current_user)
):
    if request.method == "POST" and url is None:
        body = await request.json()
        url = body.get("url")

    if not url:
        raise HTTPException(400, "URL is required")

    # 1️⃣ Fetch page
    try:
        res = requests.get(
            url,
            timeout=10,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        res.raise_for_status()
    except Exception as e:
        raise HTTPException(400, f"Failed to fetch URL: {e}")

    # 2️⃣ Parse HTML
    soup = BeautifulSoup(res.text, "html.parser")
    title = soup.title.string.strip() if soup.title else "Untitled Page"

    text = "\n".join(
        tag.get_text(strip=True)
        for tag in soup.find_all(["p", "h1", "h2", "h3", "li"])
        if tag.get_text(strip=True)
    )

    if not text.strip():
        raise HTTPException(400, "No readable text found")

    # 3️⃣ Chunk page text
    chunks = chunk_text(text)
    stored_ids = []

    # 🔹 A) Store PAGE SUMMARY vector (VERY IMPORTANT)
    summary_text = f"Webpage titled '{title}'. Content discusses: {text[:1500]}"
    summary_id = str(uuid.uuid4())

    insert_vector(
        id=summary_id,
        embedding=get_embedding(summary_text),
        payload={
            "text": summary_text,
            "modality": "url_summary",
            "title": title,
            "source_url": url,
            "user_id": current_user["id"] 
        }
    )

    stored_ids.append(summary_id)

    # 🔹 B) Store detailed chunks
    for chunk in chunks:
        uid = str(uuid.uuid4())
        insert_vector(
            id=uid,
            embedding=get_embedding(chunk),
            payload={
                "text": chunk,
                "modality": "url",
                "title": title,
                "source_url": url,
                "user_id": current_user["id"] 
            }
        )
        stored_ids.append(uid)

    return {
        "status": "stored",
        "url": url,
        "title": title,
        "chunks_stored": len(stored_ids),
        "user_id": current_user["id"] 
    }

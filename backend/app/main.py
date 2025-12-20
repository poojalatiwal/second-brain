from fastapi import FastAPI
from app.db.qdrant_db import init_qdrant

# Import routes
from app.routes import (
    ingest,
    pdf_ingest,
    audio_ingest,
    audio_chat,
    chat,
    memory,
    url_ingest,
    image_ingest,
    hybrid_search,
    stream_chat
)

app = FastAPI()


# -----------------------------------------------------------
# RUN ON STARTUP → Create Qdrant Collection
# -----------------------------------------------------------
@app.on_event("startup")
def startup_event():
    print("🚀 Running startup event...")
    init_qdrant()


# -----------------------------------------------------------
# ROUTE REGISTRATION
# -----------------------------------------------------------
# Ingestion (PDF / Text / Audio / URL / Image)
app.include_router(ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(pdf_ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(audio_ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(url_ingest.router, prefix="/ingest", tags=["Ingest"])
app.include_router(image_ingest.router, prefix="/ingest", tags=["Ingest"])

# RAG: Ask brain + hybrid search + streaming
app.include_router(hybrid_search.router, prefix="/search", tags=["Search"])
app.include_router(stream_chat.router, prefix="/stream", tags=["Chat"])
app.include_router(audio_chat.router, prefix="/brain", tags=["Brain"])
app.include_router(memory.router, prefix="/memory", tags=["Memory"])

# Normal chat (text + audio + image)
app.include_router(chat.router, prefix="/chat", tags=["Chat"])


# -----------------------------------------------------------
# HOME
# -----------------------------------------------------------
@app.get("/")
def home():
    return {"message": "Second Brain Backend Running"}

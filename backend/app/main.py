# app/main.py

from fastapi import FastAPI
from app.db.postgree import Base, engine
from app.db.qdrant_db import init_qdrant

# ========= IMPORT ROUTES =========

# Auth
from app.auth.routes import router as auth_router

# Ingestion
from app.routes.ingest import router as ingest_router
from app.routes.pdf_ingest import router as pdf_ingest_router
from app.routes.audio_ingest import router as audio_ingest_router
from app.routes.url_ingest import router as url_ingest_router
from app.routes.image_ingest import router as image_ingest_router

# RAG / Search
from app.routes.query import router as query_router
from app.routes.hybrid_search import router as hybrid_router
from app.routes.stream_chat import router as stream_router

# AI Chat
from app.routes.chat import router as chat_router
from app.routes.audio_chat import router as audio_chat_router

# Memory
from app.routes.memory import router as memory_router


# ========= INIT FASTAPI =========

app = FastAPI(title="Second Brain Backend")


# ========= INIT DATABASE =========

print("📌 Creating database tables (if not exist)...")
Base.metadata.create_all(bind=engine)


# ========= STARTUP EVENT =========

@app.on_event("startup")
def startup_event():
    print("🚀 Startup: Initializing Qdrant...")
    init_qdrant()  # Uses your qdrant_db.py code


# ========= REGISTER ROUTES =========

# Auth
app.include_router(auth_router, prefix="/auth", tags=["Auth"])

# Ingestion Routes
app.include_router(ingest_router,       prefix="/ingest", tags=["Ingest"])
app.include_router(pdf_ingest_router,   prefix="/ingest", tags=["Ingest"])
app.include_router(audio_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(url_ingest_router,   prefix="/ingest", tags=["Ingest"])
app.include_router(image_ingest_router, prefix="/ingest", tags=["Ingest"])

# RAG / Search
app.include_router(query_router, prefix="/brain", tags=["Brain"])
app.include_router(hybrid_router, prefix="/search", tags=["Search"])
app.include_router(stream_router, prefix="/stream", tags=["Chat"])

# Chat
app.include_router(chat_router, prefix="/chat", tags=["Chat"])
app.include_router(audio_chat_router, prefix="/brain", tags=["Brain"])

# Memory CRUD
app.include_router(memory_router, prefix="/memory", tags=["Memory"])


# ========= HOME =========

@app.get("/")
def home():
    return {"message": "Second Brain Backend Running 🚀"}

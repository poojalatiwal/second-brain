from dotenv import load_dotenv
load_dotenv()

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


from app.db.postgree import Base, engine
from app.db.qdrant_db import init_qdrant

# ========= ROUTERS =========
from app.auth.routes import router as auth_router
from app.auth.google import router as google_router
from app.auth.github import router as github_router

from app.routes.ingest import router as ingest_router
from app.routes.pdf_ingest import router as pdf_ingest_router
from app.routes.audio_ingest import router as audio_ingest_router
from app.routes.url_ingest import router as url_ingest_router
from app.routes.image_ingest import router as image_ingest_router

from app.routes.query import router as brain_router
from app.routes.hybrid_search import router as search_router
from app.routes.stream_chat import router as stream_router
from app.routes.chat import router as chat_router
from app.routes.audio_chat import router as audio_chat_router
from app.routes.memory import router as memory_router
from app.routes.admin import router as admin_router



# ========= INIT APP =========
app = FastAPI(title="Second Brain Backend")

# ========= SESSION (OAuth) =========
app.add_middleware(
    SessionMiddleware,
    secret_key=os.getenv("SESSION_SECRET", "dev-secret-key"),
    same_site="lax",
)

# ========= CORS =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Session-Id"],
)

# ========= DATABASE =========
Base.metadata.create_all(bind=engine)

# ========= STARTUP =========
@app.on_event("startup")
def startup_event():
    init_qdrant()

# ========= ROUTES =========

# ---- Auth ----
app.include_router(auth_router, tags=["Auth"])
app.include_router(google_router, tags=["Auth"])
app.include_router(github_router, tags=["Auth"])

# ---- Ingest ----
app.include_router(ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(pdf_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(audio_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(url_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(image_ingest_router, prefix="/ingest", tags=["Ingest"])

# ---- Brain (Memory-based) ----
app.include_router(brain_router, prefix="/brain", tags=["Brain"])
app.include_router(audio_chat_router, prefix="/brain", tags=["Brain"])

# ---- Streaming Chat ----
app.include_router(stream_router, prefix="/brain/stream", tags=["Brain"])

# ---- Free Chat ----
app.include_router(chat_router, tags=["Chat"])

# ---- Search ----
app.include_router(search_router, prefix="/search", tags=["Search"])

# ---- Memory ----
app.include_router(memory_router, prefix="/memory", tags=["Memory"])

# ---- Admin ----
app.include_router(admin_router, tags=["Admin"])

# ========= HOME =========
@app.get("/")
def home():
    return {"message": "Second Brain Backend Running 🚀"}

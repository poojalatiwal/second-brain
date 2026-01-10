from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.db.qdrant_db import ensure_qdrant_collection

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

# ========= APP =========
app = FastAPI(title="Second Brain Backend")

# ========= CORS =========
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # Vite dev
        "http://127.0.0.1:5173",

        "http://localhost:3000",   # Docker nginx
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ========= SESSION =========
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    same_site="lax",
)


# ========= STARTUP =========
@app.on_event("startup")
def startup():
    print("📌 Starting backend...")

    try:
        ensure_qdrant_collection()
        print("✅ Qdrant ready")
    except Exception as e:
        print("⚠️ Qdrant not available, skipping vector init")
        print(e)

    print("🚀 Startup complete")


# ========= ROUTES =========
app.include_router(auth_router, tags=["Auth"])
app.include_router(google_router, tags=["Auth"])
app.include_router(github_router, tags=["Auth"])

app.include_router(ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(pdf_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(audio_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(url_ingest_router, prefix="/ingest", tags=["Ingest"])
app.include_router(image_ingest_router, prefix="/ingest", tags=["Ingest"])

app.include_router(brain_router, prefix="/brain", tags=["Brain"])
app.include_router(audio_chat_router, prefix="/brain", tags=["Brain"])
app.include_router(stream_router, prefix="/brain/stream", tags=["Brain"])

app.include_router(chat_router, tags=["Chat"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(memory_router, prefix="/memory", tags=["Memory"])
app.include_router(admin_router, tags=["Admin"])

@app.get("/")
def home():
    return {"message": "Second Brain Backend Running 🚀"}

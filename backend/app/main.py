from fastapi import FastAPI
from app.db.qdrant_db import init_qdrant

app = FastAPI()

# Run Qdrant initialization BEFORE imports of routes
@app.on_event("startup")
def startup_event():
    print("🚀 Running startup event...")
    init_qdrant()

# IMPORT ROUTES AFTER startup_event IS DECLARED
from app.routes import ingest, query

# Include routes
app.include_router(ingest.router, prefix="/ingest")
app.include_router(query.router, prefix="/brain")

@app.get("/")
def home():
    return {"message": "Second Brain Backend Running"}

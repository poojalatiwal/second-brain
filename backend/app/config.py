import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")   # optional now
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")       # NEW
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")

settings = Settings()

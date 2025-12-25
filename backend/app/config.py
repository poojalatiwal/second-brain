import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")

    # Qdrant
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY", None)   # ✅ FIXED

    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

    DATABASE_URL = os.getenv("DATABASE_URL")

    # JWT CONFIG
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", 60))
    JWT_REFRESH_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", 30))

settings = Settings()

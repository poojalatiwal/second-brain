import os
from dotenv import load_dotenv

# Load env.local or .env automatically
load_dotenv()


class Settings:
    # =====================
    # ENV
    # =====================
    ENV = os.getenv("ENV", "local")

    # =====================
    # API KEYS
    # =====================
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    GROK_API_KEY = os.getenv("GROK_API_KEY")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")
    DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

    # =====================
    # QDRANT
    # =====================
    QDRANT_URL = os.getenv("QDRANT_URL")
    QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")

    # =====================
    # DATABASE
    # =====================
    DATABASE_URL = os.getenv("DATABASE_URL")

    # =====================
    # JWT
    # =====================
    JWT_SECRET = os.getenv("JWT_SECRET", "dev-secret")
    JWT_ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
    JWT_ACCESS_EXPIRE_MINUTES = int(os.getenv("JWT_ACCESS_EXPIRE_MINUTES", 60))
    JWT_REFRESH_EXPIRE_DAYS = int(os.getenv("JWT_REFRESH_EXPIRE_DAYS", 30))

    # =====================
    # SESSION
    # =====================
    SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-session")


settings = Settings()

# 🚨 HARD FAIL IF DB NOT SET
if not settings.DATABASE_URL:
    raise RuntimeError("❌ DATABASE_URL is not set")

import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
    SERPAPI_KEY = os.getenv("SERPAPI_KEY")
    IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")# ✅ ADD THIS LINE
    GROK_API_KEY = os.getenv("GROK_API_KEY") 
    DEEPINFRA_API_KEY = os.getenv("DEEPINFRA_API_KEY")

settings = Settings()

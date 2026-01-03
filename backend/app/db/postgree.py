from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# =====================
# DATABASE ENGINE
# =====================
print("USING DATABASE URL =>", settings.DATABASE_URL)

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,   # fixes stale / dropped connections
    echo=False
)

# =====================
# SESSION
# =====================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# =====================
# BASE
# =====================
Base = declarative_base()

# =====================
# IMPORT MODELS
# =====================
from app.auth.models import User  # keep importing models here


# =====================
# DEPENDENCY
# =====================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

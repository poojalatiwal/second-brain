from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config import settings

# ----------------------------------------------------
# DATABASE URL (from .env)
# ----------------------------------------------------
DATABASE_URL = settings.DATABASE_URL  
print("USING DATABASE URL =>", DATABASE_URL)

# ----------------------------------------------------
# CREATE ENGINE
# ----------------------------------------------------
engine = create_engine(
    DATABASE_URL,
    echo=True  # shows SQL queries in console (optional but useful)
)

# ----------------------------------------------------
# SESSION
# ----------------------------------------------------
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# ----------------------------------------------------
# BASE MODEL
# ----------------------------------------------------
Base = declarative_base()

# ----------------------------------------------------
# IMPORT ALL MODELS HERE
# VERY IMPORTANT: Must import BEFORE create_all()
# ----------------------------------------------------
from app.auth.models import User   # add more models here as you create them

# ----------------------------------------------------
# CREATE TABLES IF NOT PRESENT
# ----------------------------------------------------
def create_tables():
    print("📌 Creating database tables (if not exist)...")
    Base.metadata.create_all(bind=engine)


# ----------------------------------------------------
# FASTAPI DEPENDENCY
# ----------------------------------------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ----------------------------------------------------
# RUN TABLE CREATION ON IMPORT
# ----------------------------------------------------
create_tables()

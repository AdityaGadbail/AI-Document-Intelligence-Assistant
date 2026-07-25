from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.base import Base


Path("storage").mkdir(parents=True, exist_ok=True)
Path("storage/uploads").mkdir(parents=True, exist_ok=True)
Path("storage/vector_store").mkdir(parents=True, exist_ok=True)
DATABASE_URL = "sqlite:///storage/app.db"

engine = create_engine(
    DATABASE_URL,
    echo = False,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit = False
)

def init_db():
    import models
    Base.metadata.create_all(bind=engine)
    
init_db()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()    

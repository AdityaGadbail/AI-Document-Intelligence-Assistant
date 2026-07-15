from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///storage/app.db"

engine = create_engine(
    DATABASE_URL,
    echo = False
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit = False
)

def get_db():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.close()    
print("DataBase Connected Successfully")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
DATABASE_URL = "sqlite:///storage/app.db"

engine = create_engine(
    DATABASE_URL,
    echo = True
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit = False
)

print("DataBase Connected Successfully")
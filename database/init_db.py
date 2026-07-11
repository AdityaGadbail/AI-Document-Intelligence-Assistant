
from database.base import Base
from database.database import engine

from models.user import User
from models.document import Document
from models.conversation import Converstaion
from models.message import Message 

def init_database():
    """
    It will create all tabels
    """
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")

if __name__ == "__main__":
    init_database()

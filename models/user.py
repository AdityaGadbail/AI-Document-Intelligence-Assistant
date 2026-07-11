from datetime import datetime
from enum import Enum
from sqlalchemy import DateTime, Enum as SQLEnum, Integer,String
from sqlalchemy.orm import Mapped,mapped_column,relationship

from database.base import Base
class UserRole(Enum):
    USER = "USER"
    ADMIN = "ADMIN"

class User(Base):
    """
    User Table
    """
    __tablename__ = "users"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key= True,
        index=True
    )

    username:Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False

    )

    email:Mapped[str] = mapped_column(
        String(255),
        unique= True,
        nullable= False
    )

    password_hash : Mapped[str] = mapped_column(
        String(255),
        nullable= False,

    )

    created_at:Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.utcnow
        # default= lambda: datetime.now(UTC)
    )

    role: Mapped[UserRole] 
    documents = relationship("Document",back_populates="user",cascade="all, delete-orphan")
    conversation = relationship("Conversation",back_populates="user",cascade="all, delete-orphan")


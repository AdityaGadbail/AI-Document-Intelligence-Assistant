from datetime import datetime

from sqlalchemy import String, Integer, ForeignKey , DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base import Base

class Converstaion(Base):

    __tablename__ = "conversations"

    id:Mapped[int] = mapped_column(
        Integer,
        primary_key= True,
        index= True
    )

    user_id:Mapped[int] = mapped_column(
        ForeignKey("users.id",ondelete="CASCADE"),
        nullable= False
    )

    title: Mapped[str] =  mapped_column(
        String(255),
        nullable= False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    # Relationship with User
    user = relationship("User",back_populates="conversations")
    # Relationship with Messages
    user = relationship("Message",back_populates="conversation",cascade="all, delete-orphan")
from datetime import datetime
from enum import Enum

from sqlalchemy import String, Integer , DateTime, ForeignKey, Enum as SQLEnum, Text
from sqlalchemy.orm import Mapped , mapped_column, relationship

from database.base import Base

class MessageRole(Enum):
    USER = "USER"
    ASSISTANT = "ASSISTANT"


class Message(Base):

    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    conversation_id: Mapped[int] = mapped_column(
        ForeignKey("conversations.id",ondelete="CASCADE"),
        nullable= False
    )

    role: Mapped[MessageRole] = mapped_column(
        SQLEnum(MessageRole),
        nullable=False
    )

    message : Mapped[str] = mapped_column(
        Text,
        nullable= False
    )

    source_document : Mapped[int | None] = mapped_column(
        Integer,
        nullable= True
    )

    response_time_ms : Mapped[str | None] = mapped_column(
        Text,
        nullable= True
    )

    is_from_document: Mapped[bool] = mapped_column(
    default=True,
    nullable=False
    )

    confidence_score: Mapped[float | None]

    timestamp : Mapped[datetime] = mapped_column(
        DateTime,
        default= datetime.utcnow
    )

    conversation = relationship("Conversation",back_populates="messages")


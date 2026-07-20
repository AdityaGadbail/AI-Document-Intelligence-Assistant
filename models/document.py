
from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, Enum as SQLEnum, String, Integer, ForeignKey
from sqlalchemy.orm import Mapped , mapped_column , relationship

from database.base import Base

class EmbeddingStatus(Enum):
    UPLOADED = "UPLOADED"
    PROCESSING = "PROCESSING"
    READY = "READY"
    FAILED = "FAILED"

class Document(Base):

    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key = True,
        index = True
    )

    user_id:Mapped[str] = mapped_column(
        ForeignKey("users.id"),
        nullable = False
    )

    original_filename:Mapped[str] = mapped_column(
        String(255),
        nullable = False
    )

    stored_filename : Mapped[str] = mapped_column(
        String(255),
        unique = True,
        nullable = False
    )

    file_path:Mapped[str] = mapped_column(
        String(500),
        nullable= False
    )

    file_size: Mapped[int] = mapped_column(
        Integer,
        nullable =False
    )

    embedding_status : Mapped[EmbeddingStatus] = mapped_column(
        SQLEnum(EmbeddingStatus),
        default = EmbeddingStatus.UPLOADED,
        nullable = False
    )
    
    upload_date: Mapped[datetime] = mapped_column(
        DateTime,
        default = datetime.utcnow
        # default= lambda: datetime.now(UTC)
    )

    is_deleted:Mapped[bool] = mapped_column(
        default = False,
        nullable = False
    )
    
    mime_type: Mapped[str] = mapped_column(
    String(100),
    nullable=False
    )

    page_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable= True
    )

    word_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable= True
    )

    character_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable= True
    )


    user = relationship("User",back_populates="documents")
    conversations = relationship("Conversation",back_populates="document",cascade="all, delete-orphan")


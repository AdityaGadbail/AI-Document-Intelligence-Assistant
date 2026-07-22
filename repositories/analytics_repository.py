from sqlalchemy import func
from sqlalchemy.orm import Session

from models.document import Document
from models.conversation import Conversation
from models.message import Message

class AnalyticsRepository:

    @staticmethod
    def get_dashboard_statistics(db: Session,user_id: int):

        total_documents = (db.query(Document).filter(Document.user_id == user_id).count())

        total_conversations = (db.query(Conversation).filter(Conversation.user_id == user_id).count())

        total_messages = (db.query(Message).join(Conversation).filter(Conversation.user_id == user_id).count())

        total_storage = (db.query(func.sum(Document.file_size)).filter(Document.user_id == user_id).scalar() or 0)


        total_pages = (
            db.query(
                func.sum(Document.page_count)
            )
            .filter(Document.user_id == user_id)
            .scalar()
            or 0
        )

        total_words = (
            db.query(
                func.sum(Document.word_count)
            )
            .filter(Document.user_id == user_id)
            .scalar()
            or 0
        )

        average_pages = (
            db.query(
                func.avg(Document.page_count)
            )
            .filter(Document.user_id == user_id)
            .scalar()
            or 0
        )

        average_words = (
            db.query(
                func.avg(Document.word_count)
            )
            .filter(Document.user_id == user_id)
            .scalar()
            or 0
        )

        return {
            "documents": total_documents,
            "conversations": total_conversations,
            "messages": total_messages,
            "storage": total_storage,
            "pages": total_pages,
            "words": total_words,
            "average_pages": round(average_pages, 2),
            "average_words": round(average_words, 2)
        }

    @staticmethod
    def get_upload_activity(db: Session,user_id: int):
        return (
            db.query(func.date(Document.upload_date).label("date"),
                     func.count(Document.id).label("count")).filter(Document.user_id == user_id).group_by(func.date(Document.upload_date)).order_by(func.date(Document.upload_date))
        )

    @staticmethod
    def get_document_pages(db: Session,user_id: int):
        return(
            db.query(Document.original_filename,Document.page_count).filter(Document.user_id == user_id).all()
        ) 

    @staticmethod
    def get_status_distribution(db: Session,user_id: int):
        return (
            db.query(Document.embedding_status,
                     func.count(Document.id)).filter(Document.user_id == user_id).group_by(Document.embedding_status).all()
        )                    

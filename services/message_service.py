
from sqlalchemy.orm import Session
from repositories.message_repository import MessageRepository
from models.message import MessageRole

class MessageService:

    @staticmethod
    def create(db: Session,conversation_id: int,role: MessageRole,content: str):
        return MessageRepository.create(
            db=db,
            conversation_id=conversation_id,
            role=role,
            content=content
        )
    
    @staticmethod
    def get_history(
        db: Session,
        conversation_id: int
    ):

        return MessageRepository.get_by_conversation(
            db=db,
            conversation_id=conversation_id
        )
from sqlalchemy.orm import Session
from models.message import Message , MessageRole

class MessageRepository:

    @staticmethod
    def create(db:Session, conversation_id: int,role: MessageRole,content: str) -> Message:

        message = Message(conversation_id = conversation_id,role = role, message = content)

        db.add(message)
        db.commit()
        db.refresh(message)

        return message
    
    @staticmethod
    def get_by_conversation(db:Session, conversation_id:int):

        return (
            db.query(Message).filter(
                Message.conversation_id == conversation_id
            ).order_by(Message.timestamp.asc()).all()
        )
    
    @staticmethod
    def delete_all(
        db: Session,
        conversation_id: int
    ):

        (
            db.query(Message)
            .filter(
                Message.conversation_id == conversation_id
            )
            .delete()
        )

        db.commit()

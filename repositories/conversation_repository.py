
from sqlalchemy.orm import Session
from models.conversation import Conversation

class ConversationRepository:

    @staticmethod
    def create(
        db:Session,
        user_id:int,
        document_id:int,
        title:str
    ) -> Conversation:
        
        conversation = Conversation(
            user_id = user_id,
            document_id = document_id,
            title=title
        )

        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        return conversation

    @staticmethod
    def get_by_document(db:Session,user_id: int, document_id : int) -> Conversation |None:
        return (db.query(Conversation).filter(
            Conversation.user_id == user_id,
            Conversation.document_id == document_id
        ).first())

    @staticmethod
    def get_by_id(db:Session,conversation_id:int) -> Conversation | None:
        return (
            db.query(Conversation).filter(
                Conversation.id == conversation_id
            ).first()
        )
          

    @staticmethod
    def delete(db : Session, conversation: Conversation) -> None:
            db.delete(conversation)
            db.commit()
           
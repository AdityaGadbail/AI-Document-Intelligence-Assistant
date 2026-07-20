
from sqlalchemy.orm import Session

from repositories.conversation_repository import ConversationRepository

class ConversationService:

    @staticmethod
    def generate_title(question : str) -> str:

        question = question.strip()

        if len(question) <= 50:
            return question

        return question[:47] + "..."    

    @classmethod
    def get_or_create(cls, db:Session,user_id:int,document_id:int,first_question: str):

        conversation = ConversationRepository.get_by_document(db = db, user_id = user_id, document_id = document_id)    

        if conversation:
            return conversation

        title = cls.generate_title(first_question)            

        return ConversationRepository.create(db = db, user_id = user_id, document_id = document_id,title=title)

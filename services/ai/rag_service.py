
from sqlalchemy.orm import Session

from services.conversation_service import ConversationService
from services.message_service import MessageService
from models.message import MessageRole
from services.ai.gemini_service import GeminiService
from services.ai.retrieval_service import RetrievalService

class RagService:

    @classmethod
    def ask(cls, db:Session, user_id: int, document_id:int, question:str):

        conversation = ConversationService.get_or_create(
        db=db,
        user_id=user_id,
        document_id=document_id,
        first_question=question
        )

        MessageService.create(
    db=db,
    conversation_id=conversation.id,
    role=MessageRole.USER,
    content=question
)

        chunks = RetrievalService.retrieve(document_id=document_id,question=question)

        context = "\n\n".join(
            chunk["text"]
            for chunk in chunks
        )


        prompt = f"""
        You are an AI assistant.

        Answer ONLY using the provided document context.

        If the answer is not present in the document,
        reply exactly:

        "I couldn't find this information in the uploaded document."

        -------------------------
        Document Context
        -------------------------
        {context}

        -------------------------
        Question
        -------------------------
        {question}
        """
    
        answer = GeminiService.generate_answer(prompt)

        MessageService.create(
    db=db,
    conversation_id=conversation.id,
    role=MessageRole.ASSISTANT,
    content=answer
)

        return {
    "conversation_id": conversation.id,
    "answer": answer,
    "sources": chunks
}
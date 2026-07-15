
from sqlalchemy.orm import Session
from models.document import Document

class DocumentRepository:

    @staticmethod
    def create_document(db:Session,**document_data)-> Document:

        document = Document(**document_data)
        db.add(document)
        db.commit()
        db.refresh(document)

        return document

    @staticmethod
    def get_document_by_id(db:Session,document_id : int) -> Document | None:
        return (db.query(Document).filter(Document.id == document_id).first())

    @staticmethod
    def get_documents_by_user(db:Session,user_id:int)->list[Document]:
        return (db.query(Document).filter(Document.user_id == user_id).all())

    @staticmethod
    def delete_document(db:Session,document:Document):
        db.delete(document)
        db.commit()

    @staticmethod
    def update_status(db:Session,document:Document,status:str) -> Document:

        document.embedding_status = status
        db.commit()
        db.refresh(document)
        return {
        "success": True,
        "message": "Document uploaded successfully.",
        "document": document,
         }

    @staticmethod
    def count_documents(db:Session,user_id:int)->int:
        return (db.query(Document).filter(Document.user_id == user_id).count())

    @staticmethod
    def get_ready_documents(db:Session,user_id:int)->list[Document]:
        return (
            db.query(Document).filter(
                Document.user_id == user_id,
                Document.embedding_status == "READY"
            ).all()
        )    

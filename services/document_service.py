from pathlib import Path
from sqlalchemy.orm import Session

from models.document import EmbeddingStatus
from repositories.document_repository import DocumentRepository
from storage.storage_service import StorageService

from services.processing.vectorstore.vector_store import VectoreStore

from config.settings import MAX_UPLOAD_SIZE
from config.settings import ALLOWED_EXTENSIONS

class DocumentService:

    @classmethod
    def upload_document(cls,db:Session,uploaded_file,user_id:int):
        from services.processing.pipeline.document_processor import DocumentProcessor
        
        cls.validate_file(uploaded_file)
        file_info = StorageService.save_file(uploaded_file)
        document = DocumentRepository.create_document(
            db,
            user_id = user_id,
            original_filename = file_info["original_filename"],
            stored_filename = file_info["stored_filename"],
            file_path = file_info["file_path"],
            file_size = file_info["file_size"],
            mime_type = file_info["mime_type"],
            embedding_status = EmbeddingStatus.UPLOADED
            )
        
        DocumentProcessor.process(db=db,document=document)
        return document
    

    @classmethod
    def validate_file(cls,uploaded_file):
        if uploaded_file is None:
            raise ValueError("Please select a PDF file.")

        extension = Path(uploaded_file.name).suffix.lower()
        mime_type = getattr(uploaded_file, "type", "").lower()

        allowed_extensions = {
            ext.lower().strip()
            for ext in ALLOWED_EXTENSIONS
        }

        if extension not in allowed_extensions and mime_type != "application/pdf":
            raise ValueError(
                f"Only PDF files are allowed. Got name='{uploaded_file.name}', "
                f"extension='{extension}', type='{mime_type}'."
            )
        
        if uploaded_file.size > MAX_UPLOAD_SIZE:
            raise ValueError("File size cannot exceed 20 MB.")
        
    @staticmethod
    def get_user_documents(db:Session,user_id:int):

        return DocumentRepository.get_by_user(db=db,user_id=user_id) 

    @staticmethod
    def delete_document(db:Session,document_id: int,user_id: int):

        document = DocumentRepository.get_document_by_id(db = db,document_id = document_id)

        if document is None:
            raise ValueError("Document not found.")
        if document.user_id != user_id:
            raise PermissionError("Unauthorized.")

        StorageService.delete_file(document.file_path) 
        VectoreStore.delete(document_id=document.id)  
        DocumentRepository.delete_document(db=db,document=document)

        
        
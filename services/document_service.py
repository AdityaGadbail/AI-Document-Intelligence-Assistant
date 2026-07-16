from pathlib import Path
from sqlalchemy.orm import Session

from models.document import EmbeddingStatus
from repositories.document_repository import DocumentRepository
from storage.storage_service import StorageService
from config.settings import MAX_UPLOAD_SIZE

class DocumentService:

    ALLOWED_EXTENSIONS = {".pdf"}

    # MAX_FILE_SIZE = 20 * 1024 * 1024

    @classmethod
    def upload_document(cls,db:Session,uploaded_file,user_id:int):

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
        return document
    

    @classmethod
    def validate_file(cls,uploaded_file):
        if uploaded_file is None:
            raise ValueError("Please select a PDF file.")

        extension = Path(uploaded_file.name).suffix.lower()
         
        if extension not in cls.ALLOWED_EXTENSIONS:
            raise ValueError("Only PDF files are allowed.")
        
        if uploaded_file.size > MAX_UPLOAD_SIZE:
            raise ValueError("File size cannot exceed 20 MB.")
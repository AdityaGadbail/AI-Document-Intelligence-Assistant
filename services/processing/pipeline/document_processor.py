
from sqlalchemy.orm import Session

from models.document import Document, EmbeddingStatus
from repositories.document_repository import DocumentRepository

from services.processing.pdf_extractor import PDFExtractor 
from services.processing.text_cleaner import TextCleaner
from services.processing.text_chunker import TextChunker
from services.processing.embedding.embedding_service import EmbeddingService
from services.processing.vectorstore.vector_store import  VectoreStore


class DocumentProcessor:

    @classmethod
    def process(cls,db:Session,document:Document):

        document.embedding_status = EmbeddingStatus.PROCESSING
        db.commit()

        # Extract
        extraction_result = PDFExtractor.extract_pdf(document.file_path)

        # Save Statistics
        DocumentRepository.update_document_statistics(db,document,extraction_result)

        # Clean Text
        cleaned_text = TextCleaner.clean(extraction_result.text)

        # Split Into Chunks
        chunks = TextChunker.split(cleaned_text)

        # Generate Embeddings 
        embeddings = EmbeddingService.generate_embeddings(chunks)

        # Save Into Faiss
        VectoreStore.save(document_id=document.id,embeddings=embeddings,chunks=chunks)

        document.embedding_status = EmbeddingStatus.READY
        db.commit()

        return document



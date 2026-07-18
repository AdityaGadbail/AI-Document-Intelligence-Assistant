
from services.processing.embedding.embedding_service import EmbeddingService
from services.processing.vectorstore.vector_store import VectoreStore

class RetrievalService:

    @classmethod
    def retrieve(cls,document_id:int,question:str,top_k:int = 5):

        query_embedding = EmbeddingService.generate_embedding(question)

        score, indices = VectoreStore.search(document_id=document_id,query_embedding=query_embedding,top_k=top_k)

        chunk_data = VectoreStore.load_chunk_data(document_id)

        results = []

        for score, index in zip(score,indices):
            if index == -1:
                continue

            chunk = chunk_data[index]

            results.append({
                "chunk_id":chunk["chunk_id"],
                "text":chunk["text"],
                "score":float(score)
            })

        return results           


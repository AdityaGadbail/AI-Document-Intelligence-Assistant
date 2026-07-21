from pathlib import Path
import faiss
import numpy as np
import json
import shutil

from config.settings import VECTOR_STORE_DIRECTORY

class VectoreStore:

    @staticmethod
    def save(document_id:int,embeddings:list[list[float]],chunks:list[str]):
        document_directory =Path(VECTOR_STORE_DIRECTORY)/ f"doc_{document_id}"
        
        document_directory.mkdir(parents=True,exist_ok=True)

        vectors = np.array(embeddings,dtype="float32")

        dimension = vectors.shape[1]

        index = faiss.IndexFlatIP(dimension)
        index.add(vectors)

        faiss.write_index(index,str(document_directory / "index.faiss"))

        chunk_data = []

        for index_number , chunk in enumerate(chunks):
            chunk_data.append({
                "chunk_id":index_number,
                "text": chunk
            })

        with open(document_directory / "chunks.json","w",encoding="utf-8") as file:
            json.dump(chunk_data,file,indent=4,ensure_ascii=False)    

        metadata = {
            "document_id":document_id,
            "dimension": dimension,
            "total_chunks" :len(chunks)
        }            
        
        with open(document_directory / "metadata.json", "w", encoding="utf-8") as file:
            json.dump(metadata,file,indent=4)

    @staticmethod
    def load(document_id:int):

        directory = Path(VECTOR_STORE_DIRECTORY) / f"doc_{document_id}"
        return faiss.read_index(str(directory / "index.faiss"))

    # @staticmethod
    # def load_chunks(document_id:int):
    #     directory = (
    #         Path(VECTOR_STORE_DIRECTORY) / f"doc_{document_id}"
    #     )    

    #     with open(directory /"chunks.json","r",encoding="utf-8") as file:
    #         return json.load(file)
    @staticmethod
    def load_chunk_data(document_id:int):
        directory = Path(VECTOR_STORE_DIRECTORY) / f"doc_{document_id}"
            

        with open(directory /"chunks.json","r",encoding="utf-8") as file:
            return json.load(file)


    @staticmethod
    def search(document_id:int,query_embedding:list[float],top_k:int =5):

        directory =Path(VECTOR_STORE_DIRECTORY) / f"doc_{document_id}"
            

        index = faiss.read_index(
            str(directory / "index.faiss")
        )        
        
        query = np.array(
            [query_embedding],
            dtype="float32"
        )

        scores, indices = index.search(query,top_k) 

        return scores[0].tolist(),indices[0].tolist()
    
    @staticmethod
    def delete(document_id:int):
        directory = (Path(VECTOR_STORE_DIRECTORY)/ f"doc_{document_id}")

        if directory.exists():

            shutil.rmtree(directory)
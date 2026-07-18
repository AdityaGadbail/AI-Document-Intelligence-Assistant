from sentence_transformers import SentenceTransformer
from config.settings import EMBEDDING_MODEL

class EmbeddingService:

    _model = None


    @classmethod
    def get_model(cls):
        if cls._model is None:
            cls._model = SentenceTransformer(EMBEDDING_MODEL)

        return cls._model 

    @classmethod
    def generate_embedding(cls,text:str)->list[str]:
        model = cls.get_model()  
        
        embedding = model.encode(
            text,
            convert_to_numpy = True,
            normalize_embeddings = True
        )

        return embedding.tolist()
    

    @classmethod
    def generate_embeddings(cls,texts : list[str])->list[list[float]]:

        model = cls.get_model()

        embeddings = model.encode(
            texts,
            convert_to_numpy= True,
            normalize_embeddings= True
        )

        return embeddings.tolist()
    




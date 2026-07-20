
import google.generativeai as genai

from config.settings import (GEMINI_API_KEY,GEMINI_MODEL)

class GeminiService:

    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:

            genai.configure(GEMINI_API_KEY)
            cls._model =  genai.GenerativeModel(GEMINI_MODEL)

            return cls._model

    @classmethod
    def generate_answer(cls,prompt:str) -> str:            
        model = cls.get_model()

        response = model.generate_content(prompt)
        return response.text

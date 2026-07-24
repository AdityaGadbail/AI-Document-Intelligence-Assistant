
import google.generativeai as genai

from config.settings import (GEMINI_MODEL,GEMINI_API_KEY)
class GeminiService:
    
    _model = None

    @classmethod
    def get_model(cls):
        if cls._model is None:

            if not GEMINI_API_KEY:
                raise ValueError(
                "Gemini API key missing"
            )
            genai.configure(api_key=GEMINI_API_KEY)
            cls._model =  genai.GenerativeModel(GEMINI_MODEL)

        return cls._model

    @classmethod
    def generate_answer(cls,prompt:str) -> str:            
        model = cls.get_model()

        response = model.generate_content(prompt)
        return response.text

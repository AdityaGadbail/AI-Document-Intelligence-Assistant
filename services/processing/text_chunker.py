from langchain_text_splitters import RecursiveCharacterTextSplitter
from config.settings import (CHUNK_OVERLAP , CHUNK_SIZE)

class TextChunker:

    splitter = RecursiveCharacterTextSplitter(
        chunk_size = CHUNK_SIZE,
        chunk_overlap = CHUNK_OVERLAP,
        separators = [
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    @classmethod
    def split(cls,text:str)-> list[str]:
        return cls.splitter.split_text(text)
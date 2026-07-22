import os
from dotenv import load_dotenv
from pathlib import Path

# load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent / ".env", override=True)
MAX_UPLOAD_SIZE = int(os.getenv("MAX_UPLOAD_SIZE",20971520))

CHUNK_SIZE = int(
    os.getenv("CHUNK_SIZE", 1000)
)

CHUNK_OVERLAP = int(
    os.getenv("CHUNK_OVERLAP", 200)
)

UPLOAD_DIRECTORY = os.getenv(
    "UPLOAD_DIRECTORY",
    "storage/uploads"
)

ALLOWED_EXTENSIONS = [
    ext.strip().lower()
    for ext in os.getenv("ALLOWED_EXTENSIONS", ".pdf").split(",")
    if ext.strip()
]



EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

VECTOR_STORE_DIRECTORY = os.getenv(
    "VECTOR_STORE_DIRECTORY",
    "storage/vector_store"
)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")


GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)

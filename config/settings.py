import os
from dotenv import load_dotenv

load_dotenv()

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

ALLOWED_EXTENSIONS = os.getenv(
    "ALLOWED_EXTENSIONS",
    [".pdf"]
)

EMBEDDING_MODEL = os.getenv(
    "EMBEDDING_MODEL",
    "all-MiniLM-L6-v2"
)

VECTOR_STORE_DIRECTORY = os.getenv(
    "VECTOR_STORE_DIRECTORY",
    "storage/vector_store"
)
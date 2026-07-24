

from pathlib import Path
from uuid import uuid4
import shutil

class StorageService:

    STORAGE_DIR = Path("storage")
    UPLOAD_DIR = STORAGE_DIR / "uploads"

    @classmethod
    def initialize_storage(cls):
        cls.UPLOAD_DIR.mkdir(parents=True,exist_ok=True)

    @classmethod
    def generate_filename(cls,original_filename:str) -> str:

        extension = Path(original_filename).suffix
        return f"{uuid4().hex}{extension}"

    @classmethod
    def save_file(cls,uploaded_file):
        cls.initialize_storage()

        stored_filename = cls.generate_filename(uploaded_file.name)    

        file_path = cls.UPLOAD_DIR / stored_filename

        with open(file_path,"wb") as destination :
            shutil.copyfileobj(uploaded_file,destination)

        return {
            "original_filename": uploaded_file.name,
            "stored_filename":stored_filename,
            "file_path":str(file_path),
            "file_size":file_path.stat().st_size,
            "mime_type":uploaded_file.type,
        } 

    @classmethod
    def delete_file(cls,file_path:str):
        path = Path(file_path)   

        if path.exists():
            path.unlink()

    @classmethod
    def file_exist(cls,file_path:str):
        return Path(file_path).exists()
               

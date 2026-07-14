import re

# from email_validator import validate_email, EmailNotValidError

from sqlalchemy.orm import Session

from authentication.password import PasswordManager
from models.user import User
from repositories.user_repository import UserRepository



class AuthService:

    @staticmethod
    def register_user(db:Session,username:str,email:str,password:str):

        # Check username
        if UserRepository.get_user_by_username(db,username):
            raise ValueError("Username already exists.")
        
        # Check email
        if UserRepository.get_user_by_email(db,email):
            raise ValueError("Email already exists.")

        # Hash Password
        hashed_password = PasswordManager.hash_password(password)

        # Going to creat the user 

        user = User(username = username, email = email, password_hash = hashed_password)

        return UserRepository.create_user(db,user)
    

    @staticmethod
    def login_user(db:Session, email:str, password:str):

        user = UserRepository.get_user_by_email(db,email)

        if not user:
            return None

        if not PasswordManager.verify_password(password,user.password_hash):
            return None

        return user    

 


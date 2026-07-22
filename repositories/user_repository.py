from sqlalchemy.orm import Session
from models.user import User

class UserRepository:

     @staticmethod
     def create_user(db: Session, user: User):
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

     @staticmethod
     def get_user_by_email(db: Session, email: str):
        return (
            db.query(User)
            .filter(User.email == email)
            .first()
        )

     @staticmethod
     def get_user_by_username(db: Session, username: str):
        return (
            db.query(User)
            .filter(User.username == username)
            .first()
        )

     @staticmethod
     def get_user_by_id(db: Session, user_id: int):
        return (
            db.query(User)
            .filter(User.id == user_id)
            .first()
        )

     @staticmethod
     def delete_user(db: Session, user: User):
        db.delete(user)
        db.commit()
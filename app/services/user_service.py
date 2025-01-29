from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User

def create_user(db: Session, name: str, email: str, password: str):
    password_hash = bcrypt.hash(password)
    user = User(name=name, email=email, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if user and bcrypt.verify(password, user.password_hash):
        return user
    return None

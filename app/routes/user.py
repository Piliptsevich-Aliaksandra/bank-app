from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.user import UserCreateSchema, UserLoginSchema
from app.services.user_service import create_user, authenticate_user
from app.auth.token import create_access_token

router = APIRouter()

@router.post("/register")
def register_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    user_db = create_user(db, user.name, str(user.email), user.password)
    return user_db

@router.post("/login")
def login_user(user: UserLoginSchema, db: Session = Depends(get_db)):
    user = authenticate_user(db, str(user.email), user.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"id": user.id, "name": user.name, "email": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

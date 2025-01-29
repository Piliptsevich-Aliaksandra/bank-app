from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.auth.token import get_current_user
from app.schemas.account import AccountCreateSchema
from app.services.account_service import create_account, get_account, delete_account, get_accounts_by_owner

router = APIRouter()

@router.post("/")
def create_new_account(account: AccountCreateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return create_account(db, current_user["id"], account.name, float(account.balance))

@router.get("/owner")
def get_owner_accounts(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_accounts_by_owner(db, current_user["id"])

@router.get("/{account_id}")
def get_account_details(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_account(db, account_id, current_user["id"])

@router.delete("/{account_id}")
def delete_account_by_id(account_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return delete_account(db, account_id, current_user["id"])

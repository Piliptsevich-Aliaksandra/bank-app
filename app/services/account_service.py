from sqlalchemy.orm import Session
from app.models.account import Account
from fastapi import HTTPException


def create_account(db: Session, user_id: int, name: str, balance: float):
    new_account = Account(user_id=user_id, name=name, balance=balance)
    db.add(new_account)
    db.commit()
    db.refresh(new_account)
    return new_account


def get_account(db: Session, account_id: int, user_id: int):
    account = db.query(Account).filter(Account.id == account_id and Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account


def get_accounts_by_owner(db: Session, user_id: int):
    return db.query(Account).filter(Account.user_id == user_id).all()


def delete_account(db: Session, account_id: int, user_id: int):
    account = db.query(Account).filter(Account.id == account_id and Account.user_id == user_id).first()
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")

    db.delete(account)
    db.commit()
    return {"detail": "Account deleted successfully"}

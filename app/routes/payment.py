from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db

from app.auth.token import get_current_user
from app.metrics import payment_counter
from app.schemas.payment import PaymentCreateSchema
from app.services.payment_service import create_payment, get_payment, get_income_payments, get_outcome_payments

router = APIRouter()

@router.get("/income")
def get_income_payments_for_account(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_income_payments(db, current_user["id"])

@router.get("/outcome")
def get_outcome_payments_for_account(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_outcome_payments(db, current_user["id"])

@router.post("/")
def create_new_payment(payment: PaymentCreateSchema, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    payment_counter.inc()
    return create_payment(db, payment.from_account, payment.to_account, float(payment.amount), current_user["id"], current_user["email"])

@router.get("/{payment_id}")
def get_payment_details(payment_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    return get_payment(db, payment_id, current_user["id"])
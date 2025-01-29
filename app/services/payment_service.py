from sqlalchemy.orm import Session

from app.models.account import Account
from app.models.payment import Payment
from fastapi import HTTPException


def create_payment(db: Session, remitter_account_id: int, beneficiary_account_id: int, amount: float, user_id: int, email: str):
    if amount <= 0:
        raise HTTPException(status_code=400, detail="Amount must be greater than zero")

    if remitter_account_id == beneficiary_account_id:
        raise HTTPException(status_code=400, detail="Remitter and beneficiary accounts must be different")

    remitter_account = db.query(Account).filter(
        Account.id == remitter_account_id and Account.user_id == user_id).first()
    beneficiary_account = db.query(Account).filter(Account.id == beneficiary_account_id).first()

    if not remitter_account or not beneficiary_account:
        raise HTTPException(status_code=404, detail="One or both accounts not found")

    if remitter_account.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    remitter_account.balance -= amount
    beneficiary_account.balance += amount

    payment = Payment(
        remitter_account_id=remitter_account_id,
        beneficiary_account_id=beneficiary_account_id,
        amount=amount
    )
    db.add(payment)
    db.commit()
    db.refresh(payment)

    # payment_data = {
    #     'user_email': email,
    #     'payment_id': payment.id,
    #     'amount': amount
    # }
    # send_payment_event(payment_data)

    return payment


def get_payment(db: Session, payment_id: int, user_id: int):
    payment = (db.query(Payment)
               .join(Account,
                     (Account.id == Payment.remitter_account_id) | (Account.id == Payment.beneficiary_account_id))
               .filter(Payment.id == payment_id)
               .filter(Account.user_id == user_id).first())

    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    return payment


def get_outcome_payments(db: Session, user_id: int):
    payments = (db.query(Payment)
               .join(Account,
                     (Account.id == Payment.remitter_account_id))
               .filter(Account.user_id == user_id).all())
    return payments


def get_income_payments(db: Session, user_id: int):
    payments = (db.query(Payment)
                .join(Account,
                      (Account.id == Payment.beneficiary_account_id))
                .filter(Account.user_id == user_id).all())
    return payments

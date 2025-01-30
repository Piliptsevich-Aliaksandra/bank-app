import json
import pika
from sqlalchemy.orm import Session

from app.logging_config import logger
from app.metrics import successful_payment_counter
from app.models.account import Account
from app.models.payment import Payment
from fastapi import HTTPException


RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"


def send_payment_receipt_to_queue(payment_id: int, email: str):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue="payment_receipts", durable=True)

    message = json.dumps({"payment_id": payment_id, "email": email})
    channel.basic_publish(exchange='', routing_key="payment_receipts", body=message)

    logger.info("Message sent to queue", payment_id=payment_id, email=email)

    connection.close()


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

    successful_payment_counter.inc()

    send_payment_receipt_to_queue(payment.id, email)

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

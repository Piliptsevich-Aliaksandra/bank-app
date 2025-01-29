import pytest
from fastapi import HTTPException

from app.services.account_service import create_account
from app.services.payment_service import create_payment, get_payment, get_outcome_payments, get_income_payments
from app.services.user_service import create_user
from sqlalchemy.orm import Session


@pytest.mark.usefixtures("setup_db")
def test_create_payment(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    account1 = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)
    account2 = create_account(db, user_id=user.id, name="Test Account 2", balance=0.0)

    payment = create_payment(db, remitter_account_id=account1.id, beneficiary_account_id=account2.id, user_id=user.id, amount=100.0, email="aaa@aaa.com")
    assert payment.id is not None
    assert payment.remitter_account_id == account1.id
    assert payment.beneficiary_account_id == account2.id
    assert payment.amount == 100.0
    assert account1.balance == 400.0
    assert account2.balance == 100.0

@pytest.mark.usefixtures("setup_db")
def test_payment_with_negative_amount(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    account1 = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)
    account2 = create_account(db, user_id=user.id, name="Test Account 2", balance=0.0)

    with pytest.raises(HTTPException) as excinfo:
        create_payment(db, remitter_account_id=account1.id, beneficiary_account_id=account2.id, user_id=user.id, amount=-100.0, email="aaa@aaa.com")

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Amount must be greater than zero"


@pytest.mark.usefixtures("setup_db")
def test_payment_to_the_same_account(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")

    with pytest.raises(HTTPException) as excinfo:
        create_payment(db, remitter_account_id=1, beneficiary_account_id=1, user_id=user.id, amount=100.0, email="aaa@aaa.com")

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Remitter and beneficiary accounts must be different"


@pytest.mark.usefixtures("setup_db")
def test_payment_when_accounts_not_found(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")

    with pytest.raises(HTTPException) as excinfo:
        create_payment(db, remitter_account_id=1, beneficiary_account_id=2, user_id=user.id, amount=100.0, email="aaa@aaa.com")

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "One or both accounts not found"


@pytest.mark.usefixtures("setup_db")
def test_payment_with_insufficient_funds(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    account1 = create_account(db, user_id=user.id, name="Test Account 1", balance=200.0)
    account2 = create_account(db, user_id=user.id, name="Test Account 2", balance=0.0)

    with pytest.raises(HTTPException) as excinfo:
        create_payment(db, remitter_account_id=account1.id, beneficiary_account_id=account2.id, user_id=user.id, amount=250.0, email="aaa@aaa.com")

    assert excinfo.value.status_code == 400
    assert excinfo.value.detail == "Insufficient funds"


@pytest.mark.usefixtures("setup_db")
def test_get_payment(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    account1 = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)
    account2 = create_account(db, user_id=user.id, name="Test Account 2", balance=0.0)

    created_payment = create_payment(db, remitter_account_id=account1.id, beneficiary_account_id=account2.id, user_id=user.id, amount=100.0, email="aaa@aaa.com")

    payment = get_payment(db, user_id=user.id, payment_id=created_payment.id)
    assert payment is not None
    assert payment == created_payment


@pytest.mark.usefixtures("setup_db")
def test_get_payment_not_found(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")

    with pytest.raises(HTTPException) as excinfo:
        get_payment(db, user_id=user.id, payment_id=1)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Payment not found"


@pytest.mark.usefixtures("setup_db")
def test_get_outcome_payments(db: Session):
    user1 = create_user(db, name="Test User 1", email="testuser1@example.com", password="securepassword")
    user2 = create_user(db, name="Test User 2", email="testuser2@example.com", password="securepassword")
    account1 = create_account(db, user_id=user1.id, name="Test Account 1", balance=500.0)
    account2 = create_account(db, user_id=user2.id, name="Test Account 2", balance=0.0)

    created_payment = create_payment(db, remitter_account_id=account1.id, beneficiary_account_id=account2.id, user_id=user1.id, amount=100.0, email="aaa@aaa.com")

    payments = get_outcome_payments(db, user_id=user1.id)
    assert payments is not None
    assert payments == [created_payment]


@pytest.mark.usefixtures("setup_db")
def test_get_income_payments(db: Session):
    user1 = create_user(db, name="Test User 1", email="testuser1@example.com", password="securepassword")
    user2 = create_user(db, name="Test User 2", email="testuser2@example.com", password="securepassword")
    account1 = create_account(db, user_id=user1.id, name="Test Account 1", balance=500.0)
    account2 = create_account(db, user_id=user2.id, name="Test Account 2", balance=0.0)

    created_payment = create_payment(db, remitter_account_id=account1.id, beneficiary_account_id=account2.id, user_id=user1.id, amount=100.0, email="aaa@aaa.com")

    payments = get_income_payments(db, user_id=user2.id)
    assert payments is not None
    assert payments == [created_payment]

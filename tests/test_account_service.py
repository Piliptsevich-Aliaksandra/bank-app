import pytest
from fastapi import HTTPException
from sqlalchemy.orm import Session

from app.services.account_service import create_account, get_account, get_accounts_by_owner, delete_account
from app.services.user_service import create_user


@pytest.mark.usefixtures("setup_db")
def test_create_account(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    account = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)
    assert account.id is not None
    assert account.number is not None
    assert account.name == "Test Account 1"
    assert account.user_id == user.id
    assert account.balance == 500.0


@pytest.mark.usefixtures("setup_db")
def test_get_account(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    created_account = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)

    account = get_account(db, account_id=created_account.id, user_id=user.id)
    assert account == created_account


@pytest.mark.usefixtures("setup_db")
def test_get_account_not_found(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")

    with pytest.raises(HTTPException) as excinfo:
        get_account(db, account_id=1, user_id=user.id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Account not found"

@pytest.mark.usefixtures("setup_db")
def test_get_accounts_by_owner(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    created_account = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)

    accounts = get_accounts_by_owner(db, user_id=user.id)
    assert accounts == [created_account]


@pytest.mark.usefixtures("setup_db")
def test_delete_account(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    created_account = create_account(db, user_id=user.id, name="Test Account 1", balance=500.0)

    result = delete_account(db, account_id=created_account.id, user_id=user.id)
    assert result["detail"] == "Account deleted successfully"


@pytest.mark.usefixtures("setup_db")
def test_delete_account_not_found(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")

    with pytest.raises(HTTPException) as excinfo:
        delete_account(db, account_id=1, user_id=user.id)

    assert excinfo.value.status_code == 404
    assert excinfo.value.detail == "Account not found"
import pytest
from pydantic import ValidationError

from app.schemas.account import AccountCreateSchema


def test_account_create_schema_valid():
    account_data = {
        "name": "account_name",
        "balance": 100.0
    }

    account = AccountCreateSchema(**account_data)

    assert account.name == account_data["name"]
    assert account.balance == account_data["balance"]


def test_account_create_schema_invalid_amount():
    account_data = {
        "name": "account_name",
        "balance": -100.0
    }

    with pytest.raises(ValidationError):
        AccountCreateSchema(**account_data)

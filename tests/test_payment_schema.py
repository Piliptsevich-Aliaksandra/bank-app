import pytest
from pydantic import ValidationError

from app.schemas.payment import PaymentCreateSchema


def test_payment_create_schema_valid():
    payment_data = {
        "from_account": 1,
        "to_account": 2,
        "amount": 100.0
    }

    payment = PaymentCreateSchema(**payment_data)

    assert payment.from_account == payment_data["from_account"]
    assert payment.to_account == payment_data["to_account"]
    assert payment.amount == payment_data["amount"]


def test_payment_create_schema_invalid_amount():
    payment_data = {
        "from_account": 1,
        "to_account": 2,
        "amount": -10.0
    }

    with pytest.raises(ValidationError):
        PaymentCreateSchema(**payment_data)

from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywibmFtZSI6InN0cmluZyIsImVtYWlsIjoidXNlcjFAZXhhbXBsZS5jb20iLCJleHAiOjE3MzgxNzk1Njl9.9uadxgXM0H8wKvCeA4ApCoSXK_vsk-FkEA_iGPkLRZM"


@patch('app.routes.payment.get_income_payments')
@patch('app.auth.token.decode_access_token')
def test_get_income_payments(mock_decode_access_token, mock_get_income_payments):
    mock_user = {"id": 1, "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_get_income_payments.return_value = [{"id": 1, "amount": 50.0, "from_account_id": 2, "to_account_id": 1}]

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.get("/payments/income", headers=headers)

    mock_get_income_payments.assert_called_once()

    args, kwargs = mock_get_income_payments.call_args

    assert args[1] == mock_user["id"]

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "amount": 50.0, "from_account_id": 2, "to_account_id": 1}]


@patch('app.routes.payment.get_outcome_payments')
@patch('app.auth.token.decode_access_token')
def test_get_outcome_payments(mock_decode_access_token, mock_get_outcome_payments):
    mock_user = {"id": 1, "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_get_outcome_payments.return_value = [{"id": 2, "amount": 30.0, "from_account_id": 1, "to_account_id": 3}]

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.get("/payments/outcome", headers=headers)

    mock_get_outcome_payments.assert_called_once()

    args, kwargs = mock_get_outcome_payments.call_args

    assert args[1] == mock_user["id"]

    assert response.status_code == 200
    assert response.json() == [{"id": 2, "amount": 30.0, "from_account_id": 1, "to_account_id": 3}]


@patch('app.routes.payment.create_payment')
@patch('app.auth.token.decode_access_token')
def test_create_payment(mock_decode_access_token, mock_create_payment):
    mock_user = {"id": 1, "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_create_payment.return_value = {"id": 3, "amount": 20.0, "from_account_id": 1, "to_account_id": 2}

    payment_data = {
        "from_account": 1,
        "to_account": 2,
        "amount": 20.0
    }

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.post("/payments", json=payment_data, headers=headers)

    mock_create_payment.assert_called_once()

    args, kwargs = mock_create_payment.call_args

    assert args[1] == payment_data["from_account"]
    assert args[2] == payment_data["to_account"]
    assert args[3] == payment_data["amount"]
    assert args[4] == mock_user["id"]
    assert args[5] == mock_user["email"]

    assert response.status_code == 200
    assert response.json() == {"id": 3, "amount": 20.0, "from_account_id": 1, "to_account_id": 2}


@patch('app.routes.payment.get_payment')
@patch('app.auth.token.decode_access_token')
def test_get_payment_details(mock_decode_access_token, mock_get_payment):
    mock_user = {"id": 1, "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_get_payment.return_value = {"id": 4, "amount": 40.0, "from_account_id": 1, "to_account_id": 3}

    payment_id = 4

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.get(f"/payments/{payment_id}", headers=headers)

    mock_get_payment.assert_called_once()

    args, kwargs = mock_get_payment.call_args

    assert args[1] == payment_id
    assert args[2] == mock_user["id"]

    assert response.status_code == 200
    assert response.json() == {"id": 4, "amount": 40.0, "from_account_id": 1, "to_account_id": 3}

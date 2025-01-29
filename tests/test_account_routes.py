from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NywibmFtZSI6InN0cmluZyIsImVtYWlsIjoidXNlcjFAZXhhbXBsZS5jb20iLCJleHAiOjE3MzgxNzk1Njl9.9uadxgXM0H8wKvCeA4ApCoSXK_vsk-FkEA_iGPkLRZM"


@patch('app.routes.account.create_account')
@patch('app.auth.token.decode_access_token')
def test_create_account(mock_decode_access_token, mock_create_account):
    mock_user = {"id": 1, "name": "Test User", "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_create_account.return_value = {"id": 1, "name": "Test Account", "balance": 100.0}

    account_data = {
        "name": "Test Account",
        "balance": 100.0
    }

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.post("/accounts", json=account_data, headers=headers)

    mock_create_account.assert_called_once()

    args, kwargs = mock_create_account.call_args

    assert args[1] == mock_user["id"]
    assert args[2] == account_data["name"]
    assert args[3] == account_data["balance"]

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Account", "balance": 100.0}


@patch('app.routes.account.get_accounts_by_owner')
@patch('app.auth.token.decode_access_token')
def test_get_owner_accounts(mock_decode_access_token, mock_get_accounts_by_owner):
    mock_user = {"id": 1, "name": "Test User", "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_get_accounts_by_owner.return_value = [
        {"id": 1, "name": "Test Account", "balance": 100.0}]

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.get("/accounts/owner", headers=headers)

    mock_get_accounts_by_owner.assert_called_once()

    args, kwargs = mock_get_accounts_by_owner.call_args

    assert args[1] == mock_user["id"]

    assert response.status_code == 200
    assert response.json() == [{"id": 1, "name": "Test Account", "balance": 100.0}]


@patch('app.routes.account.get_account')
@patch('app.auth.token.decode_access_token')
def test_get_account_details(mock_decode_access_token, mock_get_account):
    mock_user = {"id": 1, "name": "Test User", "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_get_account.return_value = {"id": 1, "name": "Test Account", "balance": 100.0}

    account_id = 1

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.get(f"/accounts/{account_id}", headers=headers)

    mock_get_account.assert_called_once()

    args, kwargs = mock_get_account.call_args

    assert args[1] == account_id
    assert args[2] == mock_user["id"]

    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "Test Account", "balance": 100.0}


@patch('app.routes.account.delete_account')
@patch('app.auth.token.decode_access_token')
def test_delete_account(mock_decode_access_token, mock_delete_account):
    mock_user = {"id": 1, "name": "Test User", "email": "testuser@example.com"}
    mock_decode_access_token.return_value = mock_user
    mock_delete_account.return_value = {"message": "Account deleted successfully"}  # Мокаем удаление аккаунта

    account_id = 1

    headers = {"Authorization": f"Bearer ${access_token}"}
    response = client.delete(f"/accounts/{account_id}", headers=headers)

    mock_delete_account.assert_called_once()

    args, kwargs = mock_delete_account.call_args

    assert args[1] == account_id
    assert args[2] == mock_user["id"]

    assert response.status_code == 200
    assert response.json() == {"message": "Account deleted successfully"}

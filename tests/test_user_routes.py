import datetime
from unittest.mock import patch
from fastapi.testclient import TestClient
from app.main import app
from app.models.user import User

client = TestClient(app)


@patch('app.routes.user.create_user')
def test_register_user(mock_create_user):
    mock_create_user.return_value = {
        'id': 1,
        'name': 'Test User',
        'email': 'testuser@example.com'
    }

    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    response = client.post("users/register", json=user_data)

    mock_create_user.assert_called_once()

    args, kwargs = mock_create_user.call_args

    assert args[1] == user_data["name"]
    assert args[2] == user_data["email"]
    assert args[3] == user_data["password"]

    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'Test User', 'email': 'testuser@example.com'}


@patch('app.routes.user.authenticate_user')
@patch('app.routes.user.create_access_token')
def test_login_user(mock_create_access_token, mock_authenticate_user):
    mock_user = User(id=1, name='Test User', email='testuser@example.com', password_hash="password_hash", created_at=datetime.datetime.utcnow())

    mock_authenticate_user.return_value = mock_user

    mock_access_token = "mock-access-token"
    mock_create_access_token.return_value = mock_access_token

    login_data = {
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    response = client.post("users/login", json=login_data)

    mock_authenticate_user.assert_called_once_with(mock_authenticate_user.call_args[0][0],  # db
                                                   login_data["email"],
                                                   login_data["password"])

    mock_create_access_token.assert_called_once_with(data={"id": mock_user.id,
                                                           "name": mock_user.name,
                                                           "email": mock_user.email})

    assert response.status_code == 200
    assert response.json() == {"access_token": mock_access_token, "token_type": "bearer"}


@patch('app.routes.user.authenticate_user')
@patch('app.routes.user.create_access_token')
def test_invalid_login_user(mock_create_access_token, mock_authenticate_user):
    mock_authenticate_user.return_value = None

    login_data = {
        "email": "wronguser@example.com",
        "password": "wrongpassword"
    }

    response = client.post("users/login", json=login_data)

    mock_authenticate_user.assert_called_once_with(mock_authenticate_user.call_args[0][0],  # db
                                                   login_data["email"],
                                                   login_data["password"])

    assert response.status_code == 401
    assert response.json() == {"detail": "Invalid credentials"}
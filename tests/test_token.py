import jwt
import pytest
from datetime import timedelta
from unittest.mock import MagicMock, patch
from fastapi import HTTPException
from app.auth.token import create_access_token, decode_access_token, get_current_user

SECRET_KEY = "secret-key"
ALGORITHM = "HS256"


def test_create_access_token():
    data = {"sub": "user1"}
    token = create_access_token(data, timedelta(minutes=5))
    decoded_data = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded_data["sub"] == "user1"
    assert "exp" in decoded_data


def test_decode_access_token_valid():
    data = {"sub": "user1"}
    token = create_access_token(data, timedelta(minutes=5))
    decoded_data = decode_access_token(token)

    assert decoded_data["sub"] == "user1"


def test_decode_access_token_expired():
    data = {"sub": "user1"}
    expired_token = create_access_token(data, timedelta(seconds=-1))  # Истекший токен

    with pytest.raises(ValueError, match="Token has expired"):
        decode_access_token(expired_token)


def test_decode_access_token_invalid():
    invalid_token = "invalid.token.string"

    with pytest.raises(ValueError, match="Invalid token"):
        decode_access_token(invalid_token)


@patch("app.auth.token.decode_access_token")
def test_get_current_user_valid(mock_decode):
    mock_decode.return_value = {"sub": "user1"}

    mock_token = MagicMock()
    mock_token.credentials = "valid.token"

    user = get_current_user(mock_token)

    assert user == {"sub": "user1"}
    mock_decode.assert_called_once_with("valid.token")


@patch("app.auth.token.decode_access_token", side_effect=ValueError("Invalid token"))
def test_get_current_user_invalid(mock_decode):
    mock_token = MagicMock()
    mock_token.credentials = "invalid.token"

    with pytest.raises(HTTPException) as exc_info:
        get_current_user(mock_token)

    assert exc_info.value.status_code == 401
    assert str(exc_info.value.detail) == "Invalid token"
    mock_decode.assert_called_once_with("invalid.token")

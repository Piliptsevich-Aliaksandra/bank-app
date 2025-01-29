import pytest
from pydantic import ValidationError

from app.schemas.user import UserCreateSchema


def test_user_create_schema_valid():
    user_data = {
        "name": "Test User",
        "email": "testuser@example.com",
        "password": "securepassword"
    }

    user = UserCreateSchema(**user_data)

    assert user.name == user_data["name"]
    assert user.email == user_data["email"]
    assert user.password == user_data["password"]


def test_user_create_schema_invalid_email():
    user_data = {
        "name": "Test User",
        "email": "invalid-email",
        "password": "securepassword"
    }

    with pytest.raises(ValidationError):
        UserCreateSchema(**user_data)

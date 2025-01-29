import pytest
from app.services.user_service import create_user, authenticate_user
from app.models.user import User
from sqlalchemy.orm import Session

# Подключаемся к базе данных
from tests.conftest import setup_db

@pytest.mark.usefixtures("setup_db")
def test_create_user(db: Session):
    user = create_user(db, name="Test User", email="testuser@example.com", password="securepassword")
    assert user.id is not None
    assert user.name == "Test User"
    assert user.email == "testuser@example.com"

@pytest.mark.usefixtures("setup_db")
def test_authenticate_user(db: Session):
    # Сначала создаем пользователя
    create_user(db, name="Test User", email="testuser@example.com", password="securepassword")

    # Проверяем аутентификацию
    user = authenticate_user(db, email="testuser@example.com", password="securepassword")
    assert user is not None
    assert user.email == "testuser@example.com"

    # Проверяем неудачную аутентификацию
    invalid_user = authenticate_user(db, email="testuser@example.com", password="wrongpassword")
    assert invalid_user is None

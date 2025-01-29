from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app, startup_event

client = TestClient(app)


@patch("app.main.init_db")
def test_startup_event(mock_init_db):
    startup_event()
    mock_init_db.assert_called_once()


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the banking system API!"}


def test_metrics():
    response = client.get("/metrics")
    assert response.status_code == 200

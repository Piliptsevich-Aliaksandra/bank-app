from unittest.mock import patch
from app.database import init_db, engine


@patch("app.database.Base.metadata.create_all")
def test_init_db(mock_create_all):
    init_db()
    mock_create_all.assert_called_once_with(bind=engine)
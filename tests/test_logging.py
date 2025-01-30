import json
import structlog
import pytest
from io import StringIO

from app.logging_config import logger


@pytest.fixture
def log_output():
    stream = StringIO()
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.JSONRenderer()
        ],
        logger_factory=structlog.PrintLoggerFactory(file=stream)
    )
    return stream

def test_info_log(log_output):
    logger.info("Test message", key="value")

    log_output.seek(0)
    log_entry = json.loads(log_output.getvalue().strip())

    assert log_entry["event"] == "Test message"
    assert log_entry["key"] == "value"
    assert "timestamp" in log_entry

def test_error_log(log_output):
    logger.error("Error occurred", error_code=500)

    log_output.seek(0)
    log_entry = json.loads(log_output.getvalue().strip())

    assert log_entry["event"] == "Error occurred"
    assert log_entry["error_code"] == 500
    assert "timestamp" in log_entry
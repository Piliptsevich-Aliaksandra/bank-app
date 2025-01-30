import json
import time
import threading
import pytest
from unittest.mock import patch, MagicMock
from app.consumers.payment_consumer import send_email, process_message, start_consumer
from app.logging_config import logger


@pytest.fixture
def mock_logger():
    with patch.object(logger, "info") as mock:
        yield mock


def test_send_email(mock_logger):
    email = "test@example.com"
    payment_id = 123

    send_email(email, payment_id)

    time.sleep(0.1)  # Ждём, чтобы логгер успел сработать
    mock_logger.assert_called_with("Email sent", payment_id=payment_id, email=email)


@patch("app.consumers.payment_consumer.send_email")
def test_process_message(mock_send_email, mock_logger):
    ch = MagicMock()
    method = MagicMock()
    method.delivery_tag = 1
    properties = MagicMock()

    message = {"payment_id": 456, "email": "user@example.com"}
    body = json.dumps(message).encode()

    process_message(ch, method, properties, body)

    mock_logger.assert_any_call("Received message from queue", payment_id=456, email="user@example.com")
    mock_send_email.assert_called_once_with("user@example.com", 456)
    ch.basic_ack.assert_called_once_with(delivery_tag=1)


@patch("app.consumers.payment_consumer.pika.BlockingConnection")
def test_start_consumer(mock_pika, mock_logger):
    mock_channel = MagicMock()
    mock_connection = MagicMock()
    mock_connection.channel.return_value = mock_channel
    mock_pika.return_value = mock_connection

    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()

    time.sleep(0.5)

    mock_logger.assert_called_with("Consumer started")
    mock_channel.queue_declare.assert_called_once_with(queue="payment_receipts", durable=True)
    mock_channel.basic_consume.assert_called_once()

    mock_connection.close()


@patch("app.consumers.payment_consumer.start_consumer")
def test_main(mock_start_consumer):
    with patch("threading.Thread") as mock_thread:
        mock_thread.return_value.start = mock_start_consumer

        with patch('app.consumers.payment_consumer.__name__', '__main__'):
            import app.consumers.payment_consumer
            app.consumers.payment_consumer.main()

        assert mock_thread.call_count == 3
        assert mock_start_consumer.call_count == 3

import json
import pika
import threading
import time

from app.logging_config import logger

RABBITMQ_URL = "amqp://guest:guest@rabbitmq:5672/"

def send_email(email: str, payment_id: int):
    time.sleep(2)
    # Имитация отправки сообщения на почту
    logger.info("Email sent", payment_id=payment_id, email=email)

def process_message(ch, method, properties, body):
    message = json.loads(body)
    payment_id = message["payment_id"]
    email = message["email"]

    logger.info("Received message from queue", payment_id=payment_id, email=email)
    send_email(email, payment_id)

    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consumer():
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()
    channel.queue_declare(queue="payment_receipts", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="payment_receipts", on_message_callback=process_message)

    logger.info("Consumer started")
    channel.start_consuming()

def main():
    threads = []
    for i in range(3):
        thread = threading.Thread(target=start_consumer)
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()


if __name__ == "__main__":
    main()


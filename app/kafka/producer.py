# from kafka import KafkaProducer
# import json
#
# producer = KafkaProducer(
#     bootstrap_servers=['kafka:9093'],
#     value_serializer=lambda v: json.dumps(v).encode('utf-8')
# )
#
# def send_payment_event(payment_data):
#     producer.send('payments', payment_data)
#     producer.flush()
#     print("Payment event sent to Kafka")

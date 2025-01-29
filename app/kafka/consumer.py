# from kafka import KafkaConsumer
# import json
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
#
# # consumer = KafkaConsumer(
# #     'payments',
# #     bootstrap_servers=['kafka:9093'],
# #     group_id='payment-group',
# #     value_deserializer=lambda x: json.loads(x.decode('utf-8'))
# # )
#
# SMTP_SERVER = 'smtp.your-email-provider.com'
# SMTP_PORT = 587
# SMTP_USER = 'my-email@example.com'
# SMTP_PASSWORD = 'my-email-password'
#
# def send_email(to_email, subject, body):
#     print(f"Start email sent to {to_email}")
#     msg = MIMEMultipart()
#     msg['From'] = SMTP_USER
#     msg['To'] = to_email
#     msg['Subject'] = subject
#
#     msg.attach(MIMEText(body, 'plain'))
#
#     with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
#         server.starttls()
#         server.login(SMTP_USER, SMTP_PASSWORD)
#         text = msg.as_string()
#         server.sendmail(SMTP_USER, to_email, text)
#         print(f"Email sent to {to_email}")
#
# def process_payment_event(payment_data):
#     user_email = payment_data['user_email']
#     payment_amount = payment_data['amount']
#     payment_id = payment_data['payment_id']
#
#     email_subject = f"Your payment {payment_id} was successful!"
#     email_body = f"Dear customer,\n\nYour payment of {payment_amount} has been successfully processed.\nThank you for using our service!"
#
#     send_email(user_email, email_subject, email_body)
#
#
# def run(consumer: KafkaConsumer) -> None:
#     print(f"Starting consumer")
#
#     while True:
#         for message in consumer:
#             payment_data = message.value
#             process_payment_event(payment_data)
#
#
# def stop(consumer) -> None:
#     consumer.close()

from prometheus_client import Counter

successful_payment_counter = Counter("successful_payments", "Total number of successful processed payments")

payment_counter = Counter("processed_payments", "Total number of processed payments")

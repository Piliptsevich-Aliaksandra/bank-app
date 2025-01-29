import random

from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime, event, text
from sqlalchemy.orm import declarative_base
from datetime import datetime

from app.database import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    number = Column(String(16), unique=True, nullable=False, index=True)
    balance = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)


@event.listens_for(Account, "before_insert")
def generate_account_number(mapper, connection, target):
    while True:
        # Генерация случайного номера счета
        generated_number = ''.join([str(random.randint(0, 9)) for _ in range(16)])

        # Строим запрос с помощью text() и параметризуем его
        query = text("SELECT 1 FROM accounts WHERE number = :number")

        # Выполняем запрос
        existing_account = connection.execute(query, {"number": generated_number}).first()

        if not existing_account:
            target.number = generated_number
            break
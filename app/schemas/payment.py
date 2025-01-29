from pydantic import condecimal, PositiveInt, BaseModel


class PaymentCreateSchema(BaseModel):
    from_account: PositiveInt
    to_account: PositiveInt
    amount: condecimal(gt=0, decimal_places=2)
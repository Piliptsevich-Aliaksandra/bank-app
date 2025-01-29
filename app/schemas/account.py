from pydantic import BaseModel, constr, condecimal


class AccountCreateSchema(BaseModel):
    name: constr(min_length=2, max_length=50)
    balance: condecimal(gt=0, decimal_places=2)
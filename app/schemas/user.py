from pydantic import BaseModel, EmailStr, constr

class UserCreateSchema(BaseModel):
    name: constr(min_length=2, max_length=50)
    email: EmailStr
    password: constr(min_length=6, max_length=100)

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: constr(min_length=6, max_length=100)
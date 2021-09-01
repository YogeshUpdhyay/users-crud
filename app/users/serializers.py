from pydantic import BaseModel, EmailStr, HttpUrl
from pydantic.fields import *

class create_user(BaseModel):
    id: int
    first_name: str
    last_name: str
    company_name: str
    city: str
    state: str
    zip: int
    email: EmailStr
    web: HttpUrl
    age: int

class update_user(BaseModel):
    first_name: str
    last_name: str
    age: int
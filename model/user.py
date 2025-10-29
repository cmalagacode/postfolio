from pydantic import BaseModel, EmailStr, Field
from model.settings import Timezones

class UserCreate(BaseModel):
    username: str = Field(min_length=7, max_length=30)
    email: EmailStr
    password: str = Field(min_length=8, max_length=70)
    first_name: str = Field(min_length=1, max_length=50, alias="firstName")
    last_name: str = Field(min_length=1, max_length=50, alias="lastName")
    middle_name: str = Field(min_length=0, max_length=50, alias="middleName")
    timezone: Timezones = Field(default=Timezones.UTC)

from pydantic import BaseModel
from typing import Optional
from app.models import PhoneNumber

# https://fastapi.tiangolo.com/tutorial/body-nested-models/#deeply-nested-models


class EmailBase(BaseModel):
    mail: str


class Email(EmailBase):
    id: int

    class Config:
        orm_mode = True


class PhoneNumber(BaseModel):
    id: int
    number: str

    class Config:
        orm_mode = True


class User(BaseModel):
    id: int
    firstname: str
    lastname: str
    emails: list[Email] = []
    phonenumbers: list[PhoneNumber] = []

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    firstname: str
    lastname: str
    mail: str
    phoneNumber: str


class DataUpdate(BaseModel):
    old_mail: Optional[str]
    new_mail: Optional[str]
    old_number: Optional[str]
    new_number: Optional[str]


class DataAdd(BaseModel):
    mail: Optional[str]
    number: Optional[str]

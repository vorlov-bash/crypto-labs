from fastapi import Form
from pydantic import BaseModel
from typing import Optional


def form_body(cls):
    cls.__signature__ = cls.__signature__.replace(
        parameters=[
            arg.replace(default=Form(...))
            for arg in cls.__signature__.parameters.values()
        ]
    )
    return cls


@form_body
class UserRegisterSchema(BaseModel):
    username: str
    password: str
    credit_card_number: Optional[int] = None
    credit_card_pin: Optional[int] = None
    credit_card_cvv: Optional[int] = None


@form_body
class UserLoginSchema(BaseModel):
    username: str
    password: str


class UpdateUserCardInfoSchema(BaseModel):
    credit_card_number: int
    credit_card_pin: int
    credit_card_cvv: int

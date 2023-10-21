from typing import Annotated

from fastapi.params import Form
from pydantic import BaseModel, EmailStr


class UserRegistrationSchema(BaseModel):
    email: EmailStr
    password: str


class UserResponseSchema(BaseModel):
    id: int
    email: EmailStr


class TokenResponseSchema(BaseModel):
    access_token: str
    token_type: str = 'bearer'


class AuthUserCustomForm:
    def __init__(
            self,
            *,
            email: Annotated[str, Form()],
            password: Annotated[str, Form()]
    ):
        self.email = email
        self.password = password

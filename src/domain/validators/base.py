import re

from pydantic import BaseModel, Field, field_validator


class UserRegisterDTO(BaseModel):
    first_name: str = Field(...)
    last_name: str = Field(...)
    password: str = Field(...)
    email: str = Field(..., example="user@example.com")

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        email = value.strip().lower()

        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(pattern, email):
            raise ValueError("Некорректный адрес электронной почты")

        return email


class UserLoginDTO(BaseModel):
    password: str = Field(...)
    email: str = Field(..., example="user@example.com")


class RefreshTokenDTO(BaseModel):
    refresh_token: str = Field(..., example="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")

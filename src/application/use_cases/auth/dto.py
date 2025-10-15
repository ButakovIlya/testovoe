from pydantic import BaseModel, Field


class TokenDTO(BaseModel):
    access_token: str = Field(..., example="eyJhbGciOiJIUzI1N...")
    refresh_token: str = Field(..., example="dGhpcyBpcyBhIHJlZnJlc2g...")

    user_id: int = Field(..., example=1)

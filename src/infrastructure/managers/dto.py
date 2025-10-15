from pydantic import BaseModel, Field

from infrastructure.enum import RoleEnum


class UserCreateDTO(BaseModel):
    user_id: int = Field(gt=0, alias="user_id")
    email: str = Field(alias="email")
    role: RoleEnum = Field(alias="role")

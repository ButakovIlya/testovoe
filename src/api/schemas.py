from pydantic import BaseModel, ConfigDict, Field

from infrastructure.enum import RoleEnum


class CheckHealthSchema(BaseModel):
    status: str


class UserDTO(BaseModel):
    id: int = Field(gt=0, alias="user_id")
    email: str = Field(alias="email")
    role: RoleEnum = Field(alias="role")

    model_config = ConfigDict(extra="ignore")

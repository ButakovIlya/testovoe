from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, ConfigDict, Field

from infrastructure.enum import RoleEnum


class CommonUserDTO(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=255)
    last_name: Optional[str] = Field(None, min_length=1, max_length=255)

    model_config = ConfigDict(from_attributes=True)


class UserDTO(CommonUserDTO):
    id: int
    email: str
    first_name: str
    last_name: str
    registration_date: datetime | None = None
    role: RoleEnum = RoleEnum.USER

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, user: Any) -> "UserDTO":
        return cls(
            id=user.id,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            registration_date=user.registration_date,
            role=user.role,
        )


class UserCreateDTO(CommonUserDTO):
    user_id: int
    email: str = Field(..., min_length=5, max_length=35)
    role: RoleEnum


class ChangeUserRoleDTO(BaseModel):
    user_id: int
    role: RoleEnum

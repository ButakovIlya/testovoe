from fastapi import Request

from api.permissions.exceptions import UserIsNotAdminError
from infrastructure.enum import RoleEnum


async def is_admin(request: Request):
    user = getattr(request.state, "user", None)
    if not user or not getattr(user, "role", False) == RoleEnum.ADMIN:
        raise UserIsNotAdminError

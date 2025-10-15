from passlib.hash import argon2

from application.exceptions import UserDoesNotExistError, WrongPasswordError
from application.use_cases.auth.dto import TokenDTO
from application.use_cases.base import UseCase
from domain.entities.user import User
from domain.validators.base import UserLoginDTO
from infrastructure.managers.dto import UserCreateDTO
from infrastructure.managers.jwt_manager import JWTManager
from infrastructure.uow.base import UnitOfWork


class LoginUseCase(UseCase):

    def __init__(self, uow: UnitOfWork, jwt_manager: JWTManager) -> None:
        self._uow = uow
        self._jwt_manager = jwt_manager

    async def execute(self, data: UserLoginDTO) -> TokenDTO:
        async with self._uow(autocommit=True):
            user: User | None = await self._uow.users.get_by_email(email=data.email)
            if not user:
                raise UserDoesNotExistError("Неверный email или пароль")

            if not argon2.verify(data.password, user.password):
                raise WrongPasswordError("Неверный email или пароль")

        user_data = UserCreateDTO(
            user_id=user.id,
            email=user.email,
            role=user.role,
        )

        access_token = self._jwt_manager.create_access_token(user_data)
        refresh_token = self._jwt_manager.create_refresh_token(user_data)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
        )

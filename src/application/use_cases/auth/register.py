from passlib.hash import argon2

from application.exceptions import UserWithEmailAlreadyExistsError
from application.use_cases.auth.dto import TokenDTO
from application.use_cases.base import UseCase
from application.use_cases.users.dto import UserCreateDTO
from domain.entities.user import User
from domain.validators.base import UserRegisterDTO
from infrastructure.managers.jwt_manager import JWTManager
from infrastructure.uow.base import UnitOfWork


class RegisterUserUseCase(UseCase):

    def __init__(self, uow: UnitOfWork, jwt_manager: JWTManager) -> None:
        self._uow = uow
        self._jwt_manager = jwt_manager

    async def execute(self, data: UserRegisterDTO) -> TokenDTO:
        async with self._uow(autocommit=True):
            if await self._uow.users.exists(email=data.email):
                raise UserWithEmailAlreadyExistsError()

            user: User = await self._uow.users.create(
                User(
                    email=data.email,
                    first_name=data.first_name,
                    last_name=data.last_name,
                    password=self._hash_password(data.password),
                )
            )

        dto = UserCreateDTO(user_id=user.id, email=user.email, role=user.role)
        access_token = self._jwt_manager.create_access_token(dto)
        refresh_token = self._jwt_manager.create_refresh_token(dto)

        return TokenDTO(
            access_token=access_token,
            refresh_token=refresh_token,
            user_id=user.id,
        )

    def _hash_password(self, password: str) -> str:
        return argon2.hash(password)

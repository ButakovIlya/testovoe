from application.exceptions import UserDoesNotExistError
from application.use_cases.auth.dto import TokenDTO
from application.use_cases.base import UseCase
from domain.validators.base import RefreshTokenDTO
from infrastructure.managers.dto import UserCreateDTO
from infrastructure.managers.jwt_manager import JWTManager
from infrastructure.uow.base import UnitOfWork


class RefreshTokenUseCase(UseCase):
    def __init__(self, uow: UnitOfWork, jwt_manager: JWTManager) -> None:
        self._jwt_manager = jwt_manager
        self._uow = uow

    async def execute(self, data: RefreshTokenDTO) -> TokenDTO:
        payload = self._jwt_manager.decode_refresh_token(data.refresh_token)

        async with self._uow(autocommit=True):
            if not await self._uow.users.exists(email=payload["email"]):
                raise UserDoesNotExistError()

        user_data = UserCreateDTO(
            user_id=payload["user_id"],
            email=payload["email"],
            role=payload["role"],
        )

        new_access_token = self._jwt_manager.create_access_token(user_data)
        new_refresh_token = self._jwt_manager.create_refresh_token(user_data)

        return TokenDTO(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user_id=payload["user_id"],
        )

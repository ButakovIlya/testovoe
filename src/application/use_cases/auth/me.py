from application.exceptions import UserDoesNotExistError
from application.use_cases.base import UseCase
from application.use_cases.users.dto import UserDTO
from infrastructure.managers.jwt_manager import JWTManager
from infrastructure.uow.base import UnitOfWork


class GetCurrentUserUseCase(UseCase):
    def __init__(self, uow: UnitOfWork, jwt_manager: JWTManager) -> None:
        self._uow = uow
        self._jwt_manager = jwt_manager

    async def execute(self, user_id: int) -> UserDTO:
        async with self._uow(autocommit=False):
            if not await self._uow.users.exists(id=user_id):
                raise UserDoesNotExistError()

            user = await self._uow.users.get_by_id(user_id)

        return UserDTO.model_validate(user)

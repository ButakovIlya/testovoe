from common.exceptions import APIException

from application.exceptions import UserNotFound
from application.use_cases.base import UseCase
from application.use_cases.users.dto import ChangeUserRoleDTO, UserDTO
from domain.entities.user import User
from infrastructure.uow.base import UnitOfWork


class UserUpdateUseCase(UseCase):
    """
    Update user info.
    """

    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self._uow = uow

    async def execute(self, data: ChangeUserRoleDTO) -> UserDTO:
        async with self._uow(autocommit=True):
            try:
                user: User = await self._uow.users.get_by_id(data.user_id)
            except ValueError:
                raise APIException(
                    code=404,
                    message=f"Пользователь с id '{data.user_id}' не существует",
                )

            if not user:
                raise UserNotFound("Пользователь не найден")

            user.change_role(data.role)
            await self._uow.users.update(user)

        return UserDTO.model_validate(user)

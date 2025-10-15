from common.dto import CategoryRead

from application.exceptions import CategoryAlreadyExists, CategoryDoesNotExist
from application.use_cases.base import UseCase
from application.use_cases.dto import CategoryPut
from infrastructure.uow.base import UnitOfWork


class CategoryUpdateUseCase(UseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, category_id: int, data: CategoryPut) -> CategoryRead:
        async with self._uow(autocommit=True):
            if not await self._uow.categories.exists(id=category_id):
                raise CategoryDoesNotExist()

            if await self._uow.categories.exists(name=data.name):
                raise CategoryAlreadyExists()

            category = await self._uow.categories.get_by_id(category_id)

            update_data = data.model_dump()

            for key, value in update_data.items():
                setattr(category, key, value)

            await self._uow.categories.update(category)
            category = await self._uow.categories.get_by_id(category.id)

        return CategoryRead.model_validate(category)

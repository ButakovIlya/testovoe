from common.dto import CategoryRead, PostRead

from application.exceptions import (
    CategoryAlreadyExists,
    CategoryDoesNotExist,
    PostTitleAlreadyExists,
)
from application.use_cases.base import UseCase
from application.use_cases.dto import CreateCategoryDTO, CreatePostDTO
from domain.entities.category import Category
from infrastructure.uow.base import UnitOfWork


class CategoryCreateUseCase(UseCase):

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: CreateCategoryDTO) -> CategoryRead:
        async with self._uow(autocommit=True):
            category = await self._create_category(data)
        return CategoryRead.model_validate(category)

    async def _create_category(self, data: CreateCategoryDTO) -> Category:
        if await self._uow.categories.exists(name=data.name):
            raise CategoryAlreadyExists()

        return await self._uow.categories.create(Category(**data.model_dump()))

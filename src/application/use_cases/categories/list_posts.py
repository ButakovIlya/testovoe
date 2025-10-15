from common.dto import PostRead
from fastapi import Request

from application.use_cases.base import UseCase
from domain.validators.dto import PaginatedResponse
from infrastructure.managers.paginator import Paginator
from infrastructure.uow.base import UnitOfWork


class PostByCategoryUseCase(UseCase):
    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self._uow = uow

    async def execute(
        self, request: Request, category_name: str, page: int = 1, page_size: int = 10
    ) -> PaginatedResponse[PostRead]:
        async with self._uow(autocommit=True):
            category = await self._uow.categories.get_by_name(category_name)
            result = await self._uow.posts.get_list_models(category_id=category.id)

        return await Paginator(PostRead).paginate(result, request, page, page_size)

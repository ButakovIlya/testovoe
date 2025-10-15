from common.dto import PostRead

from application.exceptions import CategoryDoesNotExist
from application.use_cases.base import UseCase
from application.use_cases.dto import PostPut
from infrastructure.uow.base import UnitOfWork


class PostUpdateUseCase(UseCase):
    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, post_id: int, data: PostPut) -> PostRead:
        async with self._uow(autocommit=True):
            if not await self._uow.categories.exists(id=data.category_id):
                raise CategoryDoesNotExist()

            post = await self._uow.posts.get_by_id(post_id)

            update_data = data.model_dump()

            for key, value in update_data.items():
                setattr(post, key, value)

            post = await self._uow.posts.get_by_id(post_id)

        return PostRead.model_validate(post)

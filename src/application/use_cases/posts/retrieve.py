from common.dto import PostRead

from application.use_cases.base import UseCase
from infrastructure.uow.base import UnitOfWork


class PostRetriveUseCase(UseCase):
    def __init__(
        self,
        uow: UnitOfWork,
    ) -> None:
        self._uow = uow

    async def execute(self, title: str) -> PostRead:
        async with self._uow(autocommit=True):
            post = await self._uow.posts.get_by_title(title)

        return PostRead.model_validate(post)

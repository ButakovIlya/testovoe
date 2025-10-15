from common.dto import PostRead

from application.exceptions import CategoryDoesNotExist, PostTitleAlreadyExists
from application.use_cases.base import UseCase
from application.use_cases.dto import CreatePostDTO
from domain.entities.post import Post
from infrastructure.uow.base import UnitOfWork


class PostCreateUseCase(UseCase):

    def __init__(self, uow: UnitOfWork) -> None:
        self._uow = uow

    async def execute(self, data: CreatePostDTO) -> PostRead:
        async with self._uow(autocommit=True):
            post = await self._create_post(data)
        return PostRead.model_validate(post)

    async def _create_post(self, data: CreatePostDTO) -> Post:
        if not await self._uow.categories.exists(id=data.category_id):
            raise CategoryDoesNotExist()

        if await self._uow.posts.exists(title=data.title):
            raise PostTitleAlreadyExists()

        return await self._uow.posts.create(Post(**data.model_dump()))

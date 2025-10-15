from typing import Any

from common.exceptions import APIException
from sqlalchemy import Result, desc, select
from sqlalchemy.orm import joinedload

from domain.entities.post import Post
from infrastructure.models.alchemy.base import Post as PostModel
from infrastructure.repositories.alchemy.base import SqlAlchemyModelRepository
from infrastructure.repositories.interfaces.post import PostRepository


class SqlAlchemyPostsRepository(SqlAlchemyModelRepository[Post], PostRepository):
    MODEL = PostModel
    ENTITY = Post

    async def create(self, data: Post) -> Post:
        model = self.convert_to_model(data)
        self._session.add(model)
        await self._session.flush()
        await self._session.refresh(
            model,
            attribute_names=["author", "category"],
        )
        return self.convert_to_entity(model)

    async def get_by_id(self, model_id: int) -> Post:
        stmt = (
            select(PostModel)
            .options(
                joinedload(PostModel.author),
                joinedload(PostModel.category),
            )
            .filter(PostModel.id == model_id)
        )

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()
        if not model:
            raise APIException(code=404, message=f"Пост c id={model_id} не найден")
        return self.convert_to_entity(model)

    async def get_list_models(self, **filters: Any) -> Result:
        stmt = (
            select(PostModel)
            .filter_by(**filters)
            .options(
                joinedload(PostModel.author),
                joinedload(PostModel.category),
            )
            .order_by(desc(PostModel.created_at))
        )
        return await self._session.execute(stmt)

    async def get_by_title(self, title: str) -> Post:
        stmt = (
            select(PostModel)
            .options(
                joinedload(PostModel.author),
                joinedload(PostModel.category),
            )
            .filter(PostModel.title == title)
        )

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()
        if not model:
            raise APIException(code=404, message=f"Пост c заголовком {title} не найден")
        return self.convert_to_entity(model)

    def convert_to_model(self, entity: Post) -> PostModel:
        return PostModel(
            id=entity.id,
            author_id=entity.author_id,
            category_id=entity.category_id,
            title=entity.title,
            body=entity.body,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def convert_to_entity(self, model: PostModel) -> Post:
        return Post(
            id=model.id,
            author_id=model.author_id,
            category_id=model.category_id,
            title=model.title,
            body=model.body,
            created_at=model.created_at,
            updated_at=model.updated_at,
            author=model.author if model.author else None,
            category=model.category if model.category else None,
        )

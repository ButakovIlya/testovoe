from abc import abstractmethod
from typing import Any, TypeVar

from sqlalchemy import Result

from domain.entities.model import Model
from domain.entities.post import Post
from infrastructure.repositories.interfaces.base import ModelRepository

TModel = TypeVar("TModel", bound=Model)


class PostRepository(ModelRepository):
    @abstractmethod
    async def get_list_models(self, **filters: Any) -> Result:
        pass

    @abstractmethod
    async def get_by_title(self, title: str) -> Post:
        pass

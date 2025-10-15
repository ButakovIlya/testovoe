from abc import abstractmethod
from typing import TypeVar

from domain.entities.model import Model
from infrastructure.repositories.interfaces.base import ModelRepository

TModel = TypeVar("TModel", bound=Model)


class CategoryRepository(ModelRepository):
    @abstractmethod
    async def get_by_name(self, name: str) -> TModel:
        pass

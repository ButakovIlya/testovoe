from abc import abstractmethod
from typing import List, TypeVar

from domain.entities.model import Model
from infrastructure.repositories.interfaces.base import ModelRepository

TModel = TypeVar("TModel", bound=Model)


class UserRepository(ModelRepository):
    @abstractmethod
    async def get_by_email(self, email: str) -> TModel | None:
        pass

    @abstractmethod
    async def get_list(self) -> List[TModel]:
        pass

    @abstractmethod
    async def exists_by_email(self, email: str) -> bool:
        pass

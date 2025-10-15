from abc import ABC, abstractmethod
from types import TracebackType
from typing import Any, Type, Union

from domain.entities.enums import ModelType
from infrastructure.repositories.alchemy.categories import (
    SqlAlchemyCategoriesRepository,
)
from infrastructure.repositories.alchemy.posts import SqlAlchemyPostsRepository
from infrastructure.repositories.alchemy.users import SqlAlchemyUsersRepository
from infrastructure.repositories.interfaces.category import CategoryRepository
from infrastructure.repositories.interfaces.post import PostRepository
from infrastructure.repositories.interfaces.user import UserRepository


class UnitOfWork(ABC):
    users: UserRepository
    posts: PostRepository
    categories: CategoryRepository

    def __call__(self, *args: Any, autocommit: bool, **kwargs: Any) -> "UnitOfWork":
        self._autocommit = autocommit
        return self

    async def __aenter__(self) -> "UnitOfWork":
        return self

    async def __aexit__(
        self,
        exc_type: Type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        if exc_type is not None:
            await self.rollback()
        elif self._autocommit:
            await self.commit()
        await self.shutdown()

    @abstractmethod
    def get_model_repository(self, model_name: ModelType) -> Union[
        SqlAlchemyUsersRepository,
        SqlAlchemyPostsRepository,
        SqlAlchemyCategoriesRepository,
    ]:
        pass

    @abstractmethod
    async def rollback(self) -> None:
        pass

    @abstractmethod
    async def commit(self) -> None:
        pass

    @abstractmethod
    async def shutdown(self) -> None:
        pass

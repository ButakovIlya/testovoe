from contextlib import asynccontextmanager
from types import ModuleType
from typing import AsyncGenerator

from dependency_injector import containers, providers

from application.use_cases.auth.login import LoginUseCase
from application.use_cases.auth.me import GetCurrentUserUseCase
from application.use_cases.auth.refresh import RefreshTokenUseCase
from application.use_cases.auth.register import RegisterUserUseCase
from application.use_cases.categories.create import CategoryCreateUseCase
from application.use_cases.categories.list_posts import PostByCategoryUseCase
from application.use_cases.categories.update import CategoryUpdateUseCase
from application.use_cases.common.create import ModelObjectCreateUseCase
from application.use_cases.common.delete import ModelObjectDeleteUseCase
from application.use_cases.common.list import ModelObjectListUseCase
from application.use_cases.common.partial_update import ModelObjectPartialUpdateUseCase
from application.use_cases.common.retrieve import ModelObjectRetrieveUseCase
from application.use_cases.common.update import ModelObjectUpdateUseCase
from application.use_cases.posts.create import PostCreateUseCase
from application.use_cases.posts.retrieve import PostRetriveUseCase
from application.use_cases.posts.update import PostUpdateUseCase
from application.use_cases.users.list import UsersListUseCase
from application.use_cases.users.retrieve import UserRetrieveUseCase
from application.use_cases.users.update_user import UserUpdateUseCase
from config.settings import Settings
from infrastructure.managers.jwt_manager import JWTManager
from infrastructure.repositories.alchemy.db import Database
from infrastructure.uow import SqlAlchemyUnitOfWork, UnitOfWork


class ClientsContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(instance_of=Settings)


class DBContainer(containers.DeclarativeContainer):
    settings = providers.Dependency(instance_of=Settings)

    db: providers.Provider[Database] = providers.Singleton(
        Database, settings=settings.provided.db
    )

    uow: providers.Provider[UnitOfWork] = providers.Factory(
        SqlAlchemyUnitOfWork, session_factory=db.provided.session_factory
    )

    session = providers.Factory(lambda db: db.session_factory(), db)


class Container(containers.DeclarativeContainer):
    settings: providers.Provider[Settings] = providers.Singleton(Settings)

    db = providers.Container(DBContainer, settings=settings)

    clients = providers.Container(ClientsContainer, settings=settings)

    jwt_manager = providers.Singleton(JWTManager, settings=settings)

    ###################
    #### Use cases ####
    ###################

    register_use_case: providers.Provider[RegisterUserUseCase] = providers.Factory(
        RegisterUserUseCase, uow=db.container.uow, jwt_manager=jwt_manager
    )

    login_use_case: providers.Provider[LoginUseCase] = providers.Factory(
        LoginUseCase, uow=db.container.uow, jwt_manager=jwt_manager
    )

    refresh_token_use_case: providers.Provider[RefreshTokenUseCase] = providers.Factory(
        RefreshTokenUseCase,
        uow=db.container.uow,
        jwt_manager=jwt_manager,
    )

    get_current_user_use_case = providers.Factory(
        GetCurrentUserUseCase,
        uow=db.container.uow,
        jwt_manager=jwt_manager,
    )

    users_list_use_case = providers.Factory(
        UsersListUseCase,
        uow=db.container.uow,
    )

    user_retrieve_use_case = providers.Factory(
        UserRetrieveUseCase,
        uow=db.container.uow,
    )

    user_update_use_case = providers.Factory(
        UserUpdateUseCase,
        uow=db.container.uow,
    )

    post_create_use_case = providers.Factory(
        PostCreateUseCase,
        uow=db.container.uow,
    )

    post_retrieve_use_case = providers.Factory(
        PostRetriveUseCase,
        uow=db.container.uow,
    )

    post_update_use_case = providers.Factory(
        PostUpdateUseCase,
        uow=db.container.uow,
    )

    post_by_category_use_case = providers.Factory(
        PostByCategoryUseCase,
        uow=db.container.uow,
    )

    category_create_use_case = providers.Factory(
        CategoryCreateUseCase,
        uow=db.container.uow,
    )

    category_update_use_case = providers.Factory(
        CategoryUpdateUseCase,
        uow=db.container.uow,
    )

    # COMMON CRUD USE_CASES
    object_create_use_case: providers.Provider[ModelObjectCreateUseCase] = (
        providers.Factory(
            ModelObjectCreateUseCase,
            uow=db.container.uow,
        )
    )

    object_retrieve_use_case: providers.Provider[ModelObjectRetrieveUseCase] = (
        providers.Factory(
            ModelObjectRetrieveUseCase,
            uow=db.container.uow,
        )
    )

    object_list_use_case: providers.Provider[ModelObjectListUseCase] = (
        providers.Factory(
            ModelObjectListUseCase,
            uow=db.container.uow,
        )
    )

    object_update_use_case: providers.Provider[ModelObjectUpdateUseCase] = (
        providers.Factory(
            ModelObjectUpdateUseCase,
            uow=db.container.uow,
        )
    )

    object_partial_update_use_case: providers.Provider[
        ModelObjectPartialUpdateUseCase
    ] = providers.Factory(
        ModelObjectPartialUpdateUseCase,
        uow=db.container.uow,
    )

    object_delete_use_case: providers.Provider[ModelObjectDeleteUseCase] = (
        providers.Factory(
            ModelObjectDeleteUseCase,
            uow=db.container.uow,
        )
    )

    @classmethod
    @asynccontextmanager
    async def lifespan(
        cls, wireable_packages: list[ModuleType]
    ) -> AsyncGenerator["Container", None]:
        container = cls()
        container.wire(packages=wireable_packages)
        yield container

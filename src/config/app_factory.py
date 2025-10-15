from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator, Callable, Dict

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi

import api
from api import admin_routers, public_routers
from api.middlewares.get_jwt_token_user import JwtTokenUserMiddleware
from config.containers import Container
from config.loggers import config_loggers
from config.settings import Settings
from config.uptrace import config_uptrace
from infrastructure.middleware.sanitize_html import SanitizeHTMLMiddleware

from .exceptions import handlers


def create_app(settings: Settings) -> FastAPI:
    app = FastAPI(
        title=settings.app.title,
        debug=settings.app.debug,
        version=settings.app.version,
        lifespan=lifespan,
        docs_url=settings.api.docs_url,
        openapi_url=settings.api.openapi_url,
    )

    config_loggers()
    config_uptrace(app)

    add_middlewares(app, settings)
    app.add_middleware(SanitizeHTMLMiddleware)

    include_routers(app, settings)

    add_exception_handlers(app)

    app.openapi = custom_openapi(app)  # type: ignore

    return app


def add_exception_handlers(app: FastAPI) -> None:
    for exception, handler in handlers.items():
        app.add_exception_handler(exception, handler)


def include_routers(app: FastAPI, settings: Settings) -> None:
    for router in admin_routers:
        app.include_router(router, prefix=settings.api.admin_prefix)

    for router in public_routers:
        app.include_router(router, prefix=settings.api.public_prefix)


def add_middlewares(app: FastAPI, settings: Settings) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(JwtTokenUserMiddleware, settings=settings)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    async with Container.lifespan(
        wireable_packages=[
            api,
            api.public,
            api.admin,
        ]
    ) as container:
        app.container = container  # type: ignore
        yield


def custom_openapi(app: FastAPI) -> Callable[[], Dict[str, Any]]:
    def _wrapper() -> Dict[str, Any]:
        if app.openapi_schema:
            return app.openapi_schema

        schema = get_openapi(
            title=app.title,
            version=app.version,
            description=getattr(app, "description", None) or "API specification",
            routes=app.routes,
        )

        schema.setdefault("components", {}).setdefault("securitySchemes", {})
        schema["components"]["securitySchemes"]["BearerAuth"] = {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }

        schema["security"] = [{"BearerAuth": []}]
        app.openapi_schema = schema
        return schema

    return _wrapper

from typing import Callable

from common.exceptions import APIException
from fastapi import Request, Response
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from api.permissions.exceptions import UserIsNotAdminError, UserIsNotAuthenticatedError
from application.exceptions import (
    CategoryAlreadyExists,
    CategoryDoesNotExist,
    InvalidEmailError,
    PostTitleAlreadyExists,
    UserDoesNotExistError,
    UserWithEmailAlreadyExistsError,
    WrongPasswordError,
)
from domain.exceptions import DomainException


def create_exception_handler(
    status_code: int,
) -> Callable[[Request, Exception | DomainException], Response]:

    def get_exception_handler(
        request: Request, exc: Exception | DomainException
    ) -> Response:
        if isinstance(exc, DomainException):
            return api_exception_handler(request, exc)
        return exception_handler(request, exc)

    def api_exception_handler(request: Request, exc: DomainException) -> Response:
        code = str(exc.code)
        message = exc.message

        return JSONResponse(
            status_code=status_code,
            content={
                "error": {
                    "code": code,
                    "message": message,
                },
            },
        )

    def exception_handler(request: Request, exc: Exception) -> Response:
        return Response(
            status_code=500,
            content={"error": f"An unexpected error occurred: {exc}"},
        )

    return get_exception_handler


async def api_exception_handler(request: Request, exc: APIException):
    return JSONResponse(
        status_code=exc.code,
        content={"code": exc.code, "message": exc.message},
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Обработка ошибок валидации Pydantic (422 Unprocessable Entity)."""
    errors = exc.errors()
    formatted = []
    for err in errors:
        field = ".".join(str(x) for x in err.get("loc", []))
        message = err.get("msg")
        formatted.append({"field": field, "message": message})

    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Некорректные входные данные",
                "details": formatted,
            }
        },
    )


handlers = {
    APIException: api_exception_handler,
    UserIsNotAdminError: create_exception_handler(status_code=403),
    UserWithEmailAlreadyExistsError: create_exception_handler(status_code=400),
    UserIsNotAuthenticatedError: create_exception_handler(status_code=403),
    WrongPasswordError: create_exception_handler(status_code=400),
    UserDoesNotExistError: create_exception_handler(status_code=400),
    CategoryDoesNotExist: create_exception_handler(status_code=400),
    CategoryAlreadyExists: create_exception_handler(status_code=400),
    PostTitleAlreadyExists: create_exception_handler(status_code=400),
    InvalidEmailError: create_exception_handler(status_code=400),
    RequestValidationError: validation_exception_handler,
}

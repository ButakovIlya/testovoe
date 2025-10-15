from datetime import datetime, timezone
from typing import Any, Awaitable, Callable

import jwt
from fastapi import Request
from jwt import ExpiredSignatureError
from pydantic import ValidationError
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse, Response

from api.middlewares.exceptions import AuthenticationError, TokenExpiredError
from api.schemas import UserDTO
from config.settings import Settings
from domain.entities.user import User
from infrastructure.models.alchemy.base import User as UserModel
from infrastructure.repositories.alchemy.db import Database


class JwtTokenUserMiddleware(BaseHTTPMiddleware):
    def __init__(
        self,
        *args: Any,
        settings: Settings,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.jwt_settings = settings.jwt

        self.db = Database(settings.db)
        self.session_factory = self.db.session_factory

    async def dispatch(
        self, request: Request, call_next: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        try:
            request.state.user = await self._get_user(request)
        except (AuthenticationError, TokenExpiredError) as e:
            return JSONResponse(
                status_code=401,
                content={
                    "error": {
                        "code": e.code,
                        "message": e.message,
                        "detail": e.get_detail(),
                        "help_link": None,
                    }
                },
            )
        return await call_next(request)

    async def _get_user(self, request: Request) -> User | None:
        authorization = request.headers.get("Authorization")
        if not authorization:
            return None

        try:
            scheme, token = authorization.split()
        except ValueError:
            raise AuthenticationError(detail="Malformed Authorization header.")

        if scheme.lower() != "bearer":
            raise AuthenticationError(detail="Expected 'Bearer' authentication scheme.")

        payload = self._decode_token(token)

        if request.url.path.endswith("/refresh"):
            expected_type = "refresh"
        else:
            expected_type = "access"

        self._validate_token_type(payload, expected_type)
        self._validate_expiration_time(payload)
        validated = self._validate_payload(payload)
        async with self.session_factory() as session:
            user_from_db: UserModel = await session.get(UserModel, validated.id)
            if not user_from_db:
                raise AuthenticationError(detail="User not found in DB.")
        return User(
            id=user_from_db.id,
            email=user_from_db.email,
            role=user_from_db.role,
            registration_date=user_from_db.registration_date,
            first_name=user_from_db.first_name,
            last_name=user_from_db.last_name,
        )

    def _decode_token(self, token: str) -> dict:
        try:
            return jwt.decode(
                token,
                self.jwt_settings.secret_key,
                algorithms=[self.jwt_settings.algorithm],
            )
        except ExpiredSignatureError:
            raise TokenExpiredError(
                detail="Token expired at timestamp: {}", *["{}".format(datetime.now())]
            )
        except jwt.PyJWTError as e:
            raise AuthenticationError(detail="JWT decoding failed: {}", *[str(e)])

    def _validate_token_type(
        self, payload: dict, expected_type: str = "access"
    ) -> None:
        token_type = payload.get("token_type")
        if token_type != expected_type:
            raise AuthenticationError(
                detail=f"Token type must be '{expected_type}', got '{token_type}'"
            )

    # todo пофиксить ошибку времени жизни у токена
    def _validate_expiration_time(self, payload: dict) -> None:
        try:
            exp = payload.get("exp")
            if exp is None:
                return

            if isinstance(exp, str):
                try:
                    exp = float(exp)
                except ValueError:
                    return

            if exp > 1e12:
                exp /= 1000

            try:
                expiration_time = datetime.fromtimestamp(exp, tz=timezone.utc)
            except (OSError, OverflowError, ValueError):
                return

            current_time = datetime.now(tz=timezone.utc)
            if expiration_time < current_time:
                raise TokenExpiredError(
                    detail=f"Token expired at: {expiration_time.isoformat()}"
                )

        except Exception:
            return

    def _validate_payload(self, payload: dict) -> UserDTO:
        try:
            return UserDTO(**payload)
        except ValidationError as e:
            raise AuthenticationError(detail="Invalid token payload: {}", *[str(e)])

import json

import bleach
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

ALLOWED_TAGS = [
    "p",
    "br",
    "strong",
    "em",
    "ul",
    "ol",
    "li",
    "a",
    "h1",
    "h2",
    "h3",
    "h4",
    "blockquote",
    "code",
    "pre",
]

ALLOWED_ATTRIBUTES = {
    "*": ["title", "alt"],
    "a": ["href", "title"],
}


def sanitize_html(value: str) -> str:
    """Очистка HTML от неразрешённых тегов и атрибутов."""
    if not value:
        return ""
    return bleach.clean(
        text=value,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True,
        strip_comments=True,
    )


class SanitizeHTMLMiddleware(BaseHTTPMiddleware):
    """Middleware для автоматической очистки входящих данных с HTML."""

    async def dispatch(self, request: Request, call_next) -> Response:
        if request.method in {"POST", "PUT", "PATCH"} and request.headers.get(
            "content-type", ""
        ).startswith("application/json"):
            body = await request.body()
            if body:
                try:
                    data = json.loads(body)
                except json.JSONDecodeError:
                    return await call_next(request)

                def clean_html_in_dict(obj):
                    if isinstance(obj, dict):
                        for k, v in obj.items():
                            if k == "content_html" and isinstance(v, str):
                                obj[k] = sanitize_html(v)
                            else:
                                clean_html_in_dict(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            clean_html_in_dict(item)

                clean_html_in_dict(data)

                request._body = json.dumps(data).encode("utf-8")

        response = await call_next(request)
        return response

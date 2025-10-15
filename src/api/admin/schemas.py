from datetime import datetime
from typing import Any, List, Optional

from common.dto import UserRead
from pydantic import BaseModel

from domain.entities.post import Post
from infrastructure.enum import RoleEnum


class CommonPostBase(BaseModel):
    title: str
    body: Optional[str] = None


class PostPut(CommonPostBase):
    title: str
    body: str


class PostPatch(CommonPostBase):
    title: str
    body: str
    category_id: int


class PostRead(CommonPostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime

    author: Optional[UserRead] = None
    model_config = {"from_attributes": True, "use_enum_values": False}

    @classmethod
    def model_validate(cls, post: Post) -> "PostRead":
        return cls(
            id=post.id,
            title=post.title,
            body=post.body,
            author_id=post.author_id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author=UserRead.model_validate(post.author) if post.author else None,
        )


class PostPut(CommonPostBase):
    title: str
    body: str


class ChangeUserRoleDTO(BaseModel):
    user_id: int
    role: RoleEnum


class CommonPostBase(BaseModel):
    title: str
    body: Optional[str] = None


class PostPut(CommonPostBase):
    title: str
    body: str
    category_id: int


class CategoryPut(BaseModel):
    name: str

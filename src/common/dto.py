from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from domain.entities.post import Post


class CategoryRead(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}


class UserRead(BaseModel):
    id: int
    email: str
    first_name: Optional[str]
    last_name: Optional[str]

    model_config = {"from_attributes": True}


class PostRead(BaseModel):
    id: int
    category_id: int
    title: str
    body: str
    author_id: int
    created_at: datetime
    updated_at: datetime

    author: Optional[UserRead] = None
    category: Optional[CategoryRead] = None

    model_config = {"from_attributes": True}

    @classmethod
    def model_validate(cls, post: Post) -> "PostRead":
        return cls(
            id=post.id,
            title=post.title,
            body=post.body,
            category_id=post.category_id,
            author_id=post.author_id,
            created_at=post.created_at,
            updated_at=post.updated_at,
            author=UserRead.model_validate(post.author) if post.author else None,
            category=(
                CategoryRead.model_validate(post.category) if post.category else None
            ),
        )

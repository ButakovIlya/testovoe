from datetime import datetime
from typing import TYPE_CHECKING, Optional

from domain.entities.entity import Entity

if TYPE_CHECKING:
    from domain.entities.category import Category
    from domain.entities.user import User


class Post(Entity):
    def __init__(
        self,
        id: Optional[int] = None,
        author_id: Optional[int] = None,
        category_id: Optional[int] = None,
        title: Optional[str] = None,
        body: Optional[str] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        author: Optional["User"] = None,
        category: Optional["Category"] = None,
    ) -> None:
        super().__init__(id)

        self.author_id = author_id
        self.category_id = category_id
        self.title = title
        self.body = body
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

        self.author = author
        self.category = category

from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from domain.entities.entity import Entity
from infrastructure.enum import RoleEnum

if TYPE_CHECKING:
    from domain.entities.post import Post


class User(Entity):
    def __init__(
        self,
        id: Optional[int] = None,
        email: Optional[str] = None,
        role: Optional[RoleEnum] = RoleEnum.USER,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        password: Optional[str] = None,
        registration_date: Optional[datetime] = datetime.now(),
        posts: Optional[List["Post"]] = None,
    ) -> None:
        super().__init__(id)
        self.email = email
        self.role = role
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.registration_date = registration_date
        self.posts = posts or []

    def change_role(self, role: RoleEnum) -> None:
        self.role = role

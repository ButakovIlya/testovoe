from typing import Optional

from domain.entities.entity import Entity


class Category(Entity):
    def __init__(
        self,
        id: Optional[int] = None,
        name: Optional[str] = None,
    ) -> None:
        super().__init__(id)

        self.name = name

from common.dto import CategoryRead

from application.use_cases.dto import CreateCategoryDTO
from domain.entities.category import Category
from domain.entities.enums import ModelType

TEST_CASES = [
    (
        ModelType.CATEGORIES,
        CreateCategoryDTO,
        {"name": "test"},
        Category,
        CategoryRead,
        CategoryRead(id=1, name="test"),
    ),
]

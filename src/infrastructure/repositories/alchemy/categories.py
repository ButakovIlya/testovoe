from common.exceptions import APIException
from sqlalchemy import select

from domain.entities.category import Category
from infrastructure.models.alchemy.base import Category as CategoryModel
from infrastructure.repositories.alchemy.base import SqlAlchemyModelRepository
from infrastructure.repositories.interfaces.category import CategoryRepository


class SqlAlchemyCategoriesRepository(
    SqlAlchemyModelRepository[Category], CategoryRepository
):
    MODEL = CategoryModel
    ENTITY = Category

    async def get_by_name(self, name: str) -> Category:
        stmt = select(CategoryModel).filter(CategoryModel.name == name)

        result = await self._session.execute(stmt)
        model = result.unique().scalar_one_or_none()
        if not model:
            raise APIException(
                code=404, message=f"Категория c именем {name} не найдена"
            )
        return self.convert_to_entity(model)

    def convert_to_model(self, entity: Category) -> CategoryModel:
        return CategoryModel(
            id=entity.id,
            name=entity.name,
        )

    def convert_to_entity(self, model: CategoryModel) -> Category:
        return Category(
            id=model.id,
            name=model.name,
        )

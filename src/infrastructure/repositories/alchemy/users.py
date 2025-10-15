from sqlalchemy import delete, exists, select

from domain.entities.user import User
from infrastructure.models.alchemy.base import User as UserModel
from infrastructure.repositories.alchemy.base import SqlAlchemyModelRepository
from infrastructure.repositories.interfaces import UserRepository


class SqlAlchemyUsersRepository(SqlAlchemyModelRepository[User], UserRepository):
    MODEL = UserModel
    ENTITY = User

    async def get_by_email(self, email: str) -> User | None:
        stmt = select(self.MODEL).where(self.MODEL.email == email)
        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()
        if model:
            return self.convert_to_entity(model)
        else:
            return None

    async def get_list(self) -> list[User]:
        stmt = select(self.MODEL)
        return await self._session.execute(stmt)

    async def exists_by_email(self, email: str) -> bool:
        stmt = select(exists().where(self.MODEL.email == email))
        result = await self._session.execute(stmt)
        return bool(result.scalar())

    async def delete_by_phone(self, email: str) -> bool:
        stmt = delete(self.MODEL).where(self.MODEL.email == email)
        result = await self._session.execute(stmt)
        await self._session.commit()
        return result.rowcount > 0

    def convert_to_model(self, entity: User) -> UserModel:
        return UserModel(
            id=entity.id,
            role=entity.role,
            email=entity.email,
            first_name=entity.first_name,
            last_name=entity.last_name,
            password=entity.password,
            registration_date=entity.registration_date,
        )

    def convert_to_entity(self, model: UserModel) -> User:
        return User(
            id=model.id,
            role=model.role,
            email=model.email,
            first_name=model.first_name,
            last_name=model.last_name,
            password=model.password,
            registration_date=model.registration_date,
        )

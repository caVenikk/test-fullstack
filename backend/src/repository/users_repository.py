from sqlalchemy import select, asc, update
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.users.models import User
from src.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: async_sessionmaker):
        super().__init__(session)

    async def create(self, user: User) -> None:
        async with self._session() as s:
            async with s.begin():
                s.add(user)

    async def all(self) -> list[User]:
        async with self._session() as s:
            query = select(User).order_by(asc(User.id))
            return list((await s.execute(query)).scalars().all())

    async def admins(self) -> list[User]:
        async with self._session() as s:
            query = select(User).where(User.is_admin == True).order_by(asc(User.id))
            return list((await s.execute(query)).scalars().all())

    async def get(self, user_id: str) -> User | None:
        async with self._session() as s:
            query = select(User).where(User.id == user_id)
            return (await s.execute(query)).scalar()

    async def get_by_username(self, username: str) -> User | None:
        async with self._session() as s:
            query = select(User).where(User.username == username)
            return (await s.execute(query)).scalar()

    async def update(self, user: User) -> User | None:
        async with self._session() as s:
            async with s.begin():
                update_user_stmt = update(User).where(User.id == user.id)
                values_to_update = {}
                if user.first_name is not None:
                    values_to_update["first_name"] = user.first_name
                if user.last_name is not None:
                    values_to_update["last_name"] = user.last_name
                if user.username is not None:
                    values_to_update["username"] = user.username
                if user.is_admin is not None:
                    values_to_update["is_admin"] = user.is_admin

                if values_to_update:
                    update_user_stmt = update_user_stmt.values(**values_to_update)
                    await s.execute(update_user_stmt)
                else:
                    return None
            updated_user = await self.get(user.id)
            return updated_user

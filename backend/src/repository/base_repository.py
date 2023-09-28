from sqlalchemy.ext.asyncio import async_sessionmaker


class BaseRepository:
    def __init__(self, session: async_sessionmaker):
        self._session = session

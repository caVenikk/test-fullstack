from functools import lru_cache

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from src.config import Config
from src.utils.base import Base
from src.api.users.models import User
from src.api.products.models import Product


@lru_cache(maxsize=1)
def create_database_async_session() -> async_sessionmaker:
    config = Config.load()

    db_engine = create_async_engine(f"postgresql+asyncpg://{config.database.url}", echo=True)

    async_session = async_sessionmaker(db_engine, expire_on_commit=False)
    return async_session

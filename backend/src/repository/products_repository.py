from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import async_sessionmaker

from src.api.products.models import Product
from src.repository.base_repository import BaseRepository


class ProductRepository(BaseRepository):
    def __init__(self, session: async_sessionmaker):
        super().__init__(session)

    async def create(self, product: Product) -> None:
        async with self._session() as s:
            async with s.begin():
                s.add(product)

    async def all(self) -> list[Product]:
        async with self._session() as s:
            query = select(Product).order_by(asc(Product.id))
            return list((await s.execute(query)).scalars().all())

    async def get(self, product_id: int) -> Product | None:
        async with self._session() as s:
            query = select(Product).where(Product.id == product_id)
            return (await s.execute(query)).scalar()

from fastapi import Depends

from src.api.products.exceptions import ProductNotFound
from src.api.products.models import Product
from src.repository.crud import CRUD


async def valid_product_id(product_id: int, crud: CRUD = Depends(CRUD)) -> Product:
    if product := await crud.products.get(product_id):
        return product
    raise ProductNotFound

from fastapi import APIRouter, Depends, UploadFile, File, Form
from pydantic import TypeAdapter
from starlette.requests import Request
from starlette.responses import Response

from src.api.products.dependencies import valid_product_id
from src.api.products.models import Product
from src.api.products.schemas import ProductBaseSchema, ProductSchema
from src.repository.crud import CRUD

router = APIRouter()


@router.post(
    "/",
    response_model=ProductSchema,
)
async def create_product(
        request: Request,
        description: str = Form(...),
        image: UploadFile = File(...),
        crud: CRUD = Depends(CRUD),
) -> ProductSchema:
    image_data = await image.read()
    product = Product(description=description, image=image_data)
    await crud.products.create(product=product)
    return TypeAdapter(ProductSchema).validate_python(product)


@router.get(
    "/",
    response_model=list[ProductSchema],
)
async def get_products(request: Request, crud: CRUD = Depends(CRUD)) -> list[ProductSchema]:
    products = await crud.products.all()
    return TypeAdapter(list[ProductSchema]).validate_python(products)


@router.get(
    "/{product_id}",
    response_model=ProductBaseSchema,
)
async def get_product(
        request: Request,
        product: Product = Depends(valid_product_id),
) -> ProductSchema:
    return TypeAdapter(ProductSchema).validate_python(product)


@router.get(
    "/image/{product_id}",
    responses={200: {"content": {"image/png": {}}}},
)
async def get_product_image(
        request: Request,
        product: Product = Depends(valid_product_id),
) -> Response:
    return Response(content=product.image, media_type="image/png")

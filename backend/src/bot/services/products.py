from aiogram.client.session import aiohttp
from pydantic import TypeAdapter

from src.api.products.schemas import ProductSchema
from src.bot.loader import config


async def create_product(product_data: dict) -> ProductSchema | None:
    async with aiohttp.ClientSession() as session:
        api_url = f"{config.base_url}/api/products/"
        form_data = aiohttp.FormData()
        form_data.add_field('description', product_data["description"])
        form_data.add_field('image', product_data["image_file"], content_type='image/jpeg')

        async with session.post(api_url, data=form_data) as resp:
            if resp.status == 200:
                product = await resp.json()
                return TypeAdapter(ProductSchema).validate_python(product)
    return None


async def get_products() -> list[ProductSchema] | None:
    async with aiohttp.ClientSession() as session:
        api_url = f"{config.base_url}/api/products/"
        async with session.get(api_url) as resp:
            if resp.status == 200:
                products = await resp.json()
                return TypeAdapter(list[ProductSchema]).validate_python(products)
    return None


async def get_product_image(product_id: int) -> bytes | None:
    async with aiohttp.ClientSession() as session:
        api_url = f"{config.base_url}/api/products/image/{product_id}"
        async with session.get(api_url) as resp:
            if resp.status == 200:
                return await resp.read()
    return None

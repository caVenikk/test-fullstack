from aiogram.filters import CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, BufferedInputFile
from aiogram.utils.media_group import MediaGroupBuilder

from src.bot.services.products import create_product, get_products, get_product_image
from src.bot.services.users import is_user_admin, make_user_admin


async def process_description(message: Message, state: FSMContext) -> None:
    product_data = await state.update_data(description=message.caption if message.caption else message.text)
    await state.clear()

    product = await create_product(product_data)
    await message.answer(text=f"Товар #{product.id}: \"{product.description}\" создан")


async def make_admin(
        message: Message,
        command: CommandObject | None = None,
        state: FSMContext | None = None
) -> None:
    if not command or not command.args or len(args := command.args.split(" ")) != 1:
        if message.text.startswith("/make_admin"):
            await message.answer(
                text="Отметьте в команде одного пользователя, которого необходимо сделать админом, или введите его ID",
            )
            return
        else:
            args = [message.text]
    try:
        user_id = int(args[0])
        if await is_user_admin(user_id=user_id):
            await message.answer(text=f"Пользователь уже является админом")
            if state:
                await state.clear()
            return
        user = await make_user_admin(user_id=user_id)
    except ValueError:
        username = args[0].replace("@", "")
        if await is_user_admin(username=username):
            await message.answer(text=f"Пользователь уже является админом")
            if state:
                await state.clear()
            return
        user = await make_user_admin(username=username)
    if not user or not user.is_admin:
        await message.answer(text=f"Пользователь не найден")
        if state:
            await state.clear()
        return
    await message.answer(text=f"Пользователь @{user.username} сделан админом")
    if state:
        await state.clear()


async def send_products(message: Message):
    products = await get_products()
    images: list[bytes] = [await get_product_image(product.id) for product in products]

    media_groups: list[MediaGroupBuilder] = []
    batch_size = 10

    for i in range(0, len(products), batch_size):
        batch_products = products[i:i + batch_size]
        batch_images = images[i:i + batch_size]

        media_group = MediaGroupBuilder()

        for product, image in zip(batch_products, batch_images):
            media_group.add_photo(
                media=BufferedInputFile(
                    file=image,
                    filename=f"product_{product.id}.png"
                ),
                caption=product.description,
            )
        media_groups.append(media_group)

    await message.answer(text="Все товары (описание товаров в подписях под фото):")
    for media_group in media_groups:
        await message.answer_media_group(media=media_group.build())

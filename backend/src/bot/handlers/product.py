import io

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, File

from src.bot.loader import bot
from src.bot.states import Product
from src.bot.templates import process_description as _process_description

router = Router(name=__name__)


@router.message(Product.image)
async def process_image(message: Message, state: FSMContext) -> None:
    if image := message.document:
        file_id = image.file_id
    elif message.photo:
        file_id = message.photo[-1].file_id
    else:
        return
    result: File = await bot.get_file(file_id=file_id)
    file: io.BytesIO = await bot.download_file(file_path=result.file_path)
    await state.update_data(image_file=file)
    if message.caption:
        await _process_description(message, state)
        return
    await state.set_state(Product.description)

    await message.answer(text="Введите описание товара")


@router.message(Product.description)
async def process_description(message: Message, state: FSMContext):
    await _process_description(message, state)

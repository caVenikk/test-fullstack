from aiogram import Router
from aiogram.filters import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.api.users.schemas import UserBaseSchema
from src.bot.filters import AdminFilter
from src.bot.loader import config
from src.bot.makrups.admin_menu import AdminMenu
from src.bot.makrups.menu import UserMenu
from src.bot.services.users import create_user, make_user_admin
from src.bot.states import Product
from src.bot.templates import make_admin, send_products

router = Router(name=__name__)


@router.message(Command("start"))
async def start_handler(message: Message) -> None:
    user_data = UserBaseSchema(
        id=message.from_user.id,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name,
        username=message.from_user.username,
    )

    await create_user(user_data)
    if (user_id := message.from_user.id) in config.telegram.admin_ids:
        await make_user_admin(user_id=user_id)

    await message.answer(
        text=f"Привет, {message.from_user.first_name}!\nЧтобы увидеть список доступных команд, введите /help",
    )


@router.message(Command("help"))
async def help_handler(message: Message) -> None:
    text = "/help – Доступные команды\n/menu – Меню\n/products – Все доступные товары\n"
    admin_filter = AdminFilter()
    if await admin_filter(message=message):
        text += "/make_admin *id/@username* – Сделать пользователя админом\n/create_product – Создать товар"
    await message.answer(text=text)


@router.message(Command("make_admin"), AdminFilter())
async def admin_handler(message: Message, command: CommandObject) -> None:
    await make_admin(message, command=command)


@router.message(Command("create_product"), AdminFilter())
async def create_product_handler(message: Message, state: FSMContext) -> None:
    await message.answer(text="Отправьте изображение товара")
    await state.set_state(Product.image)


@router.message(Command("menu"), AdminFilter())
async def admin_menu_handler(message: Message) -> None:
    user_id = message.from_user.id
    AdminMenu.setup(user_id=user_id)
    await message.answer(text="Меню", reply_markup=AdminMenu.markup(user_id=user_id))


@router.message(Command("menu"), ~AdminFilter())
async def user_menu_handler(message: Message) -> None:
    user_id = message.from_user.id
    UserMenu.setup(user_id=user_id)
    await message.answer(text="Меню", reply_markup=UserMenu.markup(user_id=user_id))


@router.message(Command("products"))
async def products_handler(message: Message) -> None:
    await send_products(message)

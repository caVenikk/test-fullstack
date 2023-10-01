from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery

from src.bot.filters import AdminFilter
from src.bot.makrups.admin_menu import AdminAction, Action as adm_Action
from src.bot.states import Admin, Product
from src.bot.templates import send_products

router = Router(name=__name__)


@router.callback_query(AdminFilter(), AdminAction.filter(F.action == adm_Action.make_admin))
async def admin_callback_handler(query: CallbackQuery, callback_data: AdminAction, state: FSMContext) -> None:
    await query.answer()
    await query.message.answer(
        text="Отметьте одного пользователя, которого необходимо сделать админом, или введите его ID",
    )
    await state.set_state(Admin.username_or_id)


@router.callback_query(AdminFilter(), AdminAction.filter(F.action == adm_Action.create_product))
async def create_product_callback_handler(query: CallbackQuery, callback_data: AdminAction, state: FSMContext) -> None:
    await query.answer()
    await query.message.answer(text="Отправьте изображение товара")
    await state.set_state(Product.image)


@router.callback_query()
async def products_callback_handler(query: CallbackQuery) -> None:
    await query.answer()
    await send_products(query.message)

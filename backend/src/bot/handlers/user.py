from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.bot.states import Admin
from src.bot.templates import make_admin

router = Router(name=__name__)


@router.message(Admin.username_or_id)
async def username_or_id_handler(message: Message, state: FSMContext):
    await make_admin(message, state=state)

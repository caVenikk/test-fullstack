from aiogram.filters import Filter
from aiogram.types import Message

from src.bot.services.users import get_admin_ids


class AdminFilter(Filter):
    def __init__(self) -> None:
        pass

    async def __call__(self, message: Message) -> bool:
        return message.from_user.id in await get_admin_ids()

from enum import Enum

from aiogram.filters.callback_data import CallbackData
from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
from loguru import logger

__all__ = ["Action", "AdminAction", "AdminMenu"]


class Action(str, Enum):
    make_admin = "Сделать пользователя админом"
    create_product = "Создать товар"
    show_products = "Просмотреть товары"


class AdminAction(CallbackData, prefix="adm"):
    action: Action


class _AdminMenu:
    def __init__(self):
        pass

    @staticmethod
    def build_markup(self):
        builder = InlineKeyboardBuilder()
        for action in Action:
            builder.row(
                InlineKeyboardButton(
                    text=action.value,
                    callback_data=AdminAction(action=action).pack(),
                )
            )
        return builder.as_markup()


class AdminMenu:
    _storage: dict[int, _AdminMenu] = dict()

    @classmethod
    def setup(cls, user_id: int):
        cls._storage[user_id] = _AdminMenu()

    @classmethod
    def clear(cls, user_id):
        try:
            del cls._storage[user_id]
        except KeyError as err:
            logger.exception(err)

    @classmethod
    def markup(cls, user_id, callback_data=None):
        try:
            return cls._storage[user_id].build_markup(callback_data)
        except KeyError:
            pass

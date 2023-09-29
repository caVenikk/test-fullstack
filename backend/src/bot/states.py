from aiogram.fsm.state import StatesGroup, State


class Admin(StatesGroup):
    username_or_id = State()


class Product(StatesGroup):
    image = State()
    description = State()

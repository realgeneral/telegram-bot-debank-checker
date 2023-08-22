from aiogram.dispatcher.filters.state import State, StatesGroup


class AdminMode(StatesGroup):
    admin_menu = State()
    add_user = State()


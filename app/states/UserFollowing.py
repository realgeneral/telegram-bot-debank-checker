from aiogram.dispatcher.filters.state import State, StatesGroup


class UserFollowing(StatesGroup):
    start_navigation = State()
    check_subscribe = State()
    get_private_keys = State()
    choose_point = State()
    wallet_menu = State()
    new_private = State()
    tap_to_earn = State()

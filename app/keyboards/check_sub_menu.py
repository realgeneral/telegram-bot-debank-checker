from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

btn_subscribe = InlineKeyboardButton(text="Subscribe 🚀", url='https://t.me/ARNI_Concepts')
btn_check_subscribe = InlineKeyboardButton(text="Done ✅‍", callback_data='is_subscribe')
check_sub_menu = InlineKeyboardMarkup(row_width=1)
check_sub_menu.insert(btn_subscribe)
check_sub_menu.insert(btn_check_subscribe)

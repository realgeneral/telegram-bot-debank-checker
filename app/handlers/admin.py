import datetime

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text

from app.create_bot import dp, bot
from app.states import AdminMode, UserFollowing
from app.handlers.first_start import user_db
ADMIN_ID = ""


@dp.message_handler(Text(equals=["⬅ Go to menu"]), state=AdminMode.admin_menu)
async def go_menu(message: types.Message):
    await UserFollowing.get_wallets.set()
    await bot.send_message(message.from_user.id, "<b> Load-up your wallets below ⬇️ </b>\n\n",
                           parse_mode=types.ParseMode.HTML,
                           reply_markup=ReplyKeyboardRemove())


@dp.message_handler(Text(equals=["⬅ Go to admin menu"]), state=AdminMode.admin_menu)
async def go_admin_menu(message: types.Message):
    await send_admin_menu(message)


@dp.message_handler(commands=['admin'], state='*')
async def send_admin_menu(message: types.Message):
    if int(message.from_user.id) == 420881832 or int(message.from_user.id) == 740574479 or int(message.from_user.id) == 812233995:
        message_response = "# *ADMIN MODE* \n"

        b1 = KeyboardButton("Add premium user")
        b2 = KeyboardButton("List premium users")
        b3 = KeyboardButton("Today logs")
        b4 = KeyboardButton("⬅ Go to menu")
        buttons = ReplyKeyboardMarkup(resize_keyboard=True)
        buttons.row(b1).row(b2).row(b3).row(b4)

        await AdminMode.admin_menu.set()
        await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN, reply_markup=buttons)


@dp.message_handler(Text(equals="Add premium user"), state=AdminMode.admin_menu)
async def add_prem_user(message: types.Message):
    message_response = "Send user telegream_id"

    await AdminMode.add_user.set()
    await message.answer(message_response, reply_markup=ReplyKeyboardRemove())


@dp.message_handler(state=AdminMode.add_user)
async def save_prem_user(message: types.Message):
    telegram_id = message.text
    try:
        user_db.set_max_wallets_count((int(telegram_id)), 30)
        user_db.set_request_count((int(telegram_id)), 100)

        message_response = "Saved"
    except Exception as err_:
        message_response = f"Not saved: {err_}"

    buttons = [
        KeyboardButton(text="⬅ Go to admin menu"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await AdminMode.admin_menu.set()
    await message.answer(message_response, reply_markup=reply_markup)


@dp.message_handler(Text(equals="List premium users"), state=AdminMode.admin_menu)
async def send_list_prem_user(message: types.Message):
    message_response = "# LIST # \n \n"
    list_premium_users = user_db.get_premium_users()
    if list_premium_users is not None:
        for i in range(len(list_premium_users)):
            message_response += f"{i+1}. {list_premium_users[i]} \n"
    await message.answer(message_response, parse_mode=types.ParseMode.MARKDOWN)


@dp.message_handler(Text(equals="Today logs"), state=AdminMode.admin_menu)
async def get_today_logs(message: types.Message):
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    today_logs = []

    with open("logs/logs.log", 'r') as f:
        for line in f:
            if line.startswith(today):
                today_logs.append(line.strip())

    reply_message = "\n".join(today_logs)
    await message.answer(reply_message[-4000:])
from datetime import date

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states.UserFollowing import UserFollowing
from app.keyboards.check_sub_menu import check_sub_menu
from app.utils.UsersDb import Users

CHANNEL_ID = -1001984019900
NOTSUB_MESSAGE = "Looks like you're not subscribed yet! 🙁 Subscribe now to access all the features"
max_request_count = 2

user_db = Users()


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    buttons = [
        KeyboardButton(text="🚀 LESS GOOO!"),
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons], resize_keyboard=True)

    await UserFollowing.check_subscribe.set()
    await message.answer(f"👋 *Welcome to Sybil DeBank!* \n\n"
                         f"🔍 Our bot allows you to:\n\n"
                         f"🌐 Instantly check multiple wallet balances in all chains\n"
                         f"📲 Manage your wallets from any device\n"
                         f"📈 Keep track of your wallet farm of any size",
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=reply_markup)


def check_sub_channel(chat_member):
    if chat_member["status"] != "left":
        return True
    return False


@dp.message_handler(Text(equals="🚀 LESS GOOO!"), state=UserFollowing.check_subscribe)
async def check_subscribe(message: types.Message):
    await UserFollowing.check_subscribe.set()
    await message.answer(
        "👋📢 Whoa, hold up! Haven't joined our <a href='https://t.me/EBSH_WEB3'>channel</a> yet? \n\n"
        "We're dropping <b> crypto wisdom </b> and sharing our <b> know-how </b>. \n"
        "Your sub supports us to make <b> new retro-bots </b> for You! \n \n"
        "Hit that sub button below ⬇️, then <b> hit us back </b> with  <b> 'Done'</b>! ",
        parse_mode=types.ParseMode.HTML,
        reply_markup=check_sub_menu)


@dp.callback_query_handler(text="is_subscribe", state=UserFollowing.check_subscribe)
async def is_subscribe(callback_query: types.CallbackQuery):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    user_id = callback_query.from_user.id

    today = date.today()
    formatted_date = today.strftime('%Y-%m-%d %H:%M:%S')
    print(str(formatted_date))

    user_db.add_user(user_id, str(formatted_date), wallet_count=5, request_count=0,)

    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)):
        await UserFollowing.get_wallets.set()
        await bot.send_message(callback_query.from_user.id, "<b> Load-up your wallets below ⬇️ </b>\n\n",
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, NOTSUB_MESSAGE, reply_markup=check_sub_menu)



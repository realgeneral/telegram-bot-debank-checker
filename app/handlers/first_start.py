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
max_request_count = 5

user_db = Users()


@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    buttons = [
        KeyboardButton(text="💪 LFGGG !"),
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


# @dp.message_handler(Text(equals="💪 LFGGG !"), state=UserFollowing.check_subscribe)
async def check_subscribe(message: types.Message):
    await UserFollowing.check_subscribe.set()
    await message.answer(
        "👋📢 Whoa, hold up! Haven't joined our <a href='https://t.me/EBSH_WEB3'>channel</a> yet? \n\n"
        "We're dropping <b> crypto wisdom </b> and sharing our <b> know-how </b>. \n"
        "Your sub supports us to make <b> new retro-bots </b> for You! \n \n"
        "Hit that sub button below ⬇️, then <b> hit us back </b> with  <b> 'Done'</b>! ",
        parse_mode=types.ParseMode.HTML,
        reply_markup=check_sub_menu)


@dp.message_handler(Text(equals="💪 LFGGG !"), state=UserFollowing.check_subscribe)
async def first_free_use(message: types, state: FSMContext):
    first_use = 0
    await state.update_data(first_use=first_use)

    user_id = message.from_user.id
    today = date.today()
    formatted_date = today.strftime('%Y-%m-%d %H:%M:%S')

    user_db.add_user(user_id, str(formatted_date), wallet_count=5, request_count=100)

    is_ready = 0
    await state.update_data(is_ready=is_ready)
    await UserFollowing.get_wallets.set()
    await bot.send_message(message.from_user.id, "🔽 *DROP YOUR WALLETS BELOW AND PRESS ENTER! (max. 5)*  \n\n"
                                                 "*Format:* \n"
                                                 "• _Wallet adress1_\n"
                                                 "• _Wallet adress2_\n"
                                                 "• _Wallet adress3_",
                           parse_mode=types.ParseMode.MARKDOWN,
                           reply_markup=ReplyKeyboardRemove())




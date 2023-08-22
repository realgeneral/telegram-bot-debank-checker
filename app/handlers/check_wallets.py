from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime, date, timedelta

from app.create_bot import dp, bot
from app.states.UserFollowing import UserFollowing
from app.handlers.first_start import user_db, max_request_count
from app.utils.SeleniumWalletScreen import async_screenshot


def is_today(date_string):
    date_object = datetime.strptime(str(date_string), '%Y-%m-%d %H:%M:%S')
    today = date.today()
    if date_object.date() == today:
        return True
    else:
        return False


@dp.message_handler(state=UserFollowing.get_wallets)
async def wallets(message: types.Message, state: FSMContext):
    message_reply = ""
    user_id = message.from_user.id

    request_count = user_db.get_request_count(user_id)
    user_time = user_db.get_time_wait(user_id)

    wait_message = await message.answer("⏳ Getting information about wallets ...")

    if request_count == 100:  # если премиум версия
        max_wallet = user_db.get_max_wallets(user_id)
        wallets_list = message.text.split('\n')
        wallets_list = wallets_list[:max_wallet]
        wallets_count = len(wallets_list)
        total_balances = 0

        for wallet, i in zip(wallets_list, range(wallets_count)):
            print(f"{wallet} - {i}")
            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ Getting information about wallets {i}/{wallets_count}")

            is_screen_saved, balance = await async_screenshot(wallet)

            if is_screen_saved == 1:
                path_for_save = "app/wallets/" + wallet + ".png"
                total_balances += int(balance)
                await message.answer_photo(photo=open(path_for_save, "rb"), caption=f"✅ *{wallet}* \n"
                                                                                    f"💰 Balance *{balance}$*",
                                           parse_mode=types.ParseMode.MARKDOWN,
                                           reply_markup=types.ReplyKeyboardRemove())
            else:
                await message.answer(f"❌ *{wallet}*",
                                     parse_mode=types.ParseMode.MARKDOWN,
                                     reply_markup=ReplyKeyboardRemove())
        if wallets_count != 1:
            await message.answer(f"💰 Total balance *{total_balances}$*",
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=ReplyKeyboardRemove())
    else:
        # если сегодня и достиг максимальное количество запросов
        if is_today(user_time) and request_count == max_request_count:
            message_reply += f"☹️Daily request limit reached (max. {max_request_count})"
            await bot.delete_message(chat_id=wait_message.chat.id,
                                     message_id=wait_message.message_id)
            await message.answer(message_reply,
                                 parse_mode=types.ParseMode.MARKDOWN,
                                 reply_markup=ReplyKeyboardRemove())
            return

        elif request_count < max_request_count:  # меньше максимального количества запросов
            max_wallet = user_db.get_max_wallets(user_id)
            wallets_list = message.text.split('\n')
            wallets_list = wallets_list[:max_wallet]
            wallets_count = len(wallets_list)
            total_balances = 0

            for wallet, i in zip(wallets_list, range(wallets_count)):
                print(f"{wallet} - {i}")
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ Getting information about wallets {i}/{wallets_count}")

                is_screen_saved, balance = await async_screenshot(wallet)

                if is_screen_saved == 1:
                    path_for_save = "app/wallets/" + wallet + ".png"
                    total_balances += int(balance)
                    await message.answer_photo(photo=open(path_for_save, "rb"), caption=f"✅ *{wallet}* \n"
                                                                                        f"💰 Balance *{balance}$*",
                                               parse_mode=types.ParseMode.MARKDOWN,
                                               reply_markup=types.ReplyKeyboardRemove())
                else:
                    await message.answer(f"❌ *{wallet}*",
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=ReplyKeyboardRemove())
            if wallets_count != 1:
                await message.answer(f"💰 Total balance *{total_balances}$*",
                                     parse_mode=types.ParseMode.MARKDOWN,
                                     reply_markup=ReplyKeyboardRemove())

        elif not is_today(user_time):  # обновление было не сегодня
            today = date.today()
            formatted_date = today.strftime('%Y-%m-%d %H:%M:%S')
            user_db.set_request_count_and_date(user_id, 0, str(formatted_date))

            max_wallet = user_db.get_max_wallets(user_id)
            wallets_list = message.text.split('\n')
            wallets_list = wallets_list[:max_wallet]
            wallets_count = len(wallets_list)
            total_balances = 0

            for wallet, i in zip(wallets_list, range(wallets_count)):

                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ Getting information about wallets {i}/{wallets_count}")

                is_screen_saved, balance = await async_screenshot(wallet)

                if is_screen_saved == 1:
                    path_for_save = "app/wallets/" + wallet + ".png"
                    total_balances += int(balance)
                    await message.answer_photo(photo=open(path_for_save, "rb"), caption=f"✅ *{wallet}* \n"
                                                                                        f"💰 Balance *{balance}$*",
                                               parse_mode=types.ParseMode.MARKDOWN,
                                               reply_markup=types.ReplyKeyboardRemove())
                else:
                    await message.answer(f"❌ *{wallet}*",
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=ReplyKeyboardRemove())
            if wallets_count != 1:
                await message.answer(f"💰 Total balance *{total_balances}$*",
                                     parse_mode=types.ParseMode.MARKDOWN,
                                     reply_markup=ReplyKeyboardRemove())

        user_db.increase_request_count(user_id)

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)
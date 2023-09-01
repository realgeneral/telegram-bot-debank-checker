import random

from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup, \
    InlineKeyboardButton
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from datetime import datetime, date, timedelta

from app.create_bot import dp, bot
from app.states.UserFollowing import UserFollowing
from app.handlers.first_start import user_db, max_request_count
from app.utils.config import min_amount, id_name_dict
from app.utils.utils import setup_session
from app.utils.Checker import Checker
from app.handlers.first_start import check_sub_channel, CHANNEL_ID, NOTSUB_MESSAGE
from app.keyboards.check_sub_menu import check_sub_menu

motivational_quotes = [
    "Do the hard work especially when you don't feel like.",
    "Wake wake, it's time to workout",
    "The man who goes to the gym every single day regardless of how he feels will always beat the man who goes to the gym when he feels like going to the gym.",
    "You need to hesitate when choosing a goal. When the goal is chosen, you just need to act.",
    "Progress is progress, no matter how small.",
    "Wake wake, it's time to grind!",
    "Don't stop until you're proud.",
    "Yeah buddy, it's time to cash in and make some gains!",
    "Train hard or go home.",
    "You don’t want the Ferrari to drive fast you want it to make other men feel inferior.",
    "Push or die.",
    "The best time for a new beginning is now.",
    "Success is always stressful.",
    "If you are gonna wear gloves when you lift, just make sure they match your purse.",
    "You cannot get tired if you’re interested in what you do. That’s the key thing.",
    "Stay hungry, stay healthy, be a gentleman, fuck whores.",
    "I do squats until I fall over and pass out. So what? It’s not going to kill me. I wake up 5 minutes later and I’m OK",
    "If u are reading this and not doing 100 kg bench press then u are pussy.",
    "Everybody wants to be a bodybuilder, but don't nobody wanna lift no heavy ass weight.",
    "Eat, train, sleep. Repeat.",
    "When you hit failure your workout has just begun.",
    "Women really do pay attention to a man's glutes. A tight, compact ass is often voted even more desirable than muscular arms and chest. So, if you're lacking, start squatting!"
    "Shut up and squat.",
    "No sweat - no beauty. No squat - no booty.",
    "Try our @zora_auto_bot",
    "Try our @sybil_debank_bot",
    "Just fall over and do 20 pushups now, fighter.",
    "When everything fall apart in your life and your plan is fucked up - stay fucking hard."
]


def is_today(date_string):
    date_object = datetime.strptime(str(date_string), '%Y-%m-%d %H:%M:%S')
    today = date.today()
    if date_object.date() == today:
        return True
    else:
        return False


@dp.callback_query_handler(text="is_subscribe", state=UserFollowing.check_subscribe)
async def is_subscribe(callback_query: types.CallbackQuery, state: FSMContext):
    await bot.delete_message(chat_id=callback_query.message.chat.id, message_id=callback_query.message.message_id)

    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)):
        first_use = 2
        is_ready = 0

        data = await state.get_data()
        message = data.get("message")

        await state.update_data(first_use=first_use)
        await state.update_data(is_ready=is_ready)
        await UserFollowing.get_wallets.set()
        await wallets(message, state)

    else:
        await bot.send_message(callback_query.from_user.id, NOTSUB_MESSAGE, reply_markup=check_sub_menu)


@dp.message_handler(state=UserFollowing.get_wallets)
async def wallets(message: types.Message, state: FSMContext):
    data = await state.get_data()
    is_ready = data.get("is_ready")

    if is_ready == 0:
        is_ready = -1
        await state.update_data(is_ready=is_ready)

        first_use = data.get("first_use")

        if first_use == 1:

            await state.update_data(message=message)
            await UserFollowing.check_subscribe.set()
            await message.answer(
                "👋📢 Haven't joined our <a href='https://t.me/EBSH_WEB3'>channel</a> yet? \n\n"
                "We're dropping <b> crypto wisdom </b> and sharing our <b> know-how </b>. \n"
                "Your sub supports us to make <b> new retro-bots </b> for You! \n \n"
                "Hit that sub button below ⬇️, then <b> hit us back </b> with  <b> 'Done'</b>! ",
                parse_mode=types.ParseMode.HTML,
                reply_markup=check_sub_menu)
            return
        elif first_use == 0:
            first_use += 1
            await state.update_data(first_use=first_use)

        message_reply = ""
        user_id = message.from_user.id

        request_count = user_db.get_request_count(user_id)
        user_time = user_db.get_time_wait(user_id)

        wait_message = await message.answer("⏳ Getting information about wallets ...")

        if request_count == 100:  # если премиум версия
            max_wallet = user_db.get_max_wallets(user_id)

            wallets_list = message.text.split('\n')
            wallets_list = wallets_list[:max_wallet]
            wallets_list = [wallet.strip().lower() for wallet in wallets_list]

            for elem in wallets_list:
                if len(elem) != 42:
                    wallets_list.remove(elem)

            if len(wallets_list) == 0:
                message_reply += "🙁 Invalid address"

                is_ready = 0
                await state.update_data(is_ready=is_ready)

                await UserFollowing.get_wallets.set()
                await message.answer(message_reply, reply_markup=ReplyKeyboardRemove(),
                                     parse_mode=types.ParseMode.MARKDOWN)
                return

            wallets_count = len(wallets_list)
            total_balances = 0

            session, node_process = setup_session()

            await bot.edit_message_text(chat_id=wait_message.chat.id,
                                        message_id=wait_message.message_id,
                                        text=f"⏳ <b>Wallets are loaded</b> \n\n",
                                        parse_mode=types.ParseMode.HTML)
            counter = 1
            len_list = len(wallets_list)

            for wallet in wallets_list:
                message_reply = f"*{wallet[:4]}...{wallet[-4:]}* \n\n"
                random_quotes = random.choice(motivational_quotes)
                await bot.edit_message_text(chat_id=wait_message.chat.id,
                                            message_id=wait_message.message_id,
                                            text=f"⏳ <b>Getting information about balance {counter}/{len_list}</b> \n\n"
                                                 f"<i>{random_quotes}</i>",
                                            parse_mode=types.ParseMode.HTML)

                usd_balance = await Checker.get_usd_balance(node_process, session, wallet)

                if usd_balance == -1:
                    usd_balance = "-"
                else:
                    usd_balance = round(usd_balance, 2)
                    total_balances += usd_balance

                message_reply += f"*Wallet balance:* {usd_balance} $\n"

                list_used_chains = await Checker.get_used_chains(node_process, session, wallet)

                if list_used_chains == -1:
                    pass
                else:
                    counter_networks = 1
                    for chain, i in zip(list_used_chains, range(len(list_used_chains))):
                        if chain in id_name_dict:
                            chain_name = id_name_dict[chain]
                        else:
                            chain_name = chain

                        print(f"chain_name - {chain_name}")
                        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                                    message_id=wait_message.message_id,
                                                    text=f"⏳ <b>Getting information about networks {i + 1}/{len(list_used_chains)}</b> \n\n"
                                                         f"<i>{random_quotes}</i>",
                                                    parse_mode=types.ParseMode.HTML)
                        results = await Checker.chain_balance(node_process, session, wallet, chain, None, min_amount)

                        if results == -1:
                            continue

                        total_sum = 0

                        for result in results:
                            if result["amount"] is None or result["price"] is None:
                                continue
                            else:
                                print(f'result - {result["amount"]}')
                                print(f'price - {result["price"]}')

                                total_sum += round(result["amount"] * result["price"], 2)
                        if total_sum == 0:
                            continue

                        prefix = "├──>" if i < len(list_used_chains) - 1 else "└──>"

                        if usd_balance != -1:
                            message_reply += f' `{prefix}{chain_name}: {round(total_sum, 2)}$ ({round(total_sum / usd_balance * 100, 2)}%)`\n'
                        else:
                            message_reply += f' `{prefix}{chain_name}: {round(total_sum, 2)}$`\n'

                        counter_networks += 1

                    debank_markup = InlineKeyboardMarkup(row_width=1)
                    debank_button = InlineKeyboardButton(text="Debank", url=f'https://debank.com/profile/{wallet}')
                    debank_markup.insert(debank_button)

                    await message.answer(message_reply,
                                         parse_mode=types.ParseMode.MARKDOWN,
                                         reply_markup=debank_markup)

                counter += 1

            if wallets_count != 1:
                await message.answer(f"💰 Total balance *{round(total_balances, 2)}$*",
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

        # elif request_count < max_request_count:  # меньше максимального количества запросов
        #         max_wallet = user_db.get_max_wallets(user_id)
        #         wallets_list = message.text.split('\n')
        #         wallets_list = wallets_list[:max_wallet]
        #         wallets_count = len(wallets_list)
        #         total_balances = 0
        #
        #         for wallet, i in zip(wallets_list, range(wallets_count)):
        #             print(f"{wallet} - {i}")
        #             await bot.edit_message_text(chat_id=wait_message.chat.id,
        #                                         message_id=wait_message.message_id,
        #                                         text=f"⏳ Getting information about wallets {i}/{wallets_count}")
        #
        #             is_screen_saved, balance = await async_screenshot(wallet)
        #
        #             if is_screen_saved == 1:
        #                 path_for_save = "app/wallets/" + wallet + ".png"
        #                 total_balances += int(balance)
        #                 await message.answer_photo(photo=open(path_for_save, "rb"), caption=f"✅ *{wallet}* \n"
        #                                                                                     f"💰 Balance *{balance}$*",
        #                                            parse_mode=types.ParseMode.MARKDOWN,
        #                                            reply_markup=types.ReplyKeyboardRemove())
        #             else:
        #                 await message.answer(f"❌ *{wallet}*",
        #                                      parse_mode=types.ParseMode.MARKDOWN,
        #                                      reply_markup=ReplyKeyboardRemove())
        #         if wallets_count != 1:
        #             await message.answer(f"💰 Total balance *{total_balances}$*",
        #                                  parse_mode=types.ParseMode.MARKDOWN,
        #                                  reply_markup=ReplyKeyboardRemove())
        #
        # elif not is_today(user_time):  # обновление было не сегодня
        #         today = date.today()
        #         formatted_date = today.strftime('%Y-%m-%d %H:%M:%S')
        #         user_db.set_request_count_and_date(user_id, 0, str(formatted_date))
        #
        #         max_wallet = user_db.get_max_wallets(user_id)
        #         wallets_list = message.text.split('\n')
        #         wallets_list = wallets_list[:max_wallet]
        #         wallets_count = len(wallets_list)
        #         total_balances = 0
        #
        #         for wallet, i in zip(wallets_list, range(wallets_count)):
        #
        #             await bot.edit_message_text(chat_id=wait_message.chat.id,
        #                                         message_id=wait_message.message_id,
        #                                         text=f"⏳ Getting information about wallets {i}/{wallets_count}")
        #
        #             is_screen_saved, balance = await async_screenshot(wallet)
        #
        #             if is_screen_saved == 1:
        #                 path_for_save = "app/wallets/" + wallet + ".png"
        #                 total_balances += int(balance)
        #                 await message.answer_photo(photo=open(path_for_save, "rb"), caption=f"✅ *{wallet}* \n"
        #                                                                                     f"💰 Balance *{balance}$*",
        #                                            parse_mode=types.ParseMode.MARKDOWN,
        #                                            reply_markup=types.ReplyKeyboardRemove())
        #             else:
        #                 await message.answer(f"❌ *{wallet}*",
        #                                      parse_mode=types.ParseMode.MARKDOWN,
        #                                      reply_markup=ReplyKeyboardRemove())
        #         if wallets_count != 1:
        #             await message.answer(f"💰 Total balance *{total_balances}$*",
        #                                  parse_mode=types.ParseMode.MARKDOWN,
        #                                  reply_markup=ReplyKeyboardRemove())
        #
        # user_db.increase_request_count(user_id)

        await bot.delete_message(chat_id=wait_message.chat.id,
                                 message_id=wait_message.message_id)

        is_ready = 0
        await state.update_data(is_ready=is_ready)
        await message.answer("<b> Load-up your wallets below ⬇️ </b>\n\n",
                             parse_mode=types.ParseMode.HTML,
                             reply_markup=ReplyKeyboardRemove())
    else:
        await message.answer(f"❗️ *Wait for wallet processing*", parse_mode=types.ParseMode.MARKDOWN,
                             reply_markup=ReplyKeyboardRemove())

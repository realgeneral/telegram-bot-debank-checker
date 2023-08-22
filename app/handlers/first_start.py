from aiogram import types
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from app.create_bot import dp, bot
from app.states.UserFollowing import UserFollowing
from app.keyboards.check_sub_menu import check_sub_menu

CHANNEL_ID = -1001984019900
NOTSUB_MESSAGE = "Looks like you're not subscribed yet! 🙁 Subscribe now to access all the features"


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
    if check_sub_channel(await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=callback_query.from_user.id)):
        await UserFollowing.get_private_keys.set()
        await bot.send_message(callback_query.from_user.id, "<b> Load-up your private keys below ⬇️ </b>\n\n"
                                                            "<b>One line one wallet (press shift+enter to switch to "
                                                            "a new line)</b> \n\n"
                                                            "<a href='https://support.metamask.io/hc/en-us/articles/360015289632-How-to-export-an-account-s-private-key'>"
                                                            "<b>How to get private keys from the wallet guide</b></a>\n\n"
                                                            "<b>Example:</b>\n"
                                                            "0x0430000000000000000000000000000 \n"
                                                            "0x4349593453490203003050435043534 \n\n"
                                                            "<i><b> Free version</b></i>: up to 10 keys.\n"
                                                            "<i><b> Premium version</b></i>: up to 50 keys. \n"
                                                            "<i> For access to the premium version, please "
                                                            "<a href='https://t.me/whatheshark'>contact us</a> </i> \n\n"
                                                            "<i><u>The bot doesn't collect or store your personal data or"
                                                            "private keys. Zora bot — fully open source project.</u> \n\n "
                                                            "GitHub: https://github.com/zemetsskiy/ZoraAutomatization "
                                                            "</i>",
                               parse_mode=types.ParseMode.HTML,
                               reply_markup=ReplyKeyboardRemove())
    else:
        await bot.send_message(callback_query.from_user.id, NOTSUB_MESSAGE, reply_markup=check_sub_menu)


@dp.message_handler(state=UserFollowing.get_private_keys)
async def private_keys(message: types.Message, state: FSMContext):
    random_amount = []
    message_response = ""

    private_keys = message.text.split('\n')

    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    wait_message = await message.answer("⏳ Getting information about wallets ...")

    if int(message.from_user.id) in admin.list_of_prem_users:
        private_keys = private_keys[:50]
        max_count = 50
    else:
        private_keys = private_keys[:10]
        max_count = 10

    for _ in private_keys:
        random_amount.append(Bridger.choose_random_amount(0.009501, 0.01003))

    await state.update_data(private_keys=private_keys)
    await state.update_data(random_amount=random_amount)

    if len(private_keys) == 1:
        message_response += f"Wallet is successfully loaded! (max. {max_count})\n\n"
    else:
        message_response += f"<b>{len(private_keys)}</b> wallets are successfully loaded! (max. {max_count})\n\n"

    count_ok_wallet = 0

    for i, random in zip(range(len(private_keys)), random_amount):

        es = Estimate(private_keys[i])
        eth_balance = es.get_eth_balance()
        eth_required = es.eth_required(random)

        message_response += f"{i + 1}. <b>{es.get_eth_address()}</b> \n"
        message_response += f"({eth_balance} ETH / {eth_required} ETH required)"

        if eth_balance != "-":
            if eth_balance >= eth_required:
                message_response += " ✅\n"
                count_ok_wallet += 1
            else:
                message_response += " ❌\n"

        await bot.edit_message_text(chat_id=wait_message.chat.id,
                                    message_id=wait_message.message_id,
                                    text=f"⏳ Getting information about wallets {i + 1}/{len(private_keys)}")

    if count_ok_wallet == len(private_keys):
        is_ready_to_start = 1
    else:
        is_ready_to_start = 0
        message_response += f"\nNow deposit require ETH amount in <b>Ethereum Mainnet, using your CEX!</b> * (Withdrawal " \
                            f"takes ~ 5 minutes)\n\n "

    await state.update_data(is_ready_to_start=is_ready_to_start)

    message_response += "\n<i><u> * Be sure to use CEX or you'll link your wallets and become sybil 💀</u></i>"

    await bot.delete_message(chat_id=wait_message.chat.id,
                             message_id=wait_message.message_id)

    buttons = [
        KeyboardButton(text="⬅ Go to menu"),
    ]

    reply_markup = ReplyKeyboardMarkup(keyboard=[buttons],
                                       resize_keyboard=True)

    await UserFollowing.wallet_menu.set(),
    await message.answer(message_response,
                         parse_mode=types.ParseMode.HTML,
                         reply_markup=reply_markup)

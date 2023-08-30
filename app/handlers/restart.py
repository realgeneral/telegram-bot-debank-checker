from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from app.create_bot import dp
from app.handlers.first_start import first_free_use


@dp.message_handler(commands=['restart'], state='*')
async def restart_cmd(message: types.Message, state: FSMContext):
    await message.answer(f"📍 _We made some updates! Let's check your wallets_",
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())
    await first_free_use(message, state)

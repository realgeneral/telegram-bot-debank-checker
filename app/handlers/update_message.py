from aiogram import types
from aiogram.types import ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

from app.create_bot import dp


@dp.message_handler(state='*')
async def restart_cmd(message: types.Message, state: FSMContext):
    print("try_restart.py")
    await message.answer(f"😊 _Try /restart_",
                         parse_mode=types.ParseMode.MARKDOWN,
                         reply_markup=ReplyKeyboardRemove())

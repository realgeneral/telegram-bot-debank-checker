from aiogram import executor

from app.handlers import dp
from app.logs import logging

if __name__ == '__main__':
    logging.info("Starting bot")
    executor.start_polling(dp, skip_updates=True)
    logging.info("Stopping bot")

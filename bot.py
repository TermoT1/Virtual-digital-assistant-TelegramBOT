from aiogram import executor

import config
from dispatcher import dp
import handlers

from db import BotDB
BotDB = BotDB(config.PATH_BD)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
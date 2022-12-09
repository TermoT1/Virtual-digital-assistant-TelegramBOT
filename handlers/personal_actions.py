from aiogram import types
from dispatcher import dp
import config
import re
from bot import BotDB
from keyboards import kb_client

@dp.message_handler(commands = "start")
async def start(message: types.Message):
    if(not BotDB.user_exists(message.from_user.id)):
        BotDB.add_user(message.from_user.id)
    await message.bot.send_message(message.from_user.id, "Добро пожаловать!")





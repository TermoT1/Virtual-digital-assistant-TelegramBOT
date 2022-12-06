from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from states import registration
from dispatcher import dp
from bot import BotDB

@dp.message_handler(commands = ("quiestion", "quest", "q"), commands_prefix = "/!")
async def start(message: types.Message):
    cmd_variants = (('/quiestion', '/quiest', '/q'))
    question = message.text
    for i in cmd_variants:
        for j in i:
            question = question.replace(j, '').strip()
    await message.answer(f"Question: {question}")
    answer = BotDB.answer_question(question)
    await message.answer(f"Ответ: {answer}.")


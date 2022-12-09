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

    if len(question):
        await message.answer(f"Question: {question}")
        answer = BotDB.answer_question(question)
    else:
        await message.reply("Пустой вопрос!")

    if len(answer):
        await message.answer(f"Ответ: {answer}.")
    else:
        await message.reply("Ответ не найден!")

@dp.message_handler(commands = ("qid"), commands_prefix = "/!")
async def select_by_id(message: types.Message):
    cmd_variants = (('/qid'))
    id = message.text
    for i in cmd_variants:
        for j in i:
            id = id.replace(j, '').strip()

    if len(id):
        await message.answer(f"id: {id}")
        qst_answr = BotDB.answer_question_by_id(id)
    else:
        await message.reply("Не введен id!")

    if len(qst_answr):
        await message.answer(f"Запись: {qst_answr}.")
    else:
        await message.reply("Запись не найдена!")